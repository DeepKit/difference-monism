"""
ODD实证实验运行器
支持对照组(AI-First)和实验组(Contract-First)的切换测试
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# 任务映射：测试文件 -> (对照组实现, 实验组实现, 主要类名)
TASK_MAP = {
    "test_t001": {
        "control": "user_registration.py",
        "experiment": "user_registration_cf.py",
        "import_class": "UserRegistry"
    },
    "test_t002": {
        "control": "shopping_cart.py",
        "experiment": "shopping_cart_cf.py", 
        "import_class": "ShoppingCart"
    },
    "test_t003": {
        "control": "file_uploader.py",
        "experiment": "file_uploader_cf.py",
        "import_class": "FileUploader"
    },
    "test_t004": {
        "control": "order_cancel.py",
        "experiment": "order_cancel_cf.py",
        "import_class": "OrderCancelService"
    },
    "test_t005": {
        "control": "coupon_system.py",
        "experiment": "coupon_system_cf.py",
        "import_class": "CouponManager"  # 实验组类名不同！
    },
    "test_t006": {
        "control": "comment_system.py",
        "experiment": "comment_system_cf.py",
        "import_class": "CommentSystem"
    },
    "test_t007": {
        "control": "sms_verification.py",
        "experiment": "sms_verification_cf.py",
        "import_class": "SMSVerificationService"
    },
    "test_t008": {
        "control": "rbac_system.py",
        "experiment": "rbac_cf.py",
        "import_class": "RBACSystem"
    },
    "test_t009": {
        "control": "task_queue.py",
        "experiment": "task_queue_cf.py",
        "import_class": "TaskQueue"
    },
    "test_t010": {
        "control": "cache.py",
        "experiment": "cache_cf.py",
        "import_class": "Cache"  # 对照组是Cache，实验组是LRUCache
    },
    "test_t011": {
        "control": "rate_limiter.py",
        "experiment": "rate_limiter_cf.py",
        "import_class": "RateLimiter"
    },
    "test_t012": {
        "control": "log_analyzer.py",
        "experiment": "log_analyzer_cf.py",
        "import_class": "LogAnalyzer"
    },
    "test_t013": {
        "control": "config_manager.py",
        "experiment": "config_manager_cf.py",
        "import_class": "ConfigManager"
    },
    "test_t014": {
        "control": "gateway.py",
        "experiment": "gateway_cf.py",
        "import_class": "APIGateway"
    },
    "test_t015": {
        "control": "paginator.py",
        "experiment": "paginator_cf.py",
        "import_class": "Paginator"
    }
}

def get_test_imports(test_file):
    """从测试文件提取导入语句"""
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 from xxx import yyy
    imports = []
    for line in content.split('\n'):
        if line.strip().startswith('from ') and 'import' in line:
            imports.append(line.strip())
    return imports

def create_unified_module(task_name, mode="control"):
    """创建统一的模块文件，将选中的实现复制为标准名"""
    task_info = TASK_MAP.get(task_name)
    if not task_info:
        print(f"  未知任务: {task_name}")
        return False
    
    source_file = task_info[mode]  # 对照组或实验组文件
    base_name = source_file.replace('_cf.py', '.py')
    test_file = f"{task_name}.py"
    
    # 读取源文件
    source_path = Path(source_file)
    if not source_path.exists():
        print(f"  源文件不存在: {source_file}")
        return False
    
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    # 写入目标文件（基础名）
    with open(base_name, 'w', encoding='utf-8') as f:
        f.write(source_content)
    
    return True

def run_test(test_name, mode="control"):
    """运行单个测试"""
    task_name = test_name.replace(".py", "")
    
    # 切换实现
    success = create_unified_module(task_name, mode)
    if not success:
        return {"passed": 0, "failed": 0, "error": "切换失败"}
    
    # 运行pytest
    result = subprocess.run(
        ["python", "-m", "pytest", test_name, "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)) or "."
    )
    
    # 解析结果
    output = result.stdout + result.stderr
    
    # 提取通过/失败数量
    passed = failed = 0
    if "passed" in output:
        # 格式: "X passed" 或 "X passed, Y failed"
        import re
        match = re.search(r'(\d+) passed', output)
        if match:
            passed = int(match.group(1))
        match = re.search(r'(\d+) failed', output)
        if match:
            failed = int(match.group(1))
    
    return {"passed": passed, "failed": failed, "output": output[:500]}

def run_full_experiment():
    """运行完整实验"""
    print("=" * 60)
    print("ODD 实证实验 - 对照组 vs 实验组")
    print("=" * 60)
    
    results = {
        "control": {},  # 对照组结果
        "experiment": {}  # 实验组结果
    }
    
    # 运行对照组
    print("\n【对照组】AI-First (AI自行理解需求)")
    print("-" * 40)
    for test_name in sorted(TASK_MAP.keys()):
        print(f"运行 {test_name}...", end=" ")
        r = run_test(test_name, "control")
        results["control"][test_name] = r
        print(f"通过:{r['passed']} 失败:{r['failed']}")
    
    # 运行实验组
    print("\n【实验组】Contract-First (人类提供契约)")
    print("-" * 40)
    for test_name in sorted(TASK_MAP.keys()):
        print(f"运行 {test_name}...", end=" ")
        r = run_test(test_name, "experiment")
        results["experiment"][test_name] = r
        print(f"通过:{r['passed']} 失败:{r['failed']}")
    
    # 汇总
    print("\n" + "=" * 60)
    print("【实验结果汇总】")
    print("=" * 60)
    
    total_control_pass = sum(r['passed'] for r in results["control"].values())
    total_control_fail = sum(r['failed'] for r in results["control"].values())
    total_exp_pass = sum(r['passed'] for r in results["experiment"].values())
    total_exp_fail = sum(r['failed'] for r in results["experiment"].values())
    
    print(f"\n对照组 (AI-First):")
    print(f"  总通过: {total_control_pass}")
    print(f"  总失败: {total_control_fail}")
    
    print(f"\n实验组 (Contract-First):")
    print(f"  总通过: {total_exp_pass}")
    print(f"  总失败: {total_exp_fail}")
    
    # 比较差异
    print("\n【逐任务对比】")
    print(f"{'任务':<15} {'对照组':<15} {'实验组':<15} {'差异':<10}")
    print("-" * 55)
    for test_name in TASK_MAP.keys():
        c = results["control"][test_name]
        e = results["experiment"][test_name]
        diff = c['passed'] - e['passed']
        status = "✓" if diff == 0 else "⚠" if diff > 0 else "!"
        print(f"{test_name:<15} {c['passed']}/{c['failed']:<12} {e['passed']}/{e['failed']:<12} {diff:+d} {status}")
    
    return results

if __name__ == "__main__":
    results = run_full_experiment()