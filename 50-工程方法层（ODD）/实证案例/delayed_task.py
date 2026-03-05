
import threading
import time
import heapq
from typing import Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(order=True)
class DelayedTask:
    execute_time: float = field(compare=True)
    task_id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    timeout: Optional[float] = field(default=None, compare=False)


class DelayedTaskQueue:
    def __init__(self):
        self._heap = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._running = False
        self._worker_thread = None
        self._task_counter = 0
        
    def start(self):
        with self._lock:
            if self._running:
                return
            self._running = True
            self._worker_thread = threading.Thread(target=self._worker, daemon=True)
            self._worker_thread.start()
    
    def stop(self):
        with self._lock:
            self._running = False
            self._condition.notify()
        if self._worker_thread:
            self._worker_thread.join()
    
    def add_task(self, func: Callable, delay: float = 0, timeout: Optional[float] = None, 
                 *args, **kwargs) -> str:
        with self._lock:
            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{time.time()}"
            execute_time = time.time() + delay
            
            task = DelayedTask(
                execute_time=execute_time,
                task_id=task_id,
                func=func,
                args=args,
                kwargs=kwargs,
                timeout=timeout
            )
            
            heapq.heappush(self._heap, task)
            self._condition.notify()
            return task_id
    
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            for i, task in enumerate(self._heap):
                if task.task_id == task_id:
                    self._heap.pop(i)
                    heapq.heapify(self._heap)
                    return True
            return False
    
    def size(self) -> int:
        with self._lock:
            return len(self._heap)
    
    def _worker(self):
        while True:
            with self._condition:
                while self._running and (not self._heap or self._heap[0].execute_time > time.time()):
                    if not self._heap:
                        self._condition.wait()
                    else:
                        wait_time = self._heap[0].execute_time - time.time()
                        if wait_time > 0:
                            self._condition.wait(timeout=wait_time)
                
                if not self._running:
                    break
                
                if self._heap and self._heap[0].execute_time <= time.time():
                    task = heapq.heappop(self._heap)
                else:
                    continue
            
            self._execute_task(task)
    
    def _execute_task(self, task: DelayedTask):
        def target():
            try:
                task.func(*task.args, **task.kwargs)
            except Exception as e:
                print(f"Task {task.task_id} failed: {e}")
        
        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        
        if task.timeout:
            thread.join(timeout=task.timeout)
            if thread.is_alive():
                print(f"Task {task.task_id} timed out after {task.timeout}s")


if __name__ == "__main__":
    def sample_task(name, duration=0):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Task {name} started")
        time.sleep(duration)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Task {name} completed")
    
    queue = DelayedTaskQueue()
    queue.start()
    
    queue.add_task(sample_task, delay=1, name="A", duration=0.5)
    queue.add_task(sample_task, delay=2, name="B", duration=0.5)
    queue.add_task(sample_task, delay=0.5, timeout=0.2, name="C (timeout)", duration=1)
    
    task_id = queue.add_task(sample_task, delay=5, name="D (cancelled)")
    queue.cancel_task(task_id)
    
    time.sleep(4)
    queue.stop()
