
import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any, Callable
from datetime import datetime
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 所有活跃连接: {connection_id: websocket}
        self.active_connections: Dict[str, WebSocketServerProtocol] = {}
        
        # 房间管理: {room_id: set(connection_ids)}
        self.rooms: Dict[str, Set[str]] = {}
        
        # 连接元数据: {connection_id: metadata}
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
        
        # 消息处理器
        self.message_handlers: Dict[str, Callable] = {}
        
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocketServerProtocol, connection_id: str, 
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """注册新的WebSocket连接"""
        async with self._lock:
            self.active_connections[connection_id] = websocket
            self.connection_metadata[connection_id] = metadata or {}
            self.connection_metadata[connection_id]['connected_at'] = datetime.now().isoformat()
            
        logger.info(f"连接已建立: {connection_id}, 当前连接数: {len(self.active_connections)}")
    
    async def disconnect(self, connection_id: str) -> None:
        """断开并移除WebSocket连接"""
        async with self._lock:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            
            if connection_id in self.connection_metadata:
                del self.connection_metadata[connection_id]
            
            # 从所有房间中移除
            for room_id in list(self.rooms.keys()):
                if connection_id in self.rooms[room_id]:
                    self.rooms[room_id].discard(connection_id)
                    if not self.rooms[room_id]:
                        del self.rooms[room_id]
        
        logger.info(f"连接已断开: {connection_id}, 当前连接数: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Any, connection_id: str) -> bool:
        """发送消息给指定连接"""
        websocket = self.active_connections.get(connection_id)
        if not websocket:
            logger.warning(f"连接不存在: {connection_id}")
            return False
        
        try:
            if isinstance(message, dict):
                message = json.dumps(message, ensure_ascii=False)
            await websocket.send(message)
            return True
        except ConnectionClosed:
            logger.warning(f"连接已关闭: {connection_id}")
            await self.disconnect(connection_id)
            return False
        except Exception as e:
            logger.error(f"发送消息失败 {connection_id}: {e}")
            return False
    
    async def broadcast(self, message: Any, exclude: Optional[Set[str]] = None) -> int:
        """广播消息给所有连接"""
        exclude = exclude or set()
        success_count = 0
        
        if isinstance(message, dict):
            message = json.dumps(message, ensure_ascii=False)
        
        tasks = []
        for connection_id, websocket in list(self.active_connections.items()):
            if connection_id not in exclude:
                tasks.append(self._send_safe(websocket, message, connection_id))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success_count = sum(1 for r in results if r is True)
        
        logger.info(f"广播消息: 成功 {success_count}/{len(tasks)}")
        return success_count
    
    async def _send_safe(self, websocket: WebSocketServerProtocol, 
                        message: str, connection_id: str) -> bool:
        """安全发送消息"""
        try:
            await websocket.send(message)
            return True
        except ConnectionClosed:
            await self.disconnect(connection_id)
            return False
        except Exception as e:
            logger.error(f"发送失败 {connection_id}: {e}")
            return False
    
    async def join_room(self, connection_id: str, room_id: str) -> bool:
        """加入房间"""
        if connection_id not in self.active_connections:
            return False
        
        async with self._lock:
            if room_id not in self.rooms:
                self.rooms[room_id] = set()
            self.rooms[room_id].add(connection_id)
        
        logger.info(f"连接 {connection_id} 加入房间 {room_id}")
        return True
    
    async def leave_room(self, connection_id: str, room_id: str) -> bool:
        """离开房间"""
        async with self._lock:
            if room_id in self.rooms and connection_id in self.rooms[room_id]:
                self.rooms[room_id].discard(connection_id)
                if not self.rooms[room_id]:
                    del self.rooms[room_id]
                logger.info(f"连接 {connection_id} 离开房间 {room_id}")
                return True
        return False
    
    async def broadcast_to_room(self, room_id: str, message: Any, 
                               exclude: Optional[Set[str]] = None) -> int:
        """向房间内所有连接广播消息"""
        if room_id not in self.rooms:
            return 0
        
        exclude = exclude or set()
        success_count = 0
        
        if isinstance(message, dict):
            message = json.dumps(message, ensure_ascii=False)
        
        tasks = []
        for connection_id in self.rooms[room_id]:
            if connection_id not in exclude:
                websocket = self.active_connections.get(connection_id)
                if websocket:
                    tasks.append(self._send_safe(websocket, message, connection_id))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success_count = sum(1 for r in results if r is True)
        
        logger.info(f"房间 {room_id} 广播: 成功 {success_count}/{len(tasks)}")
        return success_count
    
    def register_handler(self, message_type: str, handler: Callable) -> None:
        """注册消息处理器"""
        self.message_handlers[message_type] = handler
        logger.info(f"注册消息处理器: {message_type}")
    
    async def handle_message(self, connection_id: str, message: str) -> None:
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type and message_type in self.message_handlers:
                handler = self.message_handlers[message_type]
                await handler(connection_id, data)
            else:
                logger.warning(f"未知消息类型: {message_type}")
        except json.JSONDecodeError:
            logger.error(f"JSON解析失败: {message}")
        except Exception as e:
            logger.error(f"消息处理异常: {e}")
    
    def get_connection_count(self) -> int:
        """获取当前连接数"""
        return len(self.active_connections)
    
    def get_room_members(self, room_id: str) -> Set[str]:
        """获取房间成员列表"""
        return self.rooms.get(room_id, set()).copy()
    
    def get_connection_metadata(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """获取连接元数据"""
        return self.connection_metadata.get(connection_id)
    
    async def close_all(self) -> None:
        """关闭所有连接"""
        tasks = []
        for connection_id, websocket in list(self.active_connections.items()):
            tasks.append(websocket.close())
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        async with self._lock:
            self.active_connections.clear()
            self.connection_metadata.clear()
            self.rooms.clear()
        
        logger.info("所有连接已关闭")


# 使用示例
async def example_handler(connection_id: str, data: Dict[str, Any]) -> None:
    """示例消息处理器"""
    logger.info(f"处理来自 {connection_id} 的消息: {data}")


# 创建全局管理器实例
ws_manager = WebSocketManager()
