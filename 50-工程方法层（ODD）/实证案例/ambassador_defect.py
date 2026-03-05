import time
import random
from typing import Optional, Callable, Any
from enum import Enum
from datetime import datetime, timedelta


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class RemoteService:
    """模拟远程服务"""
    
    def __init__(self, failure_rate: float = 0.3):
        self.failure_rate = failure_rate
        self.call_count = 0
    
    def call(self, data: str) -> str:
        """模拟远程调用"""
        self.call_count += 1
        time.sleep(0.1)  # 模拟网络延迟
        
        if random.random() < self.failure_rate:
            raise ConnectionError(f"Remote service call failed: {data}")
        
        return f"Response from service: {data}"


class Ambassador:
    """大使模式实现 - 代理远程服务调用"""
    
    def __init__(
        self,
        service: RemoteService,
        max_retries: int = 3,
        retry_delay: float = 0.5,
        circuit_threshold: int = 5,
        circuit_timeout: int = 10
    ):
        self.service = service
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # 熔断器配置
        self.circuit_threshold = circuit_threshold
        self.circuit_timeout = circuit_timeout
        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        
        # 统计信息
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
    
    def call(self, data: str) -> str:
        """通过大使调用远程服务"""
        self.total_calls += 1
        
        # 检查熔断器状态
        if not self._check_circuit():
            self.failed_calls += 1
            raise Exception("Circuit breaker is OPEN - service unavailable")
        
        # 重试逻辑
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                self._log(f"Attempt {attempt + 1}/{self.max_retries} for: {data}")
                result = self.service.call(data)
                
                # 成功调用
                self._on_success()
                self.successful_calls += 1
                return result
                
            except Exception as e:
                last_exception = e
                self._log(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # 指数退避
        
        # 所有重试都失败
        self._on_failure()
        self.failed_calls += 1
        raise Exception(f"All {self.max_retries} attempts failed: {last_exception}")
    
    def _check_circuit(self) -> bool:
        """检查熔断器状态"""
        if self.circuit_state == CircuitState.CLOSED:
            return True
        
        if self.circuit_state == CircuitState.OPEN:
            # 检查是否可以尝试半开状态
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).seconds
                if elapsed >= self.circuit_timeout:
                    self._log("Circuit breaker: OPEN -> HALF_OPEN")
                    self.circuit_state = CircuitState.HALF_OPEN
                    return True
            return False
        
        # HALF_OPEN 状态允许尝试
        return True
    
    def _on_success(self):
        """成功调用后的处理"""
        if self.circuit_state == CircuitState.HALF_OPEN:
            self._log("Circuit breaker: HALF_OPEN -> CLOSED")
            self.circuit_state = CircuitState.CLOSED
            self.failure_count = 0
    
    def _on_failure(self):
        """失败调用后的处理"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.circuit_threshold:
            if self.circuit_state != CircuitState.OPEN:
                self._log("Circuit breaker: CLOSED -> OPEN")
                self.circuit_state = CircuitState.OPEN
    
    def _log(self, message: str):
        """日志记录"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Ambassador: {message}")
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "success_rate": f"{(self.successful_calls / self.total_calls * 100):.2f}%" if self.total_calls > 0 else "0%",
            "circuit_state": self.circuit_state.value,
            "failure_count": self.failure_count
        }


class Client:
    """客户端 - 通过大使访问远程服务"""
    
    def __init__(self, ambassador: Ambassador):
        self.ambassador = ambassador
    
    def make_request(self, data: str) -> Optional[str]:
        """发起请求"""
        try:
            result = self.ambassador.call(data)
            print(f"✓ Client received: {result}\n")
            return result
        except Exception as e:
            print(f"✗ Client error: {str(e)}\n")
            return None


def main():
    """演示大使模式"""
    print("=== Ambassador Pattern Demo ===\n")
    
    # 创建远程服务（30%失败率）
    remote_service = RemoteService(failure_rate=0.3)
    
    # 创建大使（3次重试，5次失败后熔断）
    ambassador = Ambassador(
        service=remote_service,
        max_retries=3,
        retry_delay=0.2,
        circuit_threshold=5,
        circuit_timeout=5
    )
    
    # 创建客户端
    client = Client(ambassador)
    
    # 模拟多次调用
    print("--- Making 15 requests ---\n")
    for i in range(15):
        client.make_request(f"Request-{i+1}")
        time.sleep(0.3)
    
    # 显示统计信息
    print("\n=== Statistics ===")
    stats = ambassador.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print(f"\nRemote service was called {remote_service.call_count} times")


if __name__ == "__main__":
    main()