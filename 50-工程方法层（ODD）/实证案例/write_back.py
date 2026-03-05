from collections import OrderedDict
from threading import Lock
from typing import Any, Optional, Callable
import time


class WriteBackCache:
    """写回缓存实现，支持LRU淘汰策略"""
    
    def __init__(
        self,
        capacity: int,
        write_back_func: Callable[[Any, Any], None],
        ttl: Optional[int] = None
    ):
        """
        初始化写回缓存
        
        Args:
            capacity: 缓存容量
            write_back_func: 回写函数，接收(key, value)参数
            ttl: 缓存项过期时间(秒)，None表示不过期
        """
        self.capacity = capacity
        self.write_back_func = write_back_func
        self.ttl = ttl
        self.cache = OrderedDict()
        self.dirty_keys = set()
        self.timestamps = {}
        self.lock = Lock()
        
    def get(self, key: Any) -> Optional[Any]:
        """获取缓存值"""
        with self.lock:
            if key not in self.cache:
                return None
            
            # 检查是否过期
            if self._is_expired(key):
                self._evict(key)
                return None
            
            # LRU: 移到末尾
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def set(self, key: Any, value: Any) -> None:
        """设置缓存值"""
        with self.lock:
            if key in self.cache:
                # 更新现有值
                self.cache[key] = value
                self.cache.move_to_end(key)
            else:
                # 新增值
                if len(self.cache) >= self.capacity:
                    self._evict_lru()
                self.cache[key] = value
            
            # 标记为脏数据
            self.dirty_keys.add(key)
            
            # 更新时间戳
            if self.ttl:
                self.timestamps[key] = time.time()
    
    def delete(self, key: Any) -> bool:
        """删除缓存项"""
        with self.lock:
            if key not in self.cache:
                return False
            
            # 如果是脏数据，先回写
            if key in self.dirty_keys:
                self._write_back(key)
            
            del self.cache[key]
            self.dirty_keys.discard(key)
            self.timestamps.pop(key, None)
            return True
    
    def flush(self, key: Optional[Any] = None) -> None:
        """刷新缓存到存储"""
        with self.lock:
            if key is not None:
                # 刷新单个键
                if key in self.dirty_keys:
                    self._write_back(key)
            else:
                # 刷新所有脏数据
                for dirty_key in list(self.dirty_keys):
                    self._write_back(dirty_key)
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            # 先刷新所有脏数据
            self.flush()
            self.cache.clear()
            self.dirty_keys.clear()
            self.timestamps.clear()
    
    def _write_back(self, key: Any) -> None:
        """回写数据到存储（内部方法，需要持有锁）"""
        if key in self.cache:
            try:
                self.write_back_func(key, self.cache[key])
                self.dirty_keys.discard(key)
            except Exception as e:
                print(f"写回失败 key={key}: {e}")
    
    def _evict_lru(self) -> None:
        """淘汰最久未使用的项（内部方法，需要持有锁）"""
        if not self.cache:
            return
        
        # 获取最旧的键
        oldest_key = next(iter(self.cache))
        self._evict(oldest_key)
    
    def _evict(self, key: Any) -> None:
        """淘汰指定项（内部方法，需要持有锁）"""
        if key not in self.cache:
            return
        
        # 如果是脏数据，先回写
        if key in self.dirty_keys:
            self._write_back(key)
        
        del self.cache[key]
        self.dirty_keys.discard(key)
        self.timestamps.pop(key, None)
    
    def _is_expired(self, key: Any) -> bool:
        """检查是否过期（内部方法，需要持有锁）"""
        if not self.ttl or key not in self.timestamps:
            return False
        return time.time() - self.timestamps[key] > self.ttl
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self.lock:
            return len(self.cache)
    
    def dirty_count(self) -> int:
        """返回脏数据数量"""
        with self.lock:
            return len(self.dirty_keys)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()


# 使用示例
if __name__ == "__main__":
    # 模拟数据库写入
    database = {}
    
    def write_to_db(key, value):
        print(f"写入数据库: {key} = {value}")
        database[key] = value
    
    # 创建写回缓存
    cache = WriteBackCache(capacity=3, write_back_func=write_to_db, ttl=10)
    
    # 写入数据（只写缓存，不立即写数据库）
    cache.set("user:1", {"name": "Alice", "age": 25})
    cache.set("user:2", {"name": "Bob", "age": 30})
    cache.set("user:3", {"name": "Charlie", "age": 35})
    
    print(f"缓存大小: {cache.size()}, 脏数据: {cache.dirty_count()}")
    
    # 读取数据
    print(f"读取: {cache.get('user:1')}")
    
    # 触发淘汰（容量满了）
    cache.set("user:4", {"name": "David", "age": 40})
    
    # 手动刷新
    cache.flush("user:2")
    
    # 清空缓存（会自动刷新所有脏数据）
    cache.clear()
    
    print(f"数据库内容: {database}")