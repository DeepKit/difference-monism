import pytest
import sys
sys.path.insert(0, '.')

def test_modules_import():
    from memory_cache import MemoryCache
    from disk_cache import DiskCache
    from multi_level_cache import MultiLevelCache
    from cache_warming import CacheWarming
    from cache_invalidation import CacheInvalidation
    assert True
