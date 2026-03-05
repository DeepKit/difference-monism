
import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable
from functools import wraps


class Cache:
    """支持多种失效策略的缓存实现"""
    
    def __init__(self, max_size: int = 100, ttl: Optional[float] = None):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl: 生存时间(秒)，None表示永不过期
        """
        self.max_size = max_size
        self.ttl = ttl
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
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        with self._lock:
            # 如果已存在，先删除
            if key in self._cache:
                self._remove(key)
            
            # 检查容量限制
            if len(self._cache) >= self.max_size:
                # 删除最旧的项(LRU)
                oldest_key = next(iter(self._cache))
                self._remove(oldest_key)
            
            # 添加新项
            self._cache[key] = value
            self._timestamps[key] = time.time()
    
    def delete(self, key: str) -> bool:
        """删除指定缓存"""
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    def invalidate_pattern(self, pattern: str) -> int:
        """按模式失效缓存"""
        with self._lock:
            keys_to_remove = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_remove:
                self._remove(key)
            return len(keys_to_remove)
    
    def invalidate_expired(self) -> int:
        """清理所有过期缓存"""
        if self.ttl is None:
            return 0
        
        with self._lock:
            expired_keys = [k for k in self._cache.keys() if self._is_expired(k)]
            for key in expired_keys:
                self._remove(key)
            return len(expired_keys)
    
    def _is_expired(self, key: str) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        
        timestamp = self._timestamps.get(key)
        if timestamp is None:
            return True
        
        return time.time() - timestamp > self.ttl
    
    def _remove(self, key: str) -> None:
        """内部删除方法"""
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self._lock:
            return len(self._cache)


def cached(cache: Cache, key_func: Optional[Callable] = None):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


class TTLCache(Cache):
    """基于TTL的缓存"""
    
    def __init__(self, ttl: float, max_size: int = 100):
        super().__init__(max_size=max_size, ttl=ttl)


class LRUCache(Cache):
    """LRU缓存(无TTL)"""
    
    def __init__(self, max_size: int = 100):
        super().__init__(max_size=max_size, ttl=None)


# 使用示例
if __name__ == "__main__":
    # TTL缓存
    ttl_cache = TTLCache(ttl=5.0, max_size=100)
    ttl_cache.set("key1", "value1")
    
    # LRU缓存
    lru_cache = LRUCache(max_size=50)
    lru_cache.set("key2", "value2")
    
    # 装饰器使用
    cache = Cache(max_size=100, ttl=60)
    
    @cached(cache)
    def expensive_function(x, y):
        return x + y
    
    result = expensive_function(1, 2)
