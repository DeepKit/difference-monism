from abc import ABC, abstractmethod


# 抽象表达式类
class Expression(ABC):
    @abstractmethod
    def interpret(self, context):
        pass


# 终结符表达式 - 数字
class NumberExpression(Expression):
    def __init__(self, value):
        self.value = value
    
    def interpret(self, context):
        return self.value


# 终结符表达式 - 变量
class VariableExpression(Expression):
    def __init__(self, name):
        self.name = name
    
    def interpret(self, context):
        return context.get(self.name, 0)


# 非终结符表达式 - 加法
class AddExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        return self.left.interpret(context) + self.right.interpret(context)


# 非终结符表达式 - 减法
class SubtractExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        return self.left.interpret(context) - self.right.interpret(context)


# 非终结符表达式 - 乘法
class MultiplyExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        return self.left.interpret(context) * self.right.interpret(context)


# 非终结符表达式 - 除法
class DivideExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self, context):
        right_value = self.right.interpret(context)
        if right_value == 0:
            raise ValueError("除数不能为零")
        return self.left.interpret(context) / right_value


# 上下文类
class Context:
    def __init__(self):
        self.variables = {}
    
    def set(self, name, value):
        self.variables[name] = value
    
    def get(self, name, default=None):
        return self.variables.get(name, default)


# 解析器类
class Parser:
    @staticmethod
    def parse(expression_str):
        """简单的表达式解析器"""
        tokens = expression_str.replace('(', ' ( ').replace(')', ' ) ').split()
        return Parser._parse_tokens(tokens)
    
    @staticmethod
    def _parse_tokens(tokens):
        if not tokens:
            raise ValueError("空表达式")
        
        token = tokens.pop(0)
        
        if token == '(':
            left = Parser._parse_tokens(tokens)
            operator = tokens.pop(0)
            right = Parser._parse_tokens(tokens)
            tokens.pop(0)  # 移除 ')'
            
            if operator == '+':
                return AddExpression(left, right)
            elif operator == '-':
                return SubtractExpression(left, right)
            elif operator == '*':
                return MultiplyExpression(left, right)
            elif operator == '/':
                return DivideExpression(left, right)
            else:
                raise ValueError(f"未知操作符: {operator}")
        else:
            try:
                return NumberExpression(float(token))
            except ValueError:
                return VariableExpression(token)


# 使用示例
if __name__ == "__main__":
    # 创建上下文
    context = Context()
    context.set('x', 10)
    context.set('y', 5)
    
    # 示例1: 直接构建表达式树 (x + y) * 2
    expr1 = MultiplyExpression(
        AddExpression(
            VariableExpression('x'),
            VariableExpression('y')
        ),
        NumberExpression(2)
    )
    print(f"(x + y) * 2 = {expr1.interpret(context)}")  # 30
    
    # 示例2: 使用解析器
    expr2 = Parser.parse("(x + y)")
    print(f"x + y = {expr2.interpret(context)}")  # 15
    
    expr3 = Parser.parse("((x + y) * 2)")
    print(f"(x + y) * 2 = {expr3.interpret(context)}")  # 30
    
    expr4 = Parser.parse("((10 + 5) - 3)")
    print(f"(10 + 5) - 3 = {expr4.interpret(Context())}")  # 12
    
    # 示例3: 复杂表达式
    expr5 = Parser.parse("(((x * 2) + y) / 5)")
    print(f"((x * 2) + y) / 5 = {expr5.interpret(context)}")  # 5.0