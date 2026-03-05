import queue
import threading
import time
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass, field
import uuid


class Priority(Enum):
    HIGH = 1
    NORMAL = 2
    LOW = 3


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(order=True)
class Task:
    priority: int = field(compare=True)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    retry_count: int = field(default=0, compare=False)
    max_retries: int = field(default=3, compare=False)
    timeout: Optional[float] = field(default=None, compare=False)
    result: Any = field(default=None, compare=False)
    error: Optional[str] = field(default=None, compare=False)


class TaskQueue:
    def __init__(self, num_workers: int = 1):
        self.task_queue = queue.PriorityQueue()
        self.tasks = {}
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        self.lock = threading.Lock()

    def add_task(self, func: Callable, args: tuple = (), kwargs: dict = None, priority: Priority = Priority.NORMAL, timeout: Optional[float] = None, max_retries: int = 3) -> str:
        if kwargs is None:
            kwargs = {}
        task = Task(priority=priority.value, func=func, args=args, kwargs=kwargs, timeout=timeout, max_retries=max_retries)
        with self.lock:
            self.tasks[task.task_id] = task
        self.task_queue.put(task)
        return task.task_id

    def get_task_status(self, task_id: str) -> Optional[dict]:
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                return {"task_id": task.task_id, "status": task.status.value, "retry_count": task.retry_count, "result": task.result, "error": task.error}
        return None

    def _execute_task(self, task: Task) -> bool:
        with self.lock:
            task.status = TaskStatus.RUNNING
        
        result_container = {"result": None, "error": None, "completed": False}
        
        def target():
            try:
                result_container["result"] = task.func(*task.args, **task.kwargs)
                result_container["completed"] = True
            except Exception as e:
                result_container["error"] = str(e)
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout=task.timeout)
        
        if thread.is_alive():
            with self.lock:
                task.error = f"Task timed out after {task.timeout} seconds"
                task.status = TaskStatus.FAILED
            return False
        
        if result_container["completed"]:
            with self.lock:
                task.result = result_container["result"]
                task.status = TaskStatus.COMPLETED
            return True
        else:
            with self.lock:
                task.error = result_container["error"] or "Unknown error"
                task.status = TaskStatus.FAILED
            return False

    def _worker(self):
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
            except queue.Empty:
                continue
            
            success = self._execute_task(task)
            
            if not success and task.retry_count < task.max_retries:
                with self.lock:
                    task.retry_count += 1
                    task.status = TaskStatus.PENDING
                self.task_queue.put(task)
            
            self.task_queue.task_done()

    def start(self):
        if self.running:
            return
        self.running = True
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def stop(self, wait: bool = True):
        self.running = False
        if wait:
            for worker in self.workers:
                worker.join()
        self.workers.clear()

    def wait_completion(self):
        self.task_queue.join()
