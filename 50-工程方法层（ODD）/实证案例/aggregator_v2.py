from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Lock, Timer
from collections import defaultdict
import time


@dataclass
class Message:
    """消息数据类"""
    id: str
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class MessageAggregator:
    """消息聚合器"""
    
    def __init__(
        self,
        max_batch_size: int = 100,
        max_wait_time: float = 5.0,
        on_batch_ready: Optional[Callable[[List[Message]], None]] = None
    ):
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.on_batch_ready = on_batch_ready
        
        self._messages: List[Message] = []
        self._lock = Lock()
        self._timer: Optional[Timer] = None
        self._is_running = True
        
    def add_message(self, message: Message) -> None:
        """添加消息到聚合器"""
        with self._lock:
            if not self._is_running:
                return
                
            self._messages.append(message)
            
            # 启动定时器（如果还没启动）
            if self._timer is None and self.max_wait_time > 0:
                self._timer = Timer(self.max_wait_time, self._flush_by_timer)
                self._timer.start()
            
            # 检查是否达到批次大小
            if len(self._messages) >= self.max_batch_size:
                self._flush()
    
    def _flush(self) -> None:
        """刷新消息批次"""
        if not self._messages:
            return
            
        # 取消定时器
        if self._timer:
            self._timer.cancel()
            self._timer = None
        
        # 获取当前批次
        batch = self._messages.copy()
        self._messages.clear()
        
        # 处理批次
        if self.on_batch_ready:
            self.on_batch_ready(batch)
    
    def _flush_by_timer(self) -> None:
        """定时器触发的刷新"""
        with self._lock:
            self._timer = None
            self._flush()
    
    def flush(self) -> None:
        """手动刷新所有待处理消息"""
        with self._lock:
            self._flush()
    
    def stop(self) -> None:
        """停止聚合器"""
        with self._lock:
            self._is_running = False
            self._flush()
    
    def get_pending_count(self) -> int:
        """获取待处理消息数量"""
        with self._lock:
            return len(self._messages)


class GroupedMessageAggregator:
    """分组消息聚合器"""
    
    def __init__(
        self,
        max_batch_size: int = 100,
        max_wait_time: float = 5.0,
        on_batch_ready: Optional[Callable[[str, List[Message]], None]] = None
    ):
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.on_batch_ready = on_batch_ready
        
        self._groups: Dict[str, List[Message]] = defaultdict(list)
        self._timers: Dict[str, Timer] = {}
        self._lock = Lock()
        self._is_running = True
    
    def add_message(self, group_key: str, message: Message) -> None:
        """添加消息到指定分组"""
        with self._lock:
            if not self._is_running:
                return
            
            self._groups[group_key].append(message)
            
            # 启动该分组的定时器
            if group_key not in self._timers and self.max_wait_time > 0:
                timer = Timer(
                    self.max_wait_time,
                    lambda: self._flush_group_by_timer(group_key)
                )
                self._timers[group_key] = timer
                timer.start()
            
            # 检查是否达到批次大小
            if len(self._groups[group_key]) >= self.max_batch_size:
                self._flush_group(group_key)
    
    def _flush_group(self, group_key: str) -> None:
        """刷新指定分组的消息"""
        if group_key not in self._groups or not self._groups[group_key]:
            return
        
        # 取消定时器
        if group_key in self._timers:
            self._timers[group_key].cancel()
            del self._timers[group_key]
        
        # 获取批次
        batch = self._groups[group_key].copy()
        self._groups[group_key].clear()
        
        # 处理批次
        if self.on_batch_ready:
            self.on_batch_ready(group_key, batch)
    
    def _flush_group_by_timer(self, group_key: str) -> None:
        """定时器触发的分组刷新"""
        with self._lock:
            if group_key in self._timers:
                del self._timers[group_key]
            self._flush_group(group_key)
    
    def flush_group(self, group_key: str) -> None:
        """手动刷新指定分组"""
        with self._lock:
            self._flush_group(group_key)
    
    def flush_all(self) -> None:
        """手动刷新所有分组"""
        with self._lock:
            for group_key in list(self._groups.keys()):
                self._flush_group(group_key)
    
    def stop(self) -> None:
        """停止聚合器"""
        with self._lock:
            self._is_running = False
            self.flush_all()
    
    def get_group_count(self, group_key: str) -> int:
        """获取指定分组的待处理消息数量"""
        with self._lock:
            return len(self._groups.get(group_key, []))


# 使用示例
if __name__ == "__main__":
    # 简单聚合器示例
    def handle_batch(messages: List[Message]):
        print(f"处理批次: {len(messages)} 条消息")
        for msg in messages:
            print(f"  - {msg.id}: {msg.content}")
    
    aggregator = MessageAggregator(
        max_batch_size=3,
        max_wait_time=2.0,
        on_batch_ready=handle_batch
    )
    
    # 添加消息
    for i in range(5):
        msg = Message(id=f"msg_{i}", content=f"内容 {i}")
        aggregator.add_message(msg)
        time.sleep(0.5)
    
    aggregator.flush()
    aggregator.stop()
    
    print("\n" + "="*50 + "\n")
    
    # 分组聚合器示例
    def handle_grouped_batch(group_key: str, messages: List[Message]):
        print(f"处理分组 [{group_key}]: {len(messages)} 条消息")
    
    grouped_aggregator = GroupedMessageAggregator(
        max_batch_size=2,
        max_wait_time=2.0,
        on_batch_ready=handle_grouped_batch
    )
    
    # 添加分组消息
    for i in range(6):
        group = "group_A" if i % 2 == 0 else "group_B"
        msg = Message(id=f"msg_{i}", content=f"内容 {i}", source=group)
        grouped_aggregator.add_message(group, msg)
        time.sleep(0.3)
    
    grouped_aggregator.flush_all()
    grouped_aggregator.stop()