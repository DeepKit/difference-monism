import pytest
from datetime import datetime, timedelta
from coupon_system import Coupon, CouponSystem, CouponType, CouponError


@pytest.fixture
def coupon_system():
    """创建优惠券系统实例"""
    return CouponSystem()


@pytest.fixture
def valid_discount_coupon():
    """创建有效的折扣券（9折）"""
    return Coupon(
        id="DISCOUNT_001",
        type=CouponType.DISCOUNT,
        value=0.9,  # 9折
        min_amount=50.0,
        expire_date=datetime.now() + timedelta(days=30)
    )


@pytest.fixture
def valid_reduction_coupon():
    """创建有效的满减券（满100减10）"""
    return Coupon(
        id="REDUCTION_001",
        type=CouponType.REDUCTION,
        value=10.0,
        min_amount=100.0,
        threshold=100.0,
        expire_date=datetime.now() + timedelta(days=30)
    )


@pytest.fixture
def expired_coupon():
    """创建已过期的优惠券"""
    return Coupon(
        id="EXPIRED_001",
        type=CouponType.DISCOUNT,
        value=0.8,
        min_amount=50.0,
        expire_date=datetime.now() - timedelta(days=1)
    )


class TestCouponValidation:
    """测试优惠券验证功能"""
    
    def test_valid_coupon(self, coupon_system, valid_discount_coupon):
        """测试有效优惠券"""
        coupon_system.add_coupon(valid_discount_coupon)
        valid, error = coupon_system.validate_coupon("DISCOUNT_001", "user_001", 100.0)
        assert valid is True
        assert error is None
    
    def test_expired_coupon(self, coupon_system, expired_coupon):
        """测试过期优惠券"""
        coupon_system.add_coupon(expired_coupon)
        valid, error = coupon_system.validate_coupon("EXPIRED_001", "user_001", 100.0)
        assert valid is False
        assert error == CouponError.EXPIRED
    
    def test_used_coupon(self, coupon_system, valid_discount_coupon):
        """测试已使用的优惠券"""
        coupon_system.add_coupon(valid_discount_coupon)
        valid_discount_coupon.used = True
        valid, error = coupon_system.validate_coupon("DISCOUNT_001", "user_001", 100.0)
        assert valid is False
        assert error == CouponError.USED
    
    def test_min_amount_not_met(self, coupon_system, valid_discount_coupon):
        """测试未达到最低消费金额"""
        coupon_system.add_coupon(valid_discount_coupon)
        valid, error = coupon_system.validate_coupon("DISCOUNT_001", "user_001", 30.0)
        assert valid is False
        assert error == CouponError.MIN_AMOUNT_NOT_MET
    
    def test_invalid_coupon(self, coupon_system):
        """测试不存在的优惠券"""
        valid, error = coupon_system.validate_coupon("INVALID_001", "user_001", 100.0)
        assert valid is False
        assert error == CouponError.INVALID_COUPON
    
    def test_usage_limit_exceeded(self, coupon_system, valid_discount_coupon):
        """测试使用次数限制"""
        coupon_system.add_coupon(valid_discount_coupon)
        # 第一次使用
        coupon_system.use_coupon("DISCOUNT_001", "user_001", 100.0)
        
        # 重置优惠券状态以便再次验证
        valid_discount_coupon.used = False
        
        # 第二次尝试使用
        valid, error = coupon_system.validate_coupon("DISCOUNT_001", "user_001", 100.0)
        assert valid is False
        assert error == CouponError.USAGE_LIMIT_EXCEEDED


class TestDiscountCalculation:
    """测试优惠金额计算"""
    
    def test_discount_coupon_calculation(self, coupon_system, valid_discount_coupon):
        """测试折扣券计算"""
        coupon_system.add_coupon(valid_discount_coupon)
        discount = coupon_system.calculate_discount("DISCOUNT_001", 100.0)
        assert discount == 10.0  # 100 * (1 - 0.9) = 10
    
    def test_reduction_coupon_calculation(self, coupon_system, valid_reduction_coupon):
        """测试满减券计算"""
        coupon_system.add_coupon(valid_reduction_coupon)
        discount = coupon_system.calculate_discount("REDUCTION_001", 150.0)
        assert discount == 10.0


