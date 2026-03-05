
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class TaskResult:
    status: TaskStatus
    output: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class WorkflowContext:
    data: Dict[str, Any] = field(default_factory=dict)
    task_results: Dict[str, TaskResult] = field(default_factory=dict)
    
    def set(self, key: str, value: Any):
        self.data[key] = value
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        return self.task_results.get(task_id)


class Task(ABC):
    def __init__(self, task_id: str, name: str = None):
        self.task_id = task_id
        self.name = name or task_id
        self.dependencies: List[str] = []
        self.next_tasks: List[str] = []
    
    @abstractmethod
    async def execute(self, context: WorkflowContext) -> TaskResult:
        pass
    
    def add_dependency(self, task_id: str):
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
    
    def add_next(self, task_id: str):
        if task_id not in self.next_tasks:
            self.next_tasks.append(task_id)


class FunctionTask(Task):
    def __init__(self, task_id: str, func: Callable, name: str = None):
        super().__init__(task_id, name)
        self.func = func
    
    async def execute(self, context: WorkflowContext) -> TaskResult:
        start_time = datetime.now()
        try:
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(context)
            else:
                result = self.func(context)
            
            return TaskResult(
                status=TaskStatus.COMPLETED,
                output=result,
                start_time=start_time,
                end_time=datetime.now()
            )
        except Exception as e:
            return TaskResult(
                status=TaskStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now()
            )


class ConditionalTask(Task):
    def __init__(self, task_id: str, condition: Callable[[WorkflowContext], bool], 
                 true_task: str, false_task: str = None, name: str = None):
        super().__init__(task_id, name)
        self.condition = condition
        self.true_task = true_task
        self.false_task = false_task
    
    async def execute(self, context: WorkflowContext) -> TaskResult:
        start_time = datetime.now()
        try:
            result = self.condition(context)
            next_task = self.true_task if result else self.false_task
            
            return TaskResult(
                status=TaskStatus.COMPLETED,
                output={"condition_result": result, "next_task": next_task},
                start_time=start_time,
                end_time=datetime.now()
            )
        except Exception as e:
            return TaskResult(
                status=TaskStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now()
            )


class ParallelTask(Task):
    def __init__(self, task_id: str, parallel_tasks: List[str], name: str = None):
        super().__init__(task_id, name)
        self.parallel_tasks = parallel_tasks
    
    async def execute(self, context: WorkflowContext) -> TaskResult:
        return TaskResult(
            status=TaskStatus.COMPLETED,
            output={"parallel_tasks": self.parallel_tasks},
            start_time=datetime.now(),
            end_time=datetime.now()
        )


class Workflow:
    def __init__(self, workflow_id: str, name: str = None):
        self.workflow_id = workflow_id
        self.name = name or workflow_id
        self.tasks: Dict[str, Task] = {}
        self.start_tasks: List[str] = []
        self.status = WorkflowStatus.CREATED
    
    def add_task(self, task: Task) -> 'Workflow':
        self.tasks[task.task_id] = task
        return self
    
    def set_start_task(self, task_id: str) -> 'Workflow':
        if task_id not in self.start_tasks:
            self.start_tasks.append(task_id)
        return self
    
    def connect(self, from_task_id: str, to_task_id: str) -> 'Workflow':
        if from_task_id in self.tasks and to_task_id in self.tasks:
            self.tasks[from_task_id].add_next(to_task_id)
            self.tasks[to_task_id].add_dependency(from_task_id)
        return self
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)


