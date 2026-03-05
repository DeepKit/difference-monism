
from collections import defaultdict, deque
from enum import Enum
from typing import Dict, List, Set, Callable, Any, Optional


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    def __init__(self, task_id: str, func: Callable, *args, **kwargs):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.status = TaskStatus.PENDING
        self.result: Any = None
        self.error: Optional[Exception] = None
    
    def execute(self) -> Any:
        self.status = TaskStatus.RUNNING
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = TaskStatus.COMPLETED
            return self.result
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.error = e
            raise


class TaskDependencyManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.dependents: Dict[str, Set[str]] = defaultdict(set)
    
    def add_task(self, task_id: str, func: Callable, *args, **kwargs) -> None:
        if task_id in self.tasks:
            raise ValueError(f"任务 {task_id} 已存在")
        self.tasks[task_id] = Task(task_id, func, *args, **kwargs)
    
    def add_dependency(self, task_id: str, depends_on: str) -> None:
        if task_id not in self.tasks:
            raise ValueError(f"任务 {task_id} 不存在")
        if depends_on not in self.tasks:
            raise ValueError(f"依赖任务 {depends_on} 不存在")
        
        self.dependencies[task_id].add(depends_on)
        self.dependents[depends_on].add(task_id)
        
        if self._has_cycle():
            self.dependencies[task_id].remove(depends_on)
            self.dependents[depends_on].remove(task_id)
            raise ValueError(f"添加依赖会产生循环: {task_id} -> {depends_on}")
    
    def _has_cycle(self) -> bool:
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependencies.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for task_id in self.tasks:
            if task_id not in visited:
                if dfs(task_id):
                    return True
        return False
    
    def get_execution_order(self) -> List[str]:
        in_degree = {task_id: len(self.dependencies[task_id]) for task_id in self.tasks}
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        order = []
        
        while queue:
            task_id = queue.popleft()
            order.append(task_id)
            
            for dependent in self.dependents[task_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        if len(order) != len(self.tasks):
            raise ValueError("存在循环依赖")
        
        return order
    
    def execute_all(self) -> Dict[str, Any]:
        execution_order = self.get_execution_order()
        results = {}
        
        for task_id in execution_order:
            task = self.tasks[task_id]
            try:
                results[task_id] = task.execute()
            except Exception as e:
                results[task_id] = f"失败: {str(e)}"
                raise RuntimeError(f"任务 {task_id} 执行失败: {str(e)}")
        
        return results
    
    def get_task_status(self, task_id: str) -> TaskStatus:
        if task_id not in self.tasks:
            raise ValueError(f"任务 {task_id} 不存在")
        return self.tasks[task_id].status
    
    def get_all_status(self) -> Dict[str, TaskStatus]:
        return {task_id: task.status for task_id, task in self.tasks.items()}


# 使用示例
if __name__ == "__main__":
    manager = TaskDependencyManager()
    
    manager.add_task("task1", lambda: print("执行任务1") or "任务1完成")
    manager.add_task("task2", lambda: print("执行任务2") or "任务2完成")
    manager.add_task("task3", lambda: print("执行任务3") or "任务3完成")
    manager.add_task("task4", lambda: print("执行任务4") or "任务4完成")
    
    manager.add_dependency("task2", "task1")
    manager.add_dependency("task3", "task1")
    manager.add_dependency("task4", "task2")
    manager.add_dependency("task4", "task3")
    
    print("执行顺序:", manager.get_execution_order())
    results = manager.execute_all()
    print("执行结果:", results)
