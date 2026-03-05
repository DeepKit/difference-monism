from collections import OrderedDict
from typing import Any, Optional
import time


class CacheError(Exception):
    pass


class CacheKeyError(CacheError):
    pass


class CacheCapacityError(CacheError):
    pass


class LRUCache:
    def __init__(self, max_size: int = 100, default_ttl: Optional[float] = None):
        if max_size <= 0:
            raise CacheCapacityError("缓存容量必须大于0")
        self._cache = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        if not isinstance(key, str):
            raise CacheError("缓存键必须是字符串类型")
        
        expire_time = None
        ttl_to_use = ttl if ttl is not None else self._default_ttl
        if ttl_to_use is not None:
            if ttl_to_use <= 0:
                raise CacheError("TTL必须大于0")
            expire_time = time.time() + ttl_to_use
        
        if key in self._cache:
            del self._cache[key]
        
        if len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
        
        self._cache[key] = {'value': value, 'expire_time': expire_time}
    
    def get(self, key: str, default: Any = None) -> Any:
        if not isinstance(key, str):
            raise CacheError("缓存键必须是字符串类型")
        
        if key not in self._cache:
            self._misses += 1
            return default
        
        item = self._cache[key]
        if item['expire_time'] is not None and time.time() > item['expire_time']:
            del self._cache[key]
            self._misses += 1
            return default
        
        self._cache.move_to_end(key)
        self._hits += 1
        return item['value']
    
    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0
    
    def exists(self, key: str) -> bool:
        if key not in self._cache:
            return False
        item = self._cache[key]
        if item['expire_time'] is not None and time.time() > item['expire_time']:
            del self._cache[key]
            return False
        return True
    
    def size(self) -> int:
        self._cleanup_expired()
        return len(self._cache)
    
    def _cleanup_expired(self) -> None:
        current_time = time.time()
        expired_keys = [key for key, item in self._cache.items() if item['expire_time'] is not None and current_time > item['expire_time']]
        for key in expired_keys:
            del self._cache[key]
    
    def get_stats(self) -> dict:
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0.0
        return {'hits': self._hits, 'misses': self._misses, 'hit_rate': round(hit_rate, 2), 'size': self.size(), 'max_size': self._max_size}
    
    def reset_stats(self) -> None:
        self._hits = 0
        self._misses = 0
