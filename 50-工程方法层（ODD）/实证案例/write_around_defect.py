from collections import OrderedDict
from typing import Any, Optional, Callable


class WriteAroundCache:
    """绕写缓存实现 - 写操作绕过缓存直接写入后端存储"""
    
    def __init__(self, capacity: int, backend_read: Callable, backend_write: Callable):
        """
        初始化绕写缓存
        
        Args:
            capacity: 缓存容量
            backend_read: 后端读取函数 (key) -> value
            backend_write: 后端写入函数 (key, value) -> None
        """
        self.capacity = capacity
        self.cache = OrderedDict()
        self.backend_read = backend_read
        self.backend_write = backend_write
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """读取数据 - 先查缓存，未命中则从后端读取并填充缓存"""
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        
        self.misses += 1
        value = self.backend_read(key)
        
        if value is not None:
            self._add_to_cache(key, value)
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """写入数据 - 直接写入后端，不写入缓存（绕写策略）"""
        self.backend_write(key, value)
        
        # 如果缓存中存在该key，需要使其失效
        if key in self.cache:
            del self.cache[key]
    
    def _add_to_cache(self, key: str, value: Any) -> None:
        """将数据添加到缓存，使用LRU淘汰策略"""
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def invalidate(self, key: str) -> None:
        """使缓存中的某个key失效"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
    
    def stats(self) -> dict:
        """返回缓存统计信息"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache),
            'capacity': self.capacity
        }


# 使用示例
if __name__ == '__main__':
    # 模拟后端存储
    backend_storage = {}
    
    def backend_read(key):
        print(f"从后端读取: {key}")
        return backend_storage.get(key)
    
    def backend_write(key, value):
        print(f"写入后端: {key} = {value}")
        backend_storage[key] = value
    
    # 创建容量为3的绕写缓存
    cache = WriteAroundCache(capacity=3, backend_read=backend_read, backend_write=backend_write)
    
    # 写入操作 - 直接写入后端，不进缓存
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    
    print("\n--- 读取操作 ---")
    # 第一次读取 - 缓存未命中，从后端读取并填充缓存
    print(f"读取 a: {cache.get('a')}")
    print(f"读取 b: {cache.get('b')}")
    
    # 第二次读取 - 缓存命中
    print(f"再次读取 a: {cache.get('a')}")
    
    print("\n--- 写入后缓存失效 ---")
    # 写入操作会使缓存失效
    cache.set('a', 100)
    print(f"读取更新后的 a: {cache.get('a')}")
    
    print("\n--- 统计信息 ---")
    print(cache.stats())