
import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CacheItem:
    key: str
    value: Any
    loaded_at: datetime
    loader: Callable


class CacheWarming:
    def __init__(self, max_workers: int = 5):
        self.cache: Dict[str, CacheItem] = {}
        self.loaders: Dict[str, Callable] = {}
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._warming_tasks: Set[asyncio.Task] = set()
        
    def register_loader(self, key: str, loader: Callable) -> None:
        self.loaders[key] = loader
        
    def preload(self, keys: Optional[List[str]] = None) -> None:
        keys_to_load = keys if keys else list(self.loaders.keys())
        
        logger.info(f"开始预加载 {len(keys_to_load)} 个缓存项")
        start_time = time.time()
        
        for key in keys_to_load:
            if key not in self.loaders:
                logger.warning(f"未找到加载器: {key}")
                continue
                
            try:
                loader = self.loaders[key]
                value = loader()
                self.cache[key] = CacheItem(
                    key=key,
                    value=value,
                    loaded_at=datetime.now(),
                    loader=loader
                )
                logger.info(f"预加载成功: {key}")
            except Exception as e:
                logger.error(f"预加载失败 {key}: {str(e)}")
        
        elapsed = time.time() - start_time
        logger.info(f"预加载完成，耗时: {elapsed:.2f}秒")
    
    async def async_warm(self, keys: Optional[List[str]] = None) -> None:
        keys_to_warm = keys if keys else list(self.loaders.keys())
        
        logger.info(f"开始异步预热 {len(keys_to_warm)} 个缓存项")
        start_time = time.time()
        
        tasks = []
        for key in keys_to_warm:
            if key not in self.loaders:
                logger.warning(f"未找到加载器: {key}")
                continue
            task = asyncio.create_task(self._async_load_item(key))
            tasks.append(task)
            self._warming_tasks.add(task)
            task.add_done_callback(self._warming_tasks.discard)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        elapsed = time.time() - start_time
        logger.info(f"异步预热完成: {success_count}/{len(tasks)} 成功，耗时: {elapsed:.2f}秒")
    
    async def _async_load_item(self, key: str) -> None:
        try:
            loader = self.loaders[key]
            loop = asyncio.get_event_loop()
            
            if asyncio.iscoroutinefunction(loader):
                value = await loader()
            else:
                value = await loop.run_in_executor(self.executor, loader)
            
            self.cache[key] = CacheItem(
                key=key,
                value=value,
                loaded_at=datetime.now(),
                loader=loader
            )
            logger.info(f"异步预热成功: {key}")
        except Exception as e:
            logger.error(f"异步预热失败 {key}: {str(e)}")
            raise
    
    async def refresh(self, key: str) -> None:
        if key not in self.loaders:
            raise KeyError(f"未找到加载器: {key}")
        await self._async_load_item(key)
    
    async def refresh_all(self) -> None:
        await self.async_warm()
    
    def get(self, key: str) -> Any:
        if key not in self.cache:
            raise KeyError(f"缓存未命中: {key}")
        return self.cache[key].value
    
    def get_or_load(self, key: str) -> Any:
        if key in self.cache:
            return self.cache[key].value
        
        if key not in self.loaders:
            raise KeyError(f"未找到加载器: {key}")
        
        loader = self.loaders[key]
        value = loader()
        self.cache[key] = CacheItem(
            key=key,
            value=value,
            loaded_at=datetime.now(),
            loader=loader
        )
        return value
    
    def clear(self, key: Optional[str] = None) -> None:
        if key:
            self.cache.pop(key, None)
            logger.info(f"清除缓存: {key}")
        else:
            self.cache.clear()
            logger.info("清除所有缓存")
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_items": len(self.cache),
            "registered_loaders": len(self.loaders),
            "cached_keys": list(self.cache.keys()),
            "active_warming_tasks": len(self._warming_tasks)
        }
    
    def shutdown(self) -> None:
        self.executor.shutdown(wait=True)
        logger.info("CacheWarming已关闭")


# 使用示例
if __name__ == "__main__":
    def load_user_data():
        time.sleep(1)
        return {"users": [1, 2, 3]}
    
    def load_config():
        time.sleep(0.5)
        return {"setting": "value"}
    
    async def load_async_data():
        await asyncio.sleep(1)
        return {"async": "data"}
    
    cache = CacheWarming(max_workers=3)
    
    cache.register_loader("users", load_user_data)
    cache.register_loader("config", load_config)
    cache.register_loader("async_data", load_async_data)
    
    # 同步预加载
    cache.preload(["users", "config"])
    print(cache.get("users"))
    
    # 异步预热
    async def main():
        await cache.async_warm()
        print(cache.get("async_data"))
        print(cache.get_stats())
        cache.shutdown()
    
    asyncio.run(main())
