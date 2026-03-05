
from enum import Enum
from typing import Dict, Set, Callable, Optional
from datetime import datetime


class OrderState(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderStateMachine:
    def __init__(self):
        self.transitions: Dict[OrderState, Set[OrderState]] = {
            OrderState.PENDING: {OrderState.CONFIRMED, OrderState.CANCELLED},
            OrderState.CONFIRMED: {OrderState.PROCESSING, OrderState.CANCELLED},
            OrderState.PROCESSING: {OrderState.SHIPPED, OrderState.CANCELLED},
            OrderState.SHIPPED: {OrderState.DELIVERED, OrderState.CANCELLED},
            OrderState.DELIVERED: {OrderState.REFUNDED},
            OrderState.CANCELLED: set(),
            OrderState.REFUNDED: set(),
        }
        
        self.hooks: Dict[str, Callable] = {}
    
    def can_transition(self, from_state: OrderState, to_state: OrderState) -> bool:
        return to_state in self.transitions.get(from_state, set())
    
    def register_hook(self, event: str, callback: Callable):
        self.hooks[event] = callback
    
    def trigger_hook(self, event: str, order):
        if event in self.hooks:
            self.hooks[event](order)


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = OrderState.PENDING
        self.state_machine = OrderStateMachine()
        self.history = [(OrderState.PENDING, datetime.now())]
    
    def transition_to(self, new_state: OrderState, reason: Optional[str] = None) -> bool:
        if not self.state_machine.can_transition(self.state, new_state):
            raise ValueError(
                f"无法从 {self.state.value} 转换到 {new_state.value}"
            )
        
        old_state = self.state
        self.state = new_state
        self.history.append((new_state, datetime.now(), reason))
        
        self.state_machine.trigger_hook(f"on_{new_state.value}", self)
        
        return True
    
    def confirm(self):
        return self.transition_to(OrderState.CONFIRMED)
    
    def process(self):
        return self.transition_to(OrderState.PROCESSING)
    
    def ship(self):
        return self.transition_to(OrderState.SHIPPED)
    
    def deliver(self):
        return self.transition_to(OrderState.DELIVERED)
    
    def cancel(self, reason: Optional[str] = None):
        return self.transition_to(OrderState.CANCELLED, reason)
    
    def refund(self, reason: Optional[str] = None):
        return self.transition_to(OrderState.REFUNDED, reason)
    
    def get_state(self) -> OrderState:
        return self.state
    
    def get_history(self):
        return self.history
    
    def is_terminal_state(self) -> bool:
        return self.state in {OrderState.DELIVERED, OrderState.CANCELLED, OrderState.REFUNDED}


# 使用示例
if __name__ == "__main__":
    order = Order("ORD-001")
    
    # 注册状态变更钩子
    order.state_machine.register_hook(
        "on_confirmed", 
        lambda o: print(f"订单 {o.order_id} 已确认")
    )
    
    print(f"初始状态: {order.get_state().value}")
    
    order.confirm()
    print(f"当前状态: {order.get_state().value}")
    
    order.process()
    order.ship()
    order.deliver()
    
    print(f"最终状态: {order.get_state().value}")
    print(f"是否为终态: {order.is_terminal_state()}")
