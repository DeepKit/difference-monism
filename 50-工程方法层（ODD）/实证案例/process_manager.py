from enum import Enum
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
import traceback


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class Task:
    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 0


@dataclass
class WorkflowResult:
    status: WorkflowStatus
    tasks: Dict[str, Task]
    start_time: datetime
    end_time: Optional[datetime]
    error: Optional[str] = None


class WorkflowManager:
    def __init__(self, name: str = "workflow", log_level: int = logging.INFO):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.status = WorkflowStatus.IDLE
        self.logger = logging.getLogger(f"WorkflowManager.{name}")
        self.logger.setLevel(log_level)
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.context: Dict[str, Any] = {}
        
    def add_task(
        self,
        name: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        dependencies: List[str] = None,
        max_retries: int = 0
    ) -> 'WorkflowManager':
        if name in self.tasks:
            raise ValueError(f"Task '{name}' already exists")
        
        self.tasks[name] = Task(
            name=name,
            func=func,
            args=args,
            kwargs=kwargs or {},
            dependencies=dependencies or [],
            max_retries=max_retries
        )
        return self
    
    def _validate_dependencies(self) -> None:
        for task_name, task in self.tasks.items():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    raise ValueError(f"Task '{task_name}' depends on non-existent task '{dep}'")
        
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_name: str) -> bool:
            visited.add(task_name)
            rec_stack.add(task_name)
            
            for dep in self.tasks[task_name].dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(task_name)
            return False
        
        for task_name in self.tasks:
            if task_name not in visited:
                if has_cycle(task_name):
                    raise ValueError("Circular dependency detected")
    
    def _can_execute(self, task: Task) -> bool:
        if task.status != TaskStatus.PENDING:
            return False
        
        for dep_name in task.dependencies:
            dep_task = self.tasks[dep_name]
            if dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def _execute_task(self, task: Task) -> None:
        task.status = TaskStatus.RUNNING
        task.start_time = datetime.now()
        self.logger.info(f"Executing task: {task.name}")
        
        try:
            task.result = task.func(*task.args, **task.kwargs)
            task.status = TaskStatus.COMPLETED
            task.end_time = datetime.now()
            self.logger.info(f"Task completed: {task.name}")
            
        except Exception as e:
            task.error = traceback.format_exc()
            self.logger.error(f"Task failed: {task.name}\n{task.error}")
            
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                self.logger.info(f"Retrying task: {task.name} (attempt {task.retry_count}/{task.max_retries})")
            else:
                task.status = TaskStatus.FAILED
                task.end_time = datetime.now()
                raise
    
    def execute(self, fail_fast: bool = True) -> WorkflowResult:
        self.logger.info(f"Starting workflow: {self.name}")
        self.status = WorkflowStatus.RUNNING
        self.start_time = datetime.now()
        
        try:
            self._validate_dependencies()
            
            while True:
                executable_tasks = [
                    task for task in self.tasks.values()
                    if self._can_execute(task)
                ]
                
                if not executable_tasks:
                    pending_tasks = [
                        task for task in self.tasks.values()
                        if task.status == TaskStatus.PENDING
                    ]
                    if pending_tasks:
                        raise RuntimeError("Workflow stuck: tasks pending but none executable")
                    break
                
                for task in executable_tasks:
                    try:
                        self._execute_task(task)
                    except Exception:
                        if fail_fast:
                            raise
            
            failed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
            if failed_tasks:
                self.status = WorkflowStatus.FAILED
                error_msg = f"Workflow failed: {len(failed_tasks)} task(s) failed"
                self.logger.error(error_msg)
            else:
                self.status = WorkflowStatus.COMPLETED
                self.logger.info(f"Workflow completed: {self.name}")
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow error: {str(e)}")
            raise
        
        finally:
            self.end_time = datetime.now()
        
        return WorkflowResult(
            status=self.status,
            tasks=self.tasks.copy(),
            start_time=self.start_time,
            end_time=self.end_time,
            error=None if self.status == WorkflowStatus.COMPLETED else "Workflow failed"
        )
    
    def reset(self) -> None:
        for task in self.tasks.values():
            task.status = TaskStatus.PENDING
            task.result = None
            task.error = None
            task.start_time = None
            task.end_time = None
            task.retry_count = 0
        
        self.status = WorkflowStatus.IDLE
        self.start_time = None
        self.end_time = None
        self.context.clear()
    
    def get_task_result(self, task_name: str) -> Any:
        if task_name not in self.tasks:
            raise ValueError(f"Task '{task_name}' not found")
        return self.tasks[task_name].result
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "total_tasks": len(self.tasks),
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None
        }


# 使用示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    def task1():
        print("Task 1 executing")
        return "result1"
    
    def task2(data):
        print(f"Task 2 executing with {data}")
        return "result2"
    
    def task3(x, y):
        print(f"Task 3: {x} + {y}")
        return x + y
    
    workflow = WorkflowManager("example_workflow")
    workflow.add_task("task1", task1)
    workflow.add_task("task2", task2, args=("data",), dependencies=["task1"])
    workflow.add_task("task3", task3, kwargs={"x": 10, "y": 20}, dependencies=["task1", "task2"])
    
    result = workflow.execute()
    print(workflow.get_summary())