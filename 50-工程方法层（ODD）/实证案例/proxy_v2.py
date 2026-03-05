import requests
from typing import Any, Callable, Optional
from functools import wraps


class ProxyV2:
    """代理类 - 支持方法拦截和转发"""
    
    def __init__(self, target: Any):
        self._target = target
        self._interceptors = {}
    
    def add_interceptor(self, method_name: str, interceptor: Callable):
        """添加方法拦截器"""
        self._interceptors[method_name] = interceptor
    
    def __getattr__(self, name: str):
        """动态代理方法调用"""
        target_attr = getattr(self._target, name)
        
        if not callable(target_attr):
            return target_attr
        
        @wraps(target_attr)
        def wrapper(*args, **kwargs):
            # 前置拦截
            if name in self._interceptors:
                result = self._interceptors[name](
                    'before', target_attr, args, kwargs
                )
                if result is not None:
                    return result
            
            # 执行原方法
            result = target_attr(*args, **kwargs)
            
            # 后置拦截
            if name in self._interceptors:
                self._interceptors[name](
                    'after', target_attr, args, kwargs, result
                )
            
            return result
        
        return wrapper


class HTTPProxyV2:
    """HTTP代理客户端"""
    
    def __init__(
        self,
        proxy_host: str,
        proxy_port: int,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.proxy_url = f"http://{proxy_host}:{proxy_port}"
        self.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        
        if username and password:
            auth_proxy = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
            self.proxies = {
                'http': auth_proxy,
                'https': auth_proxy
            }
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET请求"""
        return requests.get(url, proxies=self.proxies, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """POST请求"""
        return requests.post(url, proxies=self.proxies, **kwargs)
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """通用请求"""
        return requests.request(
            method, url, proxies=self.proxies, **kwargs
        )


class LazyProxyV2:
    """懒加载代理"""
    
    def __init__(self, factory: Callable):
        self._factory = factory
        self._instance = None
    
    def _get_instance(self):
        if self._instance is None:
            self._instance = self._factory()
        return self._instance
    
    def __getattr__(self, name: str):
        return getattr(self._get_instance(), name)
    
    def __call__(self, *args, **kwargs):
        return self._get_instance()(*args, **kwargs)


# 使用示例
if __name__ == "__main__":
    # 1. 基础代理模式
    class Service:
        def process(self, data):
            return f"处理: {data}"
    
    service = Service()
    proxy = ProxyV2(service)
    
    def log_interceptor(phase, method, args, kwargs, result=None):
        if phase == 'before':
            print(f"调用前: {method.__name__}")
        else:
            print(f"调用后: {result}")
    
    proxy.add_interceptor('process', log_interceptor)
    proxy.process("测试数据")
    
    # 2. HTTP代理
    http_proxy = HTTPProxyV2("127.0.0.1", 8080)
    # response = http_proxy.get("https://example.com")
    
    # 3. 懒加载代理
    lazy = LazyProxyV2(lambda: Service())
    print(lazy.process("懒加载"))