
import heapq
import time
import threading
from typing import Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(order=True)
class DelayedTask:
    """延迟任务"""
    execute_time: float = field(compare=True)
    task_id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)


class DelayQueue:
    """延迟队列"""
    
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._running = False
        self._worker_thread = None
        self._task_counter = 0
    
    def add_task(self, func: Callable, delay_seconds: float, 
                 *args, **kwargs) -> str:
        """添加延迟任务"""
        with self._lock:
            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{int(time.time() * 1000)}"
            execute_time = time.time() + delay_seconds
            
            task = DelayedTask(
                execute_time=execute_time,
                task_id=task_id,
                func=func,
                args=args,
                kwargs=kwargs
            )
            
            heapq.heappush(self._queue, task)
            self._condition.notify()
            
            return task_id
    
    def add_task_at(self, func: Callable, execute_at: datetime,
                    *args, **kwargs) -> str:
        """在指定时间执行任务"""
        delay = (execute_at - datetime.now()).total_seconds()
        return self.add_task(func, max(0, delay), *args, **kwargs)
    
    def start(self):
        """启动队列处理"""
        if self._running:
            return
        
        self._running = True
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()
    
    def stop(self):
        """停止队列处理"""
        with self._lock:
            self._running = False
            self._condition.notify()
        
        if self._worker_thread:
            self._worker_thread.join()
    
    def _process_queue(self):
        """处理队列中的任务"""
        while self._running:
            with self._condition:
                while self._running and (not self._queue or 
                                        self._queue[0].execute_time > time.time()):
                    if not self._queue:
                        self._condition.wait()
                    else:
                        wait_time = self._queue[0].execute_time - time.time()
                        if wait_time > 0:
                            self._condition.wait(timeout=wait_time)
                
                if not self._running:
                    break
                
                if self._queue and self._queue[0].execute_time <= time.time():
                    task = heapq.heappop(self._queue)
            
            try:
                task.func(*task.args, **task.kwargs)
            except Exception as e:
                print(f"任务 {task.task_id} 执行失败: {e}")
    
    def size(self) -> int:
        """获取队列大小"""
        with self._lock:
            return len(self._queue)
    
    def clear(self):
        """清空队列"""
        with self._lock:
            self._queue.clear()
            self._condition.notify()


# 使用示例
if __name__ == "__main__":
    def sample_task(name: str, value: int):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 执行任务: {name}, 值: {value}")
    
    queue = DelayQueue()
    queue.start()
    
    # 添加延迟任务
    queue.add_task(sample_task, 2, "任务1", 100)
    queue.add_task(sample_task, 1, "任务2", 200)
    queue.add_task(sample_task, 3, "任务3", 300)
    
    # 在指定时间执行
    future_time = datetime.now() + timedelta(seconds=5)
    queue.add_task_at(sample_task, future_time, "定时任务", 400)
    
    time.sleep(6)
    queue.stop()
