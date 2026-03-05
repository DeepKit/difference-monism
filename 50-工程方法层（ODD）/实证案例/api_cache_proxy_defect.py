import hashlib
import json
import time
from functools import wraps
from typing import Any, Callable, Optional


class APICacheProxy:
    def __init__(self, ttl: int = 3600):
        """
        API缓存代理
        
        Args:
            ttl: 缓存过期时间(秒)，默认1小时
        """
        self.cache = {}
        self.ttl = ttl
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float) -> bool:
        """检查缓存是否过期"""
        return time.time() - timestamp > self.ttl
    
    def cached(self, func: Callable) -> Callable:
        """缓存装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = self._generate_key(func.__name__, args, kwargs)
            
            # 检查缓存
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if not self._is_expired(timestamp):
                    return cached_data
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            self.cache[cache_key] = (result, time.time())
            return result
        
        return wrapper
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def clear_expired(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]


# 使用示例
if __name__ == "__main__":
    import requests
    
    proxy = APICacheProxy(ttl=60)
    
    @proxy.cached
    def fetch_data(url: str):
        print(f"实际请求: {url}")
        response = requests.get(url)
        return response.json()
    
    # 第一次调用 - 实际请求
    data1 = fetch_data("https://api.example.com/data")
    
    # 第二次调用 - 使用缓存
    data2 = fetch_data("https://api.example.com/data")