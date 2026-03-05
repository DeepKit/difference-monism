from abc import ABC, abstractmethod
from typing import List


# Element接口
class Element(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        pass


# 具体元素类
class Book(Element):
    def __init__(self, title: str, price: float):
        self.title = title
        self.price = price
    
    def accept(self, visitor: 'Visitor'):
        visitor.visit_book(self)


class Fruit(Element):
    def __init__(self, name: str, weight: float, price_per_kg: float):
        self.name = name
        self.weight = weight
        self.price_per_kg = price_per_kg
    
    def accept(self, visitor: 'Visitor'):
        visitor.visit_fruit(self)


class Electronics(Element):
    def __init__(self, name: str, price: float, warranty_years: int):
        self.name = name
        self.price = price
        self.warranty_years = warranty_years
    
    def accept(self, visitor: 'Visitor'):
        visitor.visit_electronics(self)


# Visitor接口
class Visitor(ABC):
    @abstractmethod
    def visit_book(self, book: Book):
        pass
    
    @abstractmethod
    def visit_fruit(self, fruit: Fruit):
        pass
    
    @abstractmethod
    def visit_electronics(self, electronics: Electronics):
        pass


# 具体访问者：计算价格
class PriceCalculator(Visitor):
    def __init__(self):
        self.total = 0
    
    def visit_book(self, book: Book):
        self.total += book.price
        print(f"书籍 '{book.title}': ¥{book.price}")
    
    def visit_fruit(self, fruit: Fruit):
        cost = fruit.weight * fruit.price_per_kg
        self.total += cost
        print(f"水果 '{fruit.name}': {fruit.weight}kg × ¥{fruit.price_per_kg}/kg = ¥{cost}")
    
    def visit_electronics(self, electronics: Electronics):
        self.total += electronics.price
        print(f"电子产品 '{electronics.name}': ¥{electronics.price}")


# 具体访问者：生成报告
class ReportGenerator(Visitor):
    def __init__(self):
        self.report = []
    
    def visit_book(self, book: Book):
        self.report.append(f"[图书] {book.title} - 价格: ¥{book.price}")
    
    def visit_fruit(self, fruit: Fruit):
        self.report.append(f"[水果] {fruit.name} - {fruit.weight}kg @ ¥{fruit.price_per_kg}/kg")
    
    def visit_electronics(self, electronics: Electronics):
        self.report.append(f"[电子] {electronics.name} - ¥{electronics.price} (保修{electronics.warranty_years}年)")
    
    def get_report(self):
        return "\n".join(self.report)


# 对象结构
class ShoppingCart:
    def __init__(self):
        self.items: List[Element] = []
    
    def add_item(self, item: Element):
        self.items.append(item)
    
    def accept(self, visitor: Visitor):
        for item in self.items:
            item.accept(visitor)


# 使用示例
if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item(Book("Python设计模式", 89.0))
    cart.add_item(Fruit("苹果", 2.5, 12.0))
    cart.add_item(Electronics("无线鼠标", 159.0, 2))
    cart.add_item(Book("算法导论", 128.0))
    
    print("=== 价格计算 ===")
    price_calc = PriceCalculator()
    cart.accept(price_calc)
    print(f"\n总计: ¥{price_calc.total}\n")
    
    print("=== 生成报告 ===")
    report_gen = ReportGenerator()
    cart.accept(report_gen)
    print(report_gen.get_report())