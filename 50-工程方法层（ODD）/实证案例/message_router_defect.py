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
        
        handlers = self._handlers.get(message.type, [])
        
        if not handlers and self._default_handler:
            handlers = [self._default_handler]
        
        if not handlers:
            logger.warning(f"No handler found for message type: {message.type}")
            return []
        
        results = []
        for handler in handlers:
            try:
                result = handler(message)
                results.append(result)
            except Exception as e:
                logger.error(f"Handler error for {message.type}: {e}")
                results.append(None)
        
        return results
    
    def route_batch(self, messages: List[Message]) -> Dict[str, List[Any]]:
        """批量路由消息"""
        # 按优先级排序
        sorted_messages = sorted(messages, key=lambda m: m.priority.value, reverse=True)
        
        results = {}
        for message in sorted_messages:
            results[message.type] = self.route(message)
        
        return results
    
    def get_registered_types(self) -> List[str]:
        """获取已注册的消息类型"""
        return list(self._handlers.keys())


# 使用示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    router = MessageRouter()
    
    # 注册处理器
    @router.register("user.login", lambda msg: f"User logged in: {msg.payload['username']}")
    def handle_login(message: Message):
        return f"User logged in: {message.payload['username']}"
    
    router.register("user.logout", lambda msg: f"User logged out: {msg.payload['username']}")
    
    # 添加中间件
    def logging_middleware(message: Message) -> Message:
        logger.info(f"Processing message: {message.type}")
        return message
    
    router.add_middleware(logging_middleware)
    
    # 路由消息
    login_msg = Message(
        type="user.login",
        payload={"username": "alice"},
        priority=MessagePriority.HIGH
    )
    
    results = router.route(login_msg)
    print(results)