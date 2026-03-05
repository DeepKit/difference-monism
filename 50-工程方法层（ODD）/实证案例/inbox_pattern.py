from typing import Any, Callable, Optional, List
from queue import Queue, Empty
from threading import Thread, Lock
from dataclasses import dataclass
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Message:
    """消息类"""
    id: str
    content: Any
    timestamp: datetime
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Inbox:
    """收件箱模式实现"""
    
    def __init__(self, max_size: int = 0):
        self._queue = Queue(maxsize=max_size)
        self._handlers: List[Callable] = []
        self._lock = Lock()
        self._running = False
        self._worker_thread: Optional[Thread] = None
        self._message_count = 0
        
    def send(self, content: Any, metadata: dict = None) -> Message:
        """发送消息到收件箱"""
        with self._lock:
            self._message_count += 1
            message = Message(
                id=f"msg_{self._message_count}",
                content=content,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
        self._queue.put(message)
        return message
    
    def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        """接收一条消息"""
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None
    
    def register_handler(self, handler: Callable[[Message], None]):
        """注册消息处理器"""
        with self._lock:
            self._handlers.append(handler)
    
    def start(self):
        """启动消息处理循环"""
        if self._running:
            return
        
        self._running = True
        self._worker_thread = Thread(target=self._process_loop, daemon=True)
        self._worker_thread.start()
    
    def stop(self):
        """停止消息处理循环"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
    
    def _process_loop(self):
        """消息处理循环"""
        while self._running:
            message = self.receive(timeout=0.1)
            if message:
                self._process_message(message)
    
    def _process_message(self, message: Message):
        """处理单条消息"""
        for handler in self._handlers:
            try:
                handler(message)
            except Exception as e:
                print(f"Handler error: {e}")
    
    def size(self) -> int:
        """获取队列大小"""
        return self._queue.qsize()
    
    def is_empty(self) -> bool:
        """检查是否为空"""
        return self._queue.empty()
    
    def clear(self):
        """清空收件箱"""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except Empty:
                break


class AsyncInbox:
    """异步收件箱实现"""
    
    def __init__(self, max_size: int = 0):
        self._queue = asyncio.Queue(maxsize=max_size)
        self._handlers: List[Callable] = []
        self._lock = asyncio.Lock()
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._message_count = 0
    
    async def send(self, content: Any, metadata: dict = None) -> Message:
        """发送消息"""
        async with self._lock:
            self._message_count += 1
            message = Message(
                id=f"msg_{self._message_count}",
                content=content,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
        await self._queue.put(message)
        return message
    
    async def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        """接收消息"""
        try:
            if timeout:
                return await asyncio.wait_for(self._queue.get(), timeout=timeout)
            return await self._queue.get()
        except asyncio.TimeoutError:
            return None
    
    def register_handler(self, handler: Callable):
        """注册处理器"""
        self._handlers.append(handler)
    
    async def start(self):
        """启动处理循环"""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._process_loop())
    
    async def stop(self):
        """停止处理循环"""
        self._running = False
        if self._task:
            await self._task
    
    async def _process_loop(self):
        """处理循环"""
        while self._running:
            try:
                message = await asyncio.wait_for(self._queue.get(), timeout=0.1)
                await self._process_message(message)
            except asyncio.TimeoutError:
                continue
    
    async def _process_message(self, message: Message):
        """处理消息"""
        for handler in self._handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(message)
                else:
                    handler(message)
            except Exception as e:
                print(f"Handler error: {e}")
    
    def size(self) -> int:
        """队列大小"""
        return self._queue.qsize()
    
    def is_empty(self) -> bool:
        """是否为空"""
        return self._queue.empty()


# 使用示例
if __name__ == "__main__":
    # 同步版本
    inbox = Inbox()
    
    def handler(msg: Message):
        print(f"处理消息: {msg.id} - {msg.content}")
    
    inbox.register_handler(handler)
    inbox.start()
    
    inbox.send("Hello")
    inbox.send("World")
    
    import time
    time.sleep(1)
    inbox.stop()
    
    # 异步版本
    async def async_example():
        async_inbox = AsyncInbox()
        
        async def async_handler(msg: Message):
            print(f"异步处理: {msg.id} - {msg.content}")
        
        async_inbox.register_handler(async_handler)
        await async_inbox.start()
        
        await async_inbox.send("Async Hello")
        await async_inbox.send("Async World")
        
        await asyncio.sleep(1)
        await async_inbox.stop()
    
    asyncio.run(async_example())