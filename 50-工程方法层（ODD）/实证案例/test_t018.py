import pytest
import sys
sys.path.insert(0, '.')
from websocket_manager import WebSocketManager

def test_ws_init():
    mgr = WebSocketManager("ws://localhost:8080")
    assert mgr.url == "ws://localhost:8080"
