import pytest
import sys
sys.path.insert(0, '.')
from semaphore import Semaphore

def test_semaphore_init():
    sem = Semaphore(2)
    assert sem is not None

def test_semaphore_acquire():
    sem = Semaphore(2)
    result = sem.acquire()
    assert result == True

def test_semaphore_release():
    sem = Semaphore(2)
    sem.acquire()
    sem.release()
    assert sem.available() == 2