import threading
import queue
from typing import Any, Callable, Optional, List
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Message:
    """消息对象"""
    id: str
    topic: str
    payload: Any
    timestamp: datetime
    
    def __init__(self, topic: str, payload: Any):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.payload = payload
        self.timestamp = datetime.now()


class MessageChannel:
    """线程安全的消息通道类"""
    
    def __init__(self, max_size: int = 0):
        """
        初始化消息通道
        
        Args:
            max_size: 队列最大容量，0表示无限制
        """
        self._subscribers: dict[str, List[queue.Queue]] = {}
        self._lock = threading.RLock()
        self._max_size = max_size
        self._closed = False
        
    def subscribe(self, topic: str) -> queue.Queue:
        """
        订阅主题
        
        Args:
            topic: 主题名称
            
        Returns:
            消息队列
        """
        with self._lock:
            if self._closed:
                raise RuntimeError("Channel is closed")
                
            msg_queue = queue.Queue(maxsize=self._max_size)
            
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            
            self._subscribers[topic].append(msg_queue)
            return msg_queue
    
    def unsubscribe(self, topic: str, msg_queue: queue.Queue) -> bool:
        """
        取消订阅
        
        Args:
            topic: 主题名称
            msg_queue: 消息队列
            
        Returns:
            是否成功取消订阅
        """
        with self._lock:
            if topic in self._subscribers:
                try:
                    self._subscribers[topic].remove(msg_queue)
                    if not self._subscribers[topic]:
                        del self._subscribers[topic]
                    return True
                except ValueError:
                    return False
            return False
    
    def publish(self, topic: str, payload: Any, block: bool = True, timeout: Optional[float] = None) -> Message:
        """
        发布消息
        
        Args:
            topic: 主题名称
            payload: 消息内容
            block: 是否阻塞等待
            timeout: 超时时间（秒）
            
        Returns:
            发布的消息对象
        """
        with self._lock:
            if self._closed:
                raise RuntimeError("Channel is closed")
                
            message = Message(topic, payload)
            
            if topic not in self._subscribers:
                return message
            
            dead_queues = []
            for msg_queue in self._subscribers[topic]:
                try:
                    msg_queue.put(message, block=block, timeout=timeout)
                except queue.Full:
                    dead_queues.append(msg_queue)
            
            # 清理已满的队列
            for dead_queue in dead_queues:
                self._subscribers[topic].remove(dead_queue)
            
            return message
    
    def receive(self, msg_queue: queue.Queue, block: bool = True, timeout: Optional[float] = None) -> Optional[Message]:
        """
        接收消息
        
        Args:
            msg_queue: 消息队列
            block: 是否阻塞等待
            timeout: 超时时间（秒）
            
        Returns:
            消息对象，如果超时返回None
        """
        try:
            return msg_queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
    
    def get_subscriber_count(self, topic: str) -> int:
        """获取主题的订阅者数量"""
        with self._lock:
            return len(self._subscribers.get(topic, []))
    
    def get_topics(self) -> List[str]:
        """获取所有主题列表"""
        with self._lock:
            return list(self._subscribers.keys())
    
    def close(self):
        """关闭通道"""
        with self._lock:
            self._closed = True
            self._subscribers.clear()
    
    def is_closed(self) -> bool:
        """检查通道是否已关闭"""
        return self._closed


# 使用示例
if __name__ == "__main__":
    # 创建消息通道
    channel = MessageChannel()
    
    # 订阅主题
    queue1 = channel.subscribe("news")
    queue2 = channel.subscribe("news")
    queue3 = channel.subscribe("alerts")
    
    # 发布消息
    channel.publish("news", {"title": "Breaking News", "content": "Something happened"})
    channel.publish("alerts", {"level": "warning", "message": "System alert"})
    
    # 接收消息
    msg1 = channel.receive(queue1, timeout=1)
    msg2 = channel.receive(queue2, timeout=1)
    msg3 = channel.receive(queue3, timeout=1)
    
    print(f"Queue1 received: {msg1.payload if msg1 else None}")
    print(f"Queue2 received: {msg2.payload if msg2 else None}")
    print(f"Queue3 received: {msg3.payload if msg3 else None}")
    
    # 查看订阅信息
    print(f"Topics: {channel.get_topics()}")
    print(f"'news' subscribers: {channel.get_subscriber_count('news')}")
    
    # 取消订阅
    channel.unsubscribe("news", queue1)
    
    # 关闭通道
    channel.close()