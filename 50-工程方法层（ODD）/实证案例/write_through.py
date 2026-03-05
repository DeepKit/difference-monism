from collections import OrderedDict
from typing import Any, Optional, Callable
import time


class WriteThroughCache:
    """写透缓存实现"""
    
    def __init__(
        self,
        backing_store: Callable[[str], Any] = None,
        backing_writer: Callable[[str, Any], None] = None,
        backing_deleter: Callable[[str], None] = None,
        max_size: int = 1000,
        ttl: Optional[int] = None
    ):
        """
        初始化写透缓存
        
        Args:
            backing_store: 后端存储读取函数
            backing_writer: 后端存储写入函数
            backing_deleter: 后端存储删除函数
            max_size: 缓存最大容量
            ttl: 缓存过期时间(秒)，None表示永不过期
        """
        self.cache = OrderedDict()
        self.backing_store = backing_store or self._default_store_get
        self.backing_writer = backing_writer or self._default_store_set
        self.backing_deleter = backing_deleter or self._default_store_delete
        self.max_size = max_size
        self.ttl = ttl
        self.timestamps = {}
        self._store = {}  # 模拟后端存储
        
    def _default_store_get(self, key: str) -> Any:
        """默认后端存储读取"""
        return self._store.get(key)
    
    def _default_store_set(self, key: str, value: Any) -> None:
        """默认后端存储写入"""
        self._store[key] = value
    
    def _default_store_delete(self, key: str) -> None:
        """默认后端存储删除"""
        self._store.pop(key, None)
    
    def _is_expired(self, key: str) -> bool:
        """检查缓存项是否过期"""
        if self.ttl is None:
            return False
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl
    
    def _evict_if_needed(self) -> None:
        """如果超过容量限制则驱逐最旧的项"""
        while len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            self.timestamps.pop(oldest_key, None)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存值
        
        Args:
            key: 键
            default: 默认值
            
        Returns:
            缓存值或默认值
        """
        # 检查缓存是否存在且未过期
        if key in self.cache and not self._is_expired(key):
            # 移到末尾(LRU)
            self.cache.move_to_end(key)
            return self.cache[key]
        
        # 从后端存储读取
        value = self.backing_store(key)
        
        if value is not None:
            # 更新缓存
            self._evict_if_needed()
            self.cache[key] = value
            self.timestamps[key] = time.time()
            return value
        
        return default
    
    def set(self, key: str, value: Any) -> None:
        """
        设置缓存值(写透)
        
        Args:
            key: 键
            value: 值
        """
        # 写入后端存储
        self.backing_writer(key, value)
        
        # 写入缓存
        self._evict_if_needed()
        self.cache[key] = value
        self.timestamps[key] = time.time()
        self.cache.move_to_end(key)
    
    def delete(self, key: str) -> None:
        """
        删除缓存项
        
        Args:
            key: 键
        """
        # 从后端存储删除
        self.backing_deleter(key)
        
        # 从缓存删除
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.timestamps.clear()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if key in self.cache and not self._is_expired(key):
            return True
        return self.backing_store(key) is not None
    
    def size(self) -> int:
        """返回缓存大小"""
        return len(self.cache)
    
    def __contains__(self, key: str) -> bool:
        """支持 in 操作符"""
        return self.exists(key)
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """支持字典式赋值"""
        self.set(key, value)
    
    def __delitem__(self, key: str) -> None:
        """支持字典式删除"""
        self.delete(key)


# 使用示例
if __name__ == "__main__":
    # 创建写透缓存实例
    cache = WriteThroughCache(max_size=3, ttl=60)
    
    # 写入数据
    cache.set("user:1", {"name": "张三", "age": 25})
    cache.set("user:2", {"name": "李四", "age": 30})
    
    # 读取数据
    print(cache.get("user:1"))  # 从缓存读取
    
    # 字典式操作
    cache["user:3"] = {"name": "王五", "age": 28}
    print(cache["user:3"])
    
    # 检查存在
    print("user:1" in cache)  # True
    
    # 删除
    cache.delete("user:2")
    
    # 查看缓存大小
    print(f"缓存大小: {cache.size()}")
    
    # 清空缓存
    cache.clear()