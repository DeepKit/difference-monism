
import json
import time
import threading
import uuid
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
from pathlib import Path
import queue


@dataclass
class Message:
    id: str
    topic: str
    content: Any
    timestamp: float
    retry_count: int = 0
    max_retries: int = 3
    consumer_group: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class MessageQueue:
    def __init__(self, persistence_file: str = "message_queue.json"):
        self.persistence_file = persistence_file
        self.topics: Dict[str, queue.Queue] = defaultdict(queue.Queue)
        self.subscribers: Dict[str, List[Dict]] = defaultdict(list)
        self.consumer_groups: Dict[str, Dict] = defaultdict(lambda: {
            "consumers": [],
            "offset": 0,
            "pending_acks": {}
        })
        self.messages: Dict[str, Message] = {}
        self.pending_messages: Dict[str, Message] = {}
        self.lock = threading.RLock()
        self.running = True
        self.ack_timeout = 30
        
        self._load_persistence()
        self._start_retry_worker()
    
    def publish(self, topic: str, content: Any) -> str:
        with self.lock:
            message = Message(
                id=str(uuid.uuid4()),
                topic=topic,
                content=content,
                timestamp=time.time()
            )
            self.messages[message.id] = message
            self.topics[topic].put(message)
            self._notify_subscribers(topic, message)
            self._save_persistence()
            return message.id
    
    def subscribe(self, topic: str, callback: Callable, consumer_group: Optional[str] = None):
        with self.lock:
            subscriber = {
                "callback": callback,
                "consumer_group": consumer_group,
                "thread": None
            }
            self.subscribers[topic].append(subscriber)
            
            if consumer_group:
                if consumer_group not in self.consumer_groups:
                    self.consumer_groups[consumer_group] = {
                        "consumers": [],
                        "offset": 0,
                        "pending_acks": {},
                        "topic": topic
                    }
                self.consumer_groups[consumer_group]["consumers"].append(callback)
            
            thread = threading.Thread(
                target=self._consume_messages,
                args=(topic, subscriber),
                daemon=True
            )
            subscriber["thread"] = thread
            thread.start()
    
    def _consume_messages(self, topic: str, subscriber: Dict):
        while self.running:
            try:
                message = self.topics[topic].get(timeout=1)
                consumer_group = subscriber["consumer_group"]
                
                if consumer_group:
                    with self.lock:
                        message.consumer_group = consumer_group
                        self.pending_messages[message.id] = message
                        self.consumer_groups[consumer_group]["pending_acks"][message.id] = {
                            "message": message,
                            "timestamp": time.time()
                        }
                
                try:
                    subscriber["callback"](message)
                    if not consumer_group:
                        self._auto_ack(message.id)
                except Exception as e:
                    print(f"Error processing message {message.id}: {e}")
                    if consumer_group:
                        self._handle_failed_message(message)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Consumer error: {e}")
    
    def ack(self, message_id: str, consumer_group: str) -> bool:
        with self.lock:
            if consumer_group not in self.consumer_groups:
                return False
            
            pending_acks = self.consumer_groups[consumer_group]["pending_acks"]
            if message_id in pending_acks:
                del pending_acks[message_id]
                if message_id in self.pending_messages:
                    del self.pending_messages[message_id]
                self._save_persistence()
                return True
            return False
    
    def _auto_ack(self, message_id: str):
        with self.lock:
            if message_id in self.pending_messages:
                del self.pending_messages[message_id]
    
    def _handle_failed_message(self, message: Message):
        with self.lock:
            message.retry_count += 1
            if message.retry_count < message.max_retries:
                self.pending_messages[message.id] = message
            else:
                print(f"Message {message.id} exceeded max retries")
                if message.consumer_group:
                    group = self.consumer_groups[message.consumer_group]
                    if message.id in group["pending_acks"]:
                        del group["pending_acks"][message.id]
                if message.id in self.pending_messages:
                    del self.pending_messages[message.id]
            self._save_persistence()
    
    def _start_retry_worker(self):
        def retry_worker():
            while self.running:
                time.sleep(5)
                with self.lock:
                    current_time = time.time()
                    for group_name, group_data in self.consumer_groups.items():
                        expired_messages = []
                        for msg_id, ack_data in group_data["pending_acks"].items():
                            if current_time - ack_data["timestamp"] > self.ack_timeout:
                                expired_messages.append(msg_id)
                        
                        for msg_id in expired_messages:
                            message = group_data["pending_acks"][msg_id]["message"]
                            del group_data["pending_acks"][msg_id]
                            self._handle_failed_message(message)
                            if message.retry_count < message.max_retries:
                                self.topics[message.topic].put(message)
        
        thread = threading.Thread(target=retry_worker, daemon=True)
        thread.start()
    
    def _notify_subscribers(self, topic: str, message: Message):
        pass
    
    def _save_persistence(self):
        try:
            data = {
                "messages": {k: v.to_dict() for k, v in self.messages.items()},
                "pending_messages": {k: v.to_dict() for k, v in self.pending_messages.items()},
                "consumer_groups": {
                    k: {
                        "offset": v["offset"],
                        "topic": v.get("topic", ""),
                        "pending_acks": {
                            msg_id: {
                                "message": ack_data["message"].to_dict(),
                                "timestamp": ack_data["timestamp"]
                            }
                            for msg_id, ack_data in v["pending_acks"].items()
                        }
                    }
                    for k, v in self.consumer_groups.items()
                }
            }
            with open(self.persistence_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Persistence save error: {e}")
    
    def _load_persistence(self):
        try:
            if Path(self.persistence_file).exists():
                with open(self.persistence_file, 'r') as f:
                    data = json.load(f)
                
                self.messages = {k: Message.from_dict(v) for k, v in data.get("messages", {}).items()}
                self.pending_messages = {k: Message.from_dict(v) for k, v in data.get("pending_messages", {}).items()}
                
                for group_name, group_data in data.get("consumer_groups", {}).items():
                    self.consumer_groups[group_name] = {
                        "consumers": [],
                        "offset": group_data.get("offset", 0),
                        "topic": group_data.get("topic", ""),
                        "pending_acks": {
                            msg_id: {
                                "message": Message.from_dict(ack_data["message"]),
                                "timestamp": ack_data["timestamp"]
                            }
                            for msg_id, ack_data in group_data.get("pending_acks", {}).items()
                        }
                    }
        except Exception as e:
            print(f"Persistence load error: {e}")
    
    def get_stats(self) -> Dict:
        with self.lock:
            return {
                "total_messages": len(self.messages),
                "pending_messages": len(self.pending_messages),
                "topics": list(self.topics.keys()),
                "consumer_groups": {
                    name: {
                        "consumers": len(data["consumers"]),
                        "pending_acks": len(data["pending_acks"])
                    }
                    for name, data in self.consumer_groups.items()
                }
            }
    
    def shutdown(self):
        self.running = False
        self._save_persistence()


# 使用示例
if __name__ == "__main__":
    mq = MessageQueue()
    
    def consumer1(message: Message):
        print(f"Consumer1 received: {message.content}")
        time.sleep(0.1)
        if message.consumer_group:
            mq.ack(message.id, message.consumer_group)
    
    def consumer2(message: Message):
        print(f"Consumer2 received: {message.content}")
        time.sleep(0.1)
        if message.consumer_group:
            mq.ack(message.id, message.consumer_group)
    
    mq.subscribe("orders", consumer1, consumer_group="order-processors")
    mq.subscribe("orders", consumer2, consumer_group="order-processors")
    
    for i in range(5):
        mq.publish("orders", {"order_id": i, "amount": 100 * i})
    
    time.sleep(3)
    print(mq.get_stats())
    
    mq.shutdown()
