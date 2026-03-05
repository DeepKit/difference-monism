
import threading
import time
from typing import Any, Callable, Optional
from dataclasses import dataclass
from functools import wraps


@dataclass
class VersionedData:
    value: Any
    version: int


class OptimisticLock:
    def __init__(self, initial_value: Any = None):
        self._lock = threading.Lock()
        self._data = VersionedData(value=initial_value, version=0)
    
    def read(self) -> tuple[Any, int]:
        """读取当前值和版本号"""
        with self._lock:
            return self._data.value, self._data.version
    
    def cas_update(self, expected_version: int, new_value: Any) -> bool:
        """CAS更新：仅当版本号匹配时更新"""
        with self._lock:
            if self._data.version == expected_version:
                self._data.value = new_value
                self._data.version += 1
                return True
            return False
    
    def update_with_retry(
        self, 
        update_fn: Callable[[Any], Any], 
        max_retries: int = 10,
        backoff_ms: int = 1
    ) -> bool:
        """带重试的更新操作"""
        for attempt in range(max_retries):
            value, version = self.read()
            new_value = update_fn(value)
            
            if self.cas_update(version, new_value):
                return True
            
            if attempt < max_retries - 1:
                time.sleep(backoff_ms / 1000.0 * (attempt + 1))
        
        return False
    
    def get_value(self) -> Any:
        """获取当前值"""
        return self.read()[0]
    
    def get_version(self) -> int:
        """获取当前版本号"""
        return self.read()[1]


def with_optimistic_lock(max_retries: int = 10, backoff_ms: int = 1):
    """乐观锁装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(lock: OptimisticLock, *args, **kwargs):
            def update_fn(current_value):
                return func(current_value, *args, **kwargs)
            
            success = lock.update_with_retry(
                update_fn, 
                max_retries=max_retries,
                backoff_ms=backoff_ms
            )
            
            if not success:
                raise RuntimeError(f"更新失败，超过最大重试次数 {max_retries}")
            
            return lock.get_value()
        
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    # 基本使用
    lock = OptimisticLock(initial_value=0)
    
    # 方式1：直接使用CAS
    value, version = lock.read()
    success = lock.cas_update(version, value + 1)
    print(f"CAS更新: {success}, 当前值: {lock.get_value()}")
    
    # 方式2：使用带重试的更新
    lock.update_with_retry(lambda x: x + 10)
    print(f"重试更新后: {lock.get_value()}")
    
    # 方式3：使用装饰器
    @with_optimistic_lock(max_retries=5)
    def increment(current_value, amount):
        return current_value + amount
    
    result = increment(lock, 5)
    print(f"装饰器更新后: {result}")
    
    # 并发测试
    def concurrent_increment(lock, count):
        for _ in range(count):
            lock.update_with_retry(lambda x: x + 1)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=concurrent_increment, args=(lock, 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"并发测试后: {lock.get_value()}, 版本: {lock.get_version()}")
