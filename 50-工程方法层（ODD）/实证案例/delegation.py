# delegate.py

class Printer:
    """委托类 - 实际执行打印操作"""
    def print_message(self, message):
        print(f"Printing: {message}")
    
    def print_formatted(self, message, prefix=">>>"):
        print(f"{prefix} {message}")


class Writer:
    """委托者类 - 将打印操作委托给Printer"""
    def __init__(self):
        self.printer = Printer()  # 持有委托对象
    
    def write(self, message):
        # 委托给printer对象处理
        self.printer.print_message(message)
    
    def write_formatted(self, message, prefix=">>>"):
        # 委托给printer对象处理
        self.printer.print_formatted(message, prefix)


# 更通用的委托模式实现
class Delegate:
    """通用委托基类"""
    def __init__(self, delegate):
        self._delegate = delegate
    
    def __getattr__(self, name):
        """动态委托属性和方法访问"""
        return getattr(self._delegate, name)


class Calculator:
    """实际计算类"""
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b


class MathOperations(Delegate):
    """委托给Calculator的数学操作类"""
    def __init__(self):
        super().__init__(Calculator())
    
    def power(self, base, exp):
        """自己的方法"""
        result = 1
        for _ in range(exp):
            result = self.multiply(result, base)  # 委托的方法
        return result


# 使用示例
if __name__ == "__main__":
    # 基本委托示例
    writer = Writer()
    writer.write("Hello World")
    writer.write_formatted("Important Message", prefix="[INFO]")
    
    print("\n" + "="*50 + "\n")
    
    # 通用委托示例
    math_ops = MathOperations()
    print(f"Add: {math_ops.add(5, 3)}")
    print(f"Multiply: {math_ops.multiply(4, 7)}")
    print(f"Power: {math_ops.power(2, 10)}")