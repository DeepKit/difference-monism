import pytest
import sys
sys.path.insert(0, '.')
from order_state_machine import OrderStateMachine, OrderState

def test_state_machine():
    sm = OrderStateMachine()
    assert sm is not None
    assert OrderState is not None
