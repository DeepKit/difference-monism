from typing import Callable, Any, Optional
from abc import ABC, abstractmethod


class Middleware(ABC):
    """中间件基类"""
    
    def __init__(self, next_middleware: Optional['Middleware'] = None):
        self.next = next_middleware
    
    @abstractmethod
    def process(self, request: Any) -> Any:
        """处理请求"""
        pass
    
    def set_next(self, middleware: 'Middleware') -> 'Middleware':
        """设置下一个中间件"""
        self.next = middleware
        return middleware


class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    def process(self, request: Any) -> Any:
        print(f"[LOG] 请求开始: {request}")
        
        if self.next:
            response = self.next.process(request)
        else:
            response = request
            
        print(f"[LOG] 请求结束: {response}")
        return response


class AuthMiddleware(Middleware):
    """认证中间件"""
    
    def __init__(self, next_middleware: Optional[Middleware] = None, token: str = "valid_token"):
        super().__init__(next_middleware)
        self.valid_token = token
    
    def process(self, request: Any) -> Any:
        if not isinstance(request, dict) or request.get('token') != self.valid_token:
            raise PermissionError("认证失败")
        
        print("[AUTH] 认证通过")
        
        if self.next:
            return self.next.process(request)
        return request


class ValidationMiddleware(Middleware):
    """验证中间件"""
    
    def process(self, request: Any) -> Any:
        if not isinstance(request, dict):
            raise ValueError("请求格式错误")
        
        if 'data' not in request:
            raise ValueError("缺少必要字段: data")
        
        print("[VALIDATION] 验证通过")
        
        if self.next:
            return self.next.process(request)
        return request


class TransformMiddleware(Middleware):
    """数据转换中间件"""
    
    def process(self, request: Any) -> Any:
        if isinstance(request, dict) and 'data' in request:
            request['data'] = request['data'].upper()
            print(f"[TRANSFORM] 数据已转换: {request['data']}")
        
        if self.next:
            return self.next.process(request)
        return request


class MiddlewareChain:
    """中间件链管理器"""
    
    def __init__(self):
        self.first: Optional[Middleware] = None
        self.last: Optional[Middleware] = None
    
    def add(self, middleware: Middleware) -> 'MiddlewareChain':
        """添加中间件到链"""
        if not self.first:
            self.first = middleware
            self.last = middleware
        else:
            self.last.set_next(middleware)
            self.last = middleware
        return self
    
    def execute(self, request: Any) -> Any:
        """执行中间件链"""
        if not self.first:
            return request
        return self.first.process(request)


# 使用示例
if __name__ == "__main__":
    # 创建中间件链
    chain = MiddlewareChain()
    chain.add(LoggingMiddleware()) \
         .add(AuthMiddleware(token="valid_token")) \
         .add(ValidationMiddleware()) \
         .add(TransformMiddleware())
    
    # 测试请求
    request = {
        'token': 'valid_token',
        'data': 'hello world'
    }
    
    try:
        result = chain.execute(request)
        print(f"\n最终结果: {result}")
    except Exception as e:
        print(f"\n错误: {e}")