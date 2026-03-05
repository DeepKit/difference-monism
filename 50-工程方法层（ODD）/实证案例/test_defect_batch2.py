import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 继续测试更多defect模块

# JWT
print('=== JWT Defect ===')
try:
    import jwt_token_defect as jwt_mod
    print(f'Classes: {[c for c in dir(jwt_mod) if not c.startswith("_")]}')  
except:
    pass

# CSV
print('=== CSV Defect ===')
try:
    import csv_exporter_defect as csv_mod
    print(f'Classes: {[c for c in dir(csv_mod) if not c.startswith("_")]}')  
except:
    pass

# 限流
print('=== RateLimiter Defect ===')
try:
    import rate_limiter_v2_defect as rl_mod
    print(f'Classes: {[c for c in dir(rl_mod) if not c.startswith("_")]}')  
except:
    pass

# Order State Machine
print('=== Order State Machine Defect ===')
try:
    import order_state_machine_defect as osm_mod
    print(f'Classes: {[c for c in dir(osm_mod) if not c.startswith("_")]}')  
except:
    pass

print('\n=== 检查XSS filter ===')
try:
    from xss_filter_defect import XSSFilter
    f = XSSFilter()
    result = f.filter('<script>alert(1)</script>')
    print(f'XSS result: [{result}]')
except Exception as e:
    print(f'XSS ERROR: {e}')

print('\n=== 检查Order State Machine ===')
try:
    from order_state_machine_defect import OrderStateMachine, OrderState
    sm = OrderStateMachine()
    print('Order SM: OK')
except Exception as e:
    print(f'Order SM ERROR: {e}')
