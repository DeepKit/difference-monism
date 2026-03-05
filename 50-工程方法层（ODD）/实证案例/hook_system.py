from typing import Callable, Any, Dict, List, Optional
from functools import wraps
import inspect


class HookSystem:
    """通用钩子系统实现"""
    
    def __init__(self):
        self._hooks: Dict[str, List[Dict[str, Any]]] = {}
        self._filters: Dict[str, List[Dict[str, Any]]] = {}
    
    def register_hook(
        self, 
        hook_name: str, 
        callback: Callable, 
        priority: int = 10
    ) -> None:
        """注册动作钩子"""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        
        self._hooks[hook_name].append({
            'callback': callback,
            'priority': priority
        })
        self._hooks[hook_name].sort(key=lambda x: x['priority'])
    
    def register_filter(
        self, 
        filter_name: str, 
        callback: Callable, 
        priority: int = 10
    ) -> None:
        """注册过滤器钩子"""
        if filter_name not in self._filters:
            self._filters[filter_name] = []
        
        self._filters[filter_name].append({
            'callback': callback,
            'priority': priority
        })
        self._filters[filter_name].sort(key=lambda x: x['priority'])
    
    def do_action(self, hook_name: str, *args, **kwargs) -> None:
        """执行动作钩子"""
        if hook_name not in self._hooks:
            return
        
        for hook in self._hooks[hook_name]:
            try:
                hook['callback'](*args, **kwargs)
            except Exception as e:
                print(f"Hook '{hook_name}' error: {e}")
    
    def apply_filters(self, filter_name: str, value: Any, *args, **kwargs) -> Any:
        """应用过滤器钩子"""
        if filter_name not in self._filters:
            return value
        
        result = value
        for filter_hook in self._filters[filter_name]:
            try:
                result = filter_hook['callback'](result, *args, **kwargs)
            except Exception as e:
                print(f"Filter '{filter_name}' error: {e}")
        
        return result
    
    def remove_hook(self, hook_name: str, callback: Callable) -> bool:
        """移除动作钩子"""
        if hook_name not in self._hooks:
            return False
        
        original_length = len(self._hooks[hook_name])
        self._hooks[hook_name] = [
            h for h in self._hooks[hook_name] 
            if h['callback'] != callback
        ]
        return len(self._hooks[hook_name]) < original_length
    
    def remove_filter(self, filter_name: str, callback: Callable) -> bool:
        """移除过滤器钩子"""
        if filter_name not in self._filters:
            return False
        
        original_length = len(self._filters[filter_name])
        self._filters[filter_name] = [
            f for f in self._filters[filter_name] 
            if f['callback'] != callback
        ]
        return len(self._filters[filter_name]) < original_length
    
    def has_hook(self, hook_name: str) -> bool:
        """检查是否存在钩子"""
        return hook_name in self._hooks and len(self._hooks[hook_name]) > 0
    
    def has_filter(self, filter_name: str) -> bool:
        """检查是否存在过滤器"""
        return filter_name in self._filters and len(self._filters[filter_name]) > 0
    
    def clear_hooks(self, hook_name: Optional[str] = None) -> None:
        """清除钩子"""
        if hook_name:
            self._hooks.pop(hook_name, None)
        else:
            self._hooks.clear()
    
    def clear_filters(self, filter_name: Optional[str] = None) -> None:
        """清除过滤器"""
        if filter_name:
            self._filters.pop(filter_name, None)
        else:
            self._filters.clear()
    
    def hook(self, hook_name: str, priority: int = 10):
        """装饰器：注册动作钩子"""
        def decorator(func: Callable) -> Callable:
            self.register_hook(hook_name, func, priority)
            return func
        return decorator
    
    def filter(self, filter_name: str, priority: int = 10):
        """装饰器：注册过滤器钩子"""
        def decorator(func: Callable) -> Callable:
            self.register_filter(filter_name, func, priority)
            return func
        return decorator


# 使用示例
if __name__ == "__main__":
    hooks = HookSystem()
    
    # 注册动作钩子
    @hooks.hook('user_login', priority=5)
    def log_login(username):
        print(f"User logged in: {username}")
    
    @hooks.hook('user_login', priority=10)
    def send_notification(username):
        print(f"Notification sent to: {username}")
    
    # 执行钩子
    hooks.do_action('user_login', 'alice')
    
    # 注册过滤器
    @hooks.filter('format_name')
    def uppercase_name(name):
        return name.upper()
    
    @hooks.filter('format_name')
    def add_prefix(name):
        return f"Mr. {name}"
    
    # 应用过滤器
    result = hooks.apply_filters('format_name', 'john')
    print(f"Formatted name: {result}")