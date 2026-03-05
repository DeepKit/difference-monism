from typing import Callable, Dict, Optional
from functools import wraps


class APIVersioning:
    def __init__(self, default_version: str = "v1"):
        self.default_version = default_version
        self.versions: Dict[str, Dict[str, Callable]] = {}
    
    def register(self, version: str, endpoint: str):
        """注册特定版本的端点"""
        def decorator(func: Callable):
            if version not in self.versions:
                self.versions[version] = {}
            self.versions[version][endpoint] = func
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_handler(self, endpoint: str, version: Optional[str] = None) -> Optional[Callable]:
        """获取指定版本的处理函数"""
        version = version or self.default_version
        return self.versions.get(version, {}).get(endpoint)
    
    def route(self, endpoint: str, version: Optional[str] = None, *args, **kwargs):
        """路由到对应版本的处理函数"""
        handler = self.get_handler(endpoint, version)
        if handler:
            return handler(*args, **kwargs)
        raise ValueError(f"No handler found for {endpoint} version {version}")
    
    def list_versions(self) -> list:
        """列出所有可用版本"""
        return list(self.versions.keys())


# 使用示例
api = APIVersioning(default_version="v1")

@api.register("v1", "/users")
def get_users_v1():
    return {"version": "v1", "users": ["Alice", "Bob"]}

@api.register("v2", "/users")
def get_users_v2():
    return {"version": "v2", "users": [{"name": "Alice", "id": 1}, {"name": "Bob", "id": 2}]}

# 调用
print(api.route("/users", "v1"))  # v1版本
print(api.route("/users", "v2"))  # v2版本
print(api.route("/users"))        # 默认版本