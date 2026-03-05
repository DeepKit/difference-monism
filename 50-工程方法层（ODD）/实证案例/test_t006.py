import pytest
from datetime import datetime, timedelta
from order_cancel import (
    Order, User, Coupon, OrderStatus, CancelType,
    OrderCancelService, OrderCancelError
)


@pytest.fixture
def service():
    """创建订单取消服务实例"""
    return OrderCancelService(refund_fee_rate=0.05)


@pytest.fixture
def user():
    """创建测试用户"""
    user = User(user_id="user_001", points=1000)
    coupon = Coupon(coupon_id="coupon_001", discount_amount=50.0)
    user.add_coupon(coupon)
    return user


@pytest.fixture
def pending_order():
    """创建待支付订单"""
    return Order(
        order_id="order_001",
        user_id="user_001",
        original_amount=500.0,
        status=OrderStatus.PENDING_PAYMENT
    )


@pytest.fixture
def paid_order_with_coupon():
    """创建已支付订单（使用了优惠券）"""
    return Order(
        order_id="order_002",
        user_id="user_001",
        original_amount=500.0,
        coupon_discount=50.0,
        final_amount=450.0,
        status=OrderStatus.PAID,
        coupon_id="coupon_001",
        paid_at=datetime.now()
    )


@pytest.fixture
def paid_order_with_points():
    """创建已支付订单（使用了积分）"""
    return Order(
        order_id="order_003",
        user_id="user_001",
        original_amount=500.0,
        points_discount=100.0,
        final_amount=400.0,
        status=OrderStatus.PAID,
        points_used=1000,
        paid_at=datetime.now()
    )


class TestUserCancelOrder:
    """测试用户主动取消订单"""
    
    def test_cancel_pending_order(self, service, user, pending_order):
        """测试取消待支付订单"""
        service.register_user(user)
        service.create_order(pending_order)
        
        result = service.user_cancel_order(pending_order.order_id, "不想要了")
        
        assert result["success"] is True
        assert result["refund_amount"] == 0.0  # 待支付订单无退款
        assert pending_order.status == OrderStatus.CANCELLED
        assert result["message"] == "订单取消成功"
    
    def test_cancel_paid_order_with_fee(self, service, user, paid_order_with_coupon):
        """测试取消已支付订单（扣除手续费）"""
        # 先使用优惠券
        user.use_coupon("coupon_001")
        
        service.register_user(user)
        service.create_order(paid_order_with_coupon)
        
        result = service.user_cancel_order(paid_order_with_coupon.order_id, "不需要了")
        
        assert result["success"] is True
        # 退款金额 = 450 * (1 - 0.05) = 427.5
        assert result["refund_amount"] == 427.5
        assert result["coupon_returned"] is True
        assert result["coupon_id"] == "coupon_001"
        assert paid_order_with_coupon.status == OrderStatus.CANCELLED
        
        # 验证优惠券已返还
        coupon = user.coupons[0]
        assert coupon.is_used is False
    
    def test_cancel_paid_order_with_points(self, service, user, paid_order_with_points):
        """测试取消已支付订单（返还积分）"""
        # 先扣除积分
        user.deduct_points(1000)
        assert user.points == 0
        
        service.register_user(user)
        service.create_order(paid_order_with_points)
        
        result = service.user_cancel_order(paid_order_with_points.order_id)
        
        assert result["success"] is True
        # 退款金额 = 400 * (1 - 0.05) = 380
        assert result["refund_amount"] == 380.0
        assert result["points_returned"] == 1000
        
        # 验证积分已返还
        assert user.points == 1000
    
    def test_cancel_completed_order_fails(self, service, user):
        """测试取消已完成订单失败"""
        completed_order = Order(
            order_id="order_004",
            user_id="user_001",
            original_amount=500.0,
            status=OrderStatus.COMPLETED
        )
        
        service.register_user(user)
        service.create_order(completed_order)
        
        result = service.user_cancel_order(completed_order.order_id)
        
        assert result["success"] is False
        assert "无法取消" in result["error"]
        assert completed_order.status == OrderStatus.COMPLETED
    
    def test_cancel_nonexistent_order(self, service):
        """测试取消不存在的订单"""
        result = service.user_cancel_order("nonexistent_order")
        
        assert result["success"] is False
        assert "订单不存在" in result["error"]


