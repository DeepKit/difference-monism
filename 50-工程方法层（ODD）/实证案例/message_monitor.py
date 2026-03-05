import time
import threading
from collections import deque
from datetime import datetime
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class MessageLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


@dataclass
class Message:
    content: str
    level: MessageLevel
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self):
        dt = datetime.fromtimestamp(self.timestamp)
        return f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] {self.level.name}: {self.content}"


class MessageMonitor:
    def __init__(self, max_history: int = 1000, rate_window: int = 60):
        self.max_history = max_history
        self.rate_window = rate_window
        self.messages: deque = deque(maxlen=max_history)
        self.callbacks: List[Callable[[Message], None]] = []
        self.filters: List[Callable[[Message], bool]] = []
        self.stats: Dict[str, int] = {level.name: 0 for level in MessageLevel}
        self.lock = threading.Lock()
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        
    def add_message(self, content: str, level: MessageLevel = MessageLevel.INFO, 
                    metadata: Optional[Dict[str, Any]] = None) -> Message:
        msg = Message(content, level, metadata=metadata or {})
        
        with self.lock:
            self.messages.append(msg)
            self.stats[level.name] += 1
            
        # 执行过滤和回调
        if all(f(msg) for f in self.filters):
            for callback in self.callbacks:
                try:
                    callback(msg)
                except Exception as e:
                    print(f"回调执行错误: {e}")
                    
        return msg
    
    def register_callback(self, callback: Callable[[Message], None]):
        self.callbacks.append(callback)
        
    def add_filter(self, filter_func: Callable[[Message], bool]):
        self.filters.append(filter_func)
        
    def get_messages(self, level: Optional[MessageLevel] = None, 
                     limit: Optional[int] = None) -> List[Message]:
        with self.lock:
            msgs = list(self.messages)
            
        if level:
            msgs = [m for m in msgs if m.level == level]
            
        if limit:
            msgs = msgs[-limit:]
            
        return msgs
    
    def get_rate(self, level: Optional[MessageLevel] = None) -> float:
        current_time = time.time()
        cutoff_time = current_time - self.rate_window
        
        with self.lock:
            recent_msgs = [m for m in self.messages if m.timestamp >= cutoff_time]
            
        if level:
            recent_msgs = [m for m in recent_msgs if m.level == level]
            
        return len(recent_msgs) / self.rate_window
    
    def get_statistics(self) -> Dict[str, Any]:
        with self.lock:
            total = sum(self.stats.values())
            return {
                'total_messages': total,
                'by_level': self.stats.copy(),
                'current_rate': self.get_rate(),
                'history_size': len(self.messages)
            }
    
    def clear(self):
        with self.lock:
            self.messages.clear()
            self.stats = {level.name: 0 for level in MessageLevel}
    
    def start_monitoring(self, interval: float = 1.0, 
                        alert_threshold: Optional[float] = None):
        if self.running:
            return
            
        self.running = True
        
        def monitor_loop():
            while self.running:
                rate = self.get_rate()
                if alert_threshold and rate > alert_threshold:
                    print(f"警告: 消息速率过高 ({rate:.2f} msg/s)")
                time.sleep(interval)
                
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_monitoring()


# 使用示例
if __name__ == "__main__":
    monitor = MessageMonitor(max_history=100, rate_window=10)
    
    # 注册回调
    def print_error(msg: Message):
        if msg.level in [MessageLevel.ERROR, MessageLevel.CRITICAL]:
            print(f"严重消息: {msg}")
    
    monitor.register_callback(print_error)
    
    # 添加消息
    monitor.add_message("系统启动", MessageLevel.INFO)
    monitor.add_message("配置加载完成", MessageLevel.INFO)
    monitor.add_message("连接超时", MessageLevel.WARNING)
    monitor.add_message("数据库连接失败", MessageLevel.ERROR)
    
    # 查询消息
    errors = monitor.get_messages(level=MessageLevel.ERROR)
    print(f"\n错误消息数量: {len(errors)}")
    
    # 统计信息
    stats = monitor.get_statistics()
    print(f"\n统计信息: {stats}")
    
    # 启动监控
    monitor.start_monitoring(interval=2.0, alert_threshold=10.0)
    
    # 模拟消息流
    for i in range(5):
        monitor.add_message(f"处理任务 {i}", MessageLevel.INFO)
        time.sleep(0.5)
    
    monitor.stop_monitoring()