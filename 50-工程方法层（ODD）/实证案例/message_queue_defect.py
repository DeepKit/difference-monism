
import sqlite3
import json
import threading
import queue
import time
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class Message:
    """消息数据模型"""
    id: str
    topic: str
    payload: Any
    timestamp: float
    delivered: bool = False
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class MessageQueue:
    """消息队列核心类"""
    
    def __init__(self, db_path: str = "message_queue.db"):
        self.db_path = db_path
        self.subscribers: Dict[str, List[Callable]] = {}
        self.queues: Dict[str, queue.Queue] = {}
        self.lock = threading.RLock()
        self.running = True
        self._init_database()
        self._load_undelivered_messages()
        self._start_workers()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp REAL NOT NULL,
                delivered INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_topic_delivered 
            ON messages(topic, delivered)
        """)
        conn.commit()
        conn.close()
    
    def _persist_message(self, message: Message):
        """持久化消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (id, topic, payload, timestamp, delivered)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message.id,
            message.topic,
            json.dumps(message.payload),
            message.timestamp,
            int(message.delivered)
        ))
        conn.commit()
        conn.close()
    
    def _mark_delivered(self, message_id: str):
        """标记消息已投递"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages SET delivered = 1 WHERE id = ?
        """, (message_id,))
        conn.commit()
        conn.close()
    
    def _load_undelivered_messages(self):
        """加载未投递的消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, topic, payload, timestamp, delivered
            FROM messages WHERE delivered = 0
            ORDER BY timestamp
        """)
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            message = Message(
                id=row[0],
                topic=row[1],
                payload=json.loads(row[2]),
                timestamp=row[3],
                delivered=bool(row[4])
            )
            self._enqueue_message(message)
    
    def _enqueue_message(self, message: Message):
        """将消息加入队列"""
        with self.lock:
            if message.topic not in self.queues:
                self.queues[message.topic] = queue.Queue()
            self.queues[message.topic].put(message)
    
    def _start_workers(self):
        """启动工作线程"""
        self.worker_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.worker_thread.start()
    
    def _process_messages(self):
        """处理消息的工作线程"""
        while self.running:
            with self.lock:
                topics = list(self.queues.keys())
            
            for topic in topics:
                try:
                    msg = self.queues[topic].get_nowait()
                    self._deliver_message(msg)
                except queue.Empty:
                    continue
            
            time.sleep(0.01)
    
    def _deliver_message(self, message: Message):
        """投递消息给订阅者"""
        with self.lock:
            subscribers = self.subscribers.get(message.topic, [])
        
        for callback in subscribers:
            try:
                callback(message)
            except Exception as e:
                print(f"Error delivering message {message.id}: {e}")
        
        self._mark_delivered(message.id)
    
    def publish(self, topic: str, payload: Any) -> str:
        """发布消息"""
        message = Message(
            id=str(uuid.uuid4()),
            topic=topic,
            payload=payload,
            timestamp=time.time()
        )
        
        self._persist_message(message)
        self._enqueue_message(message)
        
        return message.id
    
    def subscribe(self, topic: str, callback: Callable[[Message], None]):
        """订阅主题"""
        with self.lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(callback)
    
    def unsubscribe(self, topic: str, callback: Callable[[Message], None]):
        """取消订阅"""
        with self.lock:
            if topic in self.subscribers:
                try:
                    self.subscribers[topic].remove(callback)
                except ValueError:
                    pass
    
    def get_message_history(self, topic: Optional[str] = None, limit: int = 100) -> List[Message]:
        """获取消息历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic:
            cursor.execute("""
                SELECT id, topic, payload, timestamp, delivered
                FROM messages WHERE topic = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (topic, limit))
        else:
            cursor.execute("""
                SELECT id, topic, payload, timestamp, delivered
                FROM messages
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        messages = []
        for row in rows:
            messages.append(Message(
                id=row[0],
                topic=row[1],
                payload=json.loads(row[2]),
                timestamp=row[3],
                delivered=bool(row[4])
            ))
        
        return messages
    
    def clear_delivered_messages(self, older_than_seconds: Optional[float] = None):
        """清理已投递的消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if older_than_seconds:
            cutoff_time = time.time() - older_than_seconds
            cursor.execute("""
                DELETE FROM messages 
                WHERE delivered = 1 AND timestamp < ?
            """, (cutoff_time,))
        else:
            cursor.execute("DELETE FROM messages WHERE delivered = 1")
        
        conn.commit()
        conn.close()
    
    def shutdown(self):
        """关闭消息队列"""
        self.running = False
        if hasattr(self, 'worker_thread'):
            self.worker_thread.join(timeout=5)


class Publisher:
    """发布者"""
    
    def __init__(self, mq: MessageQueue):
        self.mq = mq
    
    def publish(self, topic: str, payload: Any) -> str:
        """发布消息"""
        return self.mq.publish(topic, payload)


class Subscriber:
    """订阅者"""
    
    def __init__(self, mq: MessageQueue, name: str = ""):
        self.mq = mq
        self.name = name or f"subscriber_{id(self)}"
        self.subscriptions: Dict[str, Callable] = {}
    
    def subscribe(self, topic: str, callback: Optional[Callable[[Message], None]] = None):
        """订阅主题"""
        if callback is None:
            callback = self._default_handler
        
        self.subscriptions[topic] = callback
        self.mq.subscribe(topic, callback)
    
    def unsubscribe(self, topic: str):
        """取消订阅"""
        if topic in self.subscriptions:
            callback = self.subscriptions[topic]
            self.mq.unsubscribe(topic, callback)
            del self.subscriptions[topic]
    
    def _default_handler(self, message: Message):
        """默认消息处理器"""
        print(f"[{self.name}] Received message on '{message.topic}': {message.payload}")


if __name__ == "__main__":
    # 使用示例
    mq = MessageQueue("example_queue.db")
    
    # 创建发布者
    publisher = Publisher(mq)
    
    # 创建订阅者
    subscriber1 = Subscriber(mq, "Subscriber-1")
    subscriber2 = Subscriber(mq, "Subscriber-2")
    
    # 订阅主题
    subscriber1.subscribe("news")
    subscriber1.subscribe("alerts")
    subscriber2.subscribe("news")
    
    # 发布消息
    publisher.publish("news", {"title": "Breaking News", "content": "Important update"})
    publisher.publish("alerts", {"level": "warning", "message": "System maintenance"})
    publisher.publish("news", {"title": "Tech News", "content": "New release"})
    
    # 等待消息处理
    time.sleep(1)
    
    # 查看消息历史
    history = mq.get_message_history("news")
    print(f"\nMessage history for 'news': {len(history)} messages")
    
    # 清理旧消息
    mq.clear_delivered_messages(older_than_seconds=3600)
    
    # 关闭
    mq.shutdown()