class WorkflowEngine:
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def execute(self, workflow: Workflow, initial_context: Dict[str, Any] = None) -> WorkflowContext:
        context = WorkflowContext(data=initial_context or {})
        workflow.status = WorkflowStatus.RUNNING
        
        try:
            completed_tasks = set()
            pending_tasks = set(workflow.start_tasks)
            
            while pending_tasks:
                ready_tasks = self._get_ready_tasks(workflow, pending_tasks, completed_tasks)
                
                if not ready_tasks:
                    break
                
                parallel_groups = self._group_parallel_tasks(workflow, ready_tasks)
                
                for group in parallel_groups:
                    if len(group) == 1:
                        task_id = group[0]
                        await self._execute_task(workflow, task_id, context, completed_tasks, pending_tasks)
                    else:
                        await self._execute_parallel_tasks(workflow, group, context, completed_tasks, pending_tasks)
            
            workflow.status = WorkflowStatus.COMPLETED
            return context
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            raise e
    
    def _get_ready_tasks(self, workflow: Workflow, pending: set, completed: set) -> List[str]:
        ready = []
        for task_id in pending:
            task = workflow.get_task(task_id)
            if task and all(dep in completed for dep in task.dependencies):
                ready.append(task_id)
        return ready
    
    def _group_parallel_tasks(self, workflow: Workflow, ready_tasks: List[str]) -> List[List[str]]:
        groups = []
        processed = set()
        
        for task_id in ready_tasks:
            if task_id in processed:
                continue
            
            task = workflow.get_task(task_id)
            if isinstance(task, ParallelTask):
                groups.append(task.parallel_tasks)
                processed.add(task_id)
                processed.update(task.parallel_tasks)
            else:
                groups.append([task_id])
                processed.add(task_id)
        
        return groups
    
    async def _execute_task(self, workflow: Workflow, task_id: str, context: WorkflowContext,
                           completed: set, pending: set):
        task = workflow.get_task(task_id)
        if not task:
            return
        
        result = await task.execute(context)
        context.task_results[task_id] = result
        
        if result.status == TaskStatus.COMPLETED:
            completed.add(task_id)
            pending.discard(task_id)
            
            if isinstance(task, ConditionalTask):
                next_task = result.output.get("next_task")
                if next_task:
                    pending.add(next_task)
            else:
                for next_task_id in task.next_tasks:
                    pending.add(next_task_id)
        elif result.status == TaskStatus.FAILED:
            raise Exception(f"Task {task_id} failed: {result.error}")
    
    async def _execute_parallel_tasks(self, workflow: Workflow, task_ids: List[str],
                                     context: WorkflowContext, completed: set, pending: set):
        tasks = []
        for task_id in task_ids:
            task = workflow.get_task(task_id)
            if task:
                tasks.append(self._execute_single_parallel_task(task, context))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for task_id, result in zip(task_ids, results):
            if isinstance(result, Exception):
                context.task_results[task_id] = TaskResult(
                    status=TaskStatus.FAILED,
                    error=str(result)
                )
                raise result
            else:
                context.task_results[task_id] = result
                completed.add(task_id)
                pending.discard(task_id)
                
                task = workflow.get_task(task_id)
                for next_task_id in task.next_tasks:
                    pending.add(next_task_id)
    
    async def _execute_single_parallel_task(self, task: Task, context: WorkflowContext) -> TaskResult:
        return await task.execute(context)
    
    def shutdown(self):
        self.executor.shutdown(wait=True)


class WorkflowBuilder:
    def __init__(self, workflow_id: str, name: str = None):
        self.workflow = Workflow(workflow_id, name)
    
    def add_function_task(self, task_id: str, func: Callable, name: str = None) -> 'WorkflowBuilder':
        task = FunctionTask(task_id, func, name)
        self.workflow.add_task(task)
        return self
    
    def add_conditional_task(self, task_id: str, condition: Callable, 
                           true_task: str, false_task: str = None, name: str = None) -> 'WorkflowBuilder':
        task = ConditionalTask(task_id, condition, true_task, false_task, name)
        self.workflow.add_task(task)
        return self
    
    def add_parallel_task(self, task_id: str, parallel_tasks: List[str], name: str = None) -> 'WorkflowBuilder':
        task = ParallelTask(task_id, parallel_tasks, name)
        self.workflow.add_task(task)
        return self
    
    def set_start(self, task_id: str) -> 'WorkflowBuilder':
        self.workflow.set_start_task(task_id)
        return self
    
    def connect(self, from_task: str, to_task: str) -> 'WorkflowBuilder':
        self.workflow.connect(from_task, to_task)
        return self
    
    def build(self) -> Workflow:
        return self.workflow
