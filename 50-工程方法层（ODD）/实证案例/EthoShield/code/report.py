"""
ASTO MVP 1.0 - 招聘公平防火墙
报告生成器 (Report Generator)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class FairnessReport:
    """
    公平性报告生成器
    """
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.data = {}
    
    def add_section(self, name: str, content: Any):
        """添加报告章节"""
        self.data[name] = content
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'timestamp': self.timestamp,
            'report': self.data
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def save(self, filename: str):
        """保存到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


def generate_fairness_report(
    before_metrics: Dict[str, float],
    after_metrics: Dict[str, float],
    metadata: Optional[Dict[str, Any]] = None
) -> FairnessReport:
    """
    生成公平性对比报告
    
    Args:
        before_metrics: 盲化前的指标
        after_metrics: 盲化后的指标
        metadata: 元数据
        
    Returns:
        报告对象
    """
    report = FairnessReport()
    
    # 计算改善
    improvements = {}
    for key in before_metrics:
        if key in after_metrics:
            before_val = before_metrics[key]
            after_val = after_metrics[key]
            
            if key == 'disparate_impact':
                # DI越大越好
                if before_val > 0:
                    improvement = ((after_val - before_val) / before_val) * 100
                else:
                    improvement = 0
                improvements[key] = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
            else:
                # 其他指标越小越好
                if before_val > 0:
                    improvement = ((before_val - after_val) / before_val) * 100
                else:
                    improvement = 0
                improvements[key] = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
    
    # 添加指标对比
    report.add_section('metrics', {
        'before': before_metrics,
        'after': after_metrics,
        'improvements': improvements
    })
    
    # 添加总结
    summary = generate_summary(before_metrics, after_metrics)
    report.add_section('summary', summary)
    
    # 添加元数据
    if metadata:
        report.add_section('metadata', metadata)
    
    return report


def generate_summary(before: Dict[str, float], after: Dict[str, float]) -> Dict[str, Any]:
    """
    生成总结
    
    Args:
        before: 盲化前指标
        after: 盲化后指标
        
    Returns:
        总结字典
    """
    # 评估整体改善
    dp_improvement = 0.0
    di_improvement = 0.0
    
    if 'demographic_parity' in before and 'demographic_parity' in after:
        dp_before = before['demographic_parity']
        dp_after = after['demographic_parity']
        if dp_before > 0:
            dp_improvement = ((dp_before - dp_after) / dp_before) * 100
    
    if 'disparate_impact' in before and 'disparate_impact' in after:
        di_before = before['disparate_impact']
        di_after = after['disparate_impact']
        if di_before > 0:
            di_improvement = ((di_after - di_before) / di_before) * 100
    
    # 判断状态
    status = "neutral"
    message = ""
    
    if dp_improvement > 50 and di_improvement > 50:
        status = "excellent"
        message = "显著改善 - 偏见风险大幅降低"
    elif dp_improvement > 30 or di_improvement > 30:
        status = "good"
        message = "明显改善 - 偏见风险有所降低"
    elif dp_improvement > 0 or di_improvement > 0:
        status = "moderate"
        message = "轻度改善 - 仍有优化空间"
    else:
        status = "poor"
        message = "未见改善 - 建议调整盲化策略"
    
    return {
        'status': status,
        'message': message,
        'dp_improvement': f"{dp_improvement:.1f}%",
        'di_improvement': f"{di_improvement:.1f}%"
    }


def print_report(report: FairnessReport):
    """
    打印报告到控制台
    """
    data = report.data
    
    print("\n" + "="*50)
    print("       ASTO 招聘公平性评估报告")
    print("="*50)
    
    if 'metrics' in data:
        metrics = data['metrics']
        print("\n📊 公平指标对比:")
        print("-"*40)
        
        if 'before' in metrics and 'after' in metrics:
            before = metrics['before']
            after = metrics['after']
            improvements = metrics.get('improvements', {})
            
            # 人口统计 Parity
            if 'demographic_parity' in before:
                print(f"\n人口统计 Parity (越小越好):")
                print(f"  盲化前: {before['demographic_parity']:.3f}")
                print(f"  盲化后: {after['demographic_parity']:.3f}")
                if 'demographic_parity' in improvements:
                    print(f"  改善:   {improvements['demographic_parity']}")
            
            # 差别影响
            if 'disparate_impact' in before:
                print(f"\n差别影响比率 (越大越好):")
                print(f"  盲化前: {before['disparate_impact']:.3f}")
                print(f"  盲化后: {after['disparate_impact']:.3f}")
                if 'disparate_impact' in improvements:
                    print(f"  改善:   {improvements['disparate_impact']}")
    
    if 'summary' in data:
        summary = data['summary']
        print("\n📋 总结:")
        print("-"*40)
        
        status_emoji = {
            'excellent': '🟢',
            'good': '🟡',
            'moderate': '🟠',
            'poor': '🔴'
        }
        
        emoji = status_emoji.get(summary['status'], '⚪')
        print(f"\n  {emoji} {summary['message']}")
        
        print(f"\n  人口统计 Parity 改善: {summary['dp_improvement']}")
        print(f"  差别影响改善: {summary['di_improvement']}")
    
    print("\n" + "="*50)
    print(f"生成时间: {report.timestamp}")
    print("="*50 + "\n")


if __name__ == '__main__':
    # 测试报告生成
    before = {
        'demographic_parity': 0.15,
        'disparate_impact': 0.42
    }
    
    after = {
        'demographic_parity': 0.02,
        'disparate_impact': 0.88
    }
    
    metadata = {
        'total_records': 1000,
        'sensitive_fields_removed': ['gender', 'school'],
        'version': 'ASTO MVP 1.0'
    }
    
    report = generate_fairness_report(before, after, metadata)
    
    # 打印到控制台
    print_report(report)
    
    # 保存到文件
    report.save('fairness_report.json')
    print("报告已保存到 fairness_report.json")