class TestCouponUsage:
    """测试优惠券核销功能"""
    
    def test_successful_discount_coupon_usage(self, coupon_system, valid_discount_coupon):
        """测试成功使用折扣券"""
        coupon_system.add_coupon(valid_discount_coupon)
        success, error, discount = coupon_system.use_coupon("DISCOUNT_001", "user_001", 100.0)
        
        assert success is True
        assert error is None
        assert discount == 10.0
        assert valid_discount_coupon.used is True
        assert "DISCOUNT_001" in coupon_system.user_usage["user_001"]
    
    def test_successful_reduction_coupon_usage(self, coupon_system, valid_reduction_coupon):
        """测试成功使用满减券"""
        coupon_system.add_coupon(valid_reduction_coupon)
        success, error, discount = coupon_system.use_coupon("REDUCTION_001", "user_001", 150.0)
        
        assert success is True
        assert error is None
        assert discount == 10.0
        assert valid_reduction_coupon.used is True
    
    def test_failed_coupon_usage(self, coupon_system, expired_coupon):
        """测试失败的优惠券使用"""
        coupon_system.add_coupon(expired_coupon)
        success, error, discount = coupon_system.use_coupon("EXPIRED_001", "user_001", 100.0)
        
        assert success is False
        assert error == CouponError.EXPIRED.value
        assert discount is None
        assert expired_coupon.used is False
    
    def test_get_final_amount_with_discount(self, coupon_system, valid_discount_coupon):
        """测试获取折扣后的最终金额"""
        coupon_system.add_coupon(valid_discount_coupon)
        success, error, final_amount = coupon_system.get_final_amount(
            "DISCOUNT_001", "user_001", 100.0
        )
        
        assert success is True
        assert error is None
        assert final_amount == 90.0  # 100 - 10
    
    def test_get_final_amount_with_reduction(self, coupon_system, valid_reduction_coupon):
        """测试获取满减后的最终金额"""
        coupon_system.add_coupon(valid_reduction_coupon)
        success, error, final_amount = coupon_system.get_final_amount(
            "REDUCTION_001", "user_001", 150.0
        )
        
        assert success is True
        assert error is None
        assert final_amount == 140.0  # 150 - 10
    
    def test_multiple_users_same_coupon(self, coupon_system):
        """测试多个用户使用同一优惠券（应该失败，因为优惠券只能用一次）"""
        coupon = Coupon(
            id="SHARED_001",
            type=CouponType.DISCOUNT,
            value=0.9,
            min_amount=50.0,
            expire_date=datetime.now() + timedelta(days=30)
        )
        coupon_system.add_coupon(coupon)
        
        # 第一个用户使用
        success1, _, _ = coupon_system.use_coupon("SHARED_001", "user_001", 100.0)
        assert success1 is True
        
        # 第二个用户尝试使用（应该失败，因为优惠券已被使用）
        success2, error2, _ = coupon_system.use_coupon("SHARED_001", "user_002", 100.0)
        assert success2 is False
        assert error2 == CouponError.USED.value


class TestEdgeCases:
    """测试边界情况"""
    
    def test_exact_min_amount(self, coupon_system, valid_discount_coupon):
        """测试刚好达到最低消费金额"""
        coupon_system.add_coupon(valid_discount_coupon)
        success, error, discount = coupon_system.use_coupon("DISCOUNT_001", "user_001", 50.0)
        
        assert success is True
        assert discount == 5.0  # 50 * (1 - 0.9) = 5
    
    def test_zero_final_amount(self, coupon_system):
        """测试最终金额为0的情况"""
        coupon = Coupon(
            id="BIG_REDUCTION",
            type=CouponType.REDUCTION,
            value=100.0,
            min_amount=50.0,
            expire_date=datetime.now() + timedelta(days=30)
        )
        coupon_system.add_coupon(coupon)
        
        success, error, final_amount = coupon_system.get_final_amount(
            "BIG_REDUCTION", "user_001", 80.0
        )
        
        assert success is True
        assert final_amount == 0.0  # max(0, 80 - 100) = 0
    
    def test_high_discount_rate(self, coupon_system):
        """测试高折扣率（1折）"""
        coupon = Coupon(
            id="HIGH_DISCOUNT",
            type=CouponType.DISCOUNT,
            value=0.1,  # 1折
            min_amount=50.0,
            expire_date=datetime.now() + timedelta(days=30)
        )
        coupon_system.add_coupon(coupon)
        
        success, error, final_amount = coupon_system.get_final_amount(
            "HIGH_DISCOUNT", "user_001", 100.0
        )
        
        assert success is True
        assert final_amount == 10.0  # 100 * 0.1 = 10
