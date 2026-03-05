import pytest
import sys
sys.path.insert(0, '.')

def test_modules_import():
    from distributed_lock import DistributedLock
    from optimistic_lock import OptimisticLock
    from pessimistic_lock import PessimisticLock
    from semaphore import Semaphore
    from rw_lock import ReadWriteLock
    assert True