import pytest
from time import sleep
from cache import Cache, CacheError


def test_basic_set_get():
    cache = Cache(max_size=10)
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'


def test_get_nonexistent_key():
    cache = Cache()
    assert cache.get('nonexistent') is None
    assert cache.get('nonexistent', 'default') == 'default'


def test_ttl_expiration():
    cache = Cache()
    cache.set('key1', 'value1', ttl=1)
    assert cache.get('key1') == 'value1'
    sleep(1.1)
    assert cache.get('key1') is None


def test_lru_eviction():
    cache = Cache(max_size=3)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    cache.get('key1')
    cache.set('key4', 'value4')
    assert cache.get('key1') == 'value1'
    assert cache.get('key2') is None
    assert cache.get('key3') == 'value3'
    assert cache.get('key4') == 'value4'


def test_update_existing_key():
    cache = Cache(max_size=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key1', 'new_value1')
    assert cache.get('key1') == 'new_value1'
    assert cache.size() == 2


def test_delete():
    cache = Cache()
    cache.set('key1', 'value1')
    assert cache.delete('key1') is True
    assert cache.get('key1') is None
    assert cache.delete('key1') is False


def test_clear():
    cache = Cache()
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.get('key1')
    cache.clear()
    assert cache.size() == 0
    assert cache.get('key1') is None
    stats = cache.stats()
    assert stats['hits'] == 0
    assert stats['misses'] == 0


def test_stats():
    cache = Cache(max_size=10)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.get('key1')
    cache.get('key1')
    cache.get('key3')
    stats = cache.stats()
    assert stats['hits'] == 2
    assert stats['misses'] == 1
    assert stats['hit_rate'] == 2/3
    assert stats['size'] == 2
    assert stats['max_size'] == 10


def test_contains_operator():
    cache = Cache()
    cache.set('key1', 'value1')
    assert 'key1' in cache
    assert 'key2' not in cache


def test_contains_with_expired_key():
    cache = Cache()
    cache.set('key1', 'value1', ttl=1)
    assert 'key1' in cache
    sleep(1.1)
    assert 'key1' not in cache


def test_invalid_max_size():
    with pytest.raises(ValueError):
        Cache(max_size=0)
    with pytest.raises(ValueError):
        Cache(max_size=-1)


def test_different_value_types():
    cache = Cache()
    cache.set('int', 42)
    cache.set('list', [1, 2, 3])
    cache.set('dict', {'a': 1})
    cache.set('none', None)
    assert cache.get('int') == 42
    assert cache.get('list') == [1, 2, 3]
    assert cache.get('dict') == {'a': 1}
    assert cache.get('none') is None


def test_size():
    cache = Cache(max_size=5)
    assert cache.size() == 0
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    assert cache.size() == 2
    cache.delete('key1')
    assert cache.size() == 1
