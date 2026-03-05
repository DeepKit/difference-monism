from abc import ABC, abstractmethod


# 抽象组件
class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


# 具体组件
class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"


# 装饰器基类
class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    def operation(self) -> str:
        return self._component.operation()


# 具体装饰器A
class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorA({self._component.operation()})"


# 具体装饰器B
class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorB({self._component.operation()})"


# 使用示例
if __name__ == "__main__":
    # 创建基础组件
    simple = ConcreteComponent()
    print(f"Simple: {simple.operation()}")
    
    # 用装饰器A包装
    decorator_a = ConcreteDecoratorA(simple)
    print(f"Decorated A: {decorator_a.operation()}")
    
    # 用装饰器B再包装
    decorator_b = ConcreteDecoratorB(decorator_a)
    print(f"Decorated B: {decorator_b.operation()}")