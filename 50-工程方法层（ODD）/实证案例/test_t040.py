
# cache_invalidation.py
from typing import Set, Optional
from datetime import datetime, timedelta


class CacheInvalidation:
    """缓存失效管理类"""
    
    def __init__(self):
        self._invalidated_keys: Set[str] = set()
        self._invalidation_times: dict[str, datetime] = {}
    
    def invalidate(self, key: str) -> None:
        """标记缓存键为失效"""
        if not key:
            raise ValueError("Cache key cannot be empty")
        self._invalidated_keys.add(key)
        self._invalidation_times[key] = datetime.now()
    
    def is_invalidated(self, key: str) -> bool:
        """检查缓存键是否已失效"""
        return key in self._invalidated_keys
    
    def clear(self) -> None:
        """清除所有失效记录"""
        self._invalidated_keys.clear()
        self._invalidation_times.clear()
    
    def get_invalidation_time(self, key: str) -> Optional[datetime]:
        """获取缓存键的失效时间"""
        return self._invalidation_times.get(key)
    
    def invalidate_pattern(self, pattern: str) -> int:
        """按模式批量失效缓存键"""
        count = 0
        keys_to_invalidate = [k for k in self._invalidated_keys if pattern in k]
        for key in keys_to_invalidate:
            if key not in self._invalidated_keys:
                self.invalidate(key)
                count += 1
        return count
    
    def get_all_invalidated_keys(self) -> Set[str]:
        """获取所有已失效的缓存键"""
        return self._invalidated_keys.copy()
