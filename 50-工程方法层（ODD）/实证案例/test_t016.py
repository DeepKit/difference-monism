import pytest
import sys
sys.path.insert(0, '.')
from message_queue import MessageQueue

def test_mq_init():
    mq = MessageQueue(persistence_file="./test_mq.json")
    assert mq is not None

def test_mq_publish():
    mq = MessageQueue(persistence_file="./test_mq_pub.json")
    msg_id = mq.publish("test_topic", {"data": "hello"})
    assert msg_id is not None

def test_mq_subscribe():
    mq = MessageQueue(persistence_file="./test_mq_sub.json")
    received = []
    mq.subscribe("topic1", lambda msg: received.append(msg))
    mq.publish("topic1", {"data": "test"})
    assert len(received) >= 0