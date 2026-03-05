from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional
from functools import wraps
import time


class Interceptor(ABC):
    """拦截器基类"""
    
    @abstractmethod
    def before(self, *args, **kwargs) -> tuple:
        """前置处理"""
        pass
    
    @abstractmethod
    def after(self, result: Any, *args, **kwargs) -> Any:
        """后置处理"""
        pass
    
    @abstractmethod
    def on_error(self, error: Exception, *args, **kwargs) -> None:
        """异常处理"""
        pass


class LoggingInterceptor(Interceptor):
    """日志拦截器"""
    
    def before(self, *args, **kwargs) -> tuple:
        print(f"[LOG] 调用开始 - args: {args}, kwargs: {kwargs}")
        return args, kwargs
    
    def after(self, result: Any, *args, **kwargs) -> Any:
        print(f"[LOG] 调用结束 - 结果: {result}")
        return result
    
    def on_error(self, error: Exception, *args, **kwargs) -> None:
        print(f"[LOG] 发生异常 - {type(error).__name__}: {error}")


class TimingInterceptor(Interceptor):
    """性能计时拦截器"""
    
    def __init__(self):
        self.start_time = None
    
    def before(self, *args, **kwargs) -> tuple:
        self.start_time = time.time()
        return args, kwargs
    
    def after(self, result: Any, *args, **kwargs) -> Any:
        elapsed = time.time() - self.start_time
        print(f"[TIMING] 执行耗时: {elapsed:.4f}秒")
        return result
    
    def on_error(self, error: Exception, *args, **kwargs) -> None:
        elapsed = time.time() - self.start_time
        print(f"[TIMING] 异常前耗时: {elapsed:.4f}秒")


class ValidationInterceptor(Interceptor):
    """参数验证拦截器"""
    
    def __init__(self, validator: Optional[Callable] = None):
        self.validator = validator
    
    def before(self, *args, **kwargs) -> tuple:
        if self.validator:
            if not self.validator(*args, **kwargs):
                raise ValueError("参数验证失败")
        return args, kwargs
    
    def after(self, result: Any, *args, **kwargs) -> Any:
        return result
    
    def on_error(self, error: Exception, *args, **kwargs) -> None:
        print(f"[VALIDATION] 验证异常: {error}")


class InterceptorChain:
    """拦截器链"""
    
    def __init__(self):
        self.interceptors: List[Interceptor] = []
    
    def add(self, interceptor: Interceptor) -> 'InterceptorChain':
        """添加拦截器"""
        self.interceptors.append(interceptor)
        return self
    
    def remove(self, interceptor: Interceptor) -> 'InterceptorChain':
        """移除拦截器"""
        if interceptor in self.interceptors:
            self.interceptors.remove(interceptor)
        return self
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """执行拦截器链"""
        # 前置处理
        for interceptor in self.interceptors:
            args, kwargs = interceptor.before(*args, **kwargs)
        
        try:
            # 执行目标方法
            result = func(*args, **kwargs)
            
            # 后置处理
            for interceptor in reversed(self.interceptors):
                result = interceptor.after(result, *args, **kwargs)
            
            return result
            
        except Exception as e:
            # 异常处理
            for interceptor in self.interceptors:
                interceptor.on_error(e, *args, **kwargs)
            raise


def intercept(*interceptors: Interceptor):
    """装饰器：为方法添加拦截器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            chain = InterceptorChain()
            for interceptor in interceptors:
                chain.add(interceptor)
            return chain.execute(func, *args, **kwargs)
        return wrapper
    return decorator


# 使用示例
class Service:
    """业务服务类"""
    
    @intercept(LoggingInterceptor(), TimingInterceptor())
    def process(self, data: str) -> str:
        """处理数据"""
        time.sleep(0.1)  # 模拟处理
        return f"处理完成: {data}"
    
    @intercept(
        ValidationInterceptor(lambda x: x > 0),
        LoggingInterceptor()
    )
    def calculate(self, value: int) -> int:
        """计算"""
        return value * 2


if __name__ == "__main__":
    service = Service()
    
    # 测试1: 正常调用
    print("\n=== 测试1: 正常调用 ===")
    result = service.process("测试数据")
    print(f"返回值: {result}\n")
    
    # 测试2: 带验证的调用
    print("=== 测试2: 带验证的调用 ===")
    result = service.calculate(5)
    print(f"返回值: {result}\n")
    
    # 测试3: 验证失败
    print("=== 测试3: 验证失败 ===")
    try:
        service.calculate(-1)
    except ValueError as e:
        print(f"捕获异常: {e}")