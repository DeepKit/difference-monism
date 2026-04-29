# COP.B02-P5 · 反馈学习校准协议详细版

> 定位：COP 诊断管线第五协议——收集诊断后的真实结果，对比诊断结论与实际情况，校准协议参数。本文件是 B02 五协议主文中 P5 的完整展开。
> 作者：Yi Fu（付毅，ODDFounder）

---

## 一、P5 在诊断管线中的位置

```
输入采样(P1) → 状态编码(P2) → 诊断判定(P3) → 转介干预(P4) → 反馈校准(P5)
    ↑                                                           │
    └───────────────────────────────────────────────────────────┘
                      校准结果回流到采样策略
```

P5 是诊断管线的闭合环。没有 P5，COP 就是一个只会做判断但从不学习判断是否准确的系统。

---

## 二、校准数据采集时点

每次诊断后，在以下时点自动或手动采集校准信号：

| 时点 | 采集方式 | 采集内容 |
|------|---------|---------|
| 即时 | 自动 | 用户对诊断摘要的反应（接受/质疑/补充） |
| RT6 步骤 2 | 对比 | COP 诊断标签 vs RT6 扫描诊断结论是否一致 |
| RT6 步骤 6 | 对比 | 复诊发现的问题是否与初始 COP 诊断匹配 |
| 事故回溯 | 手动 | FREEZE/REFER 是否正确——是阻止了一次损害还是阻碍了本可进行的处理 |

---

## 三、三类误判的详细校准

### 3.1 False Safe（假安全）

**定义**：COP 判定为 RESOLVE/MIXED 允许推进，但实际不应推进。

**发现方式**：
- RT6 步骤 6 复盘发现：初始诊断低估了风险
- 用户报告：COP 说"可处理"但实际发生了损害
- 事故回溯：本该 FREEZE 的被放行了

**校准动作**：
```yaml
misclass: false_safe
calibration:
  - parameter: category_concentration_threshold_for_RESOLVE
    direction: up                    # 提高阈值
    magnitude: moderate
    reason: "上一批次中同类信号模式出现 2 例假安全"
  - parameter: irreversibility_sensitivity_for_this_pattern
    direction: up
    magnitude: minor
```

### 3.2 Over Freeze（过度冻结）

**定义**：COP 判定为 FREEZE，但人工复审后发现本可推进。

**发现方式**：
- 人工复审结论："此例本可 MIXED 有限推进"
- FREEZE 被 override 且 override 理由被后续证实为正确

**校准动作**：
```yaml
misclass: over_freeze
calibration:
  - parameter: freeze_trigger_threshold_for_this_pattern
    direction: down
    magnitude: moderate
    reason: "同类模式近 5 例中 3 例被人工判定为过度冻结"
```

### 3.3 Wrong Type（类型错误）

**定义**：分流方向正确但分类标签错误（如本该是 MIXED 但被标为 RESOLVE，或主标签标错）。

**发现方式**：
- RT6 步骤 2 的扫描诊断给出了不同的结论
- 编码置信度与最终结果不匹配

**校准动作**：
```yaml
misclass: wrong_type
calibration:
  - parameter: encoding_mapping_for_this_signal_pattern
    direction: remap
    magnitude: major
    reason: "该信号组合在最近 10 例中 6 例被修正为不同的主标签"
```

---

## 四、误判样本库规范

每次误判必须入库。样本库最小字段：

```yaml
misclass_entry:
  entry_id: ""
  source_diagnosis_id: ""
  misclass_type: false_safe | over_freeze | wrong_type
  actual_outcome: ""          # 真实结果
  
  # 严重度
  severity:
    false_safe: low | medium | high | critical
    over_freeze: low | medium | high
    wrong_type: low | medium | high
    
  # 根因分析
  root_cause_guess: ""        # 初步判断的根因
  # 示例："信号中缺少持续时间信息导致高估了信号完整性"
  
  # 校准结果
  parameter_adjustments: []
  review_status: pending | reviewed | applied
```

---

## 五、校准版本管理

每次协议参数调整产生一个新版本：

```yaml
protocol_version:
  version_id: "v1.2.0"
  previous_version: "v1.1.0"
  changes:
    - parameter: ""
      old_value: ""
      new_value: ""
      reason: ""
      based_on_misclass_entries: []  # 基于哪些误判样本
  release_date: ""
  rollback_conditions: ""    # 什么情况下回滚这个版本
```

---

## 六、校准纪律

1. **不得基于单例调整阈值。** 至少 3 例同类型误判才能触发参数调整。
2. **严重度 critical 的 false_safe 单例即可触发紧急复审。** 不等待积累到 3 例。
3. **每次校准必须记录基于哪些样本。** 可追溯、可回滚。
4. **校准不得在事故当天的情绪驱动下进行。** 至少间隔 48 小时冷静期。
5. **校准版本保留回滚条件。** 如果新阈值导致反向误判增多，应回滚。
