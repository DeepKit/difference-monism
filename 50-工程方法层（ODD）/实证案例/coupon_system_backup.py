from enum import Enum
from datetime import datetime
from typing import Dict, Optional
from decimal import Decimal


class DiscountType(Enum):
    AMOUNT = "amount"
    PERCENTAGE = "percentage"


class Coupon:
    def __init__(self, code: str, discount_type: DiscountType, discount_value: Decimal, expiry_date: datetime, usage_limit: int, min_order_amount: Decimal = Decimal('0')):
        self.code = code
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.expiry_date = expiry_date
        self.usage_limit = usage_limit
        self.min_order_amount = min_order_amount
        self.usage_count = 0
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expiry_date
    
    def is_usage_limit_reached(self) -> bool:
        return self.usage_count >= self.usage_limit
    
    def meets_min_order_amount(self, order_amount: Decimal) -> bool:
        return order_amount >= self.min_order_amount
    
    def calculate_discount(self, order_amount: Decimal) -> Decimal:
        if self.discount_type == DiscountType.AMOUNT:
            return min(self.discount_value, order_amount)
        else:
            return order_amount * (self.discount_value / Decimal('100'))
    
    def use(self):
        self.usage_count += 1


class CouponManager:
    def __init__(self):
        self.coupons: Dict[str, Coupon] = {}
    
    def add_coupon(self, coupon: Coupon):
        self.coupons[coupon.code] = coupon
    
    def validate_and_apply(self, code: str, order_amount: Decimal) -> Dict:
        if code not in self.coupons:
            return {'success': False, 'discount_amount': Decimal('0'), 'message': '优惠券不存在'}
        
        coupon = self.coupons[code]
        
        if coupon.is_expired():
            return {'success': False, 'discount_amount': Decimal('0'), 'message': '优惠券已过期'}
        
        if coupon.is_usage_limit_reached():
            return {'success': False, 'discount_amount': Decimal('0'), 'message': '优惠券使用次数已达上限'}
        
        if not coupon.meets_min_order_amount(order_amount):
            return {'success': False, 'discount_amount': Decimal('0'), 'message': f'订单金额未达到最低要求 {coupon.min_order_amount}'}
        
        discount_amount = coupon.calculate_discount(order_amount)
        coupon.use()
        
        return {'success': True, 'discount_amount': discount_amount, 'message': '优惠券应用成功'}
    
    def get_coupon(self, code: str) -> Optional[Coupon]:
        return self.coupons.get(code)
