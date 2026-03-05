
import time
import threading
from typing import Optional


class RateLimiter:
    """令牌桶限流器"""
    
    def __init__(self, rate: float, capacity: Optional[int] = None):
        """
        初始化限流器
        
        Args:
            rate: 每秒生成的令牌数
            capacity: 桶容量，默认等于rate
        """
        self.rate = rate
        self.capacity = capacity if capacity is not None else rate
        self.tokens = self.capacity
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_update
        new_tokens = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_update = now
    
    def acquire(self, tokens: int = 1) -> bool:
        """
        尝试获取令牌
        
        Args:
            tokens: 需要的令牌数
            
        Returns:
            是否成功获取
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait(self, tokens: int = 1, timeout: Optional[float] = None):
        """
        等待直到获取令牌
        
        Args:
            tokens: 需要的令牌数
            timeout: 超时时间（秒）
            
        Returns:
            是否成功获取
        """
        start_time = time.time()
        while True:
            if self.acquire(tokens):
                return True
            
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
            
            time.sleep(0.01)


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
        """清理过期请求"""
        now = time.time()
        cutoff = now - self.window_seconds
        self.requests = [req_time for req_time in self.requests if req_time > cutoff]
    
    def acquire(self) -> bool:
        """
        尝试获取许可
        
        Returns:
            是否允许请求
        """
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


class FixedWindowRateLimiter:
    """固定窗口限流器"""
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化限流器
        
        Args:
            max_requests: 时间窗口内最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.counter = 0
        self.window_start = time.time()
        self.lock = threading.Lock()
    
    def _reset_if_needed(self):
        """如果窗口过期则重置"""
        now = time.time()
        if now - self.window_start >= self.window_seconds:
            self.counter = 0
            self.window_start = now
    
    def acquire(self) -> bool:
        """
        尝试获取许可
        
        Returns:
            是否允许请求
        """
        with self.lock:
            self._reset_if_needed()
            if self.counter < self.max_requests:
                self.counter += 1
                return True
            return False
