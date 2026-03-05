"""
ASTO MVP 1.0 - 招聘公平防火墙
公平指标计算器 (Fairness Metrics)
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np


def demographic_parity(predictions: List[int], sensitive_attrs: List[str]) -> float:
    """
    人口统计 Parity (Demographic Parity)
    
    DP = Pr(Y=1|A=a) - Pr(Y=1|A=b)
    
    计算不同敏感属性组的正例率差异
    
    Args:
        predictions: 预测结果 (1=正面, 0=负面)
        sensitive_attrs: 敏感属性值列表
        
    Returns:
        DP值 (越小越公平)
    """
    if len(predictions) != len(sensitive_attrs):
        raise ValueError("predictions和sensitive_attrs长度不一致")
    
    # 按敏感属性分组
    groups: Dict[str, List[int]] = {}
    for i, attr in enumerate(sensitive_attrs):
        if attr not in groups:
            groups[attr] = []
        groups[attr].append(predictions[i])
    
    # 计算各组正例率
    rates: Dict[str, float] = {}
    for attr, preds in groups.items():
        rates[attr] = sum(preds) / len(preds) if preds else 0.0
    
    # 计算差异
    values = list(rates.values())
    if len(values) < 2:
        return 0.0
    
    return max(values) - min(values)


def disparate_impact(predictions: List[int], sensitive_attrs: List[str], 
                     privileged: str = None) -> float:
    """
    差别影响比率 (Disparate Impact)
    
    DI = Pr(Y=1|群体A) / Pr(Y=1|群体B)
    
    通常privileged群体为分母，目标 >= 0.8
    
    Args:
        predictions: 预测结果
        sensitive_attrs: 
        privileged:敏感属性值列表 优势群体标识
        
    Returns:
        DI值 (越大越公平，越接近1越好)
    """
    if len(predictions) != len(sensitive_attrs):
        raise ValueError("predictions和sensitive_attrs长度不一致")
    
    # 按敏感属性分组
    groups: Dict[str, List[int]] = {}
    for i, attr in enumerate(sensitive_attrs):
        if attr not in groups:
            groups[attr] = []
        groups[attr].append(predictions[i])
    
    # 计算各组正例率
    rates: Dict[str, float] = {}
    for attr, preds in groups.items():
        rates[attr] = sum(preds) / len(preds) if preds else 0.0
    
    # 获取所有属性值
    attrs = list(rates.keys())
    if len(attrs) < 2:
        return 1.0
    
    # 确定优势群体和弱势群体
    if privileged and privileged in rates:
        priv_rate = rates[privileged]
        unpriv_rate = min([v for k, v in rates.items() if k != privileged])
    else:
        # 默认：频率高的为优势群体
        sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=True)
        priv_rate = sorted_rates[0][1]
        unpriv_rate = sorted_rates[-1][1]
    
    # 计算DI
    if unpriv_rate == 0:
        return float('inf')
    
    return unpriv_rate / priv_rate


def equalized_odds(predictions: List[int], labels: List[int], 
                   sensitive_attrs: List[str]) -> float:
    """
    均等机会 (Equalized Odds)
    
    比较不同群体在相同真实标签下的预测率差异
    
    Args:
        predictions: 预测结果
        labels: 真实标签
        sensitive_attrs: 敏感属性
        
    Returns:
        最大差异 (越小越公平)
    """
    if not (len(predictions) == len(labels) == len(sensitive_attrs)):
        raise ValueError("输入长度不一致")
    
    # 按敏感属性和真实标签分组
    groups: Dict[Tuple[str, int], List[int]] = {}
    for i, (attr, label) in enumerate(zip(sensitive_attrs, labels)):
        key = (attr, label)
        if key not in groups:
            groups[key] = []
        groups[key].append(predictions[i])
    
    # 计算各组正例率
    rates: Dict[Tuple[str, int], float] = {}
    for key, preds in groups.items():
        rates[key] = sum(preds) / len(preds) if preds else 0.0
    
    # 找出最大差异
    max_diff = 0.0
    for label in set(labels):
        group_rates = [v for k, v in rates.items() if k[1] == label]
        if len(group_rates) >= 2:
            diff = max(group_rates) - min(group_rates)
            max_diff = max(max_diff, diff)
    
    return max_diff


def calculate_all_metrics(predictions: List[int], labels: List[int] = None,
                          sensitive_attrs: List[str] = None,
                          privileged: str = None) -> Dict[str, float]:
    """
    计算所有公平指标
    
    Args:
        predictions: 预测结果
        labels: 真实标签 (可选)
        sensitive_attrs: 敏感属性
        privileged: 优势群体
        
    Returns:
        指标字典
    """
    result: Dict[str, float] = {}
    
    if sensitive_attrs is None:
        return result
    
    # 人口统计 Parity
    result['demographic_parity'] = demographic_parity(predictions, sensitive_attrs)
    
    # 差别影响
    result['disparate_impact'] = disparate_impact(predictions, sensitive_attrs, privileged)
    
    # 均等机会 (如果有labels)
    if labels is not None:
        result['equalized_odds'] = equalized_odds(predictions, labels, sensitive_attrs)
    
    return result


def interpret_metrics(metrics: Dict[str, float]) -> Dict[str, str]:
    """
    解释指标含义
    
    Args:
        metrics: 指标字典
        
    Returns:
        解释字典
    """
    interpretation: Dict[str, str] = {}
    
    # 人口统计 Parity
    dp = metrics.get('demographic_parity', 0)
    if dp <= 0.1:
        interpretation['demographic_parity'] = "✅ 良好 - 差异小于10%"
    elif dp <= 0.2:
        interpretation['demographic_parity'] = "⚠️ 警告 - 差异10-20%"
    else:
        interpretation['demographic_parity'] = "❌ 危险 - 差异超过20%"
    
    # 差别影响
    di = metrics.get('disparate_impact', 0)
    if di >= 0.8:
        interpretation['disparate_impact'] = "✅ 良好 - 超过80%阈值"
    elif di >= 0.6:
        interpretation['disparate_impact'] = "⚠️ 警告 - 60-80%"
    else:
        interpretation['disparate_impact'] = "❌ 危险 - 低于60%"
    
    return interpretation


if __name__ == '__main__':
    # 测试数据
    predictions = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0]
    labels = [1, 1, 1, 0, 0, 1, 0, 0, 1, 0]
    sensitive = ['男', '男', '男', '男', '男', '女', '女', '女', '女', '女']
    
    print("=== 公平指标测试 ===")
    print(f"Demographic Parity: {demographic_parity(predictions, sensitive):.3f}")
    print(f"Disparate Impact: {disparate_impact(predictions, sensitive):.3f}")
    print(f"Equalized Odds: {equalized_odds(predictions, labels, sensitive):.3f}")
    
    print("\n=== 指标解释 ===")
    metrics = calculate_all_metrics(predictions, labels, sensitive)
    for k, v in metrics.items():
        print(f"{k}: {v:.3f}")
    for k, v in interpret_metrics(metrics).items():
        print(v)
