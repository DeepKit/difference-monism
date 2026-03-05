import time
import pickle
import hashlib
from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path
from typing import Any, Optional, Dict
from threading import Lock


class CacheLayer(ABC):
    """缓存层基类"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        pass


class MemoryCache(CacheLayer):
    """内存缓存层 (L1)"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.ttl_map: Dict[str, float] = {}
        self.lock = Lock()
    
    def _is_expired(self, key: str) -> bool:
        if key not in self.ttl_map:
            return False
        return time.time() > self.ttl_map[key]
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            if self._is_expired(key):
                self.delete(key)
                return None
            
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.max_size:
                    oldest_key = next(iter(self.cache))
                    self.delete(oldest_key)
            
            self.cache[key] = value
            
            if ttl:
                self.ttl_map[key] = time.time() + ttl
            elif key in self.ttl_map:
                del self.ttl_map[key]
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                if key in self.ttl_map:
                    del self.ttl_map[key]
                return True
            return False
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.ttl_map.clear()
    
    def exists(self, key: str) -> bool:
        with self.lock:
            if key not in self.cache:
                return False
            if self._is_expired(key):
                self.delete(key)
                return False
            return True


class DiskCache(CacheLayer):
    """磁盘缓存层 (L2)"""
    
    def __init__(self, cache_dir: str = ".cache", max_size: int = 10000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size = max_size
        self.index: OrderedDict = OrderedDict()
        self.lock = Lock()
        self._load_index()
    
    def _get_file_path(self, key: str) -> Path:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _load_index(self) -> None:
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self.index[data['key']] = data['expire_time']
            except:
                cache_file.unlink(missing_ok=True)
    
    def _is_expired(self, expire_time: Optional[float]) -> bool:
        if expire_time is None:
            return False
        return time.time() > expire_time
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.index:
                return None
            
            if self._is_expired(self.index[key]):
                self.delete(key)
                return None
            
            file_path = self._get_file_path(key)
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                    self.index.move_to_end(key)
                    return data['value']
            except:
                self.delete(key)
                return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self.lock:
            if len(self.index) >= self.max_size and key not in self.index:
                oldest_key = next(iter(self.index))
                self.delete(oldest_key)
            
            expire_time = time.time() + ttl if ttl else None
            file_path = self._get_file_path(key)
            
            data = {
                'key': key,
                'value': value,
                'expire_time': expire_time
            }
            
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)
                
                if key in self.index:
                    self.index.move_to_end(key)
                else:
                    self.index[key] = expire_time
            except Exception as e:
                print(f"Failed to write cache: {e}")
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key not in self.index:
                return False
            
            file_path = self._get_file_path(key)
            file_path.unlink(missing_ok=True)
            del self.index[key]
            return True
    
    def clear(self) -> None:
        with self.lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink(missing_ok=True)
            self.index.clear()
    
    def exists(self, key: str) -> bool:
        with self.lock:
            if key not in self.index:
                return False
            if self._is_expired(self.index[key]):
                self.delete(key)
                return False
            return True


class TieredCache:
    """分层缓存管理器"""
    
    def __init__(self, 
                 l1_size: int = 1000,
                 l2_size: int = 10000,
                 cache_dir: str = ".cache",
                 enable_l2: bool = True):
        self.l1 = MemoryCache(max_size=l1_size)
        self.l2 = DiskCache(cache_dir=cache_dir, max_size=l2_size) if enable_l2 else None
    
    def get(self, key: str) -> Optional[Any]:
        value = self.l1.get(key)
        if value is not None:
            return value
        
        if self.l2:
            value = self.l2.get(key)
            if value is not None:
                self.l1.set(key, value)
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self.l1.set(key, value, ttl)
        if self.l2:
            self.l2.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        l1_deleted = self.l1.delete(key)
        l2_deleted = self.l2.delete(key) if self.l2 else False
        return l1_deleted or l2_deleted
    
    def clear(self) -> None:
        self.l1.clear()
        if self.l2:
            self.l2.clear()
    
    def exists(self, key: str) -> bool:
        return self.l1.exists(key) or (self.l2 and self.l2.exists(key))


# 使用示例
if __name__ == "__main__":
    cache = TieredCache(l1_size=100, l2_size=1000)
    
    cache.set("user:1", {"name": "Alice", "age": 30}, ttl=60)
    cache.set("user:2", {"name": "Bob", "age": 25})
    
    print(cache.get("user:1"))
    print(cache.get("user:2"))
    print(cache.exists("user:3"))
    
    cache.delete("user:1")
    print(cache.get("user:1"))