import pytest
import time
from gateway import (
    APIGateway, CircuitBreaker, RateLimiter, 
    ResponseCache, CircuitState, Route
)


class TestCircuitBreaker:
    def test_circuit_breaker_closed_state(self):
        cb = CircuitBreaker(failure_threshold=3)
        assert cb.state == CircuitState.CLOSED
        result = cb.call(lambda: "success")
        assert result == "success"
        assert cb.state == CircuitState.CLOSED
    
    def test_circuit_breaker_opens_after_failures(self):
        cb = CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass
        assert cb.state == CircuitState.OPEN
    
    def test_circuit_breaker_half_open_transition(self):
        cb = CircuitBreaker(failure_threshold=2, timeout=1)
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass
        assert cb.state == CircuitState.OPEN
        time.sleep(1.1)
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        assert cb.state == CircuitState.HALF_OPEN
    
    def test_circuit_breaker_recovery(self):
        cb = CircuitBreaker(failure_threshold=2, timeout=1)
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass
        time.sleep(1.1)
        result = cb.call(lambda: "recovered")
        assert result == "recovered"
        assert cb.state == CircuitState.CLOSED


class TestRateLimiter:
    def test_rate_limiter_allows_requests(self):
        limiter = RateLimiter(max_requests=5, window_size=60)
        for _ in range(5):
            assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
    
    def test_rate_limiter_different_clients(self):
        limiter = RateLimiter(max_requests=2, window_size=60)
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client2") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client2") is True
    
    def test_rate_limiter_window_expiry(self):
        limiter = RateLimiter(max_requests=2, window_size=1)
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
        time.sleep(1.1)
        assert limiter.is_allowed("client1") is True


class TestResponseCache:
    def test_cache_set_and_get(self):
        cache = ResponseCache()
        key = cache.get_key("GET", "http://example.com", "")
        cache.set(key, {"result": "success"}, ttl=60)
        entry = cache.get(key)
        assert entry == {"result": "success"}
    
    def test_cache_expiry(self):
        cache = ResponseCache()
        key = cache.get_key("GET", "http://example.com", "")
        cache.set(key, "response", ttl=1)
        time.sleep(1.1)
        entry = cache.get(key)
        assert entry is None
    
    def test_cache_key_generation(self):
        cache = ResponseCache()
        key1 = cache.get_key("GET", "http://example.com/api", "")
        key2 = cache.get_key("GET", "http://example.com/api", "")
        key3 = cache.get_key("POST", "http://example.com/api", "")
        assert key1 == key2
        assert key1 != key3


class TestAPIGateway:
    def test_add_route(self):
        gateway = APIGateway()
        gateway.add_route("/api/test", "http://backend:8001", timeout=10)
        assert len(gateway.routes) == 1
        assert gateway.routes[0].path == "/api/test"
    
    def test_find_route(self):
        gateway = APIGateway()
        gateway.add_route("/api/users", "http://backend:8001")
        gateway.add_route("/api/orders", "http://backend:8002")
        route = gateway.find_route("/api/users/123")
        assert route is not None
        assert route.target == "http://backend:8001"
        route = gateway.find_route("/api/unknown")
        assert route is None
    
    def test_rate_limit_check(self):
        gateway = APIGateway()
        gateway.add_route("/api/limited", "http://backend:8001", rate_limit=2)
        assert gateway.check_rate_limit("/api/limited", "client1") is True
        assert gateway.check_rate_limit("/api/limited", "client1") is True
        assert gateway.check_rate_limit("/api/limited", "client1") is False
    
    def test_circuit_breaker_integration(self):
        gateway = APIGateway()
        gateway.add_route("/api/test", "http://backend:8001")
        
        def failing_func():
            raise Exception("error")
        
        cb = gateway.circuit_breakers["http://backend:8001"]
        for _ in range(5):
            try:
                gateway.call_with_circuit("http://backend:8001", failing_func)
            except:
                pass
        
        assert cb.state == CircuitState.OPEN
    
    def test_cache_integration(self):
        gateway = APIGateway()
        gateway.add_route("/api/test", "http://backend:8001", cache_ttl=60)
        
        cache_key = gateway.cache.get_key("GET", "http://backend:8001/api/data", "")
        gateway.cache_response(cache_key, {"cached": True}, ttl=60)
        
        cached = gateway.get_cached_response(cache_key)
        assert cached == {"cached": True}
    
    def test_stats(self):
        gateway = APIGateway()
        gateway.add_route("/api/test", "http://backend:8001")
        stats = gateway.get_stats()
        assert stats["routes"] == 1
        assert "http://backend:8001" in stats["circuit_breakers"]
