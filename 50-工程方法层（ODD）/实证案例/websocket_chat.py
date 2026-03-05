import asyncio
import websockets
import json
import logging
from datetime import datetime
from typing import Set, Dict, Optional
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Message:
    username: str
    content: str
    timestamp: str
    message_type: str = "chat"  # chat, join, leave, error


class WebSocketChatServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.usernames: Dict[websockets.WebSocketServerProtocol, str] = {}
        
    async def register(self, websocket: websockets.WebSocketServerProtocol, username: str):
        self.clients.add(websocket)
        self.usernames[websocket] = username
        logger.info(f"User {username} connected. Total clients: {len(self.clients)}")
        
        join_message = Message(
            username=username,
            content=f"{username} joined the chat",
            timestamp=datetime.now().isoformat(),
            message_type="join"
        )
        await self.broadcast(json.dumps(asdict(join_message)), exclude=websocket)
    
    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        if websocket in self.clients:
            username = self.usernames.get(websocket, "Unknown")
            self.clients.remove(websocket)
            self.usernames.pop(websocket, None)
            logger.info(f"User {username} disconnected. Total clients: {len(self.clients)}")
            
            leave_message = Message(
                username=username,
                content=f"{username} left the chat",
                timestamp=datetime.now().isoformat(),
                message_type="leave"
            )
            await self.broadcast(json.dumps(asdict(leave_message)))
    
    async def broadcast(self, message: str, exclude: Optional[websockets.WebSocketServerProtocol] = None):
        if self.clients:
            tasks = []
            for client in self.clients:
                if client != exclude:
                    tasks.append(self.send_to_client(client, message))
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_to_client(self, client: websockets.WebSocketServerProtocol, message: str):
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Failed to send message to disconnected client")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        username = None
        try:
            # First message should be username
            username_data = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            data = json.loads(username_data)
            username = data.get("username", "Anonymous")
            
            await self.register(websocket, username)
            
            async for message in websocket:
                try:
                    msg_data = json.loads(message)
                    chat_message = Message(
                        username=username,
                        content=msg_data.get("content", ""),
                        timestamp=datetime.now().isoformat(),
                        message_type="chat"
                    )
                    logger.info(f"Message from {username}: {chat_message.content}")
                    await self.broadcast(json.dumps(asdict(chat_message)))
                    
                except json.JSONDecodeError:
                    error_msg = Message(
                        username="System",
                        content="Invalid message format",
                        timestamp=datetime.now().isoformat(),
                        message_type="error"
                    )
                    await websocket.send(json.dumps(asdict(error_msg)))
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except asyncio.TimeoutError:
            logger.warning("Client connection timeout")
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for {username}")
        except Exception as e:
            logger.error(f"Error in handle_client: {e}")
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever


class WebSocketChatClient:
    def __init__(self, uri: str, username: str):
        self.uri = uri
        self.username = username
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.running = True
            
            # Send username as first message
            await self.websocket.send(json.dumps({"username": self.username}))
            logger.info(f"Connected as {self.username}")
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    async def send_message(self, content: str):
        if not self.websocket:
            raise RuntimeError("Not connected")
        
        try:
            message = {"content": content}
            await self.websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            logger.error("Connection closed, cannot send message")
            self.running = False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def receive_messages(self):
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    msg = Message(**data)
                    self.display_message(msg)
                except json.JSONDecodeError:
                    logger.error("Received invalid JSON")
                except Exception as e:
                    logger.error(f"Error processing received message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed by server")
            self.running = False
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            self.running = False
    
    def display_message(self, msg: Message):
        timestamp = datetime.fromisoformat(msg.timestamp).strftime("%H:%M:%S")
        
        if msg.message_type == "chat":
            print(f"[{timestamp}] {msg.username}: {msg.content}")
        elif msg.message_type == "join":
            print(f"[{timestamp}] >>> {msg.content}")
        elif msg.message_type == "leave":
            print(f"[{timestamp}] <<< {msg.content}")
        elif msg.message_type == "error":
            print(f"[{timestamp}] ERROR: {msg.content}")
    
    async def disconnect(self):
        self.running = False
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected")


# Server usage example
async def run_server():
    server = WebSocketChatServer(host="localhost", port=8765)
    await server.start()


# Client usage example
async def run_client(username: str):
    client = WebSocketChatClient(uri="ws://localhost:8765", username=username)
    
    try:
        await client.connect()
        
        # Start receiving messages in background
        receive_task = asyncio.create_task(client.receive_messages())
        
        # Simulate sending messages
        await client.send_message("Hello everyone!")
        await asyncio.sleep(1)
        await client.send_message("How are you?")
        
        # Wait for messages
        await asyncio.sleep(5)
        
        await client.disconnect()
        receive_task.cancel()
        
    except Exception as e:
        logger.error(f"Client error: {e}")


if __name__ == "__main__":
    # Run server
    # asyncio.run(run_server())
    
    # Run client
    # asyncio.run(run_client("Alice"))
    
    print("WebSocketChat implementation complete")
    print("To run server: asyncio.run(run_server())")
    print("To run client: asyncio.run(run_client('YourName'))")