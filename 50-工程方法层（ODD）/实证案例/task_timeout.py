
import threading
import time
from typing import Callable, Optional, Any, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    task_id: str
    timeout: float
    callback: Callable
    start_time: float
    timer: Optional[threading.Timer] = None
    data: Any = None


class TaskTimeoutHandler:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()
    
    def register_task(
        self,
        task_id: str,
        timeout: float,
        callback: Callable[[str, Any], None],
        data: Any = None
    ) -> None:
        with self._lock:
            if task_id in self._tasks:
                self.cancel_task(task_id)
            
            task = Task(
                task_id=task_id,
                timeout=timeout,
                callback=callback,
                start_time=time.time(),
                data=data
            )
            
            timer = threading.Timer(timeout, self._handle_timeout, args=[task_id])
            task.timer = timer
            self._tasks[task_id] = task
            timer.start()
    
    def _handle_timeout(self, task_id: str) -> None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                try:
                    task.callback(task_id, task.data)
                except Exception as e:
                    print(f"Error in timeout callback for task {task_id}: {e}")
                finally:
                    del self._tasks[task_id]
    
    def complete_task(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                if task.timer:
                    task.timer.cancel()
                del self._tasks[task_id]
                return True
            return False
    
    def cancel_task(self, task_id: str) -> bool:
        return self.complete_task(task_id)
    
    def get_remaining_time(self, task_id: str) -> Optional[float]:
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                elapsed = time.time() - task.start_time
                remaining = task.timeout - elapsed
                return max(0, remaining)
            return None
    
    def is_task_active(self, task_id: str) -> bool:
        with self._lock:
            return task_id in self._tasks
    
    def get_active_tasks(self) -> list[str]:
        with self._lock:
            return list(self._tasks.keys())
    
    def clear_all(self) -> None:
        with self._lock:
            for task in self._tasks.values():
                if task.timer:
                    task.timer.cancel()
            self._tasks.clear()


if __name__ == "__main__":
    def timeout_callback(task_id: str, data: Any):
        print(f"Task {task_id} timed out! Data: {data}")
    
    handler = TaskTimeoutHandler()
    
    handler.register_task("task1", 2.0, timeout_callback, data="Important task")
    handler.register_task("task2", 5.0, timeout_callback, data="Another task")
    
    time.sleep(1)
    print(f"Task1 remaining: {handler.get_remaining_time('task1'):.2f}s")
    
    handler.complete_task("task2")
    print(f"Task2 active: {handler.is_task_active('task2')}")
    
    time.sleep(2)
    print(f"Active tasks: {handler.get_active_tasks()}")
    
    time.sleep(1)
