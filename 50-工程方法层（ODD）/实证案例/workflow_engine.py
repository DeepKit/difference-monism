
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Optional
from enum import Enum
import copy


class NodeType(Enum):
    ACTION = "action"
    CONDITION = "condition"
    START = "start"
    END = "end"


class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Node(ABC):
    def __init__(self, node_id: str, name: str):
        self.node_id = node_id
        self.name = name
        self.status = NodeStatus.PENDING
        self.next_nodes: List[str] = []
        self.result: Any = None
        self.error: Optional[Exception] = None

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        pass

    def add_next(self, node_id: str):
        self.next_nodes.append(node_id)

    def reset(self):
        self.status = NodeStatus.PENDING
        self.result = None
        self.error = None


class StartNode(Node):
    def __init__(self, node_id: str = "start"):
        super().__init__(node_id, "Start")

    def execute(self, context: Dict[str, Any]) -> Any:
        self.status = NodeStatus.COMPLETED
        return True


class EndNode(Node):
    def __init__(self, node_id: str = "end"):
        super().__init__(node_id, "End")

    def execute(self, context: Dict[str, Any]) -> Any:
        self.status = NodeStatus.COMPLETED
        return context


class ActionNode(Node):
    def __init__(self, node_id: str, name: str, action: Callable[[Dict[str, Any]], Any]):
        super().__init__(node_id, name)
        self.action = action

    def execute(self, context: Dict[str, Any]) -> Any:
        try:
            self.status = NodeStatus.RUNNING
            self.result = self.action(context)
            self.status = NodeStatus.COMPLETED
            return self.result
        except Exception as e:
            self.status = NodeStatus.FAILED
            self.error = e
            raise


class ConditionNode(Node):
    def __init__(self, node_id: str, name: str, condition: Callable[[Dict[str, Any]], bool]):
        super().__init__(node_id, name)
        self.condition = condition
        self.true_branch: Optional[str] = None
        self.false_branch: Optional[str] = None

    def execute(self, context: Dict[str, Any]) -> bool:
        try:
            self.status = NodeStatus.RUNNING
            self.result = self.condition(context)
            self.status = NodeStatus.COMPLETED
            return self.result
        except Exception as e:
            self.status = NodeStatus.FAILED
            self.error = e
            raise

    def set_branches(self, true_branch: str, false_branch: str):
        self.true_branch = true_branch
        self.false_branch = false_branch

    def get_next_node(self) -> Optional[str]:
        if self.result:
            return self.true_branch
        return self.false_branch


class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.start_node: Optional[str] = None
        self.context: Dict[str, Any] = {}
        self.execution_history: List[str] = []

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node
        if isinstance(node, StartNode):
            self.start_node = node.node_id

    def connect(self, from_node_id: str, to_node_id: str):
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            raise ValueError(f"Node not found: {from_node_id} or {to_node_id}")
        self.nodes[from_node_id].add_next(to_node_id)

    def set_condition_branches(self, condition_node_id: str, true_branch: str, false_branch: str):
        node = self.nodes.get(condition_node_id)
        if not isinstance(node, ConditionNode):
            raise ValueError(f"Node {condition_node_id} is not a ConditionNode")
        node.set_branches(true_branch, false_branch)

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.start_node:
            raise ValueError("No start node defined")

        self.context = copy.deepcopy(initial_context) if initial_context else {}
        self.execution_history = []
        self._reset_nodes()

        current_node_id = self.start_node
        
        while current_node_id:
            if current_node_id not in self.nodes:
                raise ValueError(f"Node {current_node_id} not found")

            current_node = self.nodes[current_node_id]
            self.execution_history.append(current_node_id)

            try:
                current_node.execute(self.context)
            except Exception as e:
                raise RuntimeError(f"Node {current_node_id} failed: {str(e)}") from e

            if isinstance(current_node, EndNode):
                break

            current_node_id = self._get_next_node(current_node)

        return self.context

    def _get_next_node(self, node: Node) -> Optional[str]:
        if isinstance(node, ConditionNode):
            return node.get_next_node()
        elif node.next_nodes:
            return node.next_nodes[0]
        return None

    def _reset_nodes(self):
        for node in self.nodes.values():
            node.reset()

    def get_execution_history(self) -> List[str]:
        return self.execution_history.copy()

    def get_node_status(self, node_id: str) -> NodeStatus:
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        return self.nodes[node_id].status

    def visualize(self) -> str:
        lines = ["Workflow Structure:"]
        for node_id, node in self.nodes.items():
            node_type = type(node).__name__
            lines.append(f"  [{node_id}] {node.name} ({node_type})")
            if isinstance(node, ConditionNode):
                lines.append(f"    True -> {node.true_branch}")
                lines.append(f"    False -> {node.false_branch}")
            elif node.next_nodes:
                for next_node in node.next_nodes:
                    lines.append(f"    -> {next_node}")
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    engine = WorkflowEngine()

    engine.add_node(StartNode())
    
    engine.add_node(ActionNode(
        "input",
        "Get Input",
        lambda ctx: ctx.update({"value": ctx.get("input_value", 10)}) or ctx["value"]
    ))
    
    engine.add_node(ConditionNode(
        "check",
        "Check Value",
        lambda ctx: ctx.get("value", 0) > 5
    ))
    
    engine.add_node(ActionNode(
        "process_high",
        "Process High Value",
        lambda ctx: ctx.update({"result": ctx["value"] * 2, "path": "high"}) or ctx["result"]
    ))
    
    engine.add_node(ActionNode(
        "process_low",
        "Process Low Value",
        lambda ctx: ctx.update({"result": ctx["value"] + 10, "path": "low"}) or ctx["result"]
    ))
    
    engine.add_node(EndNode())

    engine.connect("start", "input")
    engine.connect("input", "check")
    engine.set_condition_branches("check", "process_high", "process_low")
    engine.connect("process_high", "end")
    engine.connect("process_low", "end")

    print(engine.visualize())
    print("\n" + "="*50 + "\n")

    result1 = engine.execute({"input_value": 8})
    print(f"Test 1 (value=8): {result1}")
    print(f"Execution path: {' -> '.join(engine.get_execution_history())}\n")

    result2 = engine.execute({"input_value": 3})
    print(f"Test 2 (value=3): {result2}")
    print(f"Execution path: {' -> '.join(engine.get_execution_history())}")
