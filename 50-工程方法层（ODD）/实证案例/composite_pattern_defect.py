from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    """组件抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def operation(self) -> str:
        """执行操作"""
        pass
    
    def add(self, component: 'Component') -> None:
        """添加子组件"""
        pass
    
    def remove(self, component: 'Component') -> None:
        """移除子组件"""
        pass
    
    def get_child(self, index: int) -> 'Component':
        """获取子组件"""
        pass


class Leaf(Component):
    """叶子节点"""
    
    def operation(self) -> str:
        return f"Leaf: {self.name}"


class Composite(Component):
    """组合节点"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Component] = []
    
    def operation(self) -> str:
        results = [f"Composite: {self.name}"]
        for child in self._children:
            results.append("  " + child.operation())
        return "\n".join(results)
    
    def add(self, component: Component) -> None:
        self._children.append(component)
    
    def remove(self, component: Component) -> None:
        self._children.remove(component)
    
    def get_child(self, index: int) -> Component:
        return self._children[index]


# 使用示例
if __name__ == "__main__":
    # 创建根节点
    root = Composite("root")
    
    # 创建分支
    branch1 = Composite("branch1")
    branch2 = Composite("branch2")
    
    # 创建叶子
    leaf1 = Leaf("leaf1")
    leaf2 = Leaf("leaf2")
    leaf3 = Leaf("leaf3")
    leaf4 = Leaf("leaf4")
    
    # 构建树结构
    root.add(branch1)
    root.add(branch2)
    root.add(leaf1)
    
    branch1.add(leaf2)
    branch1.add(leaf3)
    
    branch2.add(leaf4)
    
    # 执行操作
    print(root.operation())