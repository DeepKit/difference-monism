import asyncio
import time
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import deque
import hashlib
import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import aiohttp
from pydantic import BaseModel


class BackendConfig(BaseModel):
    url: str
    timeout: float = 5.0
    max_requests_per_second: int = 100


class RouteConfig(BaseModel):
    path: str
    backend: BackendConfig
    cache_ttl: Optional[int] = None


class RateLimiter:
    def __init__(self, max_requests: int, time_window: float = 1.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def is_allowed(self) -> bool:
        now = time.time()
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        if len(self.requests) >= self.max_requests:
            return False
        self.requests.append(now)
        return True


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, success_threshold: int = 2, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
    
    def call(self, func):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("熔断器已打开，服务暂时不可用")
        return func
    
    def on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        return self.last_failure_time is not None and time.time() - self.last_failure_time >= self.timeout


class CacheManager:
    def __init__(self):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int):
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)
    
    def _generate_key(self, method: str, url: str, body: Optional[bytes]) -> str:
        key_data = f"{method}:{url}"
        if body:
            key_data += f":{hashlib.md5(body).hexdigest()}"
        return hashlib.sha256(key_data.encode()).hexdigest()


class APIGateway:
    def __init__(self):
        self.routes: Dict[str, RouteConfig] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.cache_manager = CacheManager()
    
    def add_route(self, route_config: RouteConfig):
        self.routes[route_config.path] = route_config
        self.rate_limiters[route_config.path] = RateLimiter(route_config.backend.max_requests_per_second)
        self.circuit_breakers[route_config.path] = CircuitBreaker()
    
    async def forward_request(self, path: str, method: str, headers: dict, body: Optional[bytes]) -> tuple[int, dict, bytes]:
        if path not in self.routes:
            raise HTTPException(status_code=404, detail="路由不存在")
        
        route = self.routes[path]
        
        if not self.rate_limiters[path].is_allowed():
            raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")
        
        if method == "GET" and route.cache_ttl:
            cache_key = self.cache_manager._generate_key(method, route.backend.url, body)
            cached_response = self.cache_manager.get(cache_key)
            if cached_response:
                return cached_response
        
        circuit_breaker = self.circuit_breakers[path]
        try:
            circuit_breaker.call(lambda: None)
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))
        
        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=route.backend.timeout)
                async with session.request(method=method, url=route.backend.url, headers=headers, data=body, timeout=timeout) as response:
                    response_body = await response.read()
                    response_headers = dict(response.headers)
                    circuit_breaker.on_success()
                    
                    if method == "GET" and route.cache_ttl and response.status == 200:
                        cache_key = self.cache_manager._generate_key(method, route.backend.url, body)
                        self.cache_manager.set(cache_key, (response.status, response_headers, response_body), route.cache_ttl)
                    
                    return response.status, response_headers, response_body
        
        except asyncio.TimeoutError:
            circuit_breaker.on_failure()
            raise HTTPException(status_code=504, detail=f"请求超时（超过{route.backend.timeout}秒）")
        except aiohttp.ClientError as e:
            circuit_breaker.on_failure()
            raise HTTPException(status_code=502, detail=f"后端服务连接失败: {str(e)}")
        except Exception as e:
            circuit_breaker.on_failure()
            raise HTTPException(status_code=500, detail=f"网关内部错误: {str(e)}")


app = FastAPI(title="API Gateway")
gateway = APIGateway()


gateway.add_route(RouteConfig(path="/api/users", backend=BackendConfig(url="http://localhost:8001/users", timeout=5.0, max_requests_per_second=100), cache_ttl=60))
gateway.add_route(RouteConfig(path="/api/orders", backend=BackendConfig(url="http://localhost:8002/orders", timeout=3.0, max_requests_per_second=50), cache_ttl=30))


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(path: str, request: Request):
    try:
        body = await request.body() if request.method != "GET" else None
        headers = dict(request.headers)
        headers.pop("host", None)
        
        status, response_headers, response_body = await gateway.forward_request(f"/{path}", request.method, headers, body)
        
        return JSONResponse(content=json.loads(response_body) if response_body else {}, status_code=status, headers={k: v for k, v in response_headers.items() if k.lower() not in ["content-encoding", "content-length", "transfer-encoding"]})
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail, "status_code": e.status_code}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"error": f"未知错误: {str(e)}", "status_code": 500}, status_code=500)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/gateway/stats")
async def gateway_stats():
    stats = {}
    for path, circuit_breaker in gateway.circuit_breakers.items():
        stats[path] = {"circuit_state": circuit_breaker.state.value, "failure_count": circuit_breaker.failure_count}
    return stats
