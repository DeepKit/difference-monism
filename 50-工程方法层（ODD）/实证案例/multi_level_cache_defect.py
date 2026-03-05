
from collections import OrderedDict
from typing import Any, Optional, List
from threading import Lock
from dataclasses import dataclass
from enum import Enum


class EvictionPolicy(Enum):
    """缓存淘汰策略"""
    LRU = "lru"  # 最近最少使用
    LFU = "lfu"  # 最不经常使用
    FIFO = "fifo"  # 先进先出


@dataclass
class CacheLevel:
    """缓存级别配置"""
    name: str
    max_size: int
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU


class LRUCache:
    """LRU缓存实现"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def put(self, key: str, value: Any) -> Optional[tuple]:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                self.cache[key] = value
                return None
            
            evicted = None
            if len(self.cache) >= self.max_size:
                evicted_key, evicted_value = self.cache.popitem(last=False)
                evicted = (evicted_key, evicted_value)
            
            self.cache[key] = value
            return evicted
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self):
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        with self.lock:
            return len(self.cache)


class LFUCache:
    """LFU缓存实现"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = {}
        self.freq = {}
        self.min_freq = 0
        self.freq_list = {}
        self.lock = Lock()
    
    def _update_freq(self, key: str):
        freq = self.freq[key]
        self.freq[key] = freq + 1
        self.freq_list[freq].remove(key)
        
        if not self.freq_list[freq]:
            del self.freq_list[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        
        if freq + 1 not in self.freq_list:
            self.freq_list[freq + 1] = []
        self.freq_list[freq + 1].append(key)
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            self._update_freq(key)
            return self.cache[key]
    
    def put(self, key: str, value: Any) -> Optional[tuple]:
        with self.lock:
            if self.max_size == 0:
                return None
            
            if key in self.cache:
                self.cache[key] = value
                self._update_freq(key)
                return None
            
            evicted = None
            if len(self.cache) >= self.max_size:
                evict_key = self.freq_list[self.min_freq][0]
                self.freq_list[self.min_freq].pop(0)
                evicted = (evict_key, self.cache[evict_key])
                del self.cache[evict_key]
                del self.freq[evict_key]
            
            self.cache[key] = value
            self.freq[key] = 1
            self.min_freq = 1
            if 1 not in self.freq_list:
                self.freq_list[1] = []
            self.freq_list[1].append(key)
            
            return evicted
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                freq = self.freq[key]
                self.freq_list[freq].remove(key)
                del self.cache[key]
                del self.freq[key]
                return True
            return False
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.freq.clear()
            self.freq_list.clear()
            self.min_freq = 0
    
    def size(self) -> int:
        with self.lock:
            return len(self.cache)


class FIFOCache:
    """FIFO缓存实现"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            return self.cache.get(key)
    
    def put(self, key: str, value: Any) -> Optional[tuple]:
        with self.lock:
            if key in self.cache:
                self.cache[key] = value
                return None
            
            evicted = None
            if len(self.cache) >= self.max_size:
                evicted_key, evicted_value = self.cache.popitem(last=False)
                evicted = (evicted_key, evicted_value)
            
            self.cache[key] = value
            return evicted
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self):
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        with self.lock:
            return len(self.cache)


class MultiLevelCache:
    """多级缓存系统"""
    
    def __init__(self, levels: List[CacheLevel]):
        if not levels:
            raise ValueError("至少需要一个缓存级别")
        
        self.levels = []
        for level_config in levels:
            if level_config.eviction_policy == EvictionPolicy.LRU:
                cache = LRUCache(level_config.max_size)
            elif level_config.eviction_policy == EvictionPolicy.LFU:
                cache = LFUCache(level_config.max_size)
            elif level_config.eviction_policy == EvictionPolicy.FIFO:
                cache = FIFOCache(level_config.max_size)
            else:
                raise ValueError(f"不支持的淘汰策略: {level_config.eviction_policy}")
            
            self.levels.append({
                'name': level_config.name,
                'cache': cache
            })
        
        self.lock = Lock()
        self.stats = {
            'hits': [0] * len(levels),
            'misses': 0,
            'promotions': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值，自动提升到更高级别"""
        with self.lock:
            for i, level in enumerate(self.levels):
                value = level['cache'].get(key)
                if value is not None:
                    self.stats['hits'][i] += 1
                    
                    # 提升到更高级别
                    if i > 0:
                        self.stats['promotions'] += 1
                        for j in range(i):
                            self.levels[j]['cache'].put(key, value)
                    
                    return value
            
            self.stats['misses'] += 1
            return None
    
    def put(self, key: str, value: Any):
        """写入缓存到所有级别"""
        with self.lock:
            for level in self.levels:
                level['cache'].put(key, value)
    
    def delete(self, key: str):
        """从所有级别删除缓存"""
        with self.lock:
            for level in self.levels:
                level['cache'].delete(key)
    
    def clear(self):
        """清空所有级别缓存"""
        with self.lock:
            for level in self.levels:
                level['cache'].clear()
            self.stats = {
                'hits': [0] * len(self.levels),
                'misses': 0,
                'promotions': 0
            }
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        with self.lock:
            total_hits = sum(self.stats['hits'])
            total_requests = total_hits + self.stats['misses']
            hit_rate = total_hits / total_requests if total_requests > 0 else 0
            
            level_stats = []
            for i, level in enumerate(self.levels):
                level_stats.append({
                    'name': level['name'],
                    'size': level['cache'].size(),
                    'hits': self.stats['hits'][i]
                })
            
            return {
                'levels': level_stats,
                'total_hits': total_hits,
                'misses': self.stats['misses'],
                'promotions': self.stats['promotions'],
                'hit_rate': hit_rate
            }


# 使用示例
if __name__ == "__main__":
    # 配置三级缓存：L1(小而快) -> L2(中等) -> L3(大而慢)
    cache = MultiLevelCache([
        CacheLevel(name="L1", max_size=10, eviction_policy=EvictionPolicy.LRU),
        CacheLevel(name="L2", max_size=50, eviction_policy=EvictionPolicy.LRU),
        CacheLevel(name="L3", max_size=200, eviction_policy=EvictionPolicy.LFU)
    ])
    
    # 写入数据
    cache.put("user:1", {"name": "张三", "age": 25})
    cache.put("user:2", {"name": "李四", "age": 30})
    
    # 读取数据
    user1 = cache.get("user:1")
    print(f"用户1: {user1}")
    
    # 查看统计
    stats = cache.get_stats()
    print(f"缓存统计: {stats}")
