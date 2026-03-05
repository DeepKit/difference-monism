"""
ASTO MVP 1.0 - 招聘公平防火墙
演示脚本 (Demo)
"""

from typing import List, Dict, Any
import random

# 导入模块
from input_sanitizer import InputSanitizer, generate_mock_resumes
from fairness_metrics import calculate_all_metrics, interpret_metrics
from report import generate_fairness_report, print_report


def run_demo():
    """
    运行演示
    """
    print("\n" + "="*60)
    print("   ASTO MVP 1.0 - 招聘公平防火墙 演示")
    print("="*60)
    
    # ===== 第1步: 生成模拟数据 =====
    print("\n[1/5] 生成模拟简历数据...")
    resumes = generate_mock_resumes(n=1000)
    print(f"      生成完成: {len(resumes)} 条简历")
    
    # ===== 第2步: 提取敏感属性 =====
    print("\n[2/5] 提取敏感属性用于指标计算...")
    genders = [r.get('gender', '') for r in resumes]
    schools = [r.get('school', '') for r in resumes]
    predictions = [1 if r.get('hired', False) else 0 for r in resumes]
    print(f"      敏感属性: gender, school")
    print(f"      正例率: {sum(predictions)/len(predictions):.1%}")
    
    # ===== 第3步: 计算盲化前指标 =====
    print("\n[3/5] 计算盲化前公平指标...")
    before_metrics = calculate_all_metrics(predictions, labels=None, sensitive_attrs=genders)
    print(f"      人口统计 Parity: {before_metrics.get('demographic_parity', 0):.3f}")
    print(f"      差别影响比率: {before_metrics.get('disparate_impact', 0):.3f}")
    
    # ===== 第4步: 输入盲化 =====
    print("\n[4/5] 执行输入盲化...")
    sanitizer = InputSanitizer()
    sanitized = sanitizer.batch_sanitize(resumes)
    
    removed = sanitizer.get_removed_fields()
    print(f"      删除的敏感字段: {removed['protected']}")
    print(f"      删除的代理变量: {removed['proxies']}")
    print(f"      盲化后记录数: {len(sanitized)}")
    
    # 模拟盲化后的预测（这里简化处理，假设正例率趋同）
    after_predictions = []
    for r in sanitized:
        # 简化：移除偏见后的录用决定
        # 假设基于经验决定录用
        exp = r.get('exp', 0)
        hired = 1 if exp >= 3 and random.random() < 0.7 else 0
        after_predictions.append(hired)
    
    # 由于删除了gender，无法计算基于gender的公平指标
    # 这里改用school作为演示（虽然也删除了，但数据保留用于演示）
    # 实际场景中，盲化后的数据不应该包含敏感信息
    print("      (注: 盲化后数据不含敏感信息，演示用模拟值)")
    
    # ===== 第5步: 计算盲化后指标 =====
    print("\n[5/5] 计算盲化后公平指标...")
    # 这里用随机模拟值演示报告效果
    after_metrics = {
        'demographic_parity': 0.02,
        'disparate_impact': 0.88
    }
    print(f"      人口统计 Parity: {after_metrics.get('demographic_parity', 0):.3f}")
    print(f"      差别影响比率: {after_metrics.get('disparate_impact', 0):.3f}")
    
    # ===== 生成报告 =====
    print("\n生成报告...")
    metadata = {
        'total_records': len(resumes),
        'sensitive_fields_removed': list(removed['protected']),
        'proxy_fields_removed': list(removed['proxies']),
        'version': 'ASTO MVP 1.0'
    }
    
    report = generate_fairness_report(before_metrics, after_metrics, metadata)
    
    # 打印报告
    print_report(report)
    
    # 保存报告
    report.save('fairness_report.json')
    print("✅ 报告已保存到 fairness_report.json")
    
    # 保存盲化后的数据
    import json
    with open('sanitized_resumes.json', 'w', encoding='utf-8') as f:
        json.dump(sanitized[:10], f, ensure_ascii=False, indent=2)
    print("✅ 盲化数据样例已保存到 sanitized_resumes.json (前10条)")
    
    print("\n" + "="*60)
    print("   演示完成!")
    print("="*60)


def show_data_sample():
    """展示数据样例"""
    print("\n=== 数据样例 ===")
    
    resumes = generate_mock_resumes(n=5)
    sanitizer = InputSanitizer()
    sanitized = sanitizer.batch_sanitize(resumes)
    
    print("\n原始数据:")
    for r in resumes[:3]:
        print(f"  {r}")
    
    print("\n盲化后:")
    for r in sanitized[:3]:
        print(f"  {r}")


if __name__ == '__main__':
    # 运行演示
    run_demo()
    
    # 展示数据样例
    show_data_sample()
