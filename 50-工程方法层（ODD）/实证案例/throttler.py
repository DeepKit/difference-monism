import time
import threading
from typing import Optional
from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    """速率限制配置"""
    rate: float  # 每秒允许的请求数
    capacity: int  # 桶容量（突发请求数）


class MessageRateLimiter:
    """消息限流器 - 令牌桶算法实现"""
    
    def __init__(self, rate: float, capacity: Optional[int] = None):
        """
        初始化限流器
        
        Args:
            rate: 每秒允许的消息数
            capacity: 桶容量，默认等于rate
        """
        self.rate = rate
        self.capacity = capacity or int(rate)
        self.tokens = float(self.capacity)
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
    
    def allow(self, tokens: int = 1) -> bool:
        """
        检查是否允许通过
        
        Args:
            tokens: 需要消耗的令牌数
            
        Returns:
            True表示允许，False表示被限流
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        等待直到可以通过
        
        Args:
            tokens: 需要消耗的令牌数
            timeout: 超时时间（秒），None表示无限等待
            
        Returns:
            True表示成功获取令牌，False表示超时
        """
        start_time = time.time()
        
        while True:
            if self.allow(tokens):
                return True
            
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
            
            # 计算需要等待的时间
            with self.lock:
                self._refill()
                if self.tokens >= tokens:
                    continue
                wait_time = (tokens - self.tokens) / self.rate
            
            sleep_time = min(wait_time, 0.1)
            if timeout is not None:
                remaining = timeout - (time.time() - start_time)
                sleep_time = min(sleep_time, remaining)
                if sleep_time <= 0:
                    return False
            
            time.sleep(sleep_time)
    
    def reset(self):
        """重置限流器"""
        with self.lock:
            self.tokens = float(self.capacity)
            self.last_update = time.time()
    
    def get_available_tokens(self) -> float:
        """获取当前可用令牌数"""
        with self.lock:
            self._refill()
            return self.tokens


class SlidingWindowRateLimiter:
    """滑动窗口限流器"""
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化限流器
        
        Args:
            max_requests: 时间窗口内最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        self.lock = threading.Lock()
    
    def _clean_old_requests(self):
        """清理过期请求记录"""
        now = time.time()
        cutoff = now - self.window_seconds
        self.requests = [ts for ts in self.requests if ts > cutoff]
    
    def allow(self) -> bool:
        """检查是否允许通过"""
        with self.lock:
            self._clean_old_requests()
            if len(self.requests) < self.max_requests:
                self.requests.append(time.time())
                return True
            return False
    
    def get_remaining(self) -> int:
        """获取剩余可用请求数"""
        with self.lock:
            self._clean_old_requests()
            return max(0, self.max_requests - len(self.requests))
    
    def reset(self):
        """重置限流器"""
        with self.lock:
            self.requests.clear()


# 使用示例
if __name__ == "__main__":
    # 令牌桶：每秒5个请求，突发10个
    limiter = MessageRateLimiter(rate=5, capacity=10)
    
    for i in range(15):
        if limiter.allow():
            print(f"请求 {i+1}: 通过")
        else:
            print(f"请求 {i+1}: 被限流")
    
    print("\n等待模式:")
    limiter.reset()
    for i in range(5):
        if limiter.wait(timeout=2.0):
            print(f"请求 {i+1}: 通过")
        else:
            print(f"请求 {i+1}: 超时")
    
    # 滑动窗口：10秒内最多20个请求
    print("\n滑动窗口限流:")
    sw_limiter = SlidingWindowRateLimiter(max_requests=20, window_seconds=10)
    
    for i in range(25):
        if sw_limiter.allow():
            print(f"请求 {i+1}: 通过 (剩余: {sw_limiter.get_remaining()})")
        else:
            print(f"请求 {i+1}: 被限流")