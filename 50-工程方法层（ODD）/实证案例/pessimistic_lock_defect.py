
import threading
import time
from typing import Optional, Callable, Any
from functools import wraps


class PessimisticLock:
    """悲观锁实现"""
    
    def __init__(self, timeout: Optional[float] = None):
        """
        初始化悲观锁
        
        Args:
            timeout: 获取锁的超时时间（秒），None表示无限等待
        """
        self._lock = threading.RLock()
        self._timeout = timeout
        self._owner = None
        self._acquire_count = 0
    
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """
        获取锁
        
        Args:
            blocking: 是否阻塞等待
            timeout: 超时时间，优先级高于初始化时的timeout
            
        Returns:
            是否成功获取锁
        """
        actual_timeout = timeout if timeout is not None else self._timeout
        
        if actual_timeout is None:
            result = self._lock.acquire(blocking=blocking)
        else:
            result = self._lock.acquire(blocking=blocking, timeout=actual_timeout)
        
        if result:
            self._owner = threading.current_thread()
            self._acquire_count += 1
        
        return result
    
    def release(self):
        """释放锁"""
        if self._owner == threading.current_thread():
            self._acquire_count -= 1
            if self._acquire_count == 0:
                self._owner = None
        self._lock.release()
    
    def __enter__(self):
        """上下文管理器入口"""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.release()
        return False
    
    def locked(self) -> bool:
        """检查锁是否被持有"""
        return self._lock.locked()
    
    def is_owned_by_current_thread(self) -> bool:
        """检查当前线程是否持有锁"""
        return self._owner == threading.current_thread()
    
    def synchronize(self, func: Callable) -> Callable:
        """
        装饰器：使函数在悲观锁保护下执行
        
        Args:
            func: 要保护的函数
            
        Returns:
            包装后的函数
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with self:
                return func(*args, **kwargs)
        return wrapper


class ResourceWithPessimisticLock:
    """带悲观锁的资源访问示例"""
    
    def __init__(self):
        self._data = 0
        self._lock = PessimisticLock(timeout=5.0)
    
    def read(self) -> int:
        """读取数据（加锁）"""
        with self._lock:
            return self._data
    
    def write(self, value: int):
        """写入数据（加锁）"""
        with self._lock:
            time.sleep(0.01)  # 模拟耗时操作
            self._data = value
    
    def increment(self):
        """原子递增操作"""
        with self._lock:
            current = self._data
            time.sleep(0.01)  # 模拟耗时操作
            self._data = current + 1
    
    @property
    def lock(self) -> PessimisticLock:
        """获取锁对象"""
        return self._lock


class DatabaseConnection:
    """数据库连接悲观锁示例"""
    
    def __init__(self):
        self._connection = None
        self._lock = PessimisticLock()
    
    def execute_transaction(self, operations: list):
        """执行事务（悲观锁保护）"""
        if not self._lock.acquire(timeout=10.0):
            raise TimeoutError("无法获取数据库锁")
        
        try:
            # 模拟事务操作
            for op in operations:
                time.sleep(0.01)
                # 执行操作
                pass
        finally:
            self._lock.release()
    
    def query_with_lock(self, sql: str):
        """带锁的查询操作"""
        with self._lock:
            # 模拟查询
            time.sleep(0.01)
            return f"Result of: {sql}"


def pessimistic_lock_decorator(lock: PessimisticLock):
    """
    通用悲观锁装饰器
    
    Args:
        lock: 悲观锁实例
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator


# 全局锁示例
global_lock = PessimisticLock()

@pessimistic_lock_decorator(global_lock)
def critical_section():
    """临界区代码"""
    time.sleep(0.01)
    return "操作完成"
