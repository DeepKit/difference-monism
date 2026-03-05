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
        """获取缓存数据，未命中时自动加载"""
        with self._lock:
            # 检查缓存
            if key in self._cache:
                entry = self._cache[key]
                
                # 检查是否过期
                if entry['expires_at'] is None or time.time() < entry['expires_at']:
                    # 更新LRU顺序
                    self._cache.move_to_end(key)
                    return entry['value']
                else:
                    # 已过期，删除
                    del self._cache[key]
            
            # 缓存未命中，加载数据
            value = self.loader(key)
            self.set(key, value, ttl)
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存"""
        with self._lock:
            # 计算过期时间
            if ttl is None:
                ttl = self.default_ttl
            
            expires_at = None if ttl is None else time.time() + ttl
            
            # 如果key已存在，先删除（为了更新LRU顺序）
            if key in self._cache:
                del self._cache[key]
            
            # 检查容量限制
            if len(self._cache) >= self.max_size:
                # 删除最旧的项（LRU）
                self._cache.popitem(last=False)
            
            # 添加新项
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
    
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
        """检查key是否存在且未过期"""
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry['expires_at'] is None or time.time() < entry['expires_at']:
                return True
            
            # 已过期
            del self._cache[key]
            return False
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self._lock:
            return len(self._cache)
    
    def cleanup_expired(self) -> int:
        """清理所有过期项，返回清理数量"""
        with self._lock:
            expired_keys = []
            current_time = time.time()
            
            for key, entry in self._cache.items():
                if entry['expires_at'] is not None and current_time >= entry['expires_at']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)


def cached(cache: ReadThroughCache, key_func: Optional[Callable] = None, ttl: Optional[float] = None):
    """装饰器：为函数添加读透缓存"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 定义loader
            def loader(key):
                return func(*args, **kwargs)
            
            # 临时创建缓存实例或使用现有缓存
            temp_cache = ReadThroughCache(loader=loader, default_ttl=ttl)
            return temp_cache.get(cache_key, ttl)
        
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    # 模拟数据库查询
    def load_user(user_id: str) -> dict:
        print(f"从数据库加载用户: {user_id}")
        time.sleep(0.1)  # 模拟IO延迟
        return {"id": user_id, "name": f"User_{user_id}"}
    
    # 创建缓存实例
    cache = ReadThroughCache(
        loader=load_user,
        max_size=100,
        default_ttl=5.0  # 5秒过期
    )
    
    # 第一次访问 - 缓存未命中
    print(cache.get("user_1"))  # 从数据库加载
    
    # 第二次访问 - 缓存命中
    print(cache.get("user_1"))  # 从缓存返回
    
    # 手动设置缓存
    cache.set("user_2", {"id": "user_2", "name": "Manual User"}, ttl=10.0)
    
    # 检查存在性
    print(f"user_1 exists: {cache.exists('user_1')}")
    
    # 删除缓存
    cache.delete("user_1")
    
    # 清理过期项
    time.sleep(6)
    expired_count = cache.cleanup_expired()
    print(f"清理了 {expired_count} 个过期项")
    
    # 查看缓存大小
    print(f"当前缓存大小: {cache.size()}")