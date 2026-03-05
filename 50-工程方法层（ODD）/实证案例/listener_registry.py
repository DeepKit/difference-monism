from typing import Callable, Dict, List, Any, Optional
from abc import ABC, abstractmethod
import weakref


class Listener(ABC):
    """监听器基类"""
    
    @abstractmethod
    def on_event(self, event_type: str, data: Any) -> None:
        """处理事件"""
        pass


class ListenerRegistry:
    """监听器注册管理类"""
    
    def __init__(self):
        self._listeners: Dict[str, List[weakref.ref]] = {}
        self._callback_listeners: Dict[str, List[Callable]] = {}
    
    def register(self, event_type: str, listener: Listener) -> None:
        """注册监听器对象"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        # 使用弱引用避免内存泄漏
        self._listeners[event_type].append(weakref.ref(listener, 
            lambda ref: self._cleanup_listener(event_type, ref)))
    
    def register_callback(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """注册回调函数"""
        if event_type not in self._callback_listeners:
            self._callback_listeners[event_type] = []
        
        self._callback_listeners[event_type].append(callback)
    
    def unregister(self, event_type: str, listener: Listener) -> bool:
        """注销监听器对象"""
        if event_type not in self._listeners:
            return False
        
        for i, ref in enumerate(self._listeners[event_type]):
            if ref() is listener:
                del self._listeners[event_type][i]
                return True
        return False
    
    def unregister_callback(self, event_type: str, callback: Callable) -> bool:
        """注销回调函数"""
        if event_type not in self._callback_listeners:
            return False
        
        try:
            self._callback_listeners[event_type].remove(callback)
            return True
        except ValueError:
            return False
    
    def unregister_all(self, event_type: Optional[str] = None) -> None:
        """注销所有监听器"""
        if event_type:
            self._listeners.pop(event_type, None)
            self._callback_listeners.pop(event_type, None)
        else:
            self._listeners.clear()
            self._callback_listeners.clear()
    
    def notify(self, event_type: str, data: Any = None) -> None:
        """通知所有监听器"""
        # 通知对象监听器
        if event_type in self._listeners:
            # 清理已失效的弱引用
            self._listeners[event_type] = [
                ref for ref in self._listeners[event_type] if ref() is not None
            ]
            
            for ref in self._listeners[event_type]:
                listener = ref()
                if listener:
                    try:
                        listener.on_event(event_type, data)
                    except Exception as e:
                        print(f"监听器执行错误: {e}")
        
        # 通知回调函数
        if event_type in self._callback_listeners:
            for callback in self._callback_listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"回调函数执行错误: {e}")
    
    def has_listeners(self, event_type: str) -> bool:
        """检查是否有监听器"""
        has_obj = event_type in self._listeners and len(self._listeners[event_type]) > 0
        has_cb = event_type in self._callback_listeners and len(self._callback_listeners[event_type]) > 0
        return has_obj or has_cb
    
    def get_listener_count(self, event_type: str) -> int:
        """获取监听器数量"""
        obj_count = len(self._listeners.get(event_type, []))
        cb_count = len(self._callback_listeners.get(event_type, []))
        return obj_count + cb_count
    
    def _cleanup_listener(self, event_type: str, ref: weakref.ref) -> None:
        """清理失效的监听器引用"""
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(ref)
            except ValueError:
                pass


# 使用示例
if __name__ == "__main__":
    # 创建监听器类
    class MyListener(Listener):
        def __init__(self, name: str):
            self.name = name
        
        def on_event(self, event_type: str, data: Any) -> None:
            print(f"[{self.name}] 收到事件: {event_type}, 数据: {data}")
    
    # 创建注册器
    registry = ListenerRegistry()
    
    # 注册对象监听器
    listener1 = MyListener("监听器1")
    listener2 = MyListener("监听器2")
    registry.register("user_login", listener1)
    registry.register("user_login", listener2)
    
    # 注册回调函数
    registry.register_callback("user_login", lambda data: print(f"回调: 用户登录 - {data}"))
    
    # 触发事件
    registry.notify("user_login", {"user_id": 123, "username": "张三"})
    
    # 注销监听器
    registry.unregister("user_login", listener1)
    
    # 再次触发
    print("\n注销listener1后:")
    registry.notify("user_login", {"user_id": 456, "username": "李四"})