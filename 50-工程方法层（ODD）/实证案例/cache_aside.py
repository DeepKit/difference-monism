import time
import threading
from typing import Any, Optional, Dict
from collections import OrderedDict


class AsideCache:
    """旁路缓存类 - 支持TTL和LRU淘汰策略"""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[float] = None):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认过期时间(秒)，None表示永不过期
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # 检查是否过期
            if entry['expire_at'] is not None and time.time() > entry['expire_at']:
                del self._cache[key]
                return None
            
            # LRU: 移到末尾
            self._cache.move_to_end(key)
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存值"""
        with self._lock:
            # 计算过期时间
            expire_at = None
            ttl_to_use = ttl if ttl is not None else self.default_ttl
            if ttl_to_use is not None:
                expire_at = time.time() + ttl_to_use
            
            # 如果已存在，先删除
            if key in self._cache:
                del self._cache[key]
            
            # 检查容量限制
            if len(self._cache) >= self.max_size:
                # 删除最旧的条目
                self._cache.popitem(last=False)
            
            # 添加新条目
            self._cache[key] = {
                'value': value,
                'expire_at': expire_at
            }
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
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
        """检查键是否存在且未过期"""
        return self.get(key) is not None
    
    def size(self) -> int:
        """返回当前缓存条目数"""
        with self._lock:
            return len(self._cache)
    
    def cleanup_expired(self) -> int:
        """清理所有过期条目，返回清理数量"""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry['expire_at'] is not None and current_time > entry['expire_at']
            ]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)


# 使用示例
if __name__ == "__main__":
    cache = AsideCache(max_size=100, default_ttl=60)
    
    # 设置缓存
    cache.set("user:1", {"name": "张三", "age": 25})
    cache.set("user:2", {"name": "李四", "age": 30}, ttl=10)
    
    # 获取缓存
    user = cache.get("user:1")
    print(f"用户信息: {user}")
    
    # 检查存在
    print(f"user:1 存在: {cache.exists('user:1')}")
    
    # 删除缓存
    cache.delete("user:1")
    
    # 清理过期
    time.sleep(11)
    cleaned = cache.cleanup_expired()
    print(f"清理了 {cleaned} 个过期条目")