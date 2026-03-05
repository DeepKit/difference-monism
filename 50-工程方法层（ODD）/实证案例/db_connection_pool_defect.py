import queue
import threading
from typing import Any, Callable, Optional


class ConnectionPool:
    def __init__(
        self,
        creator: Callable[[], Any],
        max_connections: int = 10,
        min_connections: int = 2,
    ):
        """
        创建连接池
        
        :param creator: 创建数据库连接的函数
        :param max_connections: 最大连接数
        :param min_connections: 最小连接数
        """
        self.creator = creator
        self.max_connections = max_connections
        self.min_connections = min_connections
        
        self._pool = queue.Queue(maxsize=max_connections)
        self._current_size = 0
        self._lock = threading.Lock()
        
        # 初始化最小连接数
        for _ in range(min_connections):
            self._pool.put(self._create_connection())
    
    def _create_connection(self) -> Any:
        """创建新连接"""
        with self._lock:
            if self._current_size >= self.max_connections:
                raise Exception("连接池已达到最大连接数")
            self._current_size += 1
        return self.creator()
    
    def get_connection(self, timeout: Optional[float] = None) -> Any:
        """从池中获取连接"""
        try:
            return self._pool.get(block=True, timeout=timeout)
        except queue.Empty:
            # 池为空，尝试创建新连接
            if self._current_size < self.max_connections:
                return self._create_connection()
            raise Exception("无法获取连接，连接池已满")
    
    def return_connection(self, conn: Any) -> None:
        """归还连接到池中"""
        try:
            self._pool.put(conn, block=False)
        except queue.Full:
            # 池已满，关闭连接
            self._close_connection(conn)
    
    def _close_connection(self, conn: Any) -> None:
        """关闭连接"""
        with self._lock:
            self._current_size -= 1
        if hasattr(conn, 'close'):
            conn.close()
    
    def close_all(self) -> None:
        """关闭所有连接"""
        while not self._pool.empty():
            try:
                conn = self._pool.get(block=False)
                self._close_connection(conn)
            except queue.Empty:
                break
    
    def __enter__(self):
        """上下文管理器支持"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时关闭所有连接"""
        self.close_all()


# 使用示例
if __name__ == "__main__":
    import sqlite3
    
    # 创建连接池
    pool = ConnectionPool(
        creator=lambda: sqlite3.connect(":memory:"),
        max_connections=5,
        min_connections=2
    )
    
    # 获取连接
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print(cursor.fetchone())
    
    # 归还连接
    pool.return_connection(conn)
    
    # 使用上下文管理器
    with ConnectionPool(lambda: sqlite3.connect(":memory:")) as pool:
        conn = pool.get_connection()
        # 使用连接...
        pool.return_connection(conn)