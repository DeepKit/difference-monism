"""
T-016~050 完整对比测试
一次性测试所有35个任务的对照组vs实验组
"""
import sys
import time
import importlib.util
from datetime import datetime, timedelta
from decimal import Decimal

TEST_DIR = 'D:/_Progs/01Center/ODD/实证案例'

def load_module(name):
    try:
        spec = importlib.util.spec_from_file_location(name, f'{TEST_DIR}/{name}.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as e:
        return None, str(e)[:60]

def get_main_class(mod, keywords):
    """获取模块中的主类"""
    for kw in keywords:
        for attr in dir(mod):
            if kw in attr and not attr.startswith('_'):
                return getattr(mod, attr)
    # 返回第一个大写开头的类
    for attr in dir(mod):
        if attr[0].isupper() and not attr.startswith('_') and attr not in ['Any', 'Dict', 'List', 'Optional', 'Set', 'Enum', 'Callable', 'Union', 'Path', 'ABC']:
            return getattr(mod, attr)
    return None

# 定义所有测试用例
test_cases = [
    {
        'id': 'T-016',
        'name': 'MessageQueue',
        'control': 'message_queue_defect',
        'experiment': 'message_queue',
        'test': lambda mod: (
            lambda cls: (cls().publish('t', 'msg') or True) if cls else False
        )(get_main_class(mod, ['Queue', 'Message']))
    },
    {
        'id': 'T-017',
        'name': 'EmailService',
        'control': 'email_service_defect',
        'experiment': 'email_service',
        'test': lambda mod: get_main_class(mod, ['Email', 'Config']) is not None
    },
    {
        'id': 'T-018',
        'name': 'WebSocket',
        'control': 'websocket_manager_defect',
        'experiment': 'websocket_manager',
        'test': lambda mod: get_main_class(mod, ['WebSocket', 'Manager']) is not None
    },
    {
        'id': 'T-019',
        'name': 'SSE',
        'control': 'sse_server_defect',
        'experiment': 'sse_server',
        'test': lambda mod: get_main_class(mod, ['SSE', 'Manager']) is not None
    },
    {
        'id': 'T-020',
        'name': 'Broadcaster',
        'control': 'broadcaster_defect',
        'experiment': 'broadcaster',
        'test': lambda mod: (
            lambda cls: (cls().subscribe('ch', lambda x: None) or True) if cls else False
        )(get_main_class(mod, ['Broadcast', 'Message']))
    },
    {
        'id': 'T-021',
        'name': 'CSVExporter',
        'control': 'csv_exporter_defect',
        'experiment': 'csv_exporter',
        'test': lambda mod: get_main_class(mod, ['CSV', 'Exporter']) is not None
    },
    {
        'id': 'T-022',
        'name': 'ExcelParser',
        'control': 'excel_parser_defect',
        'experiment': 'excel_parser',
        'test': lambda mod: get_main_class(mod, ['Excel', 'Parser']) is not None
    },
    {
        'id': 'T-023',
        'name': 'JSONValidator',
        'control': 'json_validator_defect',
        'experiment': 'json_validator',
        'test': lambda mod: (
            lambda cls: cls({'type': 'object'}).validate({}) if cls else False
        )(get_main_class(mod, ['JSON', 'Validator']))
    },
    {
        'id': 'T-024',
        'name': 'DataMasker',
        'control': 'data_masker_defect',
        'experiment': 'data_masker',
        'test': lambda mod: (
            lambda cls: '*' in str(cls().mask_phone('13812345678')) if cls else False
        )(get_main_class(mod, ['Masker', 'Data']))
    },
    {
        'id': 'T-025',
        'name': 'DataEncryptor',
        'control': 'data_encryptor_defect',
        'experiment': 'data_encryptor',
        'test': lambda mod: get_main_class(mod, ['Encryptor', 'AES', 'Cipher']) is not None
    },
    {
        'id': 'T-026',
        'name': 'TaskScheduler',
        'control': 'task_scheduler_defect',
        'experiment': 'task_scheduler',
        'test': lambda mod: get_main_class(mod, ['Scheduler', 'Cron']) is not None
    },
    {
        'id': 'T-027',
        'name': 'DelayedTask',
        'control': 'delayed_task_defect',
        'experiment': 'delayed_task',
        'test': lambda mod: get_main_class(mod, ['Delay', 'Task']) is not None
    },
    {
        'id': 'T-028',
        'name': 'PeriodicTask',
        'control': 'periodic_task_defect',
        'experiment': 'periodic_task',
        'test': lambda mod: get_main_class(mod, ['Periodic', 'Task']) is not None
    },
    {
        'id': 'T-029',
        'name': 'TaskDependency',
        'control': 'task_dependency_defect',
        'experiment': 'task_dependency',
        'test': lambda mod: get_main_class(mod, ['Dependency', 'Task']) is not None
    },
    {
        'id': 'T-030',
        'name': 'TaskTimeout',
        'control': 'task_timeout_defect',
        'experiment': 'task_timeout',
        'test': lambda mod: get_main_class(mod, ['Timeout', 'Task']) is not None
    },
    {
        'id': 'T-031',
        'name': 'DistributedLock',
        'control': 'distributed_lock_defect',
        'experiment': 'distributed_lock',
        'test': lambda mod: get_main_class(mod, ['Lock', 'Distributed']) is not None
    },
    {
        'id': 'T-032',
        'name': 'OptimisticLock',
        'control': 'optimistic_lock_defect',
        'experiment': 'optimistic_lock',
        'test': lambda mod: get_main_class(mod, ['Optimistic', 'Lock']) is not None
    },
    {
        'id': 'T-033',
        'name': 'PessimisticLock',
        'control': 'pessimistic_lock_defect',
        'experiment': 'pessimistic_lock',
        'test': lambda mod: get_main_class(mod, ['Pessimistic', 'Lock']) is not None
    },
    {
        'id': 'T-034',
        'name': 'Semaphore',
        'control': 'semaphore_defect',
        'experiment': 'semaphore',
        'test': lambda mod: (
            lambda cls: cls(2).acquire() if cls and hasattr(cls(2), 'acquire') else (cls(2).wait() if cls and hasattr(cls(2), 'wait') else False)
        )(get_main_class(mod, ['Semaphore']))
    },
    {
        'id': 'T-035',
        'name': 'RWLock',
        'control': 'rw_lock_defect',
        'experiment': 'rw_lock',
        'test': lambda mod: get_main_class(mod, ['RW', 'Lock', 'ReadWrite']) is not None
    },
    {
        'id': 'T-036',
        'name': 'MemoryCache',
        'control': 'memory_cache_defect',
        'experiment': 'memory_cache',
        'test': lambda mod: (
            lambda cls: (lambda c: (c.set('k', 'v'), c.get('k') == 'v'))(cls()) if cls else False
        )(get_main_class(mod, ['Cache', 'Memory']))
    },
    {
        'id': 'T-037',
        'name': 'DiskCache',
        'control': 'disk_cache_defect',
        'experiment': 'disk_cache',
        'test': lambda mod: get_main_class(mod, ['Cache', 'Disk']) is not None
    },
    {
        'id': 'T-038',
        'name': 'MultiLevelCache',
        'control': 'multi_level_cache_defect',
        'experiment': 'multi_level_cache',
        'test': lambda mod: get_main_class(mod, ['Cache', 'Multi', 'Level']) is not None
    },
    {
        'id': 'T-039',
        'name': 'CacheWarming',
        'control': 'cache_warming_defect',
        'experiment': 'cache_warming',
        'test': lambda mod: get_main_class(mod, ['Warming', 'Cache']) is not None
    },
    {
        'id': 'T-040',
        'name': 'CacheInvalidation',
        'control': 'cache_invalidation_defect',
        'experiment': 'cache_invalidation',
        'test': lambda mod: get_main_class(mod, ['Invalidation', 'Cache']) is not None
    },
    {
        'id': 'T-041',
        'name': 'JWT',
        'control': 'jwt_token_defect',
        'experiment': 'jwt_token',
        'test': lambda mod: (
            lambda cls: cls('secret') is not None if cls else False
        )(get_main_class(mod, ['JWT', 'Token', 'Manager']))
    },
    {
        'id': 'T-042',
        'name': 'APISignature',
        'control': 'api_signature_defect',
        'experiment': 'api_signature',
        'test': lambda mod: get_main_class(mod, ['Signature', 'API']) is not None
    },
    {
        'id': 'T-043',
        'name': 'RateLimiter',
        'control': 'rate_limiter_v2_defect',
        'experiment': 'rate_limiter_v2',
        'test': lambda mod: get_main_class(mod, ['Rate', 'Limiter']) is not None
    },
    {
        'id': 'T-044',
        'name': 'CSRF',
        'control': 'csrf_protector_defect',
        'experiment': 'csrf_protector',
        'test': lambda mod: get_main_class(mod, ['CSRF', 'Protector']) is not None
    },
    {
        'id': 'T-045',
        'name': 'XSS',
        'control': 'xss_filter_defect',
        'experiment': 'xss_filter',
        'test': lambda mod: (
            lambda cls: (lambda f: getattr(f, 'filter', lambda x: x)('<script>test</script>'))(cls()) if cls else ''
        )(get_main_class(mod, ['XSS', 'Filter']))
    },
    {
        'id': 'T-046',
        'name': 'OrderStateMachine',
        'control': 'order_state_machine_defect',
        'experiment': 'order_state_machine',
        'test': lambda mod: get_main_class(mod, ['Order', 'State', 'Machine']) is not None
    },
    {
        'id': 'T-047',
        'name': 'WorkflowEngine',
        'control': 'workflow_engine_defect',
        'experiment': 'workflow_engine',
        'test': lambda mod: get_main_class(mod, ['Workflow', 'Engine']) is not None
    },
    {
        'id': 'T-048',
        'name': 'RulesEngine',
        'control': 'rules_engine_defect',
        'experiment': 'rules_engine',
        'test': lambda mod: get_main_class(mod, ['Rule', 'Engine']) is not None
    },
    {
        'id': 'T-049',
        'name': 'MetricsCalculator',
        'control': 'metrics_calculator_defect',
        'experiment': 'metrics_calculator',
        'test': lambda mod: get_main_class(mod, ['Metrics', 'Calculator']) is not None
    },
    {
        'id': 'T-050',
        'name': 'ReportGenerator',
        'control': 'report_generator_defect',
        'experiment': 'report_generator',
        'test': lambda mod: get_main_class(mod, ['Report', 'Generator']) is not None
    },
]

print('=' * 70)
print('T-016~050 完整对比测试报告')
print('=' * 70)
print()

results = []
stats = {
    'control_ok': 0,
    'control_error': 0,
    'experiment_ok': 0,
    'experiment_error': 0,
    'both_ok': 0,
    'control_only_error': 0,
    'experiment_only_ok': 0,
}

for tc in test_cases:
    # 测试对照组
    mod_c, err_c = load_module(tc['control'])
    if mod_c and not err_c:
        try:
            result_c = tc['test'](mod_c)
            control_ok = bool(result_c)
        except Exception as e:
            control_ok = False
            err_c = str(e)[:40]
    else:
        control_ok = False
    
    # 测试实验组
    mod_e, err_e = load_module(tc['experiment'])
    if mod_e and not err_e:
        try:
            result_e = tc['test'](mod_e)
            experiment_ok = bool(result_e)
        except Exception as e:
            experiment_ok = False
            err_e = str(e)[:40]
    else:
        experiment_ok = False
    
    # 统计
    if control_ok:
        stats['control_ok'] += 1
    else:
        stats['control_error'] += 1
    
    if experiment_ok:
        stats['experiment_ok'] += 1
    else:
        stats['experiment_error'] += 1
    
    if control_ok and experiment_ok:
        stats['both_ok'] += 1
    elif not control_ok and experiment_ok:
        stats['experiment_only_ok'] += 1
    elif not control_ok:
        stats['control_only_error'] += 1
    
    # 记录结果
    results.append({
        'id': tc['id'],
        'name': tc['name'],
        'control': control_ok,
        'experiment': experiment_ok,
        'control_err': err_c,
        'experiment_err': err_e,
    })
    
    # 输出
    c_sym = '✓' if control_ok else '✗'
    e_sym = '✓' if experiment_ok else '✗'
    status = ''
    if not control_ok and experiment_ok:
        status = ' ← 对照组有缺陷'
    elif control_ok and not experiment_ok:
        status = ' ← 实验组有缺陷'
    print(f"{tc['id']} {tc['name']:20s} 对照组:{c_sym} 实验组:{e_sym}{status}")

print()
print('=' * 70)
print('统计汇总')
print('=' * 70)
print()
print(f'对照组(缺陷版):  通过 {stats["control_ok"]}/35  ({stats["control_ok"]/35*100:.1f}%)')
print(f'实验组(正确版):  通过 {stats["experiment_ok"]}/35  ({stats["experiment_ok"]/35*100:.1f}%)')
print()
print(f'两者都通过: {stats["both_ok"]}/35')
print(f'仅实验组通过(对照组有缺陷): {stats["experiment_only_ok"]}/35')
print(f'仅对照组失败: {stats["control_only_error"]}/35')

print()
print('=' * 70)
print('结论')
print('=' * 70)
print()

defect_rate = (35 - stats['control_ok']) / 35 * 100
experiment_success_rate = stats['experiment_ok'] / 35 * 100

print(f'对照组缺陷率: {defect_rate:.1f}%')
print(f'实验组成功率: {experiment_success_rate:.1f}%')
print()

if stats['experiment_only_ok'] > 0:
    print(f'✓ Contract-First 在 {stats["experiment_only_ok"]} 个任务上优于 AI-First')

# 写入结果文件
with open(f'{TEST_DIR}/test_results.txt', 'w', encoding='utf-8') as f:
    f.write('T-016~050 对比测试结果\n')
    f.write('=' * 50 + '\n\n')
    for r in results:
        f.write(f"{r['id']} {r['name']}: 对照组={'OK' if r['control'] else 'FAIL'} 实验组={'OK' if r['experiment'] else 'FAIL'}\n")
    f.write(f'\n对照组通过率: {stats["control_ok"]/35*100:.1f}%\n')
    f.write(f'实验组通过率: {stats["experiment_ok"]/35*100:.1f}%\n')

print('结果已保存到 test_results.txt')
