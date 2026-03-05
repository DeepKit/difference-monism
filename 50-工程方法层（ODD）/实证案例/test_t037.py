
import pytest
import os
import tempfile
import shutil
from pathlib import Path

# 假设 DiskCache 在这个位置导入
# from your_module import DiskCache


class TestDiskCacheBasic:
    """DiskCache 基本功能测试"""
    
    @pytest.fixture
    def cache_dir(self):
        """创建临时缓存目录"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def cache(self, cache_dir):
        """创建 DiskCache 实例"""
        return DiskCache(cache_dir)
    
    def test_init(self, cache_dir):
        """测试初始化"""
        cache = DiskCache(cache_dir)
        assert cache is not None
        assert os.path.exists(cache_dir)
    
    def test_set_and_get(self, cache):
        """测试设置和获取值"""
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_get_nonexistent_key(self, cache):
        """测试获取不存在的键"""
        result = cache.get("nonexistent")
        assert result is None
    
    def test_get_with_default(self, cache):
        """测试带默认值的获取"""
        result = cache.get("nonexistent", default="default_value")
        assert result == "default_value"
    
    def test_contains(self, cache):
        """测试键是否存在"""
        cache.set("key1", "value1")
        assert "key1" in cache
        assert "key2" not in cache
    
    def test_delete(self, cache):
        """测试删除键"""
        cache.set("key1", "value1")
        cache.delete("key1")
        assert "key1" not in cache
    
    def test_delete_nonexistent(self, cache):
        """测试删除不存在的键"""
        # 不应该抛出异常
        cache.delete("nonexistent")
    
    def test_clear(self, cache):
        """测试清空缓存"""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert "key1" not in cache
        assert "key2" not in cache
    
    def test_multiple_types(self, cache):
        """测试不同数据类型"""
        cache.set("string", "text")
        cache.set("number", 42)
        cache.set("list", [1, 2, 3])
        cache.set("dict", {"a": 1, "b": 2})
        
        assert cache.get("string") == "text"
        assert cache.get("number") == 42
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"a": 1, "b": 2}
    
    def test_overwrite_value(self, cache):
        """测试覆盖已存在的值"""
        cache.set("key1", "value1")
        cache.set("key1", "value2")
        assert cache.get("key1") == "value2"
    
    def test_persistence(self, cache_dir):
        """测试持久化"""
        cache1 = DiskCache(cache_dir)
        cache1.set("key1", "value1")
        
        # 创建新实例，应该能读取之前的数据
        cache2 = DiskCache(cache_dir)
        assert cache2.get("key1") == "value1"
