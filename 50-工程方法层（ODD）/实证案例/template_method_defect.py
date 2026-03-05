from abc import ABC, abstractmethod


class AbstractClass(ABC):
    """模板方法抽象类"""
    
    def template_method(self):
        """模板方法 - 定义算法骨架"""
        self.base_operation1()
        self.required_operation1()
        self.base_operation2()
        self.required_operation2()
        self.hook()
    
    def base_operation1(self):
        """基础操作1 - 已实现"""
        print("AbstractClass: 执行基础操作1")
    
    def base_operation2(self):
        """基础操作2 - 已实现"""
        print("AbstractClass: 执行基础操作2")
    
    @abstractmethod
    def required_operation1(self):
        """必须实现的操作1"""
        pass
    
    @abstractmethod
    def required_operation2(self):
        """必须实现的操作2"""
        pass
    
    def hook(self):
        """钩子方法 - 可选覆盖"""
        pass


class ConcreteClass1(AbstractClass):
    """具体实现类1"""
    
    def required_operation1(self):
        print("ConcreteClass1: 实现必须操作1")
    
    def required_operation2(self):
        print("ConcreteClass1: 实现必须操作2")


class ConcreteClass2(AbstractClass):
    """具体实现类2"""
    
    def required_operation1(self):
        print("ConcreteClass2: 实现必须操作1")
    
    def required_operation2(self):
        print("ConcreteClass2: 实现必须操作2")
    
    def hook(self):
        """覆盖钩子方法"""
        print("ConcreteClass2: 覆盖钩子方法")


# 使用示例
if __name__ == "__main__":
    print("客户端: 使用ConcreteClass1")
    concrete1 = ConcreteClass1()
    concrete1.template_method()
    
    print("\n客户端: 使用ConcreteClass2")
    concrete2 = ConcreteClass2()
    concrete2.template_method()