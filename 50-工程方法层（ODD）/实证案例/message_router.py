from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


@dataclass
class Message:
    type: str
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    metadata: Optional[Dict[str, Any]] = None


class MessageRouter:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._middleware: List[Callable] = []
        self._default_handler: Optional[Callable] = None
    
    def register(self, message_type: str, handler: Callable) -> None:
        """注册消息处理器"""
        if message_type not in self._handlers:
            self._handlers[message_type] = []
        self._handlers[message_type].append(handler)
        logger.info(f"Registered handler for message type: {message_type}")
    
    def unregister(self, message_type: str, handler: Callable) -> bool:
        """注销消息处理器"""
        if message_type in self._handlers:
            try:
                self._handlers[message_type].remove(handler)
                if not self._handlers[message_type]:
                    del self._handlers[message_type]
                return True
            except ValueError:
                pass
        return False
    
    def add_middleware(self, middleware: Callable) -> None:
        """添加中间件"""
        self._middleware.append(middleware)
    
    def set_default_handler(self, handler: Callable) -> None:
        """设置默认处理器"""
        self._default_handler = handler
    
    def route(self, message: Message) -> List[Any]:
        """路由消息到对应的处理器"""
        # 执行中间件
        for middleware in self._middleware:
            message = middleware(message)
            if message is None:
                logger.warning("Message blocked by middleware")
                return []
        
        results = []
        handlers = self._handlers.get(message.type, [])
        
        if not handlers and self._default_handler:
            handlers = [self._default_handler]
        
        for handler in handlers:
            try:
                result = handler(message)
                results.append(result)
            except Exception as e:
                logger.error(f"Handler error for {message.type}: {e}")
                results.append(None)
        
        return results
    
    def route_async(self, message: Message) -> None:
        """异步路由（简化版）"""
        import threading
        thread = threading.Thread(target=self.route, args=(message,))
        thread.start()
    
    def get_registered_types(self) -> List[str]:
        """获取已注册的消息类型"""
        return list(self._handlers.keys())


# 使用示例
if __name__ == "__main__":
    router = MessageRouter()
    
    # 注册处理器
    @router.register("user.login", lambda msg: print(f"User login: {msg.payload}"))
    def handle_login(message: Message):
        print(f"Processing login: {message.payload}")
        return {"status": "success"}
    
    router.register("user.logout", lambda msg: print(f"User logout: {msg.payload}"))
    
    # 添加中间件
    def logging_middleware(message: Message) -> Message:
        print(f"[Middleware] Processing: {message.type}")
        return message
    
    router.add_middleware(logging_middleware)
    
    # 路由消息
    msg = Message(type="user.login", payload={"username": "alice"})
    results = router.route(msg)
    print(f"Results: {results}")