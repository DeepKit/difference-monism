import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 全面测试所有defect模块
print('=== 全面测试所有Defect模块 ===\n')

import importlib.util

def load_module(name):
    try:
        spec = importlib.util.spec_from_file_location(name, f'D:/_Progs/01Center/ODD/实证案例/{name}.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as e:
        return None, str(e)

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

load_errors = []
for name in defect_modules:
    mod, err = load_module(name)
    if err:
        load_errors.append((name, err))
        print(f'✗ {name}: {err[:60]}')
    else:
        print(f'✓ {name}')

print(f'\n=== 统计 ===')
print(f'加载成功: {len(defect_modules) - len(load_errors)}/{len(defect_modules)}')
print(f'加载失败: {len(load_errors)}')

if load_errors:
    print(f'\n=== 缺陷详情 ===')
    for name, err in load_errors:
        print(f'{name}: {err[:100]}')