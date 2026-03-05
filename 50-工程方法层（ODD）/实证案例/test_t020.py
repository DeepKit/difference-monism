import pytest
import sys
sys.path.insert(0, '.')
from broadcaster import MessageBroadcaster

def test_broadcaster_init():
    bc = MessageBroadcaster()
    assert bc is not None

def test_broadcaster_subscribe():
    bc = MessageBroadcaster()
    received = []
    bc.subscribe("channel1", lambda m: received.append(m))
    bc.publish("channel1", "test message")
    assert len(received) == 1

def test_broadcaster_unsubscribe():
    bc = MessageBroadcaster()
    received = []
    def handler(m): received.append(m)
    bc.subscribe("ch1", handler)
    bc.unsubscribe("ch1", handler)
    bc.publish("ch1", "msg")
    assert len(received) == 0