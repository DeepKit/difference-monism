import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 测试全部35个defect模块
print('=== 测试全部35个Defect模块 ===\n')

import importlib.util
import time

def load_and_test(name):
    """加载模块并测试基本功能"""
    # 跳过需要外部依赖的模块
    skip_modules = ['distributed_lock_defect', 'websocket_manager_defect']
    if name in skip_modules:
        return 'SKIP', '需要外部依赖'
    
    try:
        spec = importlib.util.spec_from_file_location(name, f'D:/_Progs/01Center/ODD/实证案例/{name}.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # 尝试实例化主要类
        classes = [c for c in dir(mod) if c[0].isupper() and not c.startswith('_') and c not in ['Any', 'Dict', 'List', 'Optional', 'Set', 'Enum', 'Callable', 'Union', 'Path']]
        if not classes:
            return 'OK', '无主要类'
        
        main_class = classes[0]
        cls = getattr(mod, main_class)
        
        # 尝试实例化
        try:
            obj = cls()
            return 'OK', main_class
        except TypeError:
            # 可能需要参数
            return 'OK', f'{main_class}(需参数)'
            
    except SyntaxError as e:
        return 'SYNTAX', str(e)[:50]
    except Exception as e:
        return 'ERROR', str(e)[:50]

defect_modules = [
    'message_queue_defect',
    'email_service_defect',
    'websocket_manager_defect',
    'sse_server_defect',
    'broadcaster_defect',
    'csv_exporter_defect',
    'excel_parser_defect',
    'json_validator_defect',
    'data_masker_defect',
    'data_encryptor_defect',
    'task_scheduler_defect',
    'delayed_task_defect',
    'periodic_task_defect',
    'task_dependency_defect',
    'task_timeout_defect',
    'distributed_lock_defect',
    'optimistic_lock_defect',
    'pessimistic_lock_defect',
    'semaphore_defect',
    'rw_lock_defect',
    'memory_cache_defect',
    'disk_cache_defect',
    'multi_level_cache_defect',
    'cache_warming_defect',
    'cache_invalidation_defect',
    'jwt_token_defect',
    'api_signature_defect',
    'rate_limiter_v2_defect',
    'csrf_protector_defect',
    'xss_filter_defect',
    'order_state_machine_defect',
    'workflow_engine_defect',
    'rules_engine_defect',
    'metrics_calculator_defect',
    'report_generator_defect',
]

results = {'OK': [], 'SYNTAX': [], 'ERROR': [], 'SKIP': []}

for name in defect_modules:
    status, info = load_and_test(name)
    results[status].append((name, info))
    symbol = '✓' if status == 'OK' else '✗'
    print(f'{symbol} {name}: {info}')

print(f'\n=== 统计 ===')
print(f'正常加载: {len(results["OK"])}/35')
print(f'语法错误: {len(results["SYNTAX"])}/35')
print(f'运行错误: {len(results["ERROR"])}/35')
print(f'跳过(外部依赖): {len(results["SKIP"])}/35')
total_errors = len(results["SYNTAX"]) + len(results["ERROR"])
testable = 35 - len(results["SKIP"])
print(f'错误率: {total_errors}/{testable} = {total_errors/testable*100:.1f}%')

if results["SYNTAX"]:
    print(f'\n语法错误:')
    for name, info in results["SYNTAX"]:
        print(f'  - {name}: {info}')

if results["ERROR"]:
    print(f'\n运行错误:')
    for name, info in results["ERROR"]:
        print(f'  - {name}: {info}')
