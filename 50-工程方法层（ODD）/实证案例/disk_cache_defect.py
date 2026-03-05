
import os
import pickle
import hashlib
import time
import threading
from pathlib import Path
from typing import Any, Optional
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """缓存条目"""
    value: Any
    created_at: float
    accessed_at: float
    ttl: Optional[float] = None
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl


class DiskCache:
    """磁盘缓存实现"""
    
    def __init__(
        self,
        cache_dir: str = ".cache",
        max_size: int = 1000,
        default_ttl: Optional[float] = None
    ):
        """
        初始化磁盘缓存
        
        Args:
            cache_dir: 缓存目录路径
            max_size: 最大缓存条目数
            default_ttl: 默认过期时间（秒）
        """
        self.cache_dir = Path(cache_dir)
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
        self.index = OrderedDict()
        
        # 创建缓存目录
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载现有缓存索引
        self._load_index()
    
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _load_index(self):
        """加载缓存索引"""
        with self.lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        entry = pickle.load(f)
                        if isinstance(entry, CacheEntry):
                            # 从文件名反推key
                            key_hash = cache_file.stem
                            self.index[key_hash] = entry.accessed_at
                except Exception:
                    # 损坏的缓存文件，删除
                    cache_file.unlink(missing_ok=True)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ) -> None:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None表示使用默认值
        """
        with self.lock:
            cache_path = self._get_cache_path(key)
            key_hash = cache_path.stem
            
            # 创建缓存条目
            current_time = time.time()
            entry = CacheEntry(
                value=value,
                created_at=current_time,
                accessed_at=current_time,
                ttl=ttl if ttl is not None else self.default_ttl
            )
            
            # 写入磁盘
            with open(cache_path, 'wb') as f:
                pickle.dump(entry, f)
            
            # 更新索引
            if key_hash in self.index:
                self.index.move_to_end(key_hash)
            else:
                self.index[key_hash] = current_time
            
            # 检查缓存大小限制
            self._evict_if_needed()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            缓存值或默认值
        """
        with self.lock:
            cache_path = self._get_cache_path(key)
            key_hash = cache_path.stem
            
            if not cache_path.exists():
                return default
            
            try:
                with open(cache_path, 'rb') as f:
                    entry = pickle.load(f)
                
                # 检查是否过期
                if entry.is_expired():
                    self.delete(key)
                    return default
                
                # 更新访问时间
                entry.accessed_at = time.time()
                with open(cache_path, 'wb') as f:
                    pickle.dump(entry, f)
                
                # 更新索引（LRU）
                if key_hash in self.index:
                    self.index.move_to_end(key_hash)
                    self.index[key_hash] = entry.accessed_at
                
                return entry.value
                
            except Exception:
                # 读取失败，删除损坏的缓存
                self.delete(key)
                return default
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功删除
        """
        with self.lock:
            cache_path = self._get_cache_path(key)
            key_hash = cache_path.stem
            
            if cache_path.exists():
                cache_path.unlink()
                self.index.pop(key_hash, None)
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在且未过期"""
        with self.lock:
            cache_path = self._get_cache_path(key)
            
            if not cache_path.exists():
                return False
            
            try:
                with open(cache_path, 'rb') as f:
                    entry = pickle.load(f)
                return not entry.is_expired()
            except Exception:
                return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        with self.lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink(missing_ok=True)
            self.index.clear()
    
    def _evict_if_needed(self) -> None:
        """如果超过大小限制，驱逐最旧的条目"""
        while len(self.index) > self.max_size:
            # 获取最旧的条目
            oldest_key = next(iter(self.index))
            oldest_path = self.cache_dir / f"{oldest_key}.cache"
            
            # 删除文件和索引
            oldest_path.unlink(missing_ok=True)
            self.index.pop(oldest_key, None)
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期的缓存条目
        
        Returns:
            清理的条目数
        """
        with self.lock:
            cleaned = 0
            for cache_file in list(self.cache_dir.glob("*.cache")):
                try:
                    with open(cache_file, 'rb') as f:
                        entry = pickle.load(f)
                    
                    if entry.is_expired():
                        cache_file.unlink()
                        self.index.pop(cache_file.stem, None)
                        cleaned += 1
                except Exception:
                    cache_file.unlink(missing_ok=True)
                    cleaned += 1
            
            return cleaned
    
    def size(self) -> int:
        """获取当前缓存条目数"""
        with self.lock:
            return len(self.index)
    
    def __contains__(self, key: str) -> bool:
        """支持 in 操作符"""
        return self.exists(key)
    
    def __len__(self) -> int:
        """支持 len() 函数"""
        return self.size()
