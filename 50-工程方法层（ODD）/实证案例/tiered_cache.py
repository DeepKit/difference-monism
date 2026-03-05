import time
import pickle
import hashlib
from typing import Any, Optional, Dict, List
from collections import OrderedDict
from pathlib import Path
from threading import Lock
from abc import ABC, abstractmethod


class CacheLayer(ABC):
    """缓存层抽象基类"""
    
    def __init__(self, max_size: int, ttl: Optional[int] = None):
        self.max_size = max_size
        self.ttl = ttl
        self.lock = Lock()
    
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
    def size(self) -> int:
        pass


class MemoryCache(CacheLayer):
    """内存缓存层（L1）"""
    
    def __init__(self, max_size: int = 1000, ttl: Optional[int] = None):
        super().__init__(max_size, ttl)
        self.cache: OrderedDict = OrderedDict()
        self.expiry: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            if key in self.expiry and time.time() > self.expiry[key]:
                del self.cache[key]
                del self.expiry[key]
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
                    del self.cache[oldest_key]
                    self.expiry.pop(oldest_key, None)
            
            self.cache[key] = value
            
            expire_time = ttl or self.ttl
            if expire_time:
                self.expiry[key] = time.time() + expire_time
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.expiry.pop(key, None)
                return True
            return False
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.expiry.clear()
    
    def size(self) -> int:
        return len(self.cache)


class DiskCache(CacheLayer):
    """磁盘缓存层（L2）"""
    
    def __init__(self, cache_dir: str = ".cache", max_size: int = 10000, ttl: Optional[int] = None):
        super().__init__(max_size, ttl)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.index: OrderedDict = OrderedDict()
        self._load_index()
    
    def _get_file_path(self, key: str) -> Path:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _load_index(self) -> None:
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self.index[data['key']] = {
                        'file': cache_file,
                        'expiry': data.get('expiry')
                    }
            except:
                cache_file.unlink(missing_ok=True)
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.index:
                return None
            
            entry = self.index[key]
            if entry['expiry'] and time.time() > entry['expiry']:
                self.delete(key)
                return None
            
            try:
                with open(entry['file'], 'rb') as f:
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
            
            file_path = self._get_file_path(key)
            expire_time = ttl or self.ttl
            expiry = time.time() + expire_time if expire_time else None
            
            data = {
                'key': key,
                'value': value,
                'expiry': expiry
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            self.index[key] = {
                'file': file_path,
                'expiry': expiry
            }
            self.index.move_to_end(key)
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.index:
                entry = self.index[key]
                entry['file'].unlink(missing_ok=True)
                del self.index[key]
                return True
            return False
    
    def clear(self) -> None:
        with self.lock:
            for entry in self.index.values():
                entry['file'].unlink(missing_ok=True)
            self.index.clear()
    
    def size(self) -> int:
        return len(self.index)


class TieredCache:
    """分层缓存系统"""
    
    def __init__(self, layers: List[CacheLayer]):
        self.layers = layers
    
    def get(self, key: str) -> Optional[Any]:
        for i, layer in enumerate(self.layers):
            value = layer.get(key)
            if value is not None:
                for j in range(i):
                    self.layers[j].set(key, value)
                return value
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        for layer in self.layers:
            layer.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        deleted = False
        for layer in self.layers:
            if layer.delete(key):
                deleted = True
        return deleted
    
    def clear(self) -> None:
        for layer in self.layers:
            layer.clear()
    
    def stats(self) -> Dict[str, int]:
        return {
            f"layer_{i}_size": layer.size()
            for i, layer in enumerate(self.layers)
        }


if __name__ == "__main__":
    l1 = MemoryCache(max_size=100, ttl=300)
    l2 = DiskCache(cache_dir=".cache", max_size=1000, ttl=3600)
    
    cache = TieredCache([l1, l2])
    
    cache.set("user:1", {"name": "Alice", "age": 30})
    cache.set("user:2", {"name": "Bob", "age": 25}, ttl=60)
    
    print(cache.get("user:1"))
    print(cache.get("user:2"))
    print(cache.stats())
    
    cache.delete("user:1")
    print(cache.get("user:1"))
    
    cache.clear()