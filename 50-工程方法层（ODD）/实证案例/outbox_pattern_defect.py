import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import threading
import time


class OutboxStatus(Enum):
    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"


class OutboxMessage:
    def __init__(
        self,
        id: str,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload: Dict[str, Any],
        status: OutboxStatus = OutboxStatus.PENDING,
        created_at: Optional[datetime] = None,
        published_at: Optional[datetime] = None,
        retry_count: int = 0
    ):
        self.id = id
        self.aggregate_type = aggregate_type
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.payload = payload
        self.status = status
        self.created_at = created_at or datetime.now()
        self.published_at = published_at
        self.retry_count = retry_count


class Outbox:
    def __init__(self, db_path: str = "outbox.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outbox (
                id TEXT PRIMARY KEY,
                aggregate_type TEXT NOT NULL,
                aggregate_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                published_at TEXT,
                retry_count INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
    
    def add(
        self,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload: Dict[str, Any],
        conn: Optional[sqlite3.Connection] = None
    ) -> str:
        message_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        should_close = False
        if conn is None:
            conn = sqlite3.connect(self.db_path)
            should_close = True
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO outbox (id, aggregate_type, aggregate_id, event_type, payload, status, created_at, retry_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                aggregate_type,
                aggregate_id,
                event_type,
                json.dumps(payload),
                OutboxStatus.PENDING.value,
                created_at,
                0
            ))
            
            if should_close:
                conn.commit()
            
            return message_id
        finally:
            if should_close:
                conn.close()
    
    def get_pending_messages(self, limit: int = 100) -> List[OutboxMessage]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, aggregate_type, aggregate_id, event_type, payload, status, created_at, published_at, retry_count
            FROM outbox
            WHERE status = ?
            ORDER BY created_at ASC
            LIMIT ?
        """, (OutboxStatus.PENDING.value, limit))
        
        messages = []
        for row in cursor.fetchall():
            messages.append(OutboxMessage(
                id=row[0],
                aggregate_type=row[1],
                aggregate_id=row[2],
                event_type=row[3],
                payload=json.loads(row[4]),
                status=OutboxStatus(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                published_at=datetime.fromisoformat(row[7]) if row[7] else None,
                retry_count=row[8]
            ))
        
        conn.close()
        return messages
    
    def mark_as_published(self, message_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE outbox
            SET status = ?, published_at = ?
            WHERE id = ?
        """, (OutboxStatus.PUBLISHED.value, datetime.now().isoformat(), message_id))
        conn.commit()
        conn.close()
    
    def mark_as_failed(self, message_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE outbox
            SET status = ?, retry_count = retry_count + 1
            WHERE id = ?
        """, (OutboxStatus.FAILED.value, message_id))
        conn.commit()
        conn.close()
    
    def retry_failed(self, message_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE outbox
            SET status = ?
            WHERE id = ?
        """, (OutboxStatus.PENDING.value, message_id))
        conn.commit()
        conn.close()


class MessagePublisher:
    def publish(self, message: OutboxMessage) -> bool:
        # 实现实际的消息发布逻辑（Kafka, RabbitMQ, HTTP等）
        print(f"Publishing message: {message.event_type} for {message.aggregate_type}:{message.aggregate_id}")
        print(f"Payload: {message.payload}")
        return True


class OutboxProcessor:
    def __init__(
        self,
        outbox: Outbox,
        publisher: MessagePublisher,
        poll_interval: int = 5,
        batch_size: int = 100
    ):
        self.outbox = outbox
        self.publisher = publisher
        self.poll_interval = poll_interval
        self.batch_size = batch_size
        self._running = False
        self._thread = None
    
    def start(self):
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._process_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
    
    def _process_loop(self):
        while self._running:
            try:
                self._process_batch()
            except Exception as e:
                print(f"Error processing outbox: {e}")
            
            time.sleep(self.poll_interval)
    
    def _process_batch(self):
        messages = self.outbox.get_pending_messages(self.batch_size)
        
        for message in messages:
            try:
                success = self.publisher.publish(message)
                if success:
                    self.outbox.mark_as_published(message.id)
                else:
                    self.outbox.mark_as_failed(message.id)
            except Exception as e:
                print(f"Failed to publish message {message.id}: {e}")
                self.outbox.mark_as_failed(message.id)


# 使用示例
if __name__ == "__main__":
    # 初始化
    outbox = Outbox()
    publisher = MessagePublisher()
    processor = OutboxProcessor(outbox, publisher)
    
    # 启动处理器
    processor.start()
    
    # 模拟业务操作
    conn = sqlite3.connect("outbox.db")
    try:
        # 业务逻辑和outbox写入在同一事务中
        cursor = conn.cursor()
        # 执行业务操作...
        
        # 添加事件到outbox
        outbox.add(
            aggregate_type="Order",
            aggregate_id="order-123",
            event_type="OrderCreated",
            payload={"order_id": "order-123", "amount": 100.0},
            conn=conn
        )
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()
    
    # 保持运行
    time.sleep(10)
    processor.stop()