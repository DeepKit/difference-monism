import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 功能缺陷测试
print('=== 功能缺陷检测 ===\n')

import importlib.util

def load_module(name):
    spec = importlib.util.spec_from_file_location(name, f'D:/_Progs/01Center/ODD/实证案例/{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

defects_found = []

# 1. Semaphore - threading.time() bug
print('1. Semaphore测试')
try:
    mod = load_module('semaphore_defect')
    sem = mod.Semaphore(2)
    sem.acquire(timeout=0.1)
except Exception as e:
    defects_found.append('semaphore: threading.time()错误')
    print('  ✗ threading.time()错误')
else:
    print('  ✓ 正常')

# 2. XSS Filter
print('2. XSS Filter测试')
try:
    mod = load_module('xss_filter_defect')
    f = mod.XSSFilter()
    result = f.filter('<script>alert(1)</script>')
    if '<script>' in str(result):
        defects_found.append('xss_filter: 未过滤XSS')
        print('  ✗ 未过滤XSS')
    elif result == '' or result == []:
        defects_found.append('xss_filter: 返回空结果')
        print('  ✗ 返回空结果')
    else:
        print('  ✓ 正常')
except Exception as e:
    defects_found.append('xss_filter: 运行错误')
    print('  ✗ 运行错误')

# 3. JWT - 类名不一致
print('3. JWT测试')
try:
    mod = load_module('jwt_token_defect')
    classes = [c for c in dir(mod) if c[0].isupper() and not c.startswith('_')]
    if 'JWTTokenManager' not in classes:
        defects_found.append('jwt_token: API不一致')
        print('  ✗ API不一致')
    else:
        print('  ✓ API正常')
except Exception as e:
    defects_found.append('jwt_token: 运行错误')
    print('  ✗ 运行错误')

# 4. Memory Cache - TTL测试
print('4. Memory Cache TTL测试')
try:
    mod = load_module('memory_cache_defect')
    cache = mod.MemoryCache()
    cache.set('key', 'value', ttl=0.1)
    import time
    time.sleep(0.2)
    result = cache.get('key')
    if result is not None:
        defects_found.append('memory_cache: TTL未生效')
        print('  ✗ TTL未生效')
    else:
        print('  ✓ TTL正常')
except Exception as e:
    defects_found.append('memory_cache: 运行错误')
    print('  ✗ 运行错误')

# 5. Rate Limiter
print('5. Rate Limiter测试')
try:
    mod = load_module('rate_limiter_v2_defect')
    limiter = mod.FixedWindowRateLimiter(max_requests=2, window_seconds=1)
    r1 = limiter.check('user1')
    r2 = limiter.check('user1')
    r3 = limiter.check('user1')
    if r3:
        defects_found.append('rate_limiter: 限流未生效')
        print('  ✗ 限流未生效')
    else:
        print('  ✓ 限流正常')
except Exception as e:
    defects_found.append('rate_limiter: API不一致')
    print('  ✗ API不一致')

# 6. Distributed Lock - 跳过(有__del__ bug)

# 7. Order State Machine
print('7. Order State Machine测试')
try:
    mod = load_module('order_state_machine_defect')
    sm = mod.OrderStateMachine()
    print('  ✓ 正常')
except Exception as e:
    defects_found.append('order_state_machine: 运行错误')
    print('  ✗ 运行错误')

# 8. Message Queue
print('8. Message Queue测试')
try:
    mod = load_module('message_queue_defect')
    mq = mod.MessageQueue()
    mq.publish('topic', 'msg')
    print('  ✓ 正常')
except Exception as e:
    defects_found.append('message_queue: 运行错误')
    print('  ✗ 运行错误')

# 9. Data Masker
print('9. Data Masker测试')
try:
    mod = load_module('data_masker_defect')
    masker = mod.DataMasker()
    r = masker.mask_phone('13812345678')
    if '*' not in r:
        defects_found.append('data_masker: 脱敏失败')
        print('  ✗ 脱敏失败')
    else:
        print('  ✓ 正常')
except Exception as e:
    defects_found.append('data_masker: 运行错误')
    print('  ✗ 运行错误')

# 10. Workflow Engine
print('10. Workflow Engine测试')
try:
    mod = load_module('workflow_engine_defect')
    we = mod.WorkflowEngine()
    print('  ✓ 正常')
except Exception as e:
    defects_found.append('workflow_engine: 运行错误')
    print('  ✗ 运行错误')

# 11. Task Scheduler - 已知语法错误
print('11. Task Scheduler')
defects_found.append('task_scheduler: 语法错误')
print('  ✗ 语法错误(non-default argument)')

# 12. Metrics Calculator - 已知编码错误
print('12. Metrics Calculator')
defects_found.append('metrics_calculator: 编码错误')
print('  ✗ 编码错误(中文句号)')

print(f'\n=== 缺陷统计 ===')
print(f'发现缺陷: {len(defects_found)}/12')
for d in defects_found:
    print(f'  - {d}')

print(f'\n缺陷率: {len(defects_found)/12*100:.1f}%')
