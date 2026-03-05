import queue
import threading
from dataclasses import dataclass
from typing import Optional, Callable
import time


@dataclass
class Email:
    to: str
    subject: str
    body: str
    from_addr: str = "noreply@example.com"


class EmailQueue:
    def __init__(self, max_workers: int = 3):
        self.queue = queue.Queue()
        self.max_workers = max_workers
        self.workers = []
        self.running = False
        self.send_callback: Optional[Callable] = None
    
    def set_sender(self, callback: Callable[[Email], bool]):
        """设置邮件发送回调函数"""
        self.send_callback = callback
    
    def enqueue(self, email: Email):
        """添加邮件到队列"""
        self.queue.put(email)
    
    def start(self):
        """启动工作线程"""
        if self.running:
            return
        
        self.running = True
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop(self, wait: bool = True):
        """停止队列处理"""
        self.running = False
        if wait:
            for worker in self.workers:
                worker.join()
        self.workers.clear()
    
    def _worker(self):
        """工作线程处理邮件"""
        while self.running:
            try:
                email = self.queue.get(timeout=1)
                self._send_email(email)
                self.queue.task_done()
            except queue.Empty:
                continue
    
    def _send_email(self, email: Email):
        """发送邮件"""
        if self.send_callback:
            try:
                self.send_callback(email)
            except Exception as e:
                print(f"发送失败: {email.to} - {e}")
    
    def size(self) -> int:
        """返回队列大小"""
        return self.queue.qsize()
    
    def wait_completion(self):
        """等待所有邮件处理完成"""
        self.queue.join()


# 使用示例
if __name__ == "__main__":
    def mock_send(email: Email) -> bool:
        print(f"发送邮件到 {email.to}: {email.subject}")
        time.sleep(0.5)  # 模拟发送延迟
        return True
    
    eq = EmailQueue(max_workers=2)
    eq.set_sender(mock_send)
    eq.start()
    
    # 添加邮件
    for i in range(5):
        eq.enqueue(Email(
            to=f"user{i}@example.com",
            subject=f"测试邮件 {i}",
            body=f"这是第 {i} 封邮件"
        ))
    
    eq.wait_completion()
    eq.stop()