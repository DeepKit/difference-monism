from typing import Any, Callable, Dict, TypeVar, Optional
from enum import Enum
import inspect

T = TypeVar('T')


class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class DIContainer:
    def __init__(self):
        self._services: Dict[Type, tuple[Callable, Lifetime]] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register(
        self, 
        interface: Type[T], 
        implementation: Type[T] | Callable[..., T], 
        lifetime: Lifetime = Lifetime.TRANSIENT
    ) -> 'DIContainer':
        """注册服务"""
        self._services[interface] = (implementation, lifetime)
        return self
    
    def register_singleton(self, interface: Type[T], implementation: Type[T] | Callable[..., T]) -> 'DIContainer':
        """注册单例服务"""
        return self.register(interface, implementation, Lifetime.SINGLETON)
    
    def register_transient(self, interface: Type[T], implementation: Type[T] | Callable[..., T]) -> 'DIContainer':
        """注册瞬态服务"""
        return self.register(interface, implementation, Lifetime.TRANSIENT)
    
    def resolve(self, interface: Type[T]) -> T:
        """解析服务"""
        if interface not in self._services:
            raise ValueError(f"Service {interface.__name__} not registered")
        
        implementation, lifetime = self._services[interface]
        
        # 单例模式：检查是否已创建
        if lifetime == Lifetime.SINGLETON:
            if interface in self._singletons:
                return self._singletons[interface]
        
        # 创建实例
        instance = self._create_instance(implementation)
        
        # 单例模式：缓存实例
        if lifetime == Lifetime.SINGLETON:
            self._singletons[interface] = instance
        
        return instance
    
    def _create_instance(self, implementation: Type | Callable) -> Any:
        """创建实例并注入依赖"""
        if not inspect.isclass(implementation):
            return implementation()
        
        # 获取构造函数参数
        sig = inspect.signature(implementation.__init__)
        params = sig.parameters
        
        # 解析依赖
        kwargs = {}
        for param_name, param in params.items():
            if param_name == 'self':
                continue
            
            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                continue
            
            # 递归解析依赖
            kwargs[param_name] = self.resolve(param_type)
        
        return implementation(**kwargs)


# 使用示例
if __name__ == "__main__":
    # 定义接口和实现
    class ILogger:
        def log(self, message: str):
            pass
    
    class ConsoleLogger(ILogger):
        def log(self, message: str):
            print(f"[LOG] {message}")
    
    class IDatabase:
        def query(self, sql: str):
            pass
    
    class PostgresDatabase(IDatabase):
        def __init__(self, logger: ILogger):
            self.logger = logger
        
        def query(self, sql: str):
            self.logger.log(f"Executing: {sql}")
            return "Result"
    
    class UserService:
        def __init__(self, database: IDatabase, logger: ILogger):
            self.database = database
            self.logger = logger
        
        def get_user(self, user_id: int):
            self.logger.log(f"Getting user {user_id}")
            return self.database.query(f"SELECT * FROM users WHERE id={user_id}")
    
    # 配置容器
    container = DIContainer()
    container.register_singleton(ILogger, ConsoleLogger)
    container.register_transient(IDatabase, PostgresDatabase)
    container.register_transient(UserService, UserService)
    
    # 解析服务
    service1 = container.resolve(UserService)
    service1.get_user(1)
    
    service2 = container.resolve(UserService)
    service2.get_user(2)
    
    # 验证单例
    logger1 = container.resolve(ILogger)
    logger2 = container.resolve(ILogger)
    print(f"Same logger instance: {logger1 is logger2}")  # True