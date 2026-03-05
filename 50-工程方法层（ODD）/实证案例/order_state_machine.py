
from enum import Enum
from typing import Dict, List, Callable, Optional
from datetime import datetime


class OrderState(Enum):
    """订单状态"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderEvent(Enum):
    """订单事件"""
    PAY = "pay"
    SHIP = "ship"
    DELIVER = "deliver"
    COMPLETE = "complete"
    CANCEL = "cancel"
    REFUND = "refund"


class OrderStateMachine:
    """订单状态机"""
    
    def __init__(self, order_id: str, initial_state: OrderState = OrderState.PENDING):
        self.order_id = order_id
        self.current_state = initial_state
        self.state_history: List[Dict] = [{
            "state": initial_state,
            "timestamp": datetime.now(),
            "event": None
        }]
        
        # 定义状态转换规则
        self.transitions: Dict[OrderState, Dict[OrderEvent, OrderState]] = {
            OrderState.PENDING: {
                OrderEvent.PAY: OrderState.PAID,
                OrderEvent.CANCEL: OrderState.CANCELLED
            },
            OrderState.PAID: {
                OrderEvent.SHIP: OrderState.SHIPPED,
                OrderEvent.CANCEL: OrderState.CANCELLED,
                OrderEvent.REFUND: OrderState.REFUNDED
            },
            OrderState.SHIPPED: {
                OrderEvent.DELIVER: OrderState.DELIVERED,
                OrderEvent.REFUND: OrderState.REFUNDED
            },
            OrderState.DELIVERED: {
                OrderEvent.COMPLETE: OrderState.COMPLETED,
                OrderEvent.REFUND: OrderState.REFUNDED
            },
            OrderState.COMPLETED: {},
            OrderState.CANCELLED: {},
            OrderState.REFUNDED: {}
        }
        
        # 事件回调函数
        self.event_callbacks: Dict[OrderEvent, List[Callable]] = {
            event: [] for event in OrderEvent
        }
        
        # 状态进入回调函数
        self.state_enter_callbacks: Dict[OrderState, List[Callable]] = {
            state: [] for state in OrderState
        }
        
        # 状态退出回调函数
        self.state_exit_callbacks: Dict[OrderState, List[Callable]] = {
            state: [] for state in OrderState
        }
    
    def trigger(self, event: OrderEvent, **kwargs) -> bool:
        """触发事件"""
        if self.current_state not in self.transitions:
            raise ValueError(f"Invalid current state: {self.current_state}")
        
        allowed_events = self.transitions[self.current_state]
        
        if event not in allowed_events:
            raise ValueError(
                f"Event {event.value} not allowed in state {self.current_state.value}. "
                f"Allowed events: {[e.value for e in allowed_events.keys()]}"
            )
        
        old_state = self.current_state
        new_state = allowed_events[event]
        
        # 执行状态退出回调
        self._execute_callbacks(self.state_exit_callbacks.get(old_state, []), old_state, new_state, event, **kwargs)
        
        # 执行事件回调
        self._execute_callbacks(self.event_callbacks.get(event, []), old_state, new_state, event, **kwargs)
        
        # 更新状态
        self.current_state = new_state
        
        # 记录历史
        self.state_history.append({
            "state": new_state,
            "timestamp": datetime.now(),
            "event": event,
            "from_state": old_state,
            "metadata": kwargs
        })
        
        # 执行状态进入回调
        self._execute_callbacks(self.state_enter_callbacks.get(new_state, []), old_state, new_state, event, **kwargs)
        
        return True
    
    def _execute_callbacks(self, callbacks: List[Callable], old_state: OrderState, 
                          new_state: OrderState, event: OrderEvent, **kwargs):
        """执行回调函数"""
        for callback in callbacks:
            callback(
                order_id=self.order_id,
                old_state=old_state,
                new_state=new_state,
                event=event,
                **kwargs
            )
    
    def on_event(self, event: OrderEvent, callback: Callable):
        """注册事件回调"""
        self.event_callbacks[event].append(callback)
    
    def on_enter_state(self, state: OrderState, callback: Callable):
        """注册状态进入回调"""
        self.state_enter_callbacks[state].append(callback)
    
    def on_exit_state(self, state: OrderState, callback: Callable):
        """注册状态退出回调"""
        self.state_exit_callbacks[state].append(callback)
    
    def can_trigger(self, event: OrderEvent) -> bool:
        """检查是否可以触发事件"""
        return event in self.transitions.get(self.current_state, {})
    
    def get_allowed_events(self) -> List[OrderEvent]:
        """获取当前状态允许的事件"""
        return list(self.transitions.get(self.current_state, {}).keys())
    
    def get_state_history(self) -> List[Dict]:
        """获取状态历史"""
        return self.state_history.copy()
    
    def is_final_state(self) -> bool:
        """检查是否为最终状态"""
        return self.current_state in [OrderState.COMPLETED, OrderState.CANCELLED, OrderState.REFUNDED]


# 使用示例
if __name__ == "__main__":
    # 创建订单状态机
    order = OrderStateMachine("ORDER-001")
    
    # 注册回调
    def on_payment(order_id, old_state, new_state, event, **kwargs):
        print(f"订单 {order_id} 支付成功: {old_state.value} -> {new_state.value}")
    
    def on_shipped(order_id, old_state, new_state, event, **kwargs):
        print(f"订单 {order_id} 已发货: {old_state.value} -> {new_state.value}")
    
    order.on_event(OrderEvent.PAY, on_payment)
    order.on_enter_state(OrderState.SHIPPED, on_shipped)
    
    # 状态流转
    print(f"当前状态: {order.current_state.value}")
    print(f"允许的事件: {[e.value for e in order.get_allowed_events()]}")
    
    order.trigger(OrderEvent.PAY, amount=100.0, payment_method="credit_card")
    print(f"当前状态: {order.current_state.value}")
    
    order.trigger(OrderEvent.SHIP, tracking_number="TRACK123")
    print(f"当前状态: {order.current_state.value}")
    
    order.trigger(OrderEvent.DELIVER)
    print(f"当前状态: {order.current_state.value}")
    
    order.trigger(OrderEvent.COMPLETE)
    print(f"当前状态: {order.current_state.value}")
    print(f"是否为最终状态: {order.is_final_state()}")
    
    # 查看历史
    print("\n状态历史:")
    for record in order.get_state_history():
        print(f"  {record}")
