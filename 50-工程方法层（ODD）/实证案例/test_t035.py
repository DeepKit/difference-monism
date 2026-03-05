import pytest
import sys
sys.path.insert(0, '.')
from rw_lock import ReadWriteLock

def test_rwlock_init():
    lock = ReadWriteLock()
    assert lock is not None

def test_rwlock_read():
    lock = ReadWriteLock()
    with lock.read_lock():
        pass

def test_rwlock_write():
    lock = ReadWriteLock()
    with lock.write_lock():
        pass