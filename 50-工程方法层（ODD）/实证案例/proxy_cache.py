import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable
from functools import wraps


class ProxyCache:
    """代理缓存类，支持LRU淘汰策略和TTL过期"""
    
    def __init__(self, max_size: int = 100, default_ttl: Optional[float] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache = OrderedDict()
        self._timestamps = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self._lock:
            if key not in self._cache:
                return None
            
            # 检查是否过期
            if self._is_expired(key):
                self._remove(key)
                return None
            
            # LRU: 移到末尾
            self._cache.move_to_end(key)
            return self._cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存值"""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self.max_size:
                    # 淘汰最旧的项
                    oldest_key = next(iter(self._cache))
                    self._remove(oldest_key)
            
            self._cache[key] = value
            
            # 设置过期时间
            expire_ttl = ttl if ttl is not None else self.default_ttl
            if expire_ttl:
                self._timestamps[key] = time.time() + expire_ttl
            elif key in self._timestamps:
                del self._timestamps[key]
    
    def delete(self, key: str) -> bool:
        """删除缓存项"""
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在且未过期"""
        with self._lock:
            if key not in self._cache:
                return False
            if self._is_expired(key):
                self._remove(key)
                return False
            return True
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self._lock:
            return len(self._cache)
    
    def _is_expired(self, key: str) -> bool:
        """检查键是否过期"""
        if key not in self._timestamps:
            return False
        return time.time() > self._timestamps[key]
    
    def _remove(self, key: str) -> None:
        """内部删除方法"""
        del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def cached(self, ttl: Optional[float] = None, key_func: Optional[Callable] = None):
        """装饰器：缓存函数结果"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # 尝试从缓存获取
                result = self.get(cache_key)
                if result is not None:
                    return result
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator


class ProxyCacheWithStats(ProxyCache):
    """带统计功能的代理缓存类"""
    
    def __init__(self, max_size: int = 100, default_ttl: Optional[float] = None):
        super().__init__(max_size, default_ttl)
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        result = super().get(key)
        with self._lock:
            if result is not None:
                self._hits += 1
            else:
                self._misses += 1
        return result
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            return {
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': f"{hit_rate:.2f}%",
                'size': len(self._cache),
                'max_size': self.max_size
            }
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        with self._lock:
            self._hits = 0
            self._misses = 0


# 使用示例
if __name__ == "__main__":
    # 基本使用
    cache = ProxyCache(max_size=3, default_ttl=5)
    
    cache.set("user:1", {"name": "Alice", "age": 30})
    cache.set("user:2", {"name": "Bob", "age": 25})
    
    print(cache.get("user:1"))  # {'name': 'Alice', 'age': 30}
    print(cache.exists("user:3"))  # False
    
    # 装饰器使用
    @cache.cached(ttl=10)
    def expensive_operation(x, y):
        time.sleep(1)  # 模拟耗时操作
        return x + y
    
    start = time.time()
    result1 = expensive_operation(5, 3)  # 第一次调用，执行函数
    print(f"First call: {time.time() - start:.2f}s")
    
    start = time.time()
    result2 = expensive_operation(5, 3)  # 第二次调用，从缓存获取
    print(f"Second call: {time.time() - start:.2f}s")
    
    # 带统计的缓存
    stats_cache = ProxyCacheWithStats(max_size=100)
    stats_cache.set("key1", "value1")
    stats_cache.get("key1")
    stats_cache.get("key2")
    print(stats_cache.get_stats())