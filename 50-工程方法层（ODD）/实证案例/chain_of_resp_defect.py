from abc import ABC, abstractmethod
from typing import Optional, Any


class Handler(ABC):
    """责任链处理器基类"""
    
    def __init__(self):
        self._next_handler: Optional[Handler] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """设置下一个处理器"""
        self._next_handler = handler
        return handler
    
    def handle(self, request: Any) -> Optional[str]:
        """处理请求"""
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class ConcreteHandlerA(Handler):
    """具体处理器A"""
    
    def handle(self, request: Any) -> Optional[str]:
        if request == "A":
            return f"HandlerA 处理了请求: {request}"
        return super().handle(request)


class ConcreteHandlerB(Handler):
    """具体处理器B"""
    
    def handle(self, request: Any) -> Optional[str]:
        if request == "B":
            return f"HandlerB 处理了请求: {request}"
        return super().handle(request)


class ConcreteHandlerC(Handler):
    """具体处理器C"""
    
    def handle(self, request: Any) -> Optional[str]:
        if request == "C":
            return f"HandlerC 处理了请求: {request}"
        return super().handle(request)


# 使用示例
if __name__ == "__main__":
    # 创建处理器
    handler_a = ConcreteHandlerA()
    handler_b = ConcreteHandlerB()
    handler_c = ConcreteHandlerC()
    
    # 构建责任链
    handler_a.set_next(handler_b).set_next(handler_c)
    
    # 测试
    requests = ["A", "B", "C", "D"]
    for req in requests:
        result = handler_a.handle(req)
        if result:
            print(result)
        else:
            print(f"请求 {req} 未被处理")