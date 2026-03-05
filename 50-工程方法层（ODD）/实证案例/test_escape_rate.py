"""
缺陷逃逸率测试
用相同测试同时测对照组(defect)和实验组(正确版)
"""
import sys
import pytest
import importlib.util

TEST_DIR = 'D:/_Progs/01Center/ODD/实证案例'

def load_module(name):
    spec = importlib.util.spec_from_file_location(name, f'{TEST_DIR}/{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# 测试用例定义
test_cases = [
    {
        'name': 'T-024 DataMasker',
        'control': 'data_masker_defect',
        'experiment': 'data_masker',
        'test': lambda mod: (
            # 找到主类并实例化
            [getattr(mod, c) for c in dir(mod) if 'Masker' in c][0]().mask_phone('13812345678')
        ),
        'check': lambda result: '*' in str(result),  # 应该包含*
    },
    {
        'name': 'T-036 MemoryCache',
        'control': 'memory_cache_defect',
        'experiment': 'memory_cache',
        'test': lambda mod: (
            # 测试TTL
            (lambda c: (c.set('k', 'v', ttl=0.1), __import__('time').sleep(0.2), c.get('k'))[2])
            ([getattr(mod, c) for c in dir(mod) if 'Cache' in c][0]())
        ),
        'check': lambda result: result is None,  # TTL后应该返回None
    },
    {
        'name': 'T-041 JWT',
        'control': 'jwt_token_defect',
        'experiment': 'jwt_token',
        'test': lambda mod: (
            [getattr(mod, c) for c in dir(mod) if 'JWT' in c or 'Token' in c or 'Manager' in c][0]('secret')
        ),
        'check': lambda result: result is not None,
    },
    {
        'name': 'T-046 OrderStateMachine',
        'control': 'order_state_machine_defect',
        'experiment': 'order_state_machine',
        'test': lambda mod: (
            [getattr(mod, c) for c in dir(mod) if 'StateMachine' in c or c == 'OrderStateMachine'][0]()
        ),
        'check': lambda result: result is not None,
    },
    {
        'name': 'T-045 XSSFilter',
        'control': 'xss_filter_defect',
        'experiment': 'xss_filter',
        'test': lambda mod: (
            (lambda f: getattr(f, 'filter' if hasattr(f, 'filter') else 'clean', lambda x: x)('<script>alert(1)</script>'))
            ([getattr(mod, c) for c in dir(mod) if 'Filter' in c or 'XSS' in c or c == 'XSSFilter'][0]())
        ),
        'check': lambda result: '<script>' not in str(result) and str(result) != '' and str(result) != '[]',
    },
]

print('=' * 60)
print('缺陷逃逸率测试报告')
print('=' * 60)
print()

results = {
    'control_pass_with_defect': [],  # 缺陷代码测试通过(逃逸)
    'control_fail': [],              # 缺陷代码测试失败(发现缺陷)
    'control_error': [],             # 缺陷代码运行错误
    'experiment_pass': [],           # 正确代码测试通过
    'experiment_fail': [],           # 正确代码测试失败
    'experiment_error': [],          # 正确代码运行错误
}

for tc in test_cases:
    print(f"--- {tc['name']} ---")
    
    # 测试对照组(缺陷版)
    try:
        mod = load_module(tc['control'])
        result = tc['test'](mod)
        passed = tc['check'](result)
        if passed:
            results['control_pass_with_defect'].append(tc['name'])
            print(f"  对照组: 测试通过 (缺陷逃逸!)")
        else:
            results['control_fail'].append(tc['name'])
            print(f"  对照组: 测试失败 (缺陷被发现)")
    except Exception as e:
        results['control_error'].append((tc['name'], str(e)[:40]))
        print(f"  对照组: 运行错误 - {str(e)[:40]}")
    
    # 测试实验组(正确版)
    try:
        mod = load_module(tc['experiment'])
        result = tc['test'](mod)
        passed = tc['check'](result)
        if passed:
            results['experiment_pass'].append(tc['name'])
            print(f"  实验组: 测试通过 ✓")
        else:
            results['experiment_fail'].append(tc['name'])
            print(f"  实验组: 测试失败 ✗")
    except Exception as e:
        results['experiment_error'].append((tc['name'], str(e)[:40]))
        print(f"  实验组: 运行错误 - {str(e)[:40]}")
    
    print()

print('=' * 60)
print('统计汇总')
print('=' * 60)
print()

total_control = len([tc['name'] for tc in test_cases])
total_experiment = len([tc['name'] for tc in test_cases])

print(f"对照组(缺陷版):")
print(f"  - 缺陷逃逸(测试通过): {len(results['control_pass_with_defect'])}/{total_control}")
print(f"  - 缺陷发现(测试失败): {len(results['control_fail'])}/{total_control}")
print(f"  - 运行错误: {len(results['control_error'])}/{total_control}")

print()
print(f"实验组(正确版):")
print(f"  - 测试通过: {len(results['experiment_pass'])}/{total_experiment}")
print(f"  - 测试失败: {len(results['experiment_fail'])}/{total_experiment}")
print(f"  - 运行错误: {len(results['experiment_error'])}/{total_experiment}")

print()

# 缺陷逃逸率 = 测试通过但有缺陷的 / 可运行的缺陷代码
testable_control = total_control - len(results['control_error'])
if testable_control > 0:
    escape_rate = len(results['control_pass_with_defect']) / testable_control * 100
    print(f"缺陷逃逸率: {escape_rate:.1f}%")
    print(f"  (缺陷代码测试通过率，越低越好)")
