# websocket_chat.py
import asyncio
import websockets
import json
from typing import Set

class WebSocketChat:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
    
    async def register(self, websocket):
        """注册新客户端"""
        self.clients.add(websocket)
        await self.broadcast({"type": "system", "message": "新用户加入"})
    
    async def unregister(self, websocket):
        """注销客户端"""
        self.clients.remove(websocket)
        await self.broadcast({"type": "system", "message": "用户离开"})
    
    async def broadcast(self, message: dict):
        """广播消息给所有客户端"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )
    
    async def handle_client(self, websocket):
        """处理单个客户端连接"""
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.broadcast({
                    "type": "message",
                    "user": data.get("user", "匿名"),
                    "content": data.get("content", "")
                })
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """启动服务器"""
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"WebSocket服务器运行在 ws://{self.host}:{self.port}")
            await asyncio.Future()  # 永久运行

# 使用示例
if __name__ == "__main__":
    chat = WebSocketChat()
    asyncio.run(chat.start())