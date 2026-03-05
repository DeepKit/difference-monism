import uuid
import time
from typing import Optional
import redis


class RedisDistributedLock:
    """Redis分布式锁实现"""
    
    def __init__(self, redis_client: redis.Redis, lock_name: str, 
                 expire_time: int = 10, retry_times: int = 3, 
                 retry_delay: float = 0.1):
        """
        初始化分布式锁
        
        :param redis_client: Redis客户端实例
        :param lock_name: 锁的名称
        :param expire_time: 锁过期时间(秒)
        :param retry_times: 获取锁的重试次数
        :param retry_delay: 重试间隔(秒)
        """
        self.redis_client = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.expire_time = expire_time
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.identifier = str(uuid.uuid4())
        
        # Lua脚本确保原子性释放锁
        self.unlock_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
    
    def acquire(self) -> bool:
        """获取锁"""
        for _ in range(self.retry_times):
            # SET key value NX EX expire_time
            if self.redis_client.set(
                self.lock_name, 
                self.identifier, 
                nx=True, 
                ex=self.expire_time
            ):
                return True
            time.sleep(self.retry_delay)
        return False
    
    def release(self) -> bool:
        """释放锁"""
        result = self.redis_client.eval(
            self.unlock_script, 
            1, 
            self.lock_name, 
            self.identifier
        )
        return bool(result)
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.acquire():
            raise RuntimeError(f"Failed to acquire lock: {self.lock_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.release()


# 使用示例
if __name__ == "__main__":
    # 创建Redis连接
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # 方式1: 手动获取和释放
    lock = RedisDistributedLock(r, "my_resource", expire_time=5)
    if lock.acquire():
        try:
            print("获取锁成功，执行业务逻辑")
            # 执行业务逻辑
        finally:
            lock.release()
    else:
        print("获取锁失败")
    
    # 方式2: 使用上下文管理器(推荐)
    try:
        with RedisDistributedLock(r, "my_resource", expire_time=5):
            print("在锁保护下执行业务逻辑")
            # 执行业务逻辑
    except RuntimeError as e:
        print(f"锁获取失败: {e}")