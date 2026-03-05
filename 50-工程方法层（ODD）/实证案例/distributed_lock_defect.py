
import time
import uuid
import threading
from typing import Optional
import redis
from redis import Redis


class DistributedLock:
    """
    基于Redis的分布式锁实现
    
    特性:
    - 支持自动过期防止死锁
    - 支持锁续期(watchdog)
    - 支持上下文管理器
    - 防止误删其他客户端的锁
    """
    
    def __init__(
        self,
        redis_client: Redis,
        lock_name: str,
        expire_time: int = 30,
        auto_renewal: bool = False,
        renewal_interval: Optional[int] = None
    ):
        """
        初始化分布式锁
        
        Args:
            redis_client: Redis客户端实例
            lock_name: 锁的名称
            expire_time: 锁过期时间(秒)
            auto_renewal: 是否自动续期
            renewal_interval: 续期间隔(秒)，默认为expire_time的1/3
        """
        self.redis_client = redis_client
        self.lock_name = f"distributed_lock:{lock_name}"
        self.expire_time = expire_time
        self.auto_renewal = auto_renewal
        self.renewal_interval = renewal_interval or max(1, expire_time // 3)
        
        self.lock_id = str(uuid.uuid4())
        self.is_locked = False
        self._renewal_thread: Optional[threading.Thread] = None
        self._stop_renewal = threading.Event()
    
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """
        获取锁
        
        Args:
            blocking: 是否阻塞等待
            timeout: 超时时间(秒)，None表示无限等待
            
        Returns:
            是否成功获取锁
        """
        start_time = time.time()
        
        while True:
            # 使用SET NX EX原子操作获取锁
            acquired = self.redis_client.set(
                self.lock_name,
                self.lock_id,
                nx=True,
                ex=self.expire_time
            )
            
            if acquired:
                self.is_locked = True
                if self.auto_renewal:
                    self._start_renewal()
                return True
            
            if not blocking:
                return False
            
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
            
            time.sleep(0.01)
    
    def release(self) -> bool:
        """
        释放锁
        
        Returns:
            是否成功释放锁
        """
        if not self.is_locked:
            return False
        
        if self.auto_renewal:
            self._stop_renewal_thread()
        
        # 使用Lua脚本确保只删除自己的锁
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        
        result = self.redis_client.eval(lua_script, 1, self.lock_name, self.lock_id)
        self.is_locked = False
        return bool(result)
    
    def extend(self, additional_time: Optional[int] = None) -> bool:
        """
        延长锁的过期时间
        
        Args:
            additional_time: 额外延长的时间(秒)，默认使用expire_time
            
        Returns:
            是否成功延长
        """
        if not self.is_locked:
            return False
        
        extend_time = additional_time or self.expire_time
        
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("expire", KEYS[1], ARGV[2])
        else
            return 0
        end
        """
        
        result = self.redis_client.eval(
            lua_script,
            1,
            self.lock_name,
            self.lock_id,
            extend_time
        )
        return bool(result)
    
    def _start_renewal(self):
        """启动自动续期线程"""
        self._stop_renewal.clear()
        self._renewal_thread = threading.Thread(target=self._renewal_worker, daemon=True)
        self._renewal_thread.start()
    
    def _renewal_worker(self):
        """续期工作线程"""
        while not self._stop_renewal.is_set():
            time.sleep(self.renewal_interval)
            if self.is_locked and not self._stop_renewal.is_set():
                self.extend()
    
    def _stop_renewal_thread(self):
        """停止续期线程"""
        if self._renewal_thread and self._renewal_thread.is_alive():
            self._stop_renewal.set()
            self._renewal_thread.join(timeout=1)
    
    def __enter__(self):
        """上下文管理器入口"""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.release()
        return False
    
    def __del__(self):
        """析构函数，确保释放锁"""
        if self.is_locked:
            self.release()


class RedisLockFactory:
    """Redis分布式锁工厂类"""
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        **kwargs
    ):
        """
        初始化Redis连接
        
        Args:
            host: Redis主机地址
            port: Redis端口
            db: Redis数据库编号
            password: Redis密码
            **kwargs: 其他Redis连接参数
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            **kwargs
        )
    
    def create_lock(
        self,
        lock_name: str,
        expire_time: int = 30,
        auto_renewal: bool = False
    ) -> DistributedLock:
        """
        创建分布式锁实例
        
        Args:
            lock_name: 锁名称
            expire_time: 过期时间(秒)
            auto_renewal: 是否自动续期
            
        Returns:
            DistributedLock实例
        """
        return DistributedLock(
            redis_client=self.redis_client,
            lock_name=lock_name,
            expire_time=expire_time,
            auto_renewal=auto_renewal
        )


# 使用示例
if __name__ == "__main__":
    # 创建锁工厂
    factory = RedisLockFactory(host='localhost', port=6379)
    
    # 方式1: 使用上下文管理器
    with factory.create_lock("my_resource", expire_time=10) as lock:
        print("获取锁成功，执行业务逻辑")
        time.sleep(2)
    
    # 方式2: 手动获取和释放
    lock = factory.create_lock("my_resource", expire_time=10)
    if lock.acquire(blocking=True, timeout=5):
        try:
            print("获取锁成功")
            time.sleep(2)
        finally:
            lock.release()
    
    # 方式3: 使用自动续期
    lock = factory.create_lock("my_resource", expire_time=10, auto_renewal=True)
    if lock.acquire():
        try:
            print("获取锁成功，支持自动续期")
            time.sleep(20)  # 即使超过10秒，锁也会自动续期
        finally:
            lock.release()
