from typing import Callable, Dict, List, Any
from threading import Lock
import weakref


class MessageBus:
    """线程安全的消息总线实现"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = Lock()
    
    def subscribe(self, topic: str, callback: Callable) -> None:
        """订阅主题"""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)
    
    def unsubscribe(self, topic: str, callback: Callable) -> bool:
        """取消订阅"""
        with self._lock:
            if topic in self._subscribers:
                try:
                    self._subscribers[topic].remove(callback)
                    if not self._subscribers[topic]:
                        del self._subscribers[topic]
                    return True
                except ValueError:
                    return False
            return False
    
    def publish(self, topic: str, *args, **kwargs) -> None:
        """发布消息"""
        with self._lock:
            subscribers = self._subscribers.get(topic, []).copy()
        
        for callback in subscribers:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Error in subscriber {callback}: {e}")
    
    def clear(self, topic: str = None) -> None:
        """清除订阅"""
        with self._lock:
            if topic:
                self._subscribers.pop(topic, None)
            else:
                self._subscribers.clear()
    
    def topics(self) -> List[str]:
        """获取所有主题"""
        with self._lock:
            return list(self._subscribers.keys())


# 使用示例
if __name__ == "__main__":
    bus = MessageBus()
    
    # 订阅
    def handler1(data):
        print(f"Handler 1: {data}")
    
    def handler2(data):
        print(f"Handler 2: {data}")
    
    bus.subscribe("user.login", handler1)
    bus.subscribe("user.login", handler2)
    bus.subscribe("user.logout", handler1)
    
    # 发布
    bus.publish("user.login", {"user": "alice"})
    bus.publish("user.logout", {"user": "alice"})
    
    # 取消订阅
    bus.unsubscribe("user.login", handler1)
    bus.publish("user.login", {"user": "bob"})
    
    # 查看主题
    print(f"Topics: {bus.topics()}")