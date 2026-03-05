from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field


class CouponType(Enum):
    """优惠券类型"""
    DISCOUNT = "discount"
    REDUCTION = "reduction"


class CouponError(Enum):
    """优惠券错误类型"""
    EXPIRED = "优惠券已过期"
    USED = "优惠券已使用"
    MIN_AMOUNT_NOT_MET = "未达到最低消费金额"
    USAGE_LIMIT_EXCEEDED = "已达到使用次数限制"
    INVALID_COUPON = "优惠券不存在"


@dataclass
class Coupon:
    """优惠券"""
    id: str
    type: CouponType
    value: float  # 折扣率(0-1)或满减金额
    min_amount: float
    expire_date: datetime
    used: bool = False
    threshold: Optional[float] = None  # 满减门槛
    
    def __post_init__(self):
        if self.type == CouponType.REDUCTION and self.threshold is None:
            self.threshold = self.min_amount


@dataclass
class CouponSystem:
    """优惠券核销系统"""
    coupons: Dict[str, Coupon] = field(default_factory=dict)
    user_usage: Dict[str, set] = field(default_factory=dict)  # {user_id: {coupon_ids}}
    
    def add_coupon(self, coupon: Coupon) -> None:
        self.coupons[coupon.id] = coupon
    
    def validate_coupon(self, coupon_id: str, user_id: str, order_amount: float) -> Tuple[bool, Optional[CouponError]]:
        if coupon_id not in self.coupons:
            return False, CouponError.INVALID_COUPON
        
        coupon = self.coupons[coupon_id]
        
        if coupon.used:
            return False, CouponError.USED
        
        if datetime.now() > coupon.expire_date:
            return False, CouponError.EXPIRED
        
        if order_amount < coupon.min_amount:
            return False, CouponError.MIN_AMOUNT_NOT_MET
        
        # BUG: 只检查用户是否使用过该优惠券，没有检查优惠券的全局使用次数限制！
        # 这个实现允许同一个优惠券被多个不同用户无限次使用
        if user_id in self.user_usage and coupon_id in self.user_usage[user_id]:
            return False, CouponError.USAGE_LIMIT_EXCEEDED
        
        return True, None
    
    def calculate_discount(self, coupon_id: str, order_amount: float) -> float:
        coupon = self.coupons[coupon_id]
        
        if coupon.type == CouponType.DISCOUNT:
            # 折扣券：0.9表示9折，应付90%，减免10%
            discount = order_amount * (1 - coupon.value)
        else:
            # 满减券：直接减免
            discount = coupon.value
        
        return round(discount, 2)
    
    def get_final_amount(self, coupon_id: str, user_id: str, order_amount: float) -> Tuple[bool, Optional[str], float]:
        if coupon_id not in self.coupons:
            return False, "优惠券不存在", 0.0
        
        valid, error = self.validate_coupon(coupon_id, user_id, order_amount)
        if not valid:
            return False, error.value if error else "验证失败", order_amount
        
        discount = self.calculate_discount(coupon_id, order_amount)
        final_amount = max(0, round(order_amount - discount, 2))  # 确保不为负数
        return True, None, final_amount
    
    def use_coupon(self, coupon_id: str, user_id: str, order_amount: float) -> Tuple[bool, Optional[str], Optional[float]]:
        valid, error = self.validate_coupon(coupon_id, user_id, order_amount)
        
        if not valid:
            return False, error.value if error else "未知错误", None
        
        discount = self.calculate_discount(coupon_id, order_amount)
        
        # 标记优惠券已使用（BUG：这是全局标记，导致优惠券只能使用一次！）
        self.coupons[coupon_id].used = True
        
        # 记录用户使用
        if user_id not in self.user_usage:
            self.user_usage[user_id] = set()
        self.user_usage[user_id].add(coupon_id)
        
        # 返回优惠金额
        return True, None, discount
    
    def get_available_coupons(self, user_id: str, order_amount: float) -> list:
        available = []
        for coupon in self.coupons.values():
            if (not coupon.used and 
                datetime.now() <= coupon.expire_date and 
                order_amount >= coupon.min_amount):
                if user_id not in self.user_usage or coupon.id not in self.user_usage[user_id]:
                    available.append(coupon)
        return available
