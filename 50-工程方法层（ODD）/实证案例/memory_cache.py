
from collections import OrderedDict
from typing import Any, Optional
import time
import threading


class MemoryCache:
    def __init__(self, max_size: int = 100, default_ttl: Optional[float] = None):
        """
        初始化内存缓存
        
        :param max_size: 最大缓存容量
        :param default_ttl: 默认TTL（秒），None表示永不过期
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.lock = threading.RLock()
    
    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        """
        设置缓存项
        
        :param key: 键
        :param value: 值
        :param ttl: TTL（秒），None使用默认TTL
        """
        with self.lock:
            expire_time = None
            ttl_to_use = ttl if ttl is not None else self.default_ttl
            
            if ttl_to_use is not None:
                expire_time = time.time() + ttl_to_use
            
            if key in self.cache:
                self.cache.move_to_end(key)
            
            self.cache[key] = {
                'value': value,
                'expire_time': expire_time,
                'access_time': time.time()
            }
            
            if len(self.cache) > self.max_size:
                self._evict_lru()
    
    def get(self, key: Any, default: Any = None) -> Any:
        """
        获取缓存项
        
        :param key: 键
        :param default: 默认值
        :return: 缓存的值或默认值
        """
        with self.lock:
            if key not in self.cache:
                return default
            
            entry = self.cache[key]
            
            if entry['expire_time'] is not None and time.time() > entry['expire_time']:
                del self.cache[key]
                return default
            
            self.cache.move_to_end(key)
            entry['access_time'] = time.time()
            
            return entry['value']
    
    def delete(self, key: Any) -> bool:
        """
        删除缓存项
        
        :param key: 键
        :return: 是否成功删除
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        with self.lock:
            self.cache.clear()
    
    def _evict_lru(self) -> None:
        """淘汰最少使用的项"""
        if self.cache:
            self.cache.popitem(last=False)
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期项
        
        :return: 清理的项数
        """
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry['expire_time'] is not None and current_time > entry['expire_time']
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self.lock:
            return len(self.cache)
    
    def __contains__(self, key: Any) -> bool:
        """支持 in 操作符"""
        return self.get(key) is not None
    
    def __len__(self) -> int:
        """返回缓存大小"""
        return self.size()


# 使用示例
if __name__ == "__main__":
    cache = MemoryCache(max_size=3, default_ttl=5)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2", ttl=2)
    cache.set("key3", "value3")
    
    print(cache.get("key1"))  # value1
    print(cache.get("key2"))  # value2
    
    time.sleep(3)
    print(cache.get("key2"))  # None (已过期)
    
    cache.set("key4", "value4")  # 触发LRU淘汰
    print(cache.size())  # 3
    
    cache.cleanup_expired()
    print(cache.size())
