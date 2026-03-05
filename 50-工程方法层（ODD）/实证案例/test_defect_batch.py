import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 测试多个defect模块
tests = []

# 1. semaphore - 已有bug: threading.time()

# 2. 检查读写锁
print('=== 测试 rw_lock_defect ===')
try:
    from rw_lock_defect import ReadWriteLock
    lock = ReadWriteLock()
    print('rw_lock: OK')
except Exception as e:
    print(f'rw_lock: ERROR - {e}')

# 3. 检查乐观锁
print('=== 测试 optimistic_lock_defect ===')
try:
    from optimistic_lock_defect import OptimisticLock
    lock = OptimisticLock()
    print('optimistic_lock: OK')
except Exception as e:
    print(f'optimistic_lock: ERROR - {e}')

# 4. 检查悲观锁
print('=== 测试 pessimistic_lock_defect ===')
try:
    from pessimistic_lock_defect import PessimisticLock
    lock = PessimisticLock()
    print('pessimistic_lock: OK')
except Exception as e:
    print(f'pessimistic_lock: ERROR - {e}')

# 5. 检查JWT
print('=== 测试 jwt_token_defect ===')
try:
    from jwt_token_defect import JWTTokenManager
    mgr = JWTTokenManager('secret')
    token = mgr.generate_access_token({'user': 'test'})
    print(f'jwt: OK, token={token[:20]}...')
except Exception as e:
    print(f'jwt: ERROR - {e}')

# 6. 检查CSV
print('=== 测试 csv_exporter_defect ===')
try:
    from csv_exporter_defect import CSVExporter
    exp = CSVExporter()
    print('csv: OK')
except Exception as e:
    print(f'csv: ERROR - {e}')

print('\n=== 发现的缺陷 ===')
print('1. semaphore_defect: threading.time() 错误 - 已确认')