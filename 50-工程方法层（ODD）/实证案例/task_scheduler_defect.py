
import threading
import time
import heapq
from datetime import datetime, timedelta
from typing import Callable, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid


class TaskType(Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"


@dataclass(order=True)
class Task:
    next_run: float = field(compare=True)
    task_id: str = field(compare=False, default_factory=lambda: str(uuid.uuid4()))
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    task_type: TaskType = field(default=TaskType.ONE_TIME, compare=False)
    interval: Optional[float] = field(default=None, compare=False)
    name: Optional[str] = field(default=None, compare=False)


class TaskScheduler:
    def __init__(self):
        self._tasks = []
        self._task_map = {}
        self._lock = threading.RLock()
        self._running = False
        self._scheduler_thread = None
        self._condition = threading.Condition(self._lock)
        
    def start(self):
        with self._lock:
            if self._running:
                return
            self._running = True
            self._scheduler_thread = threading.Thread(target=self._run, daemon=True)
            self._scheduler_thread.start()
    
    def stop(self, wait=True):
        with self._lock:
            self._running = False
            self._condition.notify()
        
        if wait and self._scheduler_thread:
            self._scheduler_thread.join()
    
    def schedule_once(self, func: Callable, delay: float = 0, 
                     args: tuple = (), kwargs: dict = None, 
                     name: str = None) -> str:
        if kwargs is None:
            kwargs = {}
        
        next_run = time.time() + delay
        task = Task(
            next_run=next_run,
            func=func,
            args=args,
            kwargs=kwargs,
            task_type=TaskType.ONE_TIME,
            name=name
        )
        
        with self._lock:
            heapq.heappush(self._tasks, task)
            self._task_map[task.task_id] = task
            self._condition.notify()
        
        return task.task_id
    
    def schedule_at(self, func: Callable, run_time: datetime,
                   args: tuple = (), kwargs: dict = None,
                   name: str = None) -> str:
        if kwargs is None:
            kwargs = {}
        
        delay = (run_time - datetime.now()).total_seconds()
        if delay < 0:
            delay = 0
        
        return self.schedule_once(func, delay, args, kwargs, name)
    
    def schedule_recurring(self, func: Callable, interval: float,
                          initial_delay: float = 0,
                          args: tuple = (), kwargs: dict = None,
                          name: str = None) -> str:
        if kwargs is None:
            kwargs = {}
        
        next_run = time.time() + initial_delay
        task = Task(
            next_run=next_run,
            func=func,
            args=args,
            kwargs=kwargs,
            task_type=TaskType.RECURRING,
            interval=interval,
            name=name
        )
        
        with self._lock:
            heapq.heappush(self._tasks, task)
            self._task_map[task.task_id] = task
            self._condition.notify()
        
        return task.task_id
    
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._task_map:
                del self._task_map[task_id]
                return True
            return False
    
    def get_pending_tasks(self):
        with self._lock:
            return [
                {
                    'id': task.task_id,
                    'name': task.name,
                    'next_run': datetime.fromtimestamp(task.next_run),
                    'type': task.task_type.value
                }
                for task in self._tasks if task.task_id in self._task_map
            ]
    
    def _run(self):
        while self._running:
            with self._condition:
                while self._running and (not self._tasks or 
                      self._tasks[0].task_id not in self._task_map):
                    if self._tasks and self._tasks[0].task_id not in self._task_map:
                        heapq.heappop(self._tasks)
                    else:
                        self._condition.wait(timeout=1)
                
                if not self._running:
                    break
                
                if not self._tasks:
                    continue
                
                task = self._tasks[0]
                now = time.time()
                
                if task.next_run <= now:
                    heapq.heappop(self._tasks)
                    
                    if task.task_id in self._task_map:
                        threading.Thread(
                            target=self._execute_task,
                            args=(task,),
                            daemon=True
                        ).start()
                        
                        if task.task_type == TaskType.RECURRING:
                            task.next_run = now + task.interval
                            heapq.heappush(self._tasks, task)
                        else:
                            del self._task_map[task.task_id]
                else:
                    wait_time = task.next_run - now
                    self._condition.wait(timeout=wait_time)
    
    def _execute_task(self, task: Task):
        try:
            task.func(*task.args, **task.kwargs)
        except Exception as e:
            print(f"任务执行失败 [{task.name or task.task_id}]: {e}")


if __name__ == "__main__":
    def sample_task(message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    scheduler = TaskScheduler()
    scheduler.start()
    
    scheduler.schedule_once(sample_task, delay=1, args=("一次性任务执行",))
    scheduler.schedule_recurring(sample_task, interval=3, args=("周期性任务执行",))
    
    run_time = datetime.now() + timedelta(seconds=5)
    scheduler.schedule_at(sample_task, run_time, args=("定时任务执行",))
    
    time.sleep(15)
    scheduler.stop()
