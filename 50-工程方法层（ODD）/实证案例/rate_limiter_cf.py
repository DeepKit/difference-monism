import time
import threading
from collections import deque
from typing import Optional, Set
from enum import Enum


class RateLimitError(Exception):
    pass


class FixedWindowExceeded(RateLimitError):
    def __init__(self, window_size: int, limit: int):
        super().__init__(f"固定窗口限流超限: {window_size}秒内最多允许{limit}次请求")


class SlidingWindowExceeded(RateLimitError):
    def __init__(self, window_size: int, limit: int):
        super().__init__(f"滑动窗口限流超限: {window_size}秒内最多允许{limit}次请求")


class ConcurrencyExceeded(RateLimitError):
    def __init__(self, max_concurrent: int):
        super().__init__(f"并发数超限: 最大并发数为{max_concurrent}")


class BlacklistBlocked(RateLimitError):
    def __init__(self, identifier: str):
        super().__init__(f"请求被拒绝: {identifier}在黑名单中")


class WhitelistRequired(RateLimitError):
    def __init__(self, identifier: str):
        super().__init__(f"请求被拒绝: {identifier}不在白名单中")


class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_size: int = 1):
        self.limit = limit
        self.window_size = window_size
        self.counter = 0
        self.window_start = time.time()
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        with self.lock:
            current_time = time.time()
            if current_time - self.window_start >= self.window_size:
                self.counter = 0
                self.window_start = current_time
            if self.counter < self.limit:
                self.counter += 1
                return True
            raise FixedWindowExceeded(self.window_size, self.limit)


class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_size: int = 1):
        self.limit = limit
        self.window_size = window_size
        self.requests = deque()
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        with self.lock:
            current_time = time.time()
            while self.requests and current_time - self.requests[0] > self.window_size:
                self.requests.popleft()
            if len(self.requests) < self.limit:
                self.requests.append(current_time)
                return True
            raise SlidingWindowExceeded(self.window_size, self.limit)


class ConcurrencyLimiter:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.current_concurrent = 0
        self.lock = threading.Lock()
    
    def acquire(self) -> bool:
        with self.lock:
            if self.current_concurrent < self.max_concurrent:
                self.current_concurrent += 1
                return True
            raise ConcurrencyExceeded(self.max_concurrent)
    
    def release(self):
        with self.lock:
            if self.current_concurrent > 0:
                self.current_concurrent -= 1
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class BlackWhiteListManager:
    def __init__(self, use_whitelist: bool = False):
        self.blacklist: Set[str] = set()
        self.whitelist: Set[str] = set()
        self.use_whitelist = use_whitelist
        self.lock = threading.Lock()
    
    def add_to_blacklist(self, identifier: str):
        with self.lock:
            self.blacklist.add(identifier)
    
    def remove_from_blacklist(self, identifier: str):
        with self.lock:
            self.blacklist.discard(identifier)
    
    def add_to_whitelist(self, identifier: str):
        with self.lock:
            self.whitelist.add(identifier)
    
    def remove_from_whitelist(self, identifier: str):
        with self.lock:
            self.whitelist.discard(identifier)
    
    def check(self, identifier: str) -> bool:
        with self.lock:
            if identifier in self.blacklist:
                raise BlacklistBlocked(identifier)
            if self.use_whitelist and identifier not in self.whitelist:
                raise WhitelistRequired(identifier)
            return True


class RateLimiter:
    def __init__(self, qps_limit: Optional[int] = None, max_concurrent: Optional[int] = None, use_sliding_window: bool = False, window_size: int = 1, use_whitelist: bool = False):
        self.qps_limiter = None
        if qps_limit:
            if use_sliding_window:
                self.qps_limiter = SlidingWindowRateLimiter(qps_limit, window_size)
            else:
                self.qps_limiter = FixedWindowRateLimiter(qps_limit, window_size)
        self.concurrency_limiter = None
        if max_concurrent:
            self.concurrency_limiter = ConcurrencyLimiter(max_concurrent)
        self.blackwhite_manager = BlackWhiteListManager(use_whitelist)
    
    def allow(self, identifier: Optional[str] = None) -> bool:
        if identifier:
            self.blackwhite_manager.check(identifier)
        if self.qps_limiter:
            self.qps_limiter.allow()
        if self.concurrency_limiter:
            self.concurrency_limiter.acquire()
        return True
    
    def release_concurrent(self):
        if self.concurrency_limiter:
            self.concurrency_limiter.release()
    
    def add_to_blacklist(self, identifier: str):
        self.blackwhite_manager.add_to_blacklist(identifier)
    
    def remove_from_blacklist(self, identifier: str):
        self.blackwhite_manager.remove_from_blacklist(identifier)
    
    def add_to_whitelist(self, identifier: str):
        self.blackwhite_manager.add_to_whitelist(identifier)
    
    def remove_from_whitelist(self, identifier: str):
        self.blackwhite_manager.remove_from_whitelist(identifier)
