
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CacheConfig:
    """缓存配置"""
    ttl: int = 3600  # 默认过期时间（秒）
    max_size: Optional[int] = None  # 最大缓存条目数
    warm_on_startup: bool = True  # 启动时是否预热
    warm_interval: Optional[int] = None  # 定期预热间隔（秒）


class CacheBackend(ABC):
    """缓存后端抽象基类"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass


class InMemoryCache(CacheBackend):
    """内存缓存实现"""
    
    def __init__(self, max_size: Optional[int] = None):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
    
    async def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry['expires_at'] and datetime.now() > entry['expires_at']:
            await self.delete(key)
            return None
        
        return entry['value']
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if self._max_size and len(self._cache) >= self._max_size:
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k]['created_at'])
            await self.delete(oldest_key)
        
        expires_at = None
        if ttl:
            expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self._cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'expires_at': expires_at
        }
        return True
    
    async def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def clear(self) -> bool:
        self._cache.clear()
        return True
    
    async def exists(self, key: str) -> bool:
        return key in self._cache


class RedisCache(CacheBackend):
    """Redis缓存实现（需要安装redis库）"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.Redis(host=host, port=port, db=db, 
                                        decode_responses=True)
        except ImportError:
            raise ImportError("需要安装redis库: pip install redis")
    
    async def get(self, key: str) -> Optional[Any]:
        value = await self._redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        serialized = json.dumps(value)
        if ttl:
            await self._redis.setex(key, ttl, serialized)
        else:
            await self._redis.set(key, serialized)
        return True
    
    async def delete(self, key: str) -> bool:
        result = await self._redis.delete(key)
        return result > 0
    
    async def clear(self) -> bool:
        await self._redis.flushdb()
        return True
    
    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key) > 0


@dataclass
class WarmupTask:
    """预热任务"""
    key: str
    loader: Callable[[], Any]  # 数据加载函数
    ttl: Optional[int] = None
    priority: int = 0  # 优先级，数字越大优先级越高


class CacheWarmer:
    """缓存预热器"""
    
    def __init__(self, backend: CacheBackend, config: CacheConfig):
        self.backend = backend
        self.config = config
        self._tasks: List[WarmupTask] = []
        self._is_running = False
    
    def register_task(self, task: WarmupTask):
        """注册预热任务"""
        self._tasks.append(task)
        logger.info(f"注册预热任务: {task.key}")
    
    def register(self, key: str, loader: Callable[[], Any], 
                 ttl: Optional[int] = None, priority: int = 0):
        """便捷方法注册预热任务"""
        task = WarmupTask(key=key, loader=loader, ttl=ttl, priority=priority)
        self.register_task(task)
    
    async def warmup_single(self, task: WarmupTask) -> bool:
        """执行单个预热任务"""
        try:
            logger.info(f"开始预热缓存: {task.key}")
            
            if asyncio.iscoroutinefunction(task.loader):
                data = await task.loader()
            else:
                data = task.loader()
            
            ttl = task.ttl or self.config.ttl
            await self.backend.set(task.key, data, ttl)
            
            logger.info(f"缓存预热成功: {task.key}")
            return True
            
        except Exception as e:
            logger.error(f"缓存预热失败 {task.key}: {str(e)}")
            return False
    
    async def warmup_all(self, force: bool = False):
        """执行所有预热任务"""
        if not self._tasks:
            logger.warning("没有注册的预热任务")
            return
        
        sorted_tasks = sorted(self._tasks, key=lambda t: t.priority, reverse=True)
        
        success_count = 0
        fail_count = 0
        
        for task in sorted_tasks:
            if not force and await self.backend.exists(task.key):
                logger.info(f"缓存已存在，跳过: {task.key}")
                continue
            
            result = await self.warmup_single(task)
            if result:
                success_count += 1
            else:
                fail_count += 1
        
        logger.info(f"预热完成 - 成功: {success_count}, 失败: {fail_count}")
    
    async def start_periodic_warmup(self):
        """启动定期预热"""
        if not self.config.warm_interval:
            logger.warning("未配置预热间隔，不启动定期预热")
            return
        
        self._is_running = True
        logger.info(f"启动定期预热，间隔: {self.config.warm_interval}秒")
        
        while self._is_running:
            await self.warmup_all(force=True)
            await asyncio.sleep(self.config.warm_interval)
    
    def stop_periodic_warmup(self):
        """停止定期预热"""
        self._is_running = False
        logger.info("停止定期预热")


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, backend: CacheBackend, config: Optional[CacheConfig] = None):
        self.backend = backend
        self.config = config or CacheConfig()
        self.warmer = CacheWarmer(backend, self.config)
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        return await self.backend.get(key)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        ttl = ttl or self.config.ttl
        return await self.backend.set(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        return await self.backend.delete(key)
    
    async def clear(self) -> bool:
        """清空缓存"""
        return await self.backend.clear()
    
    async def get_or_set(self, key: str, loader: Callable[[], Any], 
                        ttl: Optional[int] = None) -> Any:
        """获取缓存，不存在则加载并设置"""
        value = await self.get(key)
        if value is not None:
            return value
        
        if asyncio.iscoroutinefunction(loader):
            value = await loader()
        else:
            value = loader()
        
        await self.set(key, value, ttl)
        return value
    
    async def initialize(self):
        """初始化缓存（执行预热）"""
        if self.config.warm_on_startup:
            logger.info("启动时执行缓存预热")
            await self.warmer.warmup_all()


# 使用示例
async def example_usage():
    """使用示例"""
    
    # 创建缓存管理器
    config = CacheConfig(
        ttl=3600,
        max_size=1000,
        warm_on_startup=True,
        warm_interval=300
    )
    
    backend = InMemoryCache(max_size=config.max_size)
    cache_manager = CacheManager(backend, config)
    
    # 注册预热任务
    def load_user_data():
        return {"users": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}
    
    async def load_product_data():
        await asyncio.sleep(0.1)  # 模拟异步加载
        return {"products": [{"id": 1, "name": "商品A"}, {"id": 2, "name": "商品B"}]}
    
    def load_config_data():
        return {"app_name": "MyApp", "version": "1.0.0"}
    
    cache_manager.warmer.register("users", load_user_data, ttl=1800, priority=10)
    cache_manager.warmer.register("products", load_product_data, ttl=3600, priority=5)
    cache_manager.warmer.register("config", load_config_data, ttl=7200, priority=1)
    
    # 初始化并预热
    await cache_manager.initialize()
    
    # 获取缓存数据
    users = await cache_manager.get("users")
    print(f"用户数据: {users}")
    
    # 使用get_or_set
    settings = await cache_manager.get_or_set(
        "settings",
        lambda: {"theme": "dark", "language": "zh-CN"}
    )
    print(f"设置数据: {settings}")


if __name__ == "__main__":
    asyncio.run(example_usage())
