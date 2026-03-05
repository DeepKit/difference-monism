import threading
import queue
import logging
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


@dataclass
class Message:
    topic: str
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class MessageBridge:
    def __init__(self, max_queue_size: int = 1000):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._message_queue = queue.PriorityQueue(maxsize=max_queue_size)
        self._lock = threading.RLock()
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        self._stats = {
            'messages_sent': 0,
            'messages_processed': 0,
            'errors': 0
        }

    def subscribe(self, topic: str, callback: Callable[[Message], None]) -> None:
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)
            logger.info(f"Subscribed to topic: {topic}")

    def unsubscribe(self, topic: str, callback: Callable[[Message], None]) -> None:
        with self._lock:
            if topic in self._subscribers and callback in self._subscribers[topic]:
                self._subscribers[topic].remove(callback)
                logger.info(f"Unsubscribed from topic: {topic}")

    def publish(self, message: Message) -> bool:
        try:
            priority_value = -message.priority.value
            self._message_queue.put((priority_value, message), block=False)
            self._stats['messages_sent'] += 1
            return True
        except queue.Full:
            logger.error(f"Queue full, message dropped: {message.topic}")
            self._stats['errors'] += 1
            return False

    def start(self) -> None:
        if self._running:
            logger.warning("Bridge already running")
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._process_messages, daemon=True)
        self._worker_thread.start()
        logger.info("Message bridge started")

    def stop(self) -> None:
        if not self._running:
            return

        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
        logger.info("Message bridge stopped")

    def _process_messages(self) -> None:
        while self._running:
            try:
                priority, message = self._message_queue.get(timeout=0.1)
                self._dispatch_message(message)
                self._stats['messages_processed'] += 1
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                self._stats['errors'] += 1

    def _dispatch_message(self, message: Message) -> None:
        with self._lock:
            subscribers = self._subscribers.get(message.topic, [])
            wildcard_subscribers = self._subscribers.get('*', [])
            all_subscribers = subscribers + wildcard_subscribers

        for callback in all_subscribers:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in subscriber callback: {e}")
                self._stats['errors'] += 1

    def get_stats(self) -> Dict[str, int]:
        return self._stats.copy()

    def clear_topic(self, topic: str) -> None:
        with self._lock:
            if topic in self._subscribers:
                del self._subscribers[topic]
                logger.info(f"Cleared all subscribers for topic: {topic}")


# 使用示例
if __name__ == "__main__":
    bridge = MessageBridge()

    def handler1(msg: Message):
        print(f"Handler1 received: {msg.topic} - {msg.payload}")

    def handler2(msg: Message):
        print(f"Handler2 received: {msg.topic} - {msg.payload}")

    bridge.subscribe("user.login", handler1)
    bridge.subscribe("user.logout", handler2)
    bridge.subscribe("*", lambda msg: print(f"Wildcard: {msg.topic}"))

    bridge.start()

    bridge.publish(Message(topic="user.login", payload={"user_id": 123}))
    bridge.publish(Message(
        topic="user.logout",
        payload={"user_id": 123},
        priority=MessagePriority.HIGH
    ))

    import time
    time.sleep(1)

    print(f"Stats: {bridge.get_stats()}")
    bridge.stop()