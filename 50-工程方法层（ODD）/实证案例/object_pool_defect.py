import threading
from typing import TypeVar, Generic, Callable, Optional
from queue import Queue, Empty
import time

T = TypeVar('T')


class ObjectPool(Generic[T]):
    """线程安全的对象池实现"""
    
    def __init__(
        self,
        factory: Callable[[], T],
        reset: Optional[Callable[[T], None]] = None,
        min_size: int = 0,
        max_size: int = 10,
        timeout: float = 5.0
    ):
        """
        初始化对象池
        
        Args:
            factory: 创建新对象的工厂函数
            reset: 重置对象状态的函数（可选）
            min_size: 池中最小对象数
            max_size: 池中最大对象数
            timeout: 获取对象的超时时间（秒）
        """
        self._factory = factory
        self._reset = reset
        self._min_size = min_size
        self._max_size = max_size
        self._timeout = timeout
        
        self._pool: Queue[T] = Queue(maxsize=max_size)
        self._current_size = 0
        self._lock = threading.Lock()
        
        # 预创建最小数量的对象
        for _ in range(min_size):
            self._pool.put(self._create_object())
    
    def _create_object(self) -> T:
        """创建新对象"""
        with self._lock:
            if self._current_size >= self._max_size:
                raise RuntimeError(f"对象池已达到最大容量: {self._max_size}")
            self._current_size += 1
        return self._factory()
    
    def acquire(self) -> T:
        """从池中获取对象"""
        try:
            # 尝试从池中获取现有对象
            obj = self._pool.get(timeout=self._timeout)
            return obj
        except Empty:
            # 池为空，尝试创建新对象
            with self._lock:
                if self._current_size < self._max_size:
                    return self._create_object()
            raise TimeoutError(f"无法在 {self._timeout} 秒内获取对象")
    
    def release(self, obj: T) -> None:
        """将对象归还到池中"""
        if obj is None:
            return
        
        # 重置对象状态
        if self._reset:
            try:
                self._reset(obj)
            except Exception as e:
                print(f"重置对象失败: {e}")
                with self._lock:
                    self._current_size -= 1
                return
        
        try:
            self._pool.put_nowait(obj)
        except:
            # 池已满，丢弃对象
            with self._lock:
                self._current_size -= 1
    
    def __enter__(self):
        """上下文管理器支持"""
        return self.acquire()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器支持"""
        pass
    
    def size(self) -> int:
        """返回当前池中对象数量"""
        return self._pool.qsize()
    
    def total_size(self) -> int:
        """返回已创建的总对象数"""
        return self._current_size


class PooledObject(Generic[T]):
    """池化对象包装器，支持自动归还"""
    
    def __init__(self, pool: ObjectPool[T], obj: T):
        self._pool = pool
        self._obj = obj
        self._released = False
    
    def __enter__(self) -> T:
        return self._obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
    
    def release(self):
        """归还对象到池"""
        if not self._released:
            self._pool.release(self._obj)
            self._released = True
    
    def get(self) -> T:
        """获取实际对象"""
        return self._obj


# 使用示例
if __name__ == "__main__":
    # 示例1: 数据库连接池
    class DBConnection:
        def __init__(self):
            self.id = id(self)
            print(f"创建连接: {self.id}")
        
        def query(self, sql):
            return f"执行查询 {sql} on {self.id}"
        
        def close(self):
            print(f"关闭连接: {self.id}")
    
    def reset_connection(conn):
        """重置连接状态"""
        pass
    
    # 创建连接池
    pool = ObjectPool(
        factory=DBConnection,
        reset=reset_connection,
        min_size=2,
        max_size=5,
        timeout=3.0
    )
    
    # 使用方式1: 手动获取和释放
    conn = pool.acquire()
    print(conn.query("SELECT * FROM users"))
    pool.release(conn)
    
    # 使用方式2: 使用上下文管理器
    with PooledObject(pool, pool.acquire()) as conn:
        print(conn.query("SELECT * FROM orders"))
    
    print(f"池中对象数: {pool.size()}")
    print(f"总创建数: {pool.total_size()}")