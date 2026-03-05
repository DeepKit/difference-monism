
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid


class TaskType(Enum):
    INTERVAL = "interval"
    SCHEDULED = "scheduled"


@dataclass
class Task:
    id: str
    func: Callable
    task_type: TaskType
    interval: Optional[float] = None
    scheduled_time: Optional[datetime] = None
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    repeat: bool = True
    next_run: Optional[datetime] = None
    enabled: bool = True


class PeriodicTaskManager:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.RLock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def add_interval_task(
        self,
        func: Callable,
        interval: float,
        args: tuple = (),
        kwargs: Dict[str, Any] = None,
        repeat: bool = True,
        task_id: Optional[str] = None
    ) -> str:
        """添加间隔任务
        
        Args:
            func: 要执行的函数
            interval: 执行间隔（秒）
            args: 函数位置参数
            kwargs: 函数关键字参数
            repeat: 是否重复执行
            task_id: 任务ID，不提供则自动生成
            
        Returns:
            任务ID
        """
        if kwargs is None:
            kwargs = {}
            
        task_id = task_id or str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            func=func,
            task_type=TaskType.INTERVAL,
            interval=interval,
            args=args,
            kwargs=kwargs,
            repeat=repeat,
            next_run=datetime.now() + timedelta(seconds=interval)
        )
        
        with self._lock:
            self._tasks[task_id] = task
            
        return task_id

    def add_scheduled_task(
        self,
        func: Callable,
        scheduled_time: datetime,
        args: tuple = (),
        kwargs: Dict[str, Any] = None,
        repeat: bool = False,
        task_id: Optional[str] = None
    ) -> str:
        """添加定时任务
        
        Args:
            func: 要执行的函数
            scheduled_time: 执行时间
            args: 函数位置参数
            kwargs: 函数关键字参数
            repeat: 是否重复执行（每天同一时间）
            task_id: 任务ID，不提供则自动生成
            
        Returns:
            任务ID
        """
        if kwargs is None:
            kwargs = {}
            
        task_id = task_id or str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            func=func,
            task_type=TaskType.SCHEDULED,
            scheduled_time=scheduled_time,
            args=args,
            kwargs=kwargs,
            repeat=repeat,
            next_run=scheduled_time
        )
        
        with self._lock:
            self._tasks[task_id] = task
            
        return task_id

    def remove_task(self, task_id: str) -> bool:
        """移除任务"""
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def enable_task(self, task_id: str) -> bool:
        """启用任务"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].enabled = True
                return True
            return False

    def disable_task(self, task_id: str) -> bool:
        """禁用任务"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].enabled = False
                return True
            return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务信息"""
        with self._lock:
            return self._tasks.get(task_id)

    def list_tasks(self) -> Dict[str, Task]:
        """列出所有任务"""
        with self._lock:
            return self._tasks.copy()

    def start(self):
        """启动任务管理器"""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def stop(self, wait: bool = True):
        """停止任务管理器"""
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            self._stop_event.set()
        
        if wait and self._thread:
            self._thread.join()

    def _run_loop(self):
        """主循环"""
        while self._running:
            try:
                self._check_and_execute_tasks()
                self._stop_event.wait(0.1)
            except Exception as e:
                print(f"Error in task manager loop: {e}")

    def _check_and_execute_tasks(self):
        """检查并执行到期任务"""
        now = datetime.now()
        tasks_to_execute = []
        
        with self._lock:
            for task in self._tasks.values():
                if not task.enabled:
                    continue
                    
                if task.next_run and now >= task.next_run:
                    tasks_to_execute.append(task)
        
        for task in tasks_to_execute:
            self._execute_task(task)

    def _execute_task(self, task: Task):
        """执行任务"""
        def run():
            try:
                task.func(*task.args, **task.kwargs)
            except Exception as e:
                print(f"Error executing task {task.id}: {e}")
            finally:
                self._schedule_next_run(task)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def _schedule_next_run(self, task: Task):
        """安排下次执行时间"""
        with self._lock:
            if task.id not in self._tasks:
                return
            
            if not task.repeat:
                task.enabled = False
                task.next_run = None
                return
            
            if task.task_type == TaskType.INTERVAL:
                task.next_run = datetime.now() + timedelta(seconds=task.interval)
            elif task.task_type == TaskType.SCHEDULED:
                current_time = task.scheduled_time
                next_time = current_time + timedelta(days=1)
                while next_time <= datetime.now():
                    next_time += timedelta(days=1)
                task.next_run = next_time

    def is_running(self) -> bool:
        """检查管理器是否运行中"""
        return self._running

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


if __name__ == "__main__":
    def sample_task(name: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Task {name} executed")

    manager = PeriodicTaskManager()
    manager.start()
    
    manager.add_interval_task(sample_task, interval=2, args=("A",))
    manager.add_interval_task(sample_task, interval=3, args=("B",))
    
    scheduled_time = datetime.now() + timedelta(seconds=5)
    manager.add_scheduled_task(sample_task, scheduled_time, args=("C",))
    
    try:
        time.sleep(15)
    finally:
        manager.stop()
