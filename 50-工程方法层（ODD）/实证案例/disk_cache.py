
import os
import pickle
import time
import hashlib
import threading
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta


class DiskCache:
    def __init__(self, cache_dir: str = ".cache", max_size_mb: int = 100, default_ttl: int = 3600):
        """
        初始化磁盘缓存
        
        :param cache_dir: 缓存目录路径
        :param max_size_mb: 最大缓存大小(MB)
        :param default_ttl: 默认过期时间(秒)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl
        self.lock = threading.Lock()
        self._cleanup_thread = None
        self._start_cleanup_thread()
    
    def _get_cache_path(self, key: str) -> Path:
        """生成缓存文件路径"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _get_meta_path(self, key: str) -> Path:
        """生成元数据文件路径"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.meta"
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        设置缓存
        
        :param key: 缓存键
        :param value: 缓存值
        :param ttl: 过期时间(秒)，None使用默认值
        :return: 是否成功
        """
        try:
            with self.lock:
                cache_path = self._get_cache_path(key)
                meta_path = self._get_meta_path(key)
                
                # 序列化数据
                with open(cache_path, 'wb') as f:
                    pickle.dump(value, f)
                
                # 保存元数据
                expire_time = time.time() + (ttl if ttl is not None else self.default_ttl)
                meta = {
                    'key': key,
                    'expire_time': expire_time,
                    'created_time': time.time()
                }
                with open(meta_path, 'wb') as f:
                    pickle.dump(meta, f)
                
                # 检查缓存大小
                self._check_size_limit()
                return True
        except Exception as e:
            print(f"设置缓存失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存
        
        :param key: 缓存键
        :param default: 默认值
        :return: 缓存值或默认值
        """
        try:
            with self.lock:
                cache_path = self._get_cache_path(key)
                meta_path = self._get_meta_path(key)
                
                if not cache_path.exists() or not meta_path.exists():
                    return default
                
                # 读取元数据
                with open(meta_path, 'rb') as f:
                    meta = pickle.load(f)
                
                # 检查是否过期
                if time.time() > meta['expire_time']:
                    self._delete_cache_files(key)
                    return default
                
                # 读取缓存数据
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"获取缓存失败: {e}")
            return default
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        :param key: 缓存键
        :return: 是否成功
        """
        try:
            with self.lock:
                return self._delete_cache_files(key)
        except Exception as e:
            print(f"删除缓存失败: {e}")
            return False
    
    def _delete_cache_files(self, key: str) -> bool:
        """删除缓存文件和元数据"""
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        deleted = False
        if cache_path.exists():
            cache_path.unlink()
            deleted = True
        if meta_path.exists():
            meta_path.unlink()
            deleted = True
        
        return deleted
    
    def clear(self) -> bool:
        """清空所有缓存"""
        try:
            with self.lock:
                for file in self.cache_dir.glob("*.cache"):
                    file.unlink()
                for file in self.cache_dir.glob("*.meta"):
                    file.unlink()
                return True
        except Exception as e:
            print(f"清空缓存失败: {e}")
            return False
    
    def _check_size_limit(self):
        """检查并清理超出大小限制的缓存"""
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*"))
        
        if total_size > self.max_size_bytes:
            # 获取所有缓存文件及其创建时间
            cache_files = []
            for meta_file in self.cache_dir.glob("*.meta"):
                try:
                    with open(meta_file, 'rb') as f:
                        meta = pickle.load(f)
                        cache_files.append((meta['created_time'], meta['key']))
                except:
                    continue
            
            # 按创建时间排序，删除最旧的
            cache_files.sort()
            for _, key in cache_files:
                self._delete_cache_files(key)
                total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*"))
                if total_size <= self.max_size_bytes * 0.8:
                    break
    
    def _cleanup_expired(self):
        """清理过期缓存"""
        try:
            with self.lock:
                current_time = time.time()
                for meta_file in self.cache_dir.glob("*.meta"):
                    try:
                        with open(meta_file, 'rb') as f:
                            meta = pickle.load(f)
                        
                        if current_time > meta['expire_time']:
                            self._delete_cache_files(meta['key'])
                    except:
                        continue
        except Exception as e:
            print(f"清理过期缓存失败: {e}")
    
    def _start_cleanup_thread(self):
        """启动自动清理线程"""
        def cleanup_loop():
            while True:
                time.sleep(60)  # 每60秒清理一次
                self._cleanup_expired()
        
        self._cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        self._cleanup_thread.start()
    
    def __contains__(self, key: str) -> bool:
        """检查键是否存在"""
        return self.get(key) is not None
    
    def __len__(self) -> int:
        """返回缓存项数量"""
        return len(list(self.cache_dir.glob("*.cache")))


# 使用示例
if __name__ == "__main__":
    cache = DiskCache(cache_dir=".my_cache", max_size_mb=50, default_ttl=300)
    
    # 设置缓存
    cache.set("user:1", {"name": "Alice", "age": 30}, ttl=600)
    cache.set("user:2", {"name": "Bob", "age": 25})
    
    # 获取缓存
    user1 = cache.get("user:1")
    print(f"User 1: {user1}")
    
    # 删除缓存
    cache.delete("user:2")
    
    # 检查是否存在
    print(f"user:1 exists: {'user:1' in cache}")
    print(f"user:2 exists: {'user:2' in cache}")
    
    # 清空所有缓存
    # cache.clear()
