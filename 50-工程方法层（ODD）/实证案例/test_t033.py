
import pytest
import threading
import time
from your_module import PessimisticLock


class TestPessimisticLock:
    
    def test_acquire_and_release(self):
        """测试基本的获取和释放锁"""
        lock = PessimisticLock()
        assert lock.acquire()
        lock.release()
    
    def test_context_manager(self):
        """测试上下文管理器"""
        lock = PessimisticLock()
        with lock:
            assert lock.is_locked()
        assert not lock.is_locked()
    
    def test_double_acquire_fails(self):
        """测试重复获取锁失败"""
        lock = PessimisticLock()
        lock.acquire()
        assert not lock.acquire(blocking=False)
        lock.release()
    
    def test_concurrent_access(self):
        """测试并发访问"""
        lock = PessimisticLock()
        results = []
        
        def worker():
            with lock:
                results.append(1)
                time.sleep(0.01)
        
        threads = [threading.Thread(target=worker) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 3
    
    def test_timeout(self):
        """测试超时机制"""
        lock = PessimisticLock()
        lock.acquire()
        
        assert not lock.acquire(timeout=0.1)
        lock.release()
    
    def test_release_without_acquire(self):
        """测试未获取锁就释放"""
        lock = PessimisticLock()
        with pytest.raises(RuntimeError):
            lock.release()
