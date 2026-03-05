
import time
import threading
from typing import Any, Optional, Callable
from collections import OrderedDict
from functools import wraps


class BloomFilter:
    def __init__(self, size: int = 10000, hash_count: int = 3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size
        self.lock = threading.Lock()
    
    def _hash(self, item: str, seed: int) -> int:
        result = 0
        for char in str(item):
            result = (result * seed + ord(char)) % self.size
        return result
    
    def add(self, item: str):
        with self.lock:
            for i in range(self.hash_count):
                index = self._hash(item, i + 1)
                self.bit_array[index] = True
    
    def contains(self, item: str) -> bool:
        with self.lock:
            for i in range(self.hash_count):
                index = self._hash(item, i + 1)
                if not self.bit_array[index]:
                    return False
            return True


class LRUCache:
    def __init__(self, capacity: int, ttl: Optional[int] = None):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            if self.ttl and key in self.timestamps:
                if time.time() - self.timestamps[key] > self.ttl:
                    del self.cache[key]
                    del self.timestamps[key]
                    return None
            
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def set(self, key: str, value: Any):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.capacity:
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
                    if oldest_key in self.timestamps:
                        del self.timestamps[oldest_key]
            
            self.cache[key] = value
            if self.ttl:
                self.timestamps[key] = time.time()
    
    def delete(self, key: str):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            if key in self.timestamps:
                del self.timestamps[key]
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        with self.lock:
            return len(self.cache)


class MultiLevelCache:
    NULL_VALUE = object()
    
    def __init__(
        self,
        l1_capacity: int = 100,
        l2_capacity: int = 1000,
        l1_ttl: Optional[int] = 300,
        l2_ttl: Optional[int] = 3600,
        enable_penetration_protection: bool = True,
        bloom_filter_size: int = 10000
    ):
        self.l1_cache = LRUCache(l1_capacity, l1_ttl)
        self.l2_cache = LRUCache(l2_capacity, l2_ttl)
        self.enable_penetration_protection = enable_penetration_protection
        self.bloom_filter = BloomFilter(bloom_filter_size) if enable_penetration_protection else None
        self.lock = threading.RLock()
        self.stats = {
            'l1_hits': 0,
            'l2_hits': 0,
            'misses': 0,
            'penetration_blocks': 0
        }
    
    def get(self, key: str, loader: Optional[Callable[[], Any]] = None) -> Optional[Any]:
        value = self.l1_cache.get(key)
        if value is not None:
            with self.lock:
                self.stats['l1_hits'] += 1
            return None if value is self.NULL_VALUE else value
        
        value = self.l2_cache.get(key)
        if value is not None:
            with self.lock:
                self.stats['l2_hits'] += 1
            self.l1_cache.set(key, value)
            return None if value is self.NULL_VALUE else value
        
        if self.enable_penetration_protection and not self.bloom_filter.contains(key):
            with self.lock:
                self.stats['penetration_blocks'] += 1
            if loader:
                value = loader()
                if value is not None:
                    self.set(key, value)
                else:
                    self._cache_null_value(key)
                return value
            return None
        
        with self.lock:
            self.stats['misses'] += 1
        
        if loader:
            value = loader()
            if value is not None:
                self.set(key, value)
            else:
                self._cache_null_value(key)
            return value
        
        return None
    
    def set(self, key: str, value: Any):
        self.l1_cache.set(key, value)
        self.l2_cache.set(key, value)
        if self.enable_penetration_protection:
            self.bloom_filter.add(key)
    
    def _cache_null_value(self, key: str):
        self.l1_cache.set(key, self.NULL_VALUE)
        self.l2_cache.set(key, self.NULL_VALUE)
    
    def delete(self, key: str):
        self.l1_cache.delete(key)
        self.l2_cache.delete(key)
    
    def clear(self):
        self.l1_cache.clear()
        self.l2_cache.clear()
        with self.lock:
            self.stats = {
                'l1_hits': 0,
                'l2_hits': 0,
                'misses': 0,
                'penetration_blocks': 0
            }
    
    def get_stats(self) -> dict:
        with self.lock:
            total_requests = self.stats['l1_hits'] + self.stats['l2_hits'] + self.stats['misses']
            return {
                **self.stats,
                'total_requests': total_requests,
                'hit_rate': (self.stats['l1_hits'] + self.stats['l2_hits']) / total_requests if total_requests > 0 else 0,
                'l1_size': self.l1_cache.size(),
                'l2_size': self.l2_cache.size()
            }


# 使用示例
if __name__ == "__main__":
    cache = MultiLevelCache(
        l1_capacity=10,
        l2_capacity=100,
        l1_ttl=60,
        l2_ttl=300,
        enable_penetration_protection=True
    )
    
    # 基本使用
    cache.set("user:1", {"name": "Alice", "age": 30})
    print(cache.get("user:1"))
    
    # 使用loader函数
    def load_user(user_id):
        print(f"Loading user {user_id} from database...")
        return {"name": "Bob", "age": 25}
    
    result = cache.get("user:2", loader=lambda: load_user(2))
    print(result)
    
    # 缓存穿透保护测试
    result = cache.get("non_existent_key")
    print(f"Non-existent key result: {result}")
    
    # 统计信息
    print(cache.get_stats())
