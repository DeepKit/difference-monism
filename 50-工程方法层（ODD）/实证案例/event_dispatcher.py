from typing import Callable, Dict, List, Any, Optional
from collections import defaultdict
import inspect


class EventDispatcher:
    """事件分发器"""
    
    def __init__(self):
        self._listeners: Dict[str, List[tuple[Callable, int]]] = defaultdict(list)
        self._once_listeners: Dict[str, List[Callable]] = defaultdict(list)
    
    def on(self, event: str, callback: Callable, priority: int = 0) -> None:
        """注册事件监听器
        
        Args:
            event: 事件名称
            callback: 回调函数
            priority: 优先级，数值越大优先级越高
        """
        self._listeners[event].append((callback, priority))
        self._listeners[event].sort(key=lambda x: x[1], reverse=True)
    
    def once(self, event: str, callback: Callable) -> None:
        """注册一次性事件监听器"""
        self._once_listeners[event].append(callback)
    
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """移除事件监听器
        
        Args:
            event: 事件名称
            callback: 回调函数，如果为None则移除该事件的所有监听器
        """
        if callback is None:
            self._listeners.pop(event, None)
            self._once_listeners.pop(event, None)
        else:
            self._listeners[event] = [
                (cb, pri) for cb, pri in self._listeners[event] if cb != callback
            ]
            self._once_listeners[event] = [
                cb for cb in self._once_listeners[event] if cb != callback
            ]
    
    def emit(self, event: str, *args, **kwargs) -> List[Any]:
        """触发事件
        
        Args:
            event: 事件名称
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            所有监听器的返回值列表
        """
        results = []
        
        # 执行普通监听器
        for callback, _ in self._listeners.get(event, []):
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"事件 '{event}' 监听器执行错误: {e}")
        
        # 执行一次性监听器
        once_callbacks = self._once_listeners.pop(event, [])
        for callback in once_callbacks:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"事件 '{event}' 一次性监听器执行错误: {e}")
        
        return results
    
    def has_listeners(self, event: str) -> bool:
        """检查事件是否有监听器"""
        return bool(self._listeners.get(event) or self._once_listeners.get(event))
    
    def listener_count(self, event: str) -> int:
        """获取事件监听器数量"""
        return len(self._listeners.get(event, [])) + len(self._once_listeners.get(event, []))
    
    def clear(self) -> None:
        """清除所有事件监听器"""
        self._listeners.clear()
        self._once_listeners.clear()


# 使用示例
if __name__ == "__main__":
    dispatcher = EventDispatcher()
    
    # 注册事件
    def on_user_login(username):
        print(f"用户 {username} 登录了")
        return f"欢迎 {username}"
    
    def on_user_login_log(username):
        print(f"记录日志: {username} 登录")
    
    dispatcher.on("user:login", on_user_login, priority=10)
    dispatcher.on("user:login", on_user_login_log, priority=5)
    
    # 一次性事件
    dispatcher.once("user:login", lambda username: print(f"首次登录提示: {username}"))
    
    # 触发事件
    results = dispatcher.emit("user:login", "张三")
    print(f"返回值: {results}")
    
    # 再次触发（一次性监听器不会执行）
    dispatcher.emit("user:login", "李四")
    
    # 移除监听器
    dispatcher.off("user:login", on_user_login)
    
    # 检查监听器
    print(f"监听器数量: {dispatcher.listener_count('user:login')}")