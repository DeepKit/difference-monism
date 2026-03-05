
import threading
import time
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timedelta


class CacheInvalidation:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, datetime] = {}
        self._ttl: Dict[str, float] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
        self._delayed_tasks: Dict[str, threading.Timer] = {}
        self._lock = threading.RLock()
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = datetime.now()
            if ttl:
                self._ttl[key] = ttl
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            
            if key in self._ttl:
                elapsed = (datetime.now() - self._timestamps[key]).total_seconds()
                if elapsed > self._ttl[key]:
                    self._invalidate_internal(key)
                    return None
            
            return self._cache.get(key)
    
    def active_invalidate(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                self._invalidate_internal(key)
                return True
            return False
    
    def delayed_invalidate(self, key: str, delay_seconds: float) -> None:
        with self._lock:
            if key in self._delayed_tasks:
                self._delayed_tasks[key].cancel()
            
            timer = threading.Timer(delay_seconds, self._delayed_invalidate_callback, args=[key])
            self._delayed_tasks[key] = timer
            timer.start()
    
    def _delayed_invalidate_callback(self, key: str) -> None:
        with self._lock:
            if key in self._delayed_tasks:
                del self._delayed_tasks[key]
            self._invalidate_internal(key)
    
    def subscribe(self, key: str, callback: Callable[[str], None]) -> None:
        with self._lock:
            if key not in self._subscribers:
                self._subscribers[key] = []
            self._subscribers[key].append(callback)
    
    def unsubscribe(self, key: str, callback: Callable[[str], None]) -> None:
        with self._lock:
            if key in self._subscribers and callback in self._subscribers[key]:
                self._subscribers[key].remove(callback)
    
    def subscription_invalidate(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                self._invalidate_internal(key)
                return True
            return False
    
    def _invalidate_internal(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
        if key in self._ttl:
            del self._ttl[key]
        
        if key in self._subscribers:
            for callback in self._subscribers[key]:
                try:
                    callback(key)
                except Exception:
                    pass
    
    def clear(self) -> None:
        with self._lock:
            for key in list(self._delayed_tasks.keys()):
                self._delayed_tasks[key].cancel()
            
            self._cache.clear()
            self._timestamps.clear()
            self._ttl.clear()
            self._subscribers.clear()
            self._delayed_tasks.clear()
    
    def keys(self) -> List[str]:
        with self._lock:
            return list(self._cache.keys())
    
    def __del__(self):
        self.clear()


if __name__ == "__main__":
    cache = CacheInvalidation()
    
    # 主动失效
    cache.set("key1", "value1")
    print(f"key1: {cache.get('key1')}")
    cache.active_invalidate("key1")
    print(f"key1 after active invalidation: {cache.get('key1')}")
    
    # 延迟失效
    cache.set("key2", "value2")
    print(f"key2: {cache.get('key2')}")
    cache.delayed_invalidate("key2", 2)
    print(f"key2 immediately: {cache.get('key2')}")
    time.sleep(2.5)
    print(f"key2 after 2.5s: {cache.get('key2')}")
    
    # 订阅失效
    def on_invalidate(key: str):
        print(f"Cache invalidated: {key}")
    
    cache.set("key3", "value3")
    cache.subscribe("key3", on_invalidate)
    cache.subscription_invalidate("key3")
    
    cache.clear()
