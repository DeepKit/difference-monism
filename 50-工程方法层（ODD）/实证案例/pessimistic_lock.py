
import time
import threading
from contextlib import contextmanager
from typing import Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class PessimisticLock:
    """悲观锁实现：数据库行锁、阻塞等待"""
    
    def __init__(self, connection, table: str, key_column: str, key_value: Any, 
                 timeout: Optional[float] = None, retry_interval: float = 0.1):
        """
        初始化悲观锁
        
        Args:
            connection: 数据库连接对象
            table: 表名
            key_column: 主键列名
            key_value: 主键值
            timeout: 超时时间（秒），None表示无限等待
            retry_interval: 重试间隔（秒）
        """
        self.connection = connection
        self.table = table
        self.key_column = key_column
        self.key_value = key_value
        self.timeout = timeout
        self.retry_interval = retry_interval
        self._locked = False
        self._cursor = None
        self._lock = threading.Lock()
    
    def acquire(self) -> bool:
        """
        获取悲观锁（阻塞等待）
        
        Returns:
            bool: 是否成功获取锁
        """
        with self._lock:
            if self._locked:
                return True
            
            start_time = time.time()
            
            while True:
                try:
                    self._cursor = self.connection.cursor()
                    
                    # 使用 SELECT ... FOR UPDATE 获取行锁
                    query = f"SELECT * FROM {self.table} WHERE {self.key_column} = %s FOR UPDATE"
                    self._cursor.execute(query, (self.key_value,))
                    
                    self._locked = True
                    logger.info(f"成功获取锁: {self.table}.{self.key_column}={self.key_value}")
                    return True
                    
                except Exception as e:
                    # 检查是否超时
                    if self.timeout is not None:
                        elapsed = time.time() - start_time
                        if elapsed >= self.timeout:
                            logger.error(f"获取锁超时: {self.table}.{self.key_column}={self.key_value}")
                            if self._cursor:
                                self._cursor.close()
                            return False
                    
                    # 等待后重试
                    logger.debug(f"等待锁释放: {e}")
                    time.sleep(self.retry_interval)
    
    def release(self):
        """释放悲观锁"""
        with self._lock:
            if not self._locked:
                return
            
            try:
                # 提交事务释放锁
                self.connection.commit()
                logger.info(f"释放锁: {self.table}.{self.key_column}={self.key_value}")
            except Exception as e:
                logger.error(f"释放锁失败: {e}")
                self.connection.rollback()
            finally:
                if self._cursor:
                    self._cursor.close()
                    self._cursor = None
                self._locked = False
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.acquire():
            raise TimeoutError(f"无法获取锁: {self.table}.{self.key_column}={self.key_value}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type is not None:
            # 发生异常时回滚
            self.connection.rollback()
            if self._cursor:
                self._cursor.close()
            self._locked = False
        else:
            self.release()
        return False
    
    @property
    def is_locked(self) -> bool:
        """检查是否已锁定"""
        return self._locked


class PessimisticLockManager:
    """悲观锁管理器：支持多个锁的管理"""
    
    def __init__(self, connection):
        self.connection = connection
        self._locks = {}
    
    def lock(self, table: str, key_column: str, key_value: Any, 
             timeout: Optional[float] = None) -> PessimisticLock:
        """
        创建并返回悲观锁对象
        
        Args:
            table: 表名
            key_column: 主键列名
            key_value: 主键值
            timeout: 超时时间
            
        Returns:
            PessimisticLock: 锁对象
        """
        lock_key = f"{table}.{key_column}.{key_value}"
        
        if lock_key not in self._locks:
            self._locks[lock_key] = PessimisticLock(
                self.connection, table, key_column, key_value, timeout
            )
        
        return self._locks[lock_key]
    
    def release_all(self):
        """释放所有锁"""
        for lock in self._locks.values():
            if lock.is_locked:
                lock.release()
        self._locks.clear()
    
    @contextmanager
    def acquire_multiple(self, locks: list):
        """
        获取多个锁（按顺序获取，避免死锁）
        
        Args:
            locks: 锁对象列表
        """
        acquired = []
        try:
            for lock in locks:
                if lock.acquire():
                    acquired.append(lock)
                else:
                    raise TimeoutError(f"无法获取锁")
            yield
        finally:
            for lock in reversed(acquired):
                lock.release()


# 使用示例
if __name__ == "__main__":
    import pymysql
    
    # 创建数据库连接
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        autocommit=False
    )
    
    try:
        # 方式1：直接使用
        lock = PessimisticLock(conn, 'users', 'id', 1, timeout=10)
        if lock.acquire():
            try:
                # 执行业务逻辑
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET balance = balance - 100 WHERE id = 1")
                conn.commit()
            finally:
                lock.release()
        
        # 方式2：使用上下文管理器
        with PessimisticLock(conn, 'users', 'id', 2, timeout=10):
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance + 100 WHERE id = 2")
            conn.commit()
        
        # 方式3：使用锁管理器
        manager = PessimisticLockManager(conn)
        lock1 = manager.lock('users', 'id', 1)
        lock2 = manager.lock('users', 'id', 2)
        
        with manager.acquire_multiple([lock1, lock2]):
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance - 50 WHERE id = 1")
            cursor.execute("UPDATE users SET balance = balance + 50 WHERE id = 2")
            conn.commit()
            
    finally:
        conn.close()
