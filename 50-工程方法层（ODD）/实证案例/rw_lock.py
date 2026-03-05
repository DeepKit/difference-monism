
import threading


class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._write_ready = 0
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)
        self._write_ready_cond = threading.Condition(self._lock)

    def acquire_read(self):
        with self._lock:
            while self._writers > 0 or self._write_ready > 0:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_ready_cond.notify()

    def acquire_write(self):
        with self._lock:
            self._write_ready += 1
            while self._readers > 0 or self._writers > 0:
                self._write_ready_cond.wait()
            self._write_ready -= 1
            self._writers += 1

    def release_write(self):
        with self._lock:
            self._writers -= 1
            self._write_ready_cond.notify()
            self._read_ready.notify_all()

    def reader(self):
        return _ReaderLock(self)

    def writer(self):
        return _WriterLock(self)


class _ReaderLock:
    def __init__(self, rwlock):
        self._rwlock = rwlock

    def __enter__(self):
        self._rwlock.acquire_read()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rwlock.release_read()
        return False


class _WriterLock:
    def __init__(self, rwlock):
        self._rwlock = rwlock

    def __enter__(self):
        self._rwlock.acquire_write()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rwlock.release_write()
        return False


# 使用示例
if __name__ == "__main__":
    rwlock = ReadWriteLock()
    shared_data = []

    def reader(thread_id):
        for _ in range(3):
            with rwlock.reader():
                print(f"Reader {thread_id}: {shared_data}")
                threading.Event().wait(0.1)

    def writer(thread_id):
        for i in range(2):
            with rwlock.writer():
                shared_data.append(f"data_{thread_id}_{i}")
                print(f"Writer {thread_id}: wrote {shared_data[-1]}")
                threading.Event().wait(0.2)

    threads = []
    for i in range(3):
        threads.append(threading.Thread(target=reader, args=(i,)))
    for i in range(2):
        threads.append(threading.Thread(target=writer, args=(i,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
