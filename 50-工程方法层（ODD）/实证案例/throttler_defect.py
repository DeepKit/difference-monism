import time
import threading
from collections import deque
from typing import Optional


class RateLimiter:
    """消息限流器 - 使用令牌桶算法"""
    
    def __init__(self, rate: int, per: float = 1.0):
        """
        初始化限流器
        
        Args:
            rate: 允许的请求数量
            per: 时间窗口（秒）
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            
            # 补充令牌
            self.allowance += time_passed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            # 消耗令牌
            if self.allowance >= 1.0:
                self.allowance -= 1.0
                return True
            return False
    
    def wait(self, timeout: Optional[float] = None) -> bool:
        """等待直到允许请求"""
        start = time.time()
        while True:
            if self.allow():
                return True
            if timeout and (time.time() - start) >= timeout:
                return False
            time.sleep(0.01)


class SlidingWindowRateLimiter:
    """滑动窗口限流器"""
    
    def __init__(self, rate: int, window: float = 1.0):
        """
        初始化限流器
        
        Args:
            rate: 时间窗口内允许的最大请求数
            window: 时间窗口大小（秒）
        """
        self.rate = rate
        self.window = window
        self.requests = deque()
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            current = time.time()
            
            # 移除过期请求
            while self.requests and self.requests[0] <= current - self.window:
                self.requests.popleft()
            
            # 检查是否超过限制
            if len(self.requests) < self.rate:
                self.requests.append(current)
                return True
            return False
    
    def remaining(self) -> int:
        """返回剩余可用请求数"""
        with self.lock:
            current = time.time()
            while self.requests and self.requests[0] <= current - self.window:
                self.requests.popleft()
            return self.rate - len(self.requests)


class FixedWindowRateLimiter:
    """固定窗口限流器"""
    
    def __init__(self, rate: int, window: float = 1.0):
        """
        初始化限流器
        
        Args:
            rate: 每个窗口允许的最大请求数
            window: 窗口大小（秒）
        """
        self.rate = rate
        self.window = window
        self.counter = 0
        self.window_start = time.time()
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            current = time.time()
            
            # 检查是否需要重置窗口
            if current - self.window_start >= self.window:
                self.counter = 0
                self.window_start = current
            
            # 检查是否超过限制
            if self.counter < self.rate:
                self.counter += 1
                return True
            return False


# 使用示例
if __name__ == "__main__":
    # 令牌桶：每秒5个请求
    limiter = RateLimiter(rate=5, per=1.0)
    
    # 滑动窗口：10秒内最多20个请求
    sliding = SlidingWindowRateLimiter(rate=20, window=10.0)
    
    # 固定窗口：每秒10个请求
    fixed = FixedWindowRateLimiter(rate=10, window=1.0)
    
    # 测试
    for i in range(10):
        if limiter.allow():
            print(f"请求 {i+1}: 允许")
        else:
            print(f"请求 {i+1}: 限流")
        time.sleep(0.1)