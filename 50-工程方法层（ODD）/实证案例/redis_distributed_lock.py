import redis
import uuid
import time
import threading
from typing import Optional, Union
from contextlib import contextmanager


class RedisDistributedLock:
    """Redis分布式锁实现"""
    
    # Lua脚本：安全释放锁（检查标识符匹配）
    RELEASE_SCRIPT = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    
    # Lua脚本：续期锁
    RENEW_SCRIPT = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("expire", KEYS[1], ARGV[2])
    else
        return 0
    end
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
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
            expire_time: 锁过期时间（秒）
            auto_renewal: 是否自动续期
            renewal_interval: 续期间隔（秒），默认为expire_time的1/3
        """
        self.redis_client = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.expire_time = expire_time
        self.identifier = str(uuid.uuid4())
        self.auto_renewal = auto_renewal
        self.renewal_interval = renewal_interval or max(1, expire_time // 3)
        
        self._renewal_thread: Optional[threading.Thread] = None
        self._stop_renewal = threading.Event()
        self._locked = False
        
        # 注册Lua脚本
        self._release_script = self.redis_client.register_script(self.RELEASE_SCRIPT)
        self._renew_script = self.redis_client.register_script(self.RENEW_SCRIPT)
    
    def acquire(
        self,
        blocking: bool = True,
        timeout: Optional[Union[int, float]] = None
    ) -> bool:
        """
        获取锁
        
        Args:
            blocking: 是否阻塞等待
            timeout: 超时时间（秒），None表示无限等待
            
        Returns:
            bool: 是否成功获取锁
        """
        if self._locked:
            raise RuntimeError("锁已被当前实例持有")
        
        start_time = time.time()
        
        while True:
            try:
                # 使用SET NX EX原子操作获取锁
                acquired = self.redis_client.set(
                    self.lock_name,
                    self.identifier,
                    nx=True,
                    ex=self.expire_time
                )
                
                if acquired:
                    self._locked = True
                    
                    # 启动自动续期
                    if self.auto_renewal:
                        self._start_renewal()
                    
                    return True
                
                # 非阻塞模式直接返回
                if not blocking:
                    return False
                
                # 检查超时
                if timeout is not None:
                    elapsed = time.time() - start_time
                    if elapsed >= timeout:
                        return False
                
                # 短暂休眠后重试
                time.sleep(0.01)
                
            except redis.RedisError as e:
                raise RuntimeError(f"获取锁失败: {e}")
    
    def release(self) -> bool:
        """
        释放锁
        
        Returns:
            bool: 是否成功释放
        """
        if not self._locked:
            return False
        
        try:
            # 停止自动续期
            if self.auto_renewal:
                self._stop_renewal()
            
            # 使用Lua脚本安全释放锁
            result = self._release_script(
                keys=[self.lock_name],
                args=[self.identifier]
            )
            
            self._locked = False
            return bool(result)
            
        except redis.RedisError as e:
            raise RuntimeError(f"释放锁失败: {e}")
    
    def renew(self) -> bool:
        """
        手动续期锁
        
        Returns:
            bool: 是否成功续期
        """
        if not self._locked:
            return False
        
        try:
            result = self._renew_script(
                keys=[self.lock_name],
                args=[self.identifier, self.expire_time]
            )
            return bool(result)
        except redis.RedisError as e:
            raise RuntimeError(f"续期失败: {e}")
    
    def _start_renewal(self):
        """启动自动续期线程"""
        self._stop_renewal.clear()
        self._renewal_thread = threading.Thread(
            target=self._renewal_worker,
            daemon=True
        )
        self._renewal_thread.start()
    
    def _renewal_worker(self):
        """自动续期工作线程"""
        while not self._stop_renewal.is_set():
            try:
                time.sleep(self.renewal_interval)
                if self._locked and not self._stop_renewal.is_set():
                    self.renew()
            except Exception:
                pass
    
    def _stop_renewal(self):
        """停止自动续期"""
        if self._renewal_thread and self._renewal_thread.is_alive():
            self._stop_renewal.set()
            self._renewal_thread.join(timeout=1)
    
    def locked(self) -> bool:
        """检查锁是否被持有"""
        return self._locked
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.acquire():
            raise RuntimeError("无法获取锁")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.release()
        return False
    
    def __del__(self):
        """析构时确保释放锁"""
        if self._locked:
            try:
                self.release()
            except Exception:
                pass


# 使用示例
if __name__ == "__main__":
    # 创建Redis客户端
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # 方式1：手动管理
    lock = RedisDistributedLock(client, "my_resource", expire_time=10)
    if lock.acquire(timeout=5):
        try:
            print("获取锁成功，执行业务逻辑")
            time.sleep(2)
        finally:
            lock.release()
            print("释放锁")
    
    # 方式2：上下文管理器（推荐）
    with RedisDistributedLock(client, "my_resource", expire_time=10) as lock:
        print("在锁保护下执行业务逻辑")
        time.sleep(2)
    
    # 方式3：自动续期
    lock = RedisDistributedLock(
        client,
        "long_task",
        expire_time=10,
        auto_renewal=True,
        renewal_interval=3
    )
    with lock:
        print("执行长时间任务，锁会自动续期")
        time.sleep(20)