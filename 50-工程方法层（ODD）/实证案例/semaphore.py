
import threading
from typing import Optional
from contextlib import contextmanager


class Semaphore:
    """信号量类：用于并发控制和资源池管理"""
    
    def __init__(self, value: int = 1):
        if value < 0:
            raise ValueError("Semaphore初始值必须 >= 0")
        self._value = value
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """获取信号量"""
        with self._condition:
            if not blocking:
                if self._value > 0:
                    self._value -= 1
                    return True
                return False
            
            if timeout is not None:
                end_time = threading.time() + timeout
                while self._value == 0:
                    remaining = end_time - threading.time()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)
            else:
                while self._value == 0:
                    self._condition.wait()
            
            self._value -= 1
            return True
    
    def release(self):
        """释放信号量"""
        with self._condition:
            self._value += 1
            self._condition.notify()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
    
    @property
    def value(self) -> int:
        """获取当前信号量值"""
        with self._lock:
            return self._value


class BoundedSemaphore(Semaphore):
    """有界信号量：防止release次数超过初始值"""
    
    def __init__(self, value: int = 1):
        super().__init__(value)
        self._initial_value = value
    
    def release(self):
        with self._condition:
            if self._value >= self._initial_value:
                raise ValueError("BoundedSemaphore释放次数过多")
            self._value += 1
            self._condition.notify()


# 使用示例
if __name__ == "__main__":
    import time
    from concurrent.futures import ThreadPoolExecutor
    
    # 示例1：并发限制
    semaphore = Semaphore(3)  # 最多3个并发
    
    def worker(task_id):
        with semaphore:
            print(f"任务 {task_id} 开始执行")
            time.sleep(1)
            print(f"任务 {task_id} 完成")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(10):
            executor.submit(worker, i)
    
    # 示例2：资源池
    resource_pool = BoundedSemaphore(5)  # 5个资源
    
    def use_resource(user_id):
        if resource_pool.acquire(timeout=2):
            try:
                print(f"用户 {user_id} 获取资源")
                time.sleep(0.5)
            finally:
                resource_pool.release()
                print(f"用户 {user_id} 释放资源")
        else:
            print(f"用户 {user_id} 获取资源超时")
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(8):
            executor.submit(use_resource, i)
