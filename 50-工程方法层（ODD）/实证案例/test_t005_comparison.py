"""
T-005 优惠券系统完整对比测试
对照组 vs 实验组
"""
import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

print('=' * 60)
print('T-005 优惠券系统：对照组 vs 实验组 对比测试')
print('=' * 60)
print()

# 测试场景：同一张优惠券被多个用户使用
print('测试场景：一张优惠券(usage_limit=10)被3个不同用户使用')
print()

# ========== 对照组测试 ==========
print('--- 对照组 (coupon_system.py - AI-First) ---')
try:
    from coupon_system import CouponSystem, Coupon, CouponType
    from datetime import datetime, timedelta
    
    cs = CouponSystem()
    coupon = Coupon(
        id='COUPON10',
        type=CouponType.REDUCTION,
        value=10,
        min_amount=100,
        expire_date=datetime.now() + timedelta(days=30)
    )
    cs.add_coupon(coupon)
    
    control_results = []
    for user in ['user1', 'user2', 'user3']:
        result = cs.use_coupon('COUPON10', user, 150)
        control_results.append(result[0])  # (success, error, discount)
        print(f'  {user}使用: {"成功" if result[0] else "失败"}')
    
    control_defect = not all(control_results)  # 如果有失败，说明有缺陷
    if control_defect:
        print('  结论: 存在缺陷 - 优惠券只能用一次！')
    else:
        print('  结论: 正常')
except Exception as e:
    print(f'  错误: {e}')
    control_defect = True

print()

# ========== 实验组测试 ==========
print('--- 实验组 (coupon_system_cf.py - Contract-First) ---')
try:
    from coupon_system_cf import CouponManager, Coupon as CouponCF, DiscountType
    from decimal import Decimal
    
    cm = CouponManager()
    coupon_cf = CouponCF(
        code='COUPON10',
        discount_type=DiscountType.AMOUNT,
        discount_value=Decimal('10'),
        expiry_date=datetime.now() + timedelta(days=30),
        usage_limit=10,
        min_order_amount=Decimal('100')
    )
    cm.add_coupon(coupon_cf)
    
    experiment_results = []
    for user in ['user1', 'user2', 'user3']:
        result = cm.validate_and_apply('COUPON10', Decimal('150'))
        experiment_results.append(result['success'])
        print(f'  {user}使用: {"成功" if result["success"] else "失败"}')
    
    experiment_defect = not all(experiment_results)
    if experiment_defect:
        print('  结论: 存在缺陷')
    else:
        print('  结论: 正常 - 优惠券可被多次使用')
except Exception as e:
    print(f'  错误: {e}')
    experiment_defect = True

print()
print('=' * 60)
print('T-005 对比结果')
print('=' * 60)
print()
print(f'对照组(AI-First):     {"有缺陷" if control_defect else "正常"}')
print(f'实验组(Contract-First): {"有缺陷" if experiment_defect else "正常"}')
print()

if control_defect and not experiment_defect:
    print('结论: Contract-First成功避免了缺陷！')
elif not control_defect and not experiment_defect:
    print('结论: 两者都正常')
elif control_defect and experiment_defect:
    print('结论: 两者都有缺陷')
else:
    print('结论: 实验组有缺陷，对照组正常')
