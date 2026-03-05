
"""
任务超时处理模块
支持多种超时策略：装饰器、上下文管理器、线程、信号、异步
"""

import signal
import threading
import time
import functools
from contextlib import contextmanager
from typing import Callable, Any, Optional
import asyncio


class TimeoutError(Exception):
    """超时异常"""
    pass


# 方法1: 基于信号的超时装饰器 (仅Unix系统)
def timeout_signal(seconds: int):
    """
    使用信号实现超时装饰器（仅支持Unix系统，主线程）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"函数 {func.__name__} 执行超时 ({seconds}秒)")
            
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            return result
        return wrapper
    return decorator


# 方法2: 基于线程的超时装饰器 (跨平台)
def timeout_thread(seconds: float):
    """
    使用线程实现超时装饰器（跨平台，但无法真正终止线程）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [TimeoutError(f"函数 {func.__name__} 执行超时 ({seconds}秒)")]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e
            
            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout=seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"函数 {func.__name__} 执行超时 ({seconds}秒)")
            
            if isinstance(result[0], Exception):
                raise result[0]
            
            return result[0]
        return wrapper
    return decorator


# 方法3: 上下文管理器方式 (基于信号)
@contextmanager
def timeout_context(seconds: int):
    """
    超时上下文管理器（仅支持Unix系统）
    """
    def timeout_handler(signum, frame):
        raise TimeoutError(f"代码块执行超时 ({seconds}秒)")
    
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


# 方法4: 异步超时装饰器
def timeout_async(seconds: float):
    """
    异步函数超时装饰器
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                raise TimeoutError(f"异步函数 {func.__name__} 执行超时 ({seconds}秒)")
        return wrapper
    return decorator


# 方法5: 通用超时执行器类
class TimeoutExecutor:
    """
    通用超时执行器，支持多种策略
    """
    
    @staticmethod
    def run_with_timeout(func: Callable, args: tuple = (), kwargs: dict = None, 
                        timeout: float = 10, method: str = 'thread') -> Any:
        """
        执行函数并设置超时
        
        Args:
            func: 要执行的函数
            args: 位置参数
            kwargs: 关键字参数
            timeout: 超时时间（秒）
            method: 超时方法 ('thread' 或 'signal')
        """
        kwargs = kwargs or {}
        
        if method == 'thread':
            result = [TimeoutError(f"函数执行超时 ({timeout}秒)")]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e
            
            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout=timeout)
            
            if thread.is_alive():
                raise TimeoutError(f"函数执行超时 ({timeout}秒)")
            
            if isinstance(result[0], Exception):
                raise result[0]
            
            return result[0]
        
        elif method == 'signal':
            def timeout_handler(signum, frame):
                raise TimeoutError(f"函数执行超时 ({timeout}秒)")
            
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            return result
        
        else:
            raise ValueError(f"不支持的超时方法: {method}")
    
    @staticmethod
    async def run_async_with_timeout(coro, timeout: float):
        """
        执行异步协程并设置超时
        """
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"异步任务执行超时 ({timeout}秒)")


# 方法6: 可重试的超时装饰器
def timeout_with_retry(seconds: float, retries: int = 3, delay: float = 1):
    """
    带重试机制的超时装饰器
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    result = [TimeoutError(f"函数 {func.__name__} 执行超时")]
                    
                    def target():
                        try:
                            result[0] = func(*args, **kwargs)
                        except Exception as e:
                            result[0] = e
                    
                    thread = threading.Thread(target=target, daemon=True)
                    thread.start()
                    thread.join(timeout=seconds)
                    
                    if thread.is_alive():
                        if attempt < retries - 1:
                            time.sleep(delay)
                            continue
                        raise TimeoutError(f"函数 {func.__name__} 执行超时，已重试 {retries} 次")
                    
                    if isinstance(result[0], Exception):
                        raise result[0]
                    
                    return result[0]
                    
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    time.sleep(delay)
            
        return wrapper
    return decorator


# 使用示例（注释形式）
"""
# 示例1: 使用装饰器
@timeout_thread(5)
def slow_function():
    time.sleep(10)
    return "完成"

# 示例2: 使用上下文管理器
with timeout_context(3):
    time.sleep(10)

# 示例3: 异步函数
@timeout_async(2)
async def async_task():
    await asyncio.sleep(5)

# 示例4: 使用执行器
executor = TimeoutExecutor()
result = executor.run_with_timeout(slow_function, timeout=5, method='thread')

# 示例5: 带重试
@timeout_with_retry(seconds=3, retries=3, delay=1)
def unstable_function():
    time.sleep(2)
    return "成功"
"""
