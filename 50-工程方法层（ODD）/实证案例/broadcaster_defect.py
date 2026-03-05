
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import threading


@dataclass
class Message:
    """消息数据类"""
    topic: str
    content: Any
    timestamp: datetime = None
    sender: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class Subscriber:
    """订阅者基类"""
    def __init__(self, name: str):
        self.name = name
    
    def on_message(self, message: Message):
        """接收消息的回调方法"""
        raise NotImplementedError


class MessageBroadcaster:
    """消息广播器"""
    def __init__(self):
        self._subscribers: Dict[str, List[Subscriber]] = {}
        self._global_subscribers: List[Subscriber] = []
        self._lock = threading.Lock()
    
    def subscribe(self, subscriber: Subscriber, topic: Optional[str] = None):
        """订阅消息"""
        with self._lock:
            if topic is None:
                if subscriber not in self._global_subscribers:
                    self._global_subscribers.append(subscriber)
            else:
                if topic not in self._subscribers:
                    self._subscribers[topic] = []
                if subscriber not in self._subscribers[topic]:
                    self._subscribers[topic].append(subscriber)
    
    def unsubscribe(self, subscriber: Subscriber, topic: Optional[str] = None):
        """取消订阅"""
        with self._lock:
            if topic is None:
                if subscriber in self._global_subscribers:
                    self._global_subscribers.remove(subscriber)
            else:
                if topic in self._subscribers and subscriber in self._subscribers[topic]:
                    self._subscribers[topic].remove(subscriber)
                    if not self._subscribers[topic]:
                        del self._subscribers[topic]
    
    def broadcast(self, message: Message):
        """广播消息"""
        with self._lock:
            subscribers = self._global_subscribers.copy()
            if message.topic in self._subscribers:
                subscribers.extend(self._subscribers[message.topic])
        
        for subscriber in subscribers:
            try:
                subscriber.on_message(message)
            except Exception as e:
                print(f"Error delivering message to {subscriber.name}: {e}")
    
    def publish(self, topic: str, content: Any, sender: Optional[str] = None):
        """发布消息的便捷方法"""
        message = Message(topic=topic, content=content, sender=sender)
        self.broadcast(message)
    
    def get_topics(self) -> List[str]:
        """获取所有主题"""
        with self._lock:
            return list(self._subscribers.keys())
    
    def get_subscriber_count(self, topic: Optional[str] = None) -> int:
        """获取订阅者数量"""
        with self._lock:
            if topic is None:
                return len(self._global_subscribers)
            return len(self._subscribers.get(topic, []))


class FunctionSubscriber(Subscriber):
    """基于函数的订阅者"""
    def __init__(self, name: str, callback: Callable[[Message], None]):
        super().__init__(name)
        self.callback = callback
    
    def on_message(self, message: Message):
        self.callback(message)


class LogSubscriber(Subscriber):
    """日志订阅者示例"""
    def on_message(self, message: Message):
        print(f"[{message.timestamp}] [{message.topic}] {message.content}")


class EmailSubscriber(Subscriber):
    """邮件订阅者示例"""
    def __init__(self, name: str, email: str):
        super().__init__(name)
        self.email = email
    
    def on_message(self, message: Message):
        print(f"Sending email to {self.email}: [{message.topic}] {message.content}")


# 使用示例
if __name__ == "__main__":
    broadcaster = MessageBroadcaster()
    
    # 创建订阅者
    logger = LogSubscriber("Logger")
    email_sub = EmailSubscriber("EmailNotifier", "user@example.com")
    
    # 订阅特定主题
    broadcaster.subscribe(logger, "system")
    broadcaster.subscribe(email_sub, "alerts")
    
    # 发布消息
    broadcaster.publish("system", "System started", sender="Server")
    broadcaster.publish("alerts", "High CPU usage detected", sender="Monitor")
    broadcaster.publish("info", "Regular update", sender="App")
