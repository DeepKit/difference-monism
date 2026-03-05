
import asyncio
import json
import logging
from typing import Optional, Callable, Any
from datetime import datetime
import websockets
from websockets.client import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(
        self,
        url: str,
        heartbeat_interval: int = 30,
        reconnect_interval: int = 5,
        max_reconnect_attempts: int = 0,
        ping_timeout: int = 10,
    ):
        self.url = url
        self.heartbeat_interval = heartbeat_interval
        self.reconnect_interval = reconnect_interval
        self.max_reconnect_attempts = max_reconnect_attempts
        self.ping_timeout = ping_timeout
        
        self.ws: Optional[WebSocketClientProtocol] = None
        self.is_connected = False
        self.is_running = False
        self.reconnect_count = 0
        
        self.on_message_callback: Optional[Callable] = None
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        self.on_error_callback: Optional[Callable] = None
        
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._reconnect_task: Optional[asyncio.Task] = None

    def on_message(self, callback: Callable[[Any], None]):
        self.on_message_callback = callback
        return self

    def on_connect(self, callback: Callable[[], None]):
        self.on_connect_callback = callback
        return self

    def on_disconnect(self, callback: Callable[[], None]):
        self.on_disconnect_callback = callback
        return self

    def on_error(self, callback: Callable[[Exception], None]):
        self.on_error_callback = callback
        return self

    async def connect(self):
        try:
            self.ws = await websockets.connect(
                self.url,
                ping_interval=None,
                ping_timeout=self.ping_timeout,
            )
            self.is_connected = True
            self.reconnect_count = 0
            logger.info(f"Connected to {self.url}")
            
            if self.on_connect_callback:
                await self._safe_callback(self.on_connect_callback)
            
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            self._receive_task = asyncio.create_task(self._receive_loop())
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            if self.on_error_callback:
                await self._safe_callback(self.on_error_callback, e)
            raise

    async def disconnect(self):
        self.is_running = False
        
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._receive_task:
            self._receive_task.cancel()
        if self._reconnect_task:
            self._reconnect_task.cancel()
        
        if self.ws and not self.ws.closed:
            await self.ws.close()
        
        self.is_connected = False
        logger.info("Disconnected")
        
        if self.on_disconnect_callback:
            await self._safe_callback(self.on_disconnect_callback)

    async def send(self, message: Any):
        if not self.is_connected or not self.ws:
            raise ConnectionError("WebSocket is not connected")
        
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            await self.ws.send(message)
            logger.debug(f"Sent: {message}")
        except Exception as e:
            logger.error(f"Send failed: {e}")
            raise

    async def start(self):
        self.is_running = True
        await self.connect()
        
        while self.is_running:
            await asyncio.sleep(1)

    async def _heartbeat_loop(self):
        while self.is_connected and self.is_running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                if self.ws and not self.ws.closed:
                    pong = await self.ws.ping()
                    await asyncio.wait_for(pong, timeout=self.ping_timeout)
                    logger.debug("Heartbeat sent")
            except asyncio.TimeoutError:
                logger.warning("Heartbeat timeout")
                await self._handle_disconnect()
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await self._handle_disconnect()
                break

    async def _receive_loop(self):
        while self.is_connected and self.is_running:
            try:
                message = await self.ws.recv()
                logger.debug(f"Received: {message}")
                
                try:
                    parsed_message = json.loads(message)
                except json.JSONDecodeError:
                    parsed_message = message
                
                if self.on_message_callback:
                    await self._safe_callback(self.on_message_callback, parsed_message)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Connection closed")
                await self._handle_disconnect()
                break
            except Exception as e:
                logger.error(f"Receive error: {e}")
                if self.on_error_callback:
                    await self._safe_callback(self.on_error_callback, e)

    async def _handle_disconnect(self):
        self.is_connected = False
        
        if self.on_disconnect_callback:
            await self._safe_callback(self.on_disconnect_callback)
        
        if self.is_running:
            self._reconnect_task = asyncio.create_task(self._reconnect())

    async def _reconnect(self):
        while self.is_running:
            if self.max_reconnect_attempts > 0 and self.reconnect_count >= self.max_reconnect_attempts:
                logger.error("Max reconnection attempts reached")
                self.is_running = False
                break
            
            self.reconnect_count += 1
            logger.info(f"Reconnecting... (attempt {self.reconnect_count})")
            
            try:
                await asyncio.sleep(self.reconnect_interval)
                await self.connect()
                logger.info("Reconnected successfully")
                break
            except Exception as e:
                logger.error(f"Reconnection failed: {e}")
                if self.on_error_callback:
                    await self._safe_callback(self.on_error_callback, e)

    async def _safe_callback(self, callback: Callable, *args):
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(*args)
            else:
                callback(*args)
        except Exception as e:
            logger.error(f"Callback error: {e}")


# 使用示例
async def main():
    manager = WebSocketManager(
        url="wss://echo.websocket.org",
        heartbeat_interval=30,
        reconnect_interval=5,
        max_reconnect_attempts=10
    )
    
    async def on_message(message):
        print(f"Message received: {message}")
    
    async def on_connect():
        print("Connected!")
        await manager.send({"type": "hello", "timestamp": datetime.now().isoformat()})
    
    async def on_disconnect():
        print("Disconnected!")
    
    async def on_error(error):
        print(f"Error: {error}")
    
    manager.on_message(on_message)
    manager.on_connect(on_connect)
    manager.on_disconnect(on_disconnect)
    manager.on_error(on_error)
    
    try:
        await manager.start()
    except KeyboardInterrupt:
        await manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
