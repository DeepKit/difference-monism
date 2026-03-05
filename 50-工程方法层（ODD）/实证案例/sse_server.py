
import asyncio
import time
from typing import Dict, Set, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import json


@dataclass
class SSEClient:
    id: str
    queue: asyncio.Queue
    channels: Set[str]
    connected_at: float


class SSEManager:
    def __init__(self):
        self._clients: Dict[str, SSEClient] = {}
        self._channels: Dict[str, Set[str]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def add_client(self, client_id: str, channels: Optional[Set[str]] = None) -> SSEClient:
        async with self._lock:
            if client_id in self._clients:
                await self.remove_client(client_id)
            
            channels = channels or {"default"}
            client = SSEClient(
                id=client_id,
                queue=asyncio.Queue(),
                channels=channels,
                connected_at=time.time()
            )
            
            self._clients[client_id] = client
            for channel in channels:
                self._channels[channel].add(client_id)
            
            return client

    async def remove_client(self, client_id: str):
        async with self._lock:
            if client_id not in self._clients:
                return
            
            client = self._clients[client_id]
            for channel in client.channels:
                self._channels[channel].discard(client_id)
                if not self._channels[channel]:
                    del self._channels[channel]
            
            del self._clients[client_id]

    async def subscribe_channel(self, client_id: str, channel: str):
        async with self._lock:
            if client_id not in self._clients:
                return
            
            client = self._clients[client_id]
            client.channels.add(channel)
            self._channels[channel].add(client_id)

    async def unsubscribe_channel(self, client_id: str, channel: str):
        async with self._lock:
            if client_id not in self._clients:
                return
            
            client = self._clients[client_id]
            client.channels.discard(channel)
            self._channels[channel].discard(client_id)
            
            if not self._channels[channel]:
                del self._channels[channel]

    async def push_event(
        self,
        event: str,
        data: Any,
        event_id: Optional[str] = None,
        channel: Optional[str] = None,
        client_id: Optional[str] = None
    ):
        message = self._format_sse(event, data, event_id)
        
        if client_id:
            await self._push_to_client(client_id, message)
        elif channel:
            await self._push_to_channel(channel, message)
        else:
            await self._broadcast(message)

    async def _push_to_client(self, client_id: str, message: str):
        async with self._lock:
            if client_id in self._clients:
                await self._clients[client_id].queue.put(message)

    async def _push_to_channel(self, channel: str, message: str):
        async with self._lock:
            if channel in self._channels:
                for client_id in self._channels[channel]:
                    if client_id in self._clients:
                        await self._clients[client_id].queue.put(message)

    async def _broadcast(self, message: str):
        async with self._lock:
            for client in self._clients.values():
                await client.queue.put(message)

    def _format_sse(self, event: str, data: Any, event_id: Optional[str] = None) -> str:
        lines = []
        
        if event_id:
            lines.append(f"id: {event_id}")
        
        lines.append(f"event: {event}")
        
        if isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False)
        
        for line in str(data).split("\n"):
            lines.append(f"data: {line}")
        
        lines.append("")
        return "\n".join(lines) + "\n"

    async def stream(self, client_id: str):
        if client_id not in self._clients:
            return
        
        client = self._clients[client_id]
        
        try:
            while client_id in self._clients:
                try:
                    message = await asyncio.wait_for(client.queue.get(), timeout=30.0)
                    yield message
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            await self.remove_client(client_id)

    def get_client_count(self) -> int:
        return len(self._clients)

    def get_channel_clients(self, channel: str) -> Set[str]:
        return self._channels.get(channel, set()).copy()

    def get_client_channels(self, client_id: str) -> Set[str]:
        if client_id in self._clients:
            return self._clients[client_id].channels.copy()
        return set()
