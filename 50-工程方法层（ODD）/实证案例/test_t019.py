import pytest
import sys
sys.path.insert(0, '.')
from sse_server import SSEManager

def test_sse_init():
    mgr = SSEManager()
    assert mgr is not None

def test_sse_add_client():
    mgr = SSEManager()
    client = mgr.add_client("client1")
    assert client is not None