# ASTO / EthoShield MVP 1.0 - 招聘公平防火墙

> **版本**: 1.0  
> **创建日期**: 2026-02-19  
> **目标**: 7天完成，200行代码，可演示

---

## 1. 产品定位

### 1.1 核心价值

```
┌─────────────────────────────────────────────────────────┐
│              ASTO MVP 1.0 - 招聘公平防火墙             │
├─────────────────────────────────────────────────────────┤
│  输入：含偏见的简历数据                                │
│        ↓                                               │
│  处理：输入盲化 + 公平性检测                           │
│        ↓                                               │
│  输出：脱敏数据 + 偏见风险报告                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 为什么选择这个场景

| 维度 | 分析 |
|------|------|
| **痛点真实** | 招聘偏见是社会关注热点 |
| **数据易得** | 可用合成数据演示 |
| **效果可见** | 偏见指标下降直观 |
| **技术验证** | 输入盲化的工程化表达 |

---

## 2. 技术架构

### 2.1 模块结构

```
ASTO-MVP/
├── input_sanitizer.py      # 输入盲化器 (80行)
├── fairness_metrics.py     # 公平指标 (60行)
├── report.py               # 报告生成 (40行)
├── demo.py                 # 演示脚本 (20行)
└── README.md               # 本文档
```

### 2.2 数据流程

```
原始简历数据
    │
    ▼
┌─────────────────┐
│  输入盲化器      │ ← 删除敏感字段 + 代理变量
│ input_sanitizer │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  公平指标计算    │ ← 计算 DI / DP
│ fairness_metrics │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  报告生成器      │ ← 输出JSON + 可视化
│    report       │
└────────┬────────┘
         │
         ▼
   脱敏数据 + 偏见报告
```

---

## 3. 模块设计

### 3.1 输入盲化器 (input_sanitizer.py)

**功能**：
- 删除显式敏感字段（性别、民族、年龄）
- 删除高相关代理变量（学校、籍贯）
- 支持配置化的盲化规则

**核心代码**：

```python
class InputSanitizer:
    def __init__(self):
        # 显式敏感字段
        self.explicit_protected = ['gender', 'ethnicity', 'age', 'religion']
        
        # 代理变量（需配置）
        self.proxy_vars = ['school', 'birthplace', 'zipcode']
    
    def sanitize(self, resume):
        """输入盲化"""
        sanitized = resume.copy()
        
        # 删除显式敏感字段
        for field in self.explicit_protected:
            if field in sanitized:
                del sanitized[field]
        
        # 删除代理变量
        for field in self.proxy_vars:
            if field in sanitized:
                del sanitized[field]
        
        return sanitized
    
    def batch_sanitize(self, resumes):
        """批量盲化"""
        return [self.sanitize(r) for r in resumes]
```

### 3.2 公平指标 (fairness_metrics.py)

**指标**：

| 指标 | 名称 | 计算公式 | 阈值 |
|------|------|---------|------|
| DI | 差别影响比率 | Pr(正\|群体A) / Pr(正\|群体B) | >= 0.8 |
| DP | 人口统计 parity | Pr(预测=正\|A) - Pr(预测=正\|B) | <= 0.1 |

**核心代码**：

```python
def demographic_parity(predictions, sensitive_attr):
    """
    人口统计 parity
    DP = Pr(Y=1|A=a) - Pr(Y=1|A=b)
    """
    # 按敏感属性分组
    groups = {}
    for i, attr in enumerate(sensitive_attr):
        if attr not in groups:
            groups[attr] = []
        groups[attr].append(predictions[i])
    
    # 计算各组正例率
    rates = {}
    for attr, preds in groups.items():
        rates[attr] = sum(preds) / len(preds) if preds else 0
    
    # 计算差异
    values = list(rates.values())
    return max(values) - min(values)


def disparate_impact(predictions, sensitive_attr):
    """
    差别影响比率
    DI = Pr(Y=1|群体A) / Pr(Y=1|群体B)
    """
    groups = {}
    for i, attr in enumerate(sensitive_attr):
        if attr not in groups:
            groups[attr] = []
        groups[attr].append(predictions[i])
    
    rates = {}
    for attr, preds in groups.items():
        rates[attr] = sum(preds) / len(preds) if preds else 0
    
    values = sorted(rates.values())
    if values[0] == 0:
        return float('inf')
    
    return values[1] / values[0]
