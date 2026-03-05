import threading
import time
import queue
from typing import Optional, Callable, Any
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PooledConnection:
    """包装的连接对象"""
    
    def __init__(self, connection: Any, pool: 'ConnectionPool'):
        self.connection = connection
        self.pool = pool
        self.created_at = time.time()
        self.last_used = time.time()
        self.in_use = False
        
    def is_expired(self, max_lifetime: float) -> bool:
        """检查连接是否过期"""
        return time.time() - self.created_at > max_lifetime
    
    def mark_in_use(self):
        """标记连接正在使用"""
        self.in_use = True
        self.last_used = time.time()
    
    def mark_available(self):
        """标记连接可用"""
        self.in_use = False
        self.last_used = time.time()


class ConnectionPool:
    """数据库连接池"""
    
    def __init__(
        self,
        create_connection: Callable[[], Any],
        min_size: int = 2,
        max_size: int = 10,
        max_lifetime: float = 3600,
        timeout: float = 30,
        validate_connection: Optional[Callable[[Any], bool]] = None
    ):
        """
        初始化连接池
        
        Args:
            create_connection: 创建连接的函数
            min_size: 最小连接数
            max_size: 最大连接数
            max_lifetime: 连接最大生命周期(秒)
            timeout: 获取连接超时时间(秒)
            validate_connection: 验证连接有效性的函数
        """
        if min_size < 0 or max_size < min_size:
            raise ValueError("无效的连接池大小配置")
        
        self._create_connection = create_connection
        self._min_size = min_size
        self._max_size = max_size
        self._max_lifetime = max_lifetime
        self._timeout = timeout
        self._validate_connection = validate_connection or self._default_validate
        
        self._pool: queue.Queue = queue.Queue(maxsize=max_size)
        self._all_connections: list[PooledConnection] = []
        self._lock = threading.RLock()
        self._closed = False
        
        # 初始化最小连接数
        self._initialize_pool()
        
        # 启动清理线程
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired, daemon=True)
        self._cleanup_thread.start()
    
    def _default_validate(self, connection: Any) -> bool:
        """默认连接验证"""
        return connection is not None
    
    def _initialize_pool(self):
        """初始化连接池"""
        with self._lock:
            for _ in range(self._min_size):
                try:
                    conn = self._create_new_connection()
                    self._pool.put(conn, block=False)
                except Exception as e:
                    logger.error(f"初始化连接失败: {e}")
                    raise
    
    def _create_new_connection(self) -> PooledConnection:
        """创建新连接"""
        try:
            raw_conn = self._create_connection()
            pooled_conn = PooledConnection(raw_conn, self)
            
            with self._lock:
                self._all_connections.append(pooled_conn)
            
            logger.info(f"创建新连接，当前总连接数: {len(self._all_connections)}")
            return pooled_conn
        except Exception as e:
            logger.error(f"创建连接失败: {e}")
            raise
    
    def _validate_and_refresh(self, pooled_conn: PooledConnection) -> PooledConnection:
        """验证并刷新连接"""
        # 检查连接是否过期
        if pooled_conn.is_expired(self._max_lifetime):
            logger.info("连接已过期，创建新连接")
            self._close_connection(pooled_conn)
            return self._create_new_connection()
        
        # 验证连接有效性
        try:
            if not self._validate_connection(pooled_conn.connection):
                logger.warning("连接验证失败，创建新连接")
                self._close_connection(pooled_conn)
                return self._create_new_connection()
        except Exception as e:
            logger.error(f"连接验证异常: {e}")
            self._close_connection(pooled_conn)
            return self._create_new_connection()
        
        return pooled_conn
    
    def get_connection(self, timeout: Optional[float] = None) -> PooledConnection:
        """
        获取连接
        
        Args:
            timeout: 超时时间，None使用默认值
            
        Returns:
            PooledConnection对象
            
        Raises:
            RuntimeError: 连接池已关闭
            TimeoutError: 获取连接超时
        """
        if self._closed:
            raise RuntimeError("连接池已关闭")
        
        timeout = timeout if timeout is not None else self._timeout
        start_time = time.time()
        
        while True:
            try:
                # 尝试从池中获取连接
                pooled_conn = self._pool.get(block=True, timeout=0.1)
                pooled_conn = self._validate_and_refresh(pooled_conn)
                pooled_conn.mark_in_use()
                return pooled_conn
                
            except queue.Empty:
                # 池中无可用连接，尝试创建新连接
                with self._lock:
                    if len(self._all_connections) < self._max_size:
                        try:
                            pooled_conn = self._create_new_connection()
                            pooled_conn.mark_in_use()
                            return pooled_conn
                        except Exception as e:
                            logger.error(f"创建新连接失败: {e}")
                
                # 检查超时
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"获取连接超时({timeout}秒)")
    
    def return_connection(self, pooled_conn: PooledConnection):
        """
        归还连接到池中
        
        Args:
            pooled_conn: 要归还的连接
        """
        if self._closed:
            self._close_connection(pooled_conn)
            return
        
        try:
            pooled_conn.mark_available()
            self._pool.put(pooled_conn, block=False)
        except queue.Full:
            logger.warning("连接池已满，关闭多余连接")
            self._close_connection(pooled_conn)
    
    @contextmanager
    def connection(self, timeout: Optional[float] = None):
        """
        上下文管理器方式使用连接
        
        Usage:
            with pool.connection() as conn:
                # 使用conn.connection访问原始连接
                cursor = conn.connection.cursor()
        """
        pooled_conn = None
        try:
            pooled_conn = self.get_connection(timeout)
            yield pooled_conn
        except Exception as e:
            logger.error(f"连接使用异常: {e}")
            if pooled_conn:
                # 发生异常时关闭连接
                self._close_connection(pooled_conn)
                pooled_conn = None
            raise
        finally:
            if pooled_conn:
                self.return_connection(pooled_conn)
    
    def _close_connection(self, pooled_conn: PooledConnection):
        """关闭单个连接"""
        try:
            if hasattr(pooled_conn.connection, 'close'):
                pooled_conn.connection.close()
            
            with self._lock:
                if pooled_conn in self._all_connections:
                    self._all_connections.remove(pooled_conn)
            
            logger.info(f"关闭连接，当前总连接数: {len(self._all_connections)}")
        except Exception as e:
            logger.error(f"关闭连接失败: {e}")
    
    def _cleanup_expired(self):
        """清理过期连接的后台线程"""
        while not self._closed:
            time.sleep(60)  # 每分钟检查一次
            
            with self._lock:
                expired = [
                    conn for conn in self._all_connections
                    if not conn.in_use and conn.is_expired(self._max_lifetime)
                ]
            
            for conn in expired:
                try:
                    # 尝试从队列中移除
                    temp_queue = queue.Queue()
                    while not self._pool.empty():
                        try:
                            item = self._pool.get_nowait()
                            if item != conn:
                                temp_queue.put(item)
                            else:
                                self._close_connection(conn)
                        except queue.Empty:
                            break
                    
                    # 将其他连接放回
                    while not temp_queue.empty():
                        self._pool.put(temp_queue.get())
                        
                except Exception as e:
                    logger.error(f"清理过期连接失败: {e}")
    
    def close(self):
        """关闭连接池"""
        if self._closed:
            return
        
        self._closed = True
        logger.info("正在关闭连接池...")
        
        with self._lock:
            for conn in self._all_connections[:]:
                self._close_connection(conn)
        
        logger.info("连接池已关闭")
    
    def get_stats(self) -> dict:
        """获取连接池统计信息"""
        with self._lock:
            return {
                'total_connections': len(self._all_connections),
                'available_connections': self._pool.qsize(),
                'in_use_connections': sum(1 for c in self._all_connections if c.in_use),
                'min_size': self._min_size,
                'max_size': self._max_size,
                'closed': self._closed
            }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# 使用示例
if __name__ == "__main__":
    import sqlite3
    
    # 创建连接函数
    def create_db_connection():
        return sqlite3.connect(':memory:', check_same_thread=False)
    
    # 验证连接函数
    def validate_db_connection(conn):
        try:
            conn.execute("SELECT 1")
            return True
        except:
            return False
    
    # 创建连接池
    pool = ConnectionPool(
        create_connection=create_db_connection,
        min_size=2,
        max_size=5,
        max_lifetime=3600,
        timeout=10,
        validate_connection=validate_db_connection
    )
    
    try:
        # 使用方式1：手动获取和归还
        conn = pool.get_connection()
        cursor = conn.connection.cursor()
        cursor.execute("SELECT 1")
        print("查询结果:", cursor.fetchone())
        pool.return_connection(conn)
        
        # 使用方式2：上下文管理器
        with pool.connection() as conn:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT 2")
            print("查询结果:", cursor.fetchone())
        
        # 查看统计信息
        print("连接池统计:", pool.get_stats())
        
    finally:
        pool.close()