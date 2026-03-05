
from collections import defaultdict, deque
from typing import List, Set, Dict, Optional


class TaskDependencyManager:
    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)
        self.tasks: Set[str] = set()
    
    def add_task(self, task: str) -> None:
        self.tasks.add(task)
        if task not in self.graph:
            self.graph[task] = set()
        if task not in self.reverse_graph:
            self.reverse_graph[task] = set()
    
    def add_dependency(self, task: str, depends_on: str) -> bool:
        self.add_task(task)
        self.add_task(depends_on)
        
        if self._would_create_cycle(task, depends_on):
            return False
        
        self.graph[depends_on].add(task)
        self.reverse_graph[task].add(depends_on)
        return True
    
    def remove_dependency(self, task: str, depends_on: str) -> None:
        if depends_on in self.graph:
            self.graph[depends_on].discard(task)
        if task in self.reverse_graph:
            self.reverse_graph[task].discard(depends_on)
    
    def remove_task(self, task: str) -> None:
        if task not in self.tasks:
            return
        
        self.tasks.discard(task)
        
        for dependent in self.graph.get(task, set()).copy():
            self.reverse_graph[dependent].discard(task)
        
        for dependency in self.reverse_graph.get(task, set()).copy():
            self.graph[dependency].discard(task)
        
        del self.graph[task]
        del self.reverse_graph[task]
    
    def get_dependencies(self, task: str) -> Set[str]:
        return self.reverse_graph.get(task, set()).copy()
    
    def get_dependents(self, task: str) -> Set[str]:
        return self.graph.get(task, set()).copy()
    
    def _would_create_cycle(self, task: str, depends_on: str) -> bool:
        if task == depends_on:
            return True
        
        visited = set()
        stack = [depends_on]
        
        while stack:
            current = stack.pop()
            if current == task:
                return True
            
            if current in visited:
                continue
            
            visited.add(current)
            stack.extend(self.reverse_graph.get(current, set()))
        
        return False
    
    def has_cycle(self) -> bool:
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for task in self.tasks:
            if task not in visited:
                if dfs(task):
                    return True
        
        return False
    
    def topological_sort(self) -> Optional[List[str]]:
        in_degree = {task: len(self.reverse_graph.get(task, set())) for task in self.tasks}
        
        queue = deque([task for task in self.tasks if in_degree[task] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for dependent in self.graph.get(current, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        if len(result) != len(self.tasks):
            return None
        
        return result
    
    def get_execution_order(self) -> Optional[List[str]]:
        return self.topological_sort()
    
    def get_all_dependencies(self, task: str) -> Set[str]:
        if task not in self.tasks:
            return set()
        
        all_deps = set()
        stack = [task]
        
        while stack:
            current = stack.pop()
            for dep in self.reverse_graph.get(current, set()):
                if dep not in all_deps:
                    all_deps.add(dep)
                    stack.append(dep)
        
        return all_deps
    
    def get_all_dependents(self, task: str) -> Set[str]:
        if task not in self.tasks:
            return set()
        
        all_deps = set()
        stack = [task]
        
        while stack:
            current = stack.pop()
            for dep in self.graph.get(current, set()):
                if dep not in all_deps:
                    all_deps.add(dep)
                    stack.append(dep)
        
        return all_deps
    
    def get_ready_tasks(self, completed: Set[str]) -> Set[str]:
        ready = set()
        for task in self.tasks:
            if task not in completed:
                deps = self.get_dependencies(task)
                if deps.issubset(completed):
                    ready.add(task)
        return ready
    
    def __repr__(self) -> str:
        return f"TaskDependencyManager(tasks={len(self.tasks)}, dependencies={sum(len(deps) for deps in self.reverse_graph.values())})"
