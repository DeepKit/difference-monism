
import time
import threading
from collections import OrderedDict
from typing import Any, Optional


class MemoryCache:
    """线程安全的内存缓存实现，支持TTL和LRU淘汰策略"""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[float] = None):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认过期时间（秒），None表示永不过期
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache = OrderedDict()
        self._lock = threading.RLock()
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None使用默认TTL
        """
        with self._lock:
            expire_time = None
            ttl_to_use = ttl if ttl is not None else self.default_ttl
            
            if ttl_to_use is not None:
                expire_time = time.time() + ttl_to_use
            
            if key in self._cache:
                del self._cache[key]
            
            self._cache[key] = {
                'value': value,
                'expire_time': expire_time
            }
            self._cache.move_to_end(key)
            
            if len(self._cache) > self.max_size:
                self._cache.popitem(last=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            default: 键不存在或已过期时的默认值
            
        Returns:
            缓存值或默认值
        """
        with self._lock:
            if key not in self._cache:
                return default
            
            item = self._cache[key]
            
            if item['expire_time'] is not None and time.time() > item['expire_time']:
                del self._cache[key]
                return default
            
            self._cache.move_to_end(key)
            return item['value']
    
    def delete(self, key: str) -> bool:
        """
        删除缓存项
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功删除
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()
    
    def exists(self, key: str) -> bool:
        """
        检查键是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            键是否存在
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            item = self._cache[key]
            if item['expire_time'] is not None and time.time() > item['expire_time']:
                del self._cache[key]
                return False
            
            return True
    
    def size(self) -> int:
        """返回当前缓存条目数"""
        with self._lock:
            return len(self._cache)
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期条目
        
        Returns:
            清理的条目数
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, item in self._cache.items()
                if item['expire_time'] is not None and current_time > item['expire_time']
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)