class TestSystemCancelOrder:
    """测试系统自动取消订单"""
    
    def test_cancel_timeout_order(self, service, user):
        """测试取消超时未支付订单"""
        # 创建一个超时的订单
        timeout_order = Order(
            order_id="order_005",
            user_id="user_001",
            original_amount=500.0,
            status=OrderStatus.PENDING_PAYMENT,
            created_at=datetime.now() - timedelta(minutes=35)
        )
        
        service.register_user(user)
        service.create_order(timeout_order)
        
        results = service.system_cancel_timeout_orders(timeout_minutes=30)
        
        assert len(results) == 1
        assert results[0]["success"] is True
        assert results[0]["cancel_type"] == CancelType.SYSTEM_TIMEOUT.value
        assert "超时未支付" in results[0]["reason"]
        assert timeout_order.status == OrderStatus.CANCELLED
    
    def test_cancel_timeout_paid_order_with_full_refund(self, service, user):
        """测试系统取消已支付订单（全额退款）"""
        # 创建一个已支付但被系统取消的订单（模拟特殊情况）
        paid_order = Order(
            order_id="order_006",
            user_id="user_001",
            original_amount=500.0,
            final_amount=500.0,
            status=OrderStatus.PAID,
            paid_at=datetime.now()
        )
        
        service.register_user(user)
        service.create_order(paid_order)
        
        result = service.cancel_order(
            paid_order.order_id, 
            CancelType.SYSTEM_TIMEOUT,
            "系统异常"
        )
        
        assert result["success"] is True
        # 系统取消，全额退款，不扣手续费
        assert result["refund_amount"] == 500.0
    
    def test_no_timeout_orders(self, service, user, pending_order):
        """测试没有超时订单的情况"""
        service.register_user(user)
        service.create_order(pending_order)
        
        results = service.system_cancel_timeout_orders(timeout_minutes=30)
        
        assert len(results) == 0
        assert pending_order.status == OrderStatus.PENDING_PAYMENT


class TestRefundCalculation:
    """测试退款金额计算"""
    
    def test_refund_pending_order(self, service, pending_order):
        """测试待支付订单退款金额"""
        refund = service.calculate_refund_amount(
            pending_order, 
            CancelType.USER_CANCEL
        )
        assert refund == 0.0
    
    def test_refund_paid_order_user_cancel(self, service):
        """测试用户取消已支付订单的退款金额"""
        paid_order = Order(
            order_id="order_007",
            user_id="user_001",
            original_amount=1000.0,
            final_amount=1000.0,
            status=OrderStatus.PAID
        )
        
        refund = service.calculate_refund_amount(
            paid_order, 
            CancelType.USER_CANCEL
        )
        # 1000 * (1 - 0.05) = 950
        assert refund == 950.0
    
    def test_refund_paid_order_system_cancel(self, service):
        """测试系统取消已支付订单的退款金额"""
        paid_order = Order(
            order_id="order_008",
            user_id="user_001",
            original_amount=1000.0,
            final_amount=1000.0,
            status=OrderStatus.PAID
        )
        
        refund = service.calculate_refund_amount(
            paid_order, 
            CancelType.SYSTEM_TIMEOUT
        )
        # 系统取消，全额退款
        assert refund == 1000.0
    
    def test_custom_refund_fee_rate(self):
        """测试自定义退款手续费率"""
        service = OrderCancelService(refund_fee_rate=0.10)  # 10%手续费
        
        paid_order = Order(
            order_id="order_009",
            user_id="user_001",
            original_amount=1000.0,
            final_amount=1000.0,
            status=OrderStatus.PAID
        )
        
        refund = service.calculate_refund_amount(
            paid_order, 
            CancelType.USER_CANCEL
        )
        # 1000 * (1 - 0.10) = 900
        assert refund == 900.0


