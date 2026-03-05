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
        self.queue = []
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread = None
        
    def add_message(self, message: Any, delay_seconds: float, 
                   callback: Optional[Callable] = None, 
                   message_id: str = "") -> str:
        """添加延迟消息"""
        execute_at = time.time() + delay_seconds
        
        if not message_id:
            message_id = f"msg_{int(time.time() * 1000000)}"
        
        delayed_msg = DelayedMessage(
            execute_at=execute_at,
            message=message,
            callback=callback,
            message_id=message_id
        )
        
        with self.lock:
            heapq.heappush(self.queue, delayed_msg)
        
        return message_id
    
    def add_message_at(self, message: Any, execute_time: datetime,
                      callback: Optional[Callable] = None,
                      message_id: str = "") -> str:
        """在指定时间执行消息"""
        delay = (execute_time - datetime.now()).total_seconds()
        return self.add_message(message, max(0, delay), callback, message_id)
    
    def cancel_message(self, message_id: str) -> bool:
        """取消消息"""
        with self.lock:
            for i, msg in enumerate(self.queue):
                if msg.message_id == message_id:
                    self.queue.pop(i)
                    heapq.heapify(self.queue)
                    return True
        return False
    
    def start(self):
        """启动处理线程"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """停止处理线程"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
    
    def _process_queue(self):
        """处理队列中的消息"""
        while self.running:
            current_time = time.time()
            
            with self.lock:
                if self.queue and self.queue[0].execute_at <= current_time:
                    delayed_msg = heapq.heappop(self.queue)
                else:
                    delayed_msg = None
            
            if delayed_msg:
                try:
                    if delayed_msg.callback:
                        delayed_msg.callback(delayed_msg.message)
                except Exception as e:
                    print(f"Error processing message {delayed_msg.message_id}: {e}")
            else:
                time.sleep(0.01)
    
    def size(self) -> int:
        """获取队列大小"""
        with self.lock:
            return len(self.queue)
    
    def clear(self):
        """清空队列"""
        with self.lock:
            self.queue.clear()


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
    future_time = datetime.now() + timedelta(seconds=4)
    queue.add_message_at("消息4 - 4秒后执行", future_time, print_message)
    
    # 取消消息
    msg_id = queue.add_message("消息5 - 将被取消", 5, print_message, "cancel_me")
    time.sleep(0.5)
    queue.cancel_message("cancel_me")
    print("已取消消息5")
    
    # 等待所有消息处理完成
    time.sleep(6)
    queue.stop()