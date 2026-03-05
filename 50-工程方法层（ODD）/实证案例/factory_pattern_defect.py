from abc import ABC, abstractmethod


# 产品接口
class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


# 具体产品A
class ConcreteProductA(Product):
    def operation(self) -> str:
        return "产品A的操作结果"


# 具体产品B
class ConcreteProductB(Product):
    def operation(self) -> str:
        return "产品B的操作结果"


# 工厂接口
class Factory(ABC):
    @abstractmethod
    def create_product(self) -> Product:
        pass


# 具体工厂A
class ConcreteFactoryA(Factory):
    def create_product(self) -> Product:
        return ConcreteProductA()


# 具体工厂B
class ConcreteFactoryB(Factory):
    def create_product(self) -> Product:
        return ConcreteProductB()


# 使用示例
if __name__ == "__main__":
    # 创建工厂A并生产产品
    factory_a = ConcreteFactoryA()
    product_a = factory_a.create_product()
    print(product_a.operation())
    
    # 创建工厂B并生产产品
    factory_b = ConcreteFactoryB()
    product_b = factory_b.create_product()
    print(product_b.operation())