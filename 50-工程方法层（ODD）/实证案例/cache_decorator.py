import functools
import time
import threading
from typing import Any, Callable, Optional, Dict, Tuple
from collections import OrderedDict
import hashlib
import pickle


class CacheDecorator:
    def __init__(
        self,
        maxsize: Optional[int] = 128,
        ttl: Optional[float] = None,
        typed: bool = False,
        thread_safe: bool = True
    ):
        self.maxsize = maxsize
        self.ttl = ttl
        self.typed = typed
        self.thread_safe = thread_safe
        self.cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.lock = threading.RLock() if thread_safe else None

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                cache_key = self._make_key(args, kwargs, self.typed)
            except Exception:
                return func(*args, **kwargs)

            if self.thread_safe:
                with self.lock:
                    return self._get_or_compute(func, cache_key, args, kwargs)
            else:
                return self._get_or_compute(func, cache_key, args, kwargs)

        wrapper.cache_info = self.cache_info
        wrapper.cache_clear = self.cache_clear
        wrapper.cache = self.cache
        return wrapper

    def _get_or_compute(self, func: Callable, cache_key: str, args: Tuple, kwargs: Dict) -> Any:
        if cache_key in self.cache:
            result, timestamp = self.cache[cache_key]
            
            if self.ttl is None or (time.time() - timestamp) < self.ttl:
                self.cache.move_to_end(cache_key)
                self.hits += 1
                return result
            else:
                del self.cache[cache_key]

        self.misses += 1
        result = func(*args, **kwargs)
        
        self.cache[cache_key] = (result, time.time())
        
        if self.maxsize is not None and len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        
        return result

    def _make_key(self, args: Tuple, kwargs: Dict, typed: bool) -> str:
        try:
            key_parts = []
            
            for arg in args:
                try:
                    key_parts.append(str(hash(arg)))
                except TypeError:
                    key_parts.append(hashlib.md5(pickle.dumps(arg)).hexdigest())
            
            for k, v in sorted(kwargs.items()):
                try:
                    key_parts.append(f"{k}:{hash(v)}")
                except TypeError:
                    key_parts.append(f"{k}:{hashlib.md5(pickle.dumps(v)).hexdigest()}")
            
            if typed:
                key_parts.append(str([type(arg).__name__ for arg in args]))
                key_parts.append(str({k: type(v).__name__ for k, v in kwargs.items()}))
            
            return "|".join(key_parts)
        except Exception as e:
            raise TypeError(f"Cannot create cache key: {e}")

    def cache_info(self) -> Dict[str, Any]:
        if self.thread_safe:
            with self.lock:
                return {
                    "hits": self.hits,
                    "misses": self.misses,
                    "maxsize": self.maxsize,
                    "currsize": len(self.cache),
                    "ttl": self.ttl
                }
        else:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "maxsize": self.maxsize,
                "currsize": len(self.cache),
                "ttl": self.ttl
            }

    def cache_clear(self) -> None:
        if self.thread_safe:
            with self.lock:
                self.cache.clear()
                self.hits = 0
                self.misses = 0
        else:
            self.cache.clear()
            self.hits = 0
            self.misses = 0


# 使用示例
if __name__ == "__main__":
    @CacheDecorator(maxsize=100, ttl=5.0)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    @CacheDecorator(maxsize=50, typed=True)
    def expensive_operation(x, y, operation="add"):
        time.sleep(0.1)
        if operation == "add":
            return x + y
        elif operation == "multiply":
            return x * y
        return None

    print(fibonacci(10))
    print(fibonacci.cache_info())
    
    print(expensive_operation(5, 3))
    print(expensive_operation(5, 3))
    print(expensive_operation.cache_info())
    
    expensive_operation.cache_clear()
    print(expensive_operation.cache_info())