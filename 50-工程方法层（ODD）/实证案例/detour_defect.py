from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re


class MessageType(Enum):
    TEXT = "text"
    COMMAND = "command"
    EVENT = "event"
    SYSTEM = "system"


@dataclass
class Message:
    type: MessageType
    content: Any
    sender: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MessageRouter:
    def __init__(self):
        self._handlers: Dict[MessageType, List[Callable]] = {
            msg_type: [] for msg_type in MessageType
        }
        self._pattern_handlers: List[tuple[re.Pattern, Callable]] = []
        self._middleware: List[Callable] = []
        self._default_handler: Optional[Callable] = None
    
    def register(self, message_type: MessageType, handler: Callable):
        """注册消息类型处理器"""
        self._handlers[message_type].append(handler)
        return self
    
    def register_pattern(self, pattern: str, handler: Callable):
        """注册正则模式处理器"""
        compiled_pattern = re.compile(pattern)
        self._pattern_handlers.append((compiled_pattern, handler))
        return self
    
    def use_middleware(self, middleware: Callable):
        """添加中间件"""
        self._middleware.append(middleware)
        return self
    
    def set_default(self, handler: Callable):
        """设置默认处理器"""
        self._default_handler = handler
        return self
    
    def route(self, message: Message) -> List[Any]:
        """路由消息到对应处理器"""
        # 应用中间件
        for middleware in self._middleware:
            message = middleware(message)
            if message is None:
                return []
        
        results = []
        handled = False
        
        # 类型匹配处理
        if message.type in self._handlers:
            for handler in self._handlers[message.type]:
                result = handler(message)
                results.append(result)
                handled = True
        
        # 模式匹配处理
        if isinstance(message.content, str):
            for pattern, handler in self._pattern_handlers:
                if pattern.search(message.content):
                    result = handler(message)
                    results.append(result)
                    handled = True
        
        # 默认处理器
        if not handled and self._default_handler:
            result = self._default_handler(message)
            results.append(result)
        
        return results
    
    def broadcast(self, message: Message) -> List[Any]:
        """广播消息到所有处理器"""
        results = []
        for handlers in self._handlers.values():
            for handler in handlers:
                result = handler(message)
                results.append(result)
        return results


class MessageBypass:
    def __init__(self):
        self._routers: Dict[str, MessageRouter] = {}
        self._filters: List[Callable[[Message], bool]] = []
        self._interceptors: List[Callable[[Message], Message]] = []
    
    def create_router(self, name: str) -> MessageRouter:
        """创建命名路由器"""
        router = MessageRouter()
        self._routers[name] = router
        return router
    
    def get_router(self, name: str) -> Optional[MessageRouter]:
        """获取路由器"""
        return self._routers.get(name)
    
    def add_filter(self, filter_func: Callable[[Message], bool]):
        """添加消息过滤器"""
        self._filters.append(filter_func)
        return self
    
    def add_interceptor(self, interceptor: Callable[[Message], Message]):
        """添加消息拦截器"""
        self._interceptors.append(interceptor)
        return self
    
    def send(self, router_name: str, message: Message) -> List[Any]:
        """发送消息到指定路由器"""
        # 应用过滤器
        for filter_func in self._filters:
            if not filter_func(message):
                return []
        
        # 应用拦截器
        for interceptor in self._interceptors:
            message = interceptor(message)
        
        # 路由消息
        router = self._routers.get(router_name)
        if router:
            return router.route(message)
        return []
    
    def broadcast_all(self, message: Message) -> Dict[str, List[Any]]:
        """广播到所有路由器"""
        results = {}
        for name, router in self._routers.items():
            results[name] = router.route(message)
        return results


# 使用示例
if __name__ == "__main__":
    bypass = MessageBypass()
    
    # 创建路由器
    main_router = bypass.create_router("main")
    
    # 注册处理器
    main_router.register(MessageType.TEXT, lambda msg: f"处理文本: {msg.content}")
    main_router.register(MessageType.COMMAND, lambda msg: f"执行命令: {msg.content}")
    main_router.register_pattern(r"^/help", lambda msg: "显示帮助信息")
    
    # 添加中间件
    main_router.use_middleware(lambda msg: Message(
        msg.type, msg.content.upper() if isinstance(msg.content, str) else msg.content,
        msg.sender, msg.metadata
    ))
    
    # 添加过滤器
    bypass.add_filter(lambda msg: msg.sender != "blocked_user")
    
    # 发送消息
    msg1 = Message(MessageType.TEXT, "hello world", "user1")
    results = bypass.send("main", msg1)
    print(results)
    
    msg2 = Message(MessageType.COMMAND, "/help me", "user2")
    results = bypass.send("main", msg2)
    print(results)