
import threading


class Semaphore:
    """信号量实现，用于控制对共享资源的并发访问"""
    
    def __init__(self, value=1):
        """
        初始化信号量
        
        Args:
            value: 初始计数值，必须 >= 0
        """
        if value < 0:
            raise ValueError("信号量初始值不能为负数")
        self._value = value
        self._condition = threading.Condition(threading.Lock())
    
    def acquire(self, blocking=True, timeout=None):
        """
        获取信号量（P操作）
        
        Args:
            blocking: 是否阻塞等待
            timeout: 超时时间（秒），仅在blocking=True时有效
            
        Returns:
            bool: 成功获取返回True，否则返回False
        """
        with self._condition:
            if not blocking:
                if self._value > 0:
                    self._value -= 1
                    return True
                return False
            
            if timeout is None:
                while self._value == 0:
                    self._condition.wait()
                self._value -= 1
                return True
            else:
                end_time = threading.time() + timeout
                while self._value == 0:
                    remaining = end_time - threading.time()
                    if remaining <= 0:
                        return False
                    self._condition.wait(remaining)
                self._value -= 1
                return True
    
    def release(self):
        """释放信号量（V操作）"""
        with self._condition:
            self._value += 1
            self._condition.notify()
    
    def __enter__(self):
        """支持上下文管理器"""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.release()
        return False


class BoundedSemaphore(Semaphore):
    """有界信号量，release时不能超过初始值"""
    
    def __init__(self, value=1):
        super().__init__(value)
        self._initial_value = value
    
    def release(self):
        """释放信号量，但不能超过初始值"""
        with self._condition:
            if self._value >= self._initial_value:
                raise ValueError("BoundedSemaphore释放次数超过获取次数")
            self._value += 1
            self._condition.notify()
