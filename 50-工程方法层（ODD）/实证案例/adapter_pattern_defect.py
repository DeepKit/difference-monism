from abc import ABC, abstractmethod


# 目标接口
class Target(ABC):
    """客户端期望的接口"""
    
    @abstractmethod
    def request(self) -> str:
        pass


# 被适配者类
class Adaptee:
    """需要被适配的类，接口不兼容"""
    
    def specific_request(self) -> str:
        return "被适配者的特殊请求"


# 适配器类
class Adapter(Target):
    """将Adaptee的接口转换为Target接口"""
    
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee
    
    def request(self) -> str:
        return f"适配器: (转换) {self._adaptee.specific_request()}"


# 客户端代码
def client_code(target: Target) -> None:
    """客户端通过Target接口工作"""
    print(target.request())


# 使用示例
if __name__ == "__main__":
    print("客户端: 我可以直接使用Target对象:")
    target = Adapter(Adaptee())
    client_code(target)
    
    print("\n客户端: Adaptee类有不兼容的接口:")
    adaptee = Adaptee()
    print(f"Adaptee: {adaptee.specific_request()}")
    
    print("\n客户端: 但我可以通过适配器使用它:")
    adapter = Adapter(adaptee)
    client_code(adapter)