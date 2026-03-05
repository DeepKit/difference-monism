from datetime import datetime, timedelta
from enum import Enum
from typing import Dict
from dataclasses import dataclass


class OrderStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


@dataclass
class Order:
    order_id: str
    user_id: str
    amount: float
    points_used: int
    created_at: datetime
    status: OrderStatus


class OrderCancellationResult:
    def __init__(self, success: bool, message: str, refund_amount: float = 0, refund_points: int = 0):
        self.success = success
        self.message = message
        self.refund_amount = refund_amount
        self.refund_points = refund_points


class OrderService:
    def __init__(self):
        self.orders: Dict[str, Order] = {}
    
    def create_order(self, order_id: str, user_id: str, amount: float, points_used: int) -> Order:
        order = Order(order_id=order_id, user_id=user_id, amount=amount, points_used=points_used, created_at=datetime.now(), status=OrderStatus.ACTIVE)
        self.orders[order_id] = order
        return order
    
    def cancel_order(self, order_id: str, user_id: str) -> OrderCancellationResult:
        if order_id not in self.orders:
            return OrderCancellationResult(success=False, message="订单不存在")
        
        order = self.orders[order_id]
        
        if order.user_id != user_id:
            return OrderCancellationResult(success=False, message="无权取消此订单")
        
        if order.status == OrderStatus.CANCELLED:
            return OrderCancellationResult(success=False, message="订单已取消，不能重复取消")
        
        refund_amount = self._calculate_refund(order)
        refund_points = order.points_used
        order.status = OrderStatus.CANCELLED
        
        return OrderCancellationResult(success=True, message="订单取消成功", refund_amount=refund_amount, refund_points=refund_points)
    
    def _calculate_refund(self, order: Order) -> float:
        time_elapsed = datetime.now() - order.created_at
        if time_elapsed <= timedelta(hours=24):
            return order.amount
        return order.amount * 0.9
