from typing import Any, Callable, Dict, Optional, Type


class ServiceLocator:
    """服务定位器类，用于管理和访问服务实例"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
    
    def register(self, name: str, service: Any) -> None:
        """注册服务实例"""
        self._services[name] = service
    
    def register_factory(self, name: str, factory: Callable) -> None:
        """注册服务工厂函数"""
        self._factories[name] = factory
    
    def get(self, name: str) -> Any:
        """获取服务实例"""
        if name in self._services:
            return self._services[name]
        
        if name in self._factories:
            service = self._factories[name]()
            self._services[name] = service
            return service
        
        raise KeyError(f"Service '{name}' not found")
    
    def has(self, name: str) -> bool:
        """检查服务是否存在"""
        return name in self._services or name in self._factories
    
    def unregister(self, name: str) -> None:
        """注销服务"""
        self._services.pop(name, None)
        self._factories.pop(name, None)
    
    def clear(self) -> None:
        """清空所有服务"""
        self._services.clear()
        self._factories.clear()


# 使用示例
if __name__ == "__main__":
    # 创建服务定位器
    locator = ServiceLocator()
    
    # 注册服务实例
    class DatabaseService:
        def connect(self):
            return "Connected to database"
    
    db = DatabaseService()
    locator.register("database", db)
    
    # 注册工厂函数
    class CacheService:
        def __init__(self):
            self.data = {}
    
    locator.register_factory("cache", lambda: CacheService())
    
    # 获取服务
    database = locator.get("database")
    print(database.connect())
    
    cache = locator.get("cache")
    print(f"Cache service: {cache}")
    
    # 检查服务
    print(f"Has database: {locator.has('database')}")
    print(f"Has logger: {locator.has('logger')}")