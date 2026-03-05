from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
import threading
from collections import defaultdict


@dataclass
class Event:
    """事件数据类"""
    name: str
    data: Any
    source: Optional[str] = None


class PublisherCenter:
    """发布者中心类 - 实现发布订阅模式"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._lock = threading.RLock()
    
    def subscribe(self, event_name: str, callback: Callable[[Event], None]) -> None:
        """订阅事件"""
        with self._lock:
            if callback not in self._subscribers[event_name]:
                self._subscribers[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable[[Event], None]) -> bool:
        """取消订阅"""
        with self._lock:
            if event_name in self._subscribers and callback in self._subscribers[event_name]:
                self._subscribers[event_name].remove(callback)
                if not self._subscribers[event_name]:
                    del self._subscribers[event_name]
                return True
            return False
    
    def unsubscribe_all(self, event_name: str) -> None:
        """取消某事件的所有订阅"""
        with self._lock:
            if event_name in self._subscribers:
                del self._subscribers[event_name]
    
    def publish(self, event_name: str, data: Any = None, source: Optional[str] = None) -> int:
        """发布事件，返回通知的订阅者数量"""
        event = Event(name=event_name, data=data, source=source)
        with self._lock:
            subscribers = self._subscribers.get(event_name, []).copy()
        
        count = 0
        for callback in subscribers:
            try:
                callback(event)
                count += 1
            except Exception as e:
                print(f"订阅者回调执行失败: {e}")
        
        return count
    
    def has_subscribers(self, event_name: str) -> bool:
        """检查事件是否有订阅者"""
        with self._lock:
            return event_name in self._subscribers and len(self._subscribers[event_name]) > 0
    
    def get_subscriber_count(self, event_name: str) -> int:
        """获取事件的订阅者数量"""
        with self._lock:
            return len(self._subscribers.get(event_name, []))
    
    def clear(self) -> None:
        """清空所有订阅"""
        with self._lock:
            self._subscribers.clear()
    
    def get_all_events(self) -> List[str]:
        """获取所有已订阅的事件名称"""
        with self._lock:
            return list(self._subscribers.keys())


# 使用示例
if __name__ == "__main__":
    center = PublisherCenter()
    
    # 定义订阅者回调
    def on_user_login(event: Event):
        print(f"用户登录: {event.data}")
    
    def on_user_logout(event: Event):
        print(f"用户登出: {event.data}")
    
    def on_data_update(event: Event):
        print(f"数据更新: {event.data}")
    
    # 订阅事件
    center.subscribe("user.login", on_user_login)
    center.subscribe("user.logout", on_user_logout)
    center.subscribe("data.update", on_data_update)
    
    # 发布事件
    center.publish("user.login", {"username": "alice", "time": "2024-01-01"})
    center.publish("data.update", {"table": "users", "count": 100})
    center.publish("user.logout", {"username": "alice"})
    
    # 取消订阅
    center.unsubscribe("user.login", on_user_login)
    
    # 再次发布（不会触发已取消的订阅）
    center.publish("user.login", {"username": "bob"})