```

### 3.3 报告生成 (report.py)

**输出格式**：

```python
{
    "metrics": {
        "before": {
            "demographic_parity": 0.15,
            "disparate_impact": 0.42
        },
        "after": {
            "demographic_parity": 0.02,
            "disparate_impact": 0.88
        }
    },
    "improvement": {
        "dp_reduction": "87%",
        "di_improvement": "110%"
    },
    "summary": "偏见风险显著降低"
}
```

**可视化**：柱状图对比

---

## 4. 演示流程

### 4.1 演示脚本 (demo.py)

```python
def demo():
    # 1. 生成模拟数据
    resumes = generate_mock_data(n=1000)
    
    # 2. 计算盲化前指标
    before_dp = demographic_parity(predictions, sensitive_attr)
    before_di = disparate_impact(predictions, sensitive_attr)
    
    # 3. 输入盲化
    sanitizer = InputSanitizer()
    sanitized = sanitizer.batch_sanitize(resumes)
    
    # 4. 重新计算指标（实际应用中需要重新预测）
    after_dp = ...
    after_di = ...
    
    # 5. 生成报告
    report = generate_report(before_dp, before_di, after_dp, after_di)
    print(report)
    
    # 6. 可视化
    visualize(report)
```

### 4.2 演示数据

```json
[
  {"id": 1, "name": "张雪", "gender": "女", "school": "北大", "exp": 5, "hired": true},
  {"id": 2, "name": "李明", "gender": "男", "school": "清华", "exp": 3, "hired": true},
  {"id": 3, "name": "王芳", "gender": "女", "school": "普本", "exp": 2, "hired": false},
  ...
]
```

### 4.3 演示结果

```
┌─────────────────────────────────────────────┐
│           偏见风险评估报告                    │
├─────────────────────────────────────────────┤
│  指标            │  盲化前  │  盲化后  │ 改善 │
├─────────────────────────────────────────────┤
│  人口统计Parity │  0.15   │  0.02   │ 87%  │
│  差别影响比率   │  0.42   │  0.88   │110%  │
└─────────────────────────────────────────────┘

结论：输入盲化后，偏见风险显著降低
```

---

## 5. 验收标准

### 5.1 功能验收

- [ ] 能读取模拟简历数据
- [ ] 能删除敏感字段
- [ ] 能计算DI指标
- [ ] 能计算DP指标
- [ ] 能生成JSON报告
- [ ] 能生成可视化图表

### 5.2 性能验收

- [ ] 处理1000条数据 < 1秒
- [ ] 演示流程 < 5分钟

### 5.3 演示验收

- [ ] 偏见指标改善明显
- [ ] 观众能理解
- [ ] 可录屏演示

---

## 6. 时间规划

| 天数 | 任务 | 交付物 |
|------|------|--------|
| Day 1-2 | 输入盲化器 | input_sanitizer.py |
| Day 3-4 | 公平指标 | fairness_metrics.py |
| Day 5 | 报告生成 | report.py |
| Day 6 | 演示整合 | demo.py + 数据 |
| Day 7 | 演示录制 | 演示视频 |

---

## 7. 下一步（v2.0 Roadmap）

### 7.1 扩展功能

- [ ] 代理变量自动检测
- [ ] 更多公平指标（equalized odds, calibration）
- [ ] PCTL规则引擎
- [ ] 伦理流形可视化

### 7.2 系统集成

- [ ] 与WiseLLM集成
- [ ] API接口
- [ ] Web界面

### 7.3 理论深化

- [ ] 属集演算形式化
- [ ] 七序干预机制
- [ ] 伦理单纯形

---

## 8. 附录

### 8.1 依赖

```python
# requirements.txt
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
```

### 8.2 运行

```bash
python demo.py
```

---

*文档版本: 1.0 | 更新: 2026-02-19*
