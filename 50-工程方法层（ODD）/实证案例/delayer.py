import time
import heapq
import threading
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(order=True)
class DelayedMessage:
    execute_at: float = field(compare=True)
    message: Any = field(compare=False)
    callback: Optional[Callable] = field(default=None, compare=False)
    message_id: str = field(default="", compare=False)


class MessageDelayQueue:
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._worker_thread = None
        self._message_count = 0

    def add_message(
        self,
        message: Any,
        delay_seconds: float,
        callback: Optional[Callable] = None,
        message_id: Optional[str] = None,
    ) -> str:
        """添加延迟消息"""
        execute_at = time.time() + delay_seconds
        
        if message_id is None:
            self._message_count += 1
            message_id = f"msg_{self._message_count}"
        
        delayed_msg = DelayedMessage(
            execute_at=execute_at,
            message=message,
            callback=callback,
            message_id=message_id,
        )
        
        with self._lock:
            heapq.heappush(self._queue, delayed_msg)
        
        return message_id

    def add_message_at(
        self,
        message: Any,
        execute_at: datetime,
        callback: Optional[Callable] = None,
        message_id: Optional[str] = None,
    ) -> str:
        """在指定时间执行消息"""
        delay = (execute_at - datetime.now()).total_seconds()
        return self.add_message(message, max(0, delay), callback, message_id)

    def start(self):
        """启动处理线程"""
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._process_messages, daemon=True)
            self._worker_thread.start()

    def stop(self):
        """停止处理线程"""
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join()

    def _process_messages(self):
        """处理消息的工作线程"""
        while not self._stop_event.is_set():
            current_time = time.time()
            
            with self._lock:
                if self._queue and self._queue[0].execute_at <= current_time:
                    delayed_msg = heapq.heappop(self._queue)
                else:
                    delayed_msg = None
            
            if delayed_msg:
                try:
                    if delayed_msg.callback:
                        delayed_msg.callback(delayed_msg.message)
                except Exception as e:
                    print(f"Error processing message {delayed_msg.message_id}: {e}")
            else:
                time.sleep(0.1)

    def get_pending_count(self) -> int:
        """获取待处理消息数量"""
        with self._lock:
            return len(self._queue)

    def clear(self):
        """清空所有消息"""
        with self._lock:
            self._queue.clear()


# 使用示例
if __name__ == "__main__":
    def print_message(msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    # 创建延迟队列
    queue = MessageDelayQueue()
    queue.start()

    # 添加延迟消息
    queue.add_message("消息1 - 延迟1秒", 1, print_message)
    queue.add_message("消息2 - 延迟3秒", 3, print_message)
    queue.add_message("消息3 - 延迟2秒", 2, print_message)

    # 指定时间执行
    future_time = datetime.now() + timedelta(seconds=5)
    queue.add_message_at("消息4 - 5秒后执行", future_time, print_message)

    print(f"待处理消息数: {queue.get_pending_count()}")

    # 等待所有消息处理完成
    time.sleep(6)
    queue.stop()