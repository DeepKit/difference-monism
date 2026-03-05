import time
import threading
from typing import Any, Callable, Optional, Dict
from collections import OrderedDict
from functools import wraps


class ReadThroughCache:
    """读透缓存实现，支持TTL和LRU淘汰策略"""
    
    def __init__(
        self,
        loader: Callable[[str], Any],
        max_size: int = 1000,
        default_ttl: Optional[float] = None
    ):
        """
        Args:
            loader: 缓存未命中时的数据加载函数
            max_size: 缓存最大容量
            default_ttl: 默认过期时间(秒)，None表示永不过期
        """
        self.loader = loader
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str, ttl: Optional[float] = None) -> Any:
        """获取缓存值，缓存未命中时自动加载"""
        with self._lock:
            # 检查缓存是否存在且未过期
            if key in self._cache:
                entry = self._cache[key]
                if not self._is_expired(entry):
                    # 更新LRU顺序
                    self._cache.move_to_end(key)
                    return entry['value']
                else:
                    # 过期则删除
                    del self._cache[key]
            
            # 缓存未命中，加载数据
            value = self.loader(key)
            self.set(key, value, ttl)
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存值"""
        with self._lock:
            # 如果达到容量上限，删除最旧的项
            if key not in self._cache and len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            
            expire_time = None
            if ttl is not None:
                expire_time = time.time() + ttl
            elif self.default_ttl is not None:
                expire_time = time.time() + self.default_ttl
            
            self._cache[key] = {
                'value': value,
                'expire_time': expire_time
            }
            self._cache.move_to_end(key)
    
    def delete(self, key: str) -> bool:
        """删除缓存项"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在且未过期"""
        with self._lock:
            if key not in self._cache:
                return False
            entry = self._cache[key]
            if self._is_expired(entry):
                del self._cache[key]
                return False
            return True
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self._lock:
            return len(self._cache)
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """检查缓存项是否过期"""
        expire_time = entry.get('expire_time')
        if expire_time is None:
            return False
        return time.time() > expire_time
    
    def cleanup_expired(self) -> int:
        """清理所有过期项，返回清理数量"""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if self._is_expired(entry)
            ]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)


def cached(cache: ReadThroughCache, ttl: Optional[float] = None):
    """装饰器：为函数添加读透缓存"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(key: str, *args, **kwargs) -> Any:
            return cache.get(key, ttl)
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    # 模拟数据源
    def load_from_db(key: str) -> str:
        print(f"从数据库加载: {key}")
        time.sleep(0.1)  # 模拟IO延迟
        return f"value_for_{key}"
    
    # 创建缓存实例
    cache = ReadThroughCache(
        loader=load_from_db,
        max_size=100,
        default_ttl=5.0  # 5秒过期
    )
    
    # 测试读透功能
    print(cache.get("key1"))  # 缓存未命中，从数据库加载
    print(cache.get("key1"))  # 缓存命中，直接返回
    
    # 手动设置
    cache.set("key2", "manual_value", ttl=10.0)
    print(cache.get("key2"))
    
    # 检查存在性
    print(f"key1存在: {cache.exists('key1')}")
    
    # 删除
    cache.delete("key1")
    print(f"删除后key1存在: {cache.exists('key1')}")
    
    # 查看缓存大小
    print(f"缓存大小: {cache.size()}")
    
    # 清空缓存
    cache.clear()
    print(f"清空后大小: {cache.size()}")