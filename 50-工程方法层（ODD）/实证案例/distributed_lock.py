
import redis
import uuid
import time
from typing import Optional


class DistributedLock:
    def __init__(
        self,
        redis_client: redis.Redis,
        lock_name: str,
        timeout: int = 10,
        retry_times: int = 3,
        retry_delay: float = 0.1
    ):
        self.redis_client = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.identifier = str(uuid.uuid4())
        self._locked = False

    def acquire(self) -> bool:
        for _ in range(self.retry_times):
            result = self.redis_client.set(
                self.lock_name,
                self.identifier,
                nx=True,
                ex=self.timeout
            )
            if result:
                self._locked = True
                return True
            time.sleep(self.retry_delay)
        return False

    def release(self) -> bool:
        if not self._locked:
            return False

        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        result = self.redis_client.eval(lua_script, 1, self.lock_name, self.identifier)
        self._locked = False
        return bool(result)

    def __enter__(self):
        if not self.acquire():
            raise RuntimeError(f"Failed to acquire lock: {self.lock_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


# 使用示例
if __name__ == "__main__":
    # 创建Redis客户端
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # 方式1：手动获取和释放
    lock = DistributedLock(redis_client, "my_resource", timeout=30)
    if lock.acquire():
        try:
            print("Lock acquired, doing work...")
            time.sleep(2)
        finally:
            lock.release()
            print("Lock released")

    # 方式2：使用上下文管理器
    try:
        with DistributedLock(redis_client, "my_resource", timeout=30):
            print("Lock acquired via context manager")
            time.sleep(2)
    except RuntimeError as e:
        print(f"Failed to acquire lock: {e}")
