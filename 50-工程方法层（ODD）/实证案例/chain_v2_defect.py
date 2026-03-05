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
    """具体处理器A - 处理0-10的请求"""
    
    def handle(self, request: Any) -> Optional[str]:
        if isinstance(request, int) and 0 <= request < 10:
            return f"HandlerA 处理了请求: {request}"
        return super().handle(request)


class ConcreteHandlerB(Handler):
    """具体处理器B - 处理10-20的请求"""
    
    def handle(self, request: Any) -> Optional[str]:
        if isinstance(request, int) and 10 <= request < 20:
            return f"HandlerB 处理了请求: {request}"
        return super().handle(request)


class ConcreteHandlerC(Handler):
    """具体处理器C - 处理20以上的请求"""
    
    def handle(self, request: Any) -> Optional[str]:
        if isinstance(request, int) and request >= 20:
            return f"HandlerC 处理了请求: {request}"
        return super().handle(request)


class DefaultHandler(Handler):
    """默认处理器 - 处理所有未被处理的请求"""
    
    def handle(self, request: Any) -> Optional[str]:
        return f"DefaultHandler 处理了请求: {request}"


# 使用示例
if __name__ == "__main__":
    # 创建处理器
    handler_a = ConcreteHandlerA()
    handler_b = ConcreteHandlerB()
    handler_c = ConcreteHandlerC()
    default_handler = DefaultHandler()
    
    # 构建责任链
    handler_a.set_next(handler_b).set_next(handler_c).set_next(default_handler)
    
    # 测试不同的请求
    requests = [5, 15, 25, "字符串请求", -1]
    
    for req in requests:
        result = handler_a.handle(req)
        print(f"请求 {req}: {result}")