class TestCouponAndPoints:
    """测试优惠券和积分处理"""
    
    def test_coupon_return(self, service, user, paid_order_with_coupon):
        """测试优惠券返还"""
        # 使用优惠券
        user.use_coupon("coupon_001")
        assert user.coupons[0].is_used is True
        
        service.register_user(user)
        service.create_order(paid_order_with_coupon)
        
        result = service.user_cancel_order(paid_order_with_coupon.order_id)
        
        assert result["coupon_returned"] is True
        assert user.coupons[0].is_used is False
    
    def test_points_return(self, service, user, paid_order_with_points):
        """测试积分返还"""
        original_points = user.points
        user.deduct_points(1000)
        
        service.register_user(user)
        service.create_order(paid_order_with_points)
        
        result = service.user_cancel_order(paid_order_with_points.order_id)
        
        assert result["points_returned"] == 1000
        assert user.points == original_points
    
    def test_order_without_coupon_or_points(self, service, user):
        """测试没有使用优惠券和积分的订单"""
        simple_order = Order(
            order_id="order_010",
            user_id="user_001",
            original_amount=500.0,
            status=OrderStatus.PAID
        )
        
        service.register_user(user)
        service.create_order(simple_order)
        
        result = service.user_cancel_order(simple_order.order_id)
        
        assert result["coupon_returned"] is False
        assert result["coupon_id"] is None
        assert result["points_returned"] == 0


class TestOrderStatus:
    """测试订单状态相关功能"""
    
    def test_order_is_cancellable(self):
        """测试订单是否可取消"""
        pending = Order(
            order_id="o1", user_id="u1", original_amount=100,
            status=OrderStatus.PENDING_PAYMENT
        )
        paid = Order(
            order_id="o2", user_id="u1", original_amount=100,
            status=OrderStatus.PAID
        )
        completed = Order(
            order_id="o3", user_id="u1", original_amount=100,
            status=OrderStatus.COMPLETED
        )
        
        assert pending.is_cancellable() is True
        assert paid.is_cancellable() is True
        assert completed.is_cancellable() is False
    
    def test_order_is_timeout(self):
        """测试订单是否超时"""
        timeout_order = Order(
            order_id="o1", user_id="u1", original_amount=100,
            status=OrderStatus.PENDING_PAYMENT,
            created_at=datetime.now() - timedelta(minutes=35)
        )
        normal_order = Order(
            order_id="o2", user_id="u1", original_amount=100,
            status=OrderStatus.PENDING_PAYMENT,
            created_at=datetime.now() - timedelta(minutes=10)
        )
        paid_order = Order(
            order_id="o3", user_id="u1", original_amount=100,
            status=OrderStatus.PAID,
            created_at=datetime.now() - timedelta(minutes=35)
        )
        
        assert timeout_order.is_timeout(30) is True
        assert normal_order.is_timeout(30) is False
        assert paid_order.is_timeout(30) is False  # 已支付订单不算超时


class TestComplexScenarios:
    """测试复杂场景"""
    
    def test_cancel_order_with_both_coupon_and_points(self, service, user):
        """测试取消同时使用优惠券和积分的订单"""
        # 使用优惠券和积分
        user.use_coupon("coupon_001")
        user.deduct_points(500)
        
        complex_order = Order(
            order_id="order_011",
            user_id="user_001",
            original_amount=1000.0,
            coupon_discount=50.0,
            points_discount=50.0,
            final_amount=900.0,
            status=OrderStatus.PAID,
            coupon_id="coupon_001",
            points_used=500
        )
        
        service.register_user(user)
        service.create_order(complex_order)
        
        result = service.user_cancel_order(complex_order.order_id)
        
        assert result["success"] is True
        # 退款 = 900 * 0.95 = 855
        assert result["refund_amount"] == 855.0
        assert result["coupon_returned"] is True
        assert result["points_returned"] == 500
        
        # 验证优惠券和积分都已返还
        assert user.coupons[0].is_used is False
        assert user.points == 1000  # 原始1000 - 500 + 500
    
    def test_multiple_orders_cancellation(self, service, user):
        """测试批量取消多个订单"""
        orders = []
        for i in range(3):
            order = Order(
                order_id=f"order_{i}",
                user_id="user_001",
                original_amount=100.0 * (i + 1),
                status=OrderStatus.PENDING_PAYMENT,
                created_at=datetime.now() - timedelta(minutes=35)
            )
            orders.append(order)
            service.create_order(order)
        
        service.register_user(user)
        
        results = service.system_cancel_timeout_orders(timeout_minutes=30)
        
        assert len(results) == 3
        for result in results:
            assert result["success"] is True
        
        for order in orders:
            assert order.status == OrderStatus.CANCELLED
