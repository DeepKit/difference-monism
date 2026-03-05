
import threading


class ReadWriteLock:
    """读写锁实现
    
    允许多个读者同时访问，但写者独占访问。
    写者优先策略：当有写者等待时，新的读者需要等待。
    """
    
    def __init__(self):
        self._readers = 0  # 当前读者数量
        self._writers = 0  # 当前写者数量（0或1）
        self._waiting_writers = 0  # 等待的写者数量
        self._lock = threading.Lock()  # 保护内部状态的锁
        self._read_ready = threading.Condition(self._lock)  # 读者条件变量
        self._write_ready = threading.Condition(self._lock)  # 写者条件变量
    
    def acquire_read(self):
        """获取读锁"""
        with self._lock:
            # 如果有写者在写或有写者在等待，读者需要等待
            while self._writers > 0 or self._waiting_writers > 0:
                self._read_ready.wait()
            self._readers += 1
    
    def release_read(self):
        """释放读锁"""
        with self._lock:
            self._readers -= 1
            # 如果没有读者了，唤醒等待的写者
            if self._readers == 0:
                self._write_ready.notify()
    
    def acquire_write(self):
        """获取写锁"""
        with self._lock:
            self._waiting_writers += 1
            # 等待直到没有读者和写者
            while self._readers > 0 or self._writers > 0:
                self._write_ready.wait()
            self._waiting_writers -= 1
            self._writers = 1
    
    def release_write(self):
        """释放写锁"""
        with self._lock:
            self._writers = 0
            # 优先唤醒写者，如果没有等待的写者则唤醒所有读者
            if self._waiting_writers > 0:
                self._write_ready.notify()
            else:
                self._read_ready.notify_all()
    
    def reader(self):
        """返回读锁上下文管理器"""
        return _ReadLockContext(self)
    
    def writer(self):
        """返回写锁上下文管理器"""
        return _WriteLockContext(self)


class _ReadLockContext:
    """读锁上下文管理器"""
    
    def __init__(self, rwlock):
        self._rwlock = rwlock
    
    def __enter__(self):
        self._rwlock.acquire_read()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rwlock.release_read()
        return False


class _WriteLockContext:
    """写锁上下文管理器"""
    
    def __init__(self, rwlock):
        self._rwlock = rwlock
    
    def __enter__(self):
        self._rwlock.acquire_write()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rwlock.release_write()
        return False
