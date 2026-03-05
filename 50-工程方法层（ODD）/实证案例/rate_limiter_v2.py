
import time
from threading import Lock
from collections import deque
from enum import Enum


class RateLimitStrategy(Enum):
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"


class RequestRateLimiter:
    def __init__(self, strategy: RateLimitStrategy, rate: int, capacity: int = None):
        """
        初始化限流器
        
        :param strategy: 限流策略
        :param rate: 速率（令牌桶：每秒生成令牌数；滑动窗口：时间窗口内最大请求数）
        :param capacity: 容量（令牌桶：桶容量；滑动窗口：时间窗口秒数，默认为1秒）
        """
        self.strategy = strategy
        self.rate = rate
        self.lock = Lock()
        
        if strategy == RateLimitStrategy.TOKEN_BUCKET:
            self.capacity = capacity if capacity else rate
            self.tokens = self.capacity
            self.last_update = time.time()
        elif strategy == RateLimitStrategy.SLIDING_WINDOW:
            self.window_size = capacity if capacity else 1
            self.requests = deque()
    
    def allow_request(self) -> bool:
        """
        检查是否允许请求
        
        :return: True表示允许，False表示拒绝
        """
        if self.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return self._token_bucket_allow()
        elif self.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return self._sliding_window_allow()
        return False
    
    def _token_bucket_allow(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # 添加新令牌
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            # 尝试消耗一个令牌
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    def _sliding_window_allow(self) -> bool:
        with self.lock:
            now = time.time()
            window_start = now - self.window_size
            
            # 移除窗口外的请求
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()
            
            # 检查是否超过限制
            if len(self.requests) < self.rate:
                self.requests.append(now)
                return True
            return False
    
    def reset(self):
        """重置限流器状态"""
        with self.lock:
            if self.strategy == RateLimitStrategy.TOKEN_BUCKET:
                self.tokens = self.capacity
                self.last_update = time.time()
            elif self.strategy == RateLimitStrategy.SLIDING_WINDOW:
                self.requests.clear()


# 使用示例
if __name__ == "__main__":
    # 令牌桶：每秒10个令牌，桶容量20
    token_limiter = RequestRateLimiter(
        strategy=RateLimitStrategy.TOKEN_BUCKET,
        rate=10,
        capacity=20
    )
    
    # 滑动窗口：1秒内最多5个请求
    window_limiter = RequestRateLimiter(
        strategy=RateLimitStrategy.SLIDING_WINDOW,
        rate=5,
        capacity=1
    )
    
    # 测试令牌桶
    print("令牌桶测试:")
    for i in range(15):
        allowed = token_limiter.allow_request()
        print(f"请求 {i+1}: {'允许' if allowed else '拒绝'}")
    
    print("\n滑动窗口测试:")
    for i in range(10):
        allowed = window_limiter.allow_request()
        print(f"请求 {i+1}: {'允许' if allowed else '拒绝'}")
        if i == 4:
            time.sleep(1.1)  # 等待窗口滑动
