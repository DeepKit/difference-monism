from functools import wraps
from typing import Callable, Any


class CacheDecorator:
    def __init__(self, max_size: int = 128):
        self.cache = {}
        self.max_size = max_size
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            cache_key = (args, tuple(sorted(kwargs.items())))
            
            # 检查缓存
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            
            # 简单的LRU：超过大小限制时删除第一个
            if len(self.cache) >= self.max_size:
                self.cache.pop(next(iter(self.cache)))
            
            self.cache[cache_key] = result
            return result
        
        # 添加清除缓存方法
        wrapper.clear_cache = lambda: self.cache.clear()
        return wrapper


# 使用示例
@CacheDecorator(max_size=100)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@CacheDecorator()
def expensive_operation(x: int, y: int) -> int:
    return x ** y


# 测试
if __name__ == "__main__":
    print(fibonacci(10))  # 55
    print(expensive_operation(2, 10))  # 1024
    expensive_operation.clear_cache()  # 清除缓存