# COP.B02-P3 · 诊断判定协议详细版

> 定位：COP 诊断管线第三协议——基于编码向量做分流判定。本文件是 B02 五协议主文中 P3 的完整展开。
> 作者：Yi Fu（付毅，ODDFounder）

---

## 一、P3 在诊断管线中的位置

```
输入采样(P1) → 状态编码(P2) → 诊断判定(P3) → 转介干预(P4) → 反馈校准(P5)
```

P3 是诊断管线的判定核心。它回答：**当前是否清楚、是否安全、是否该继续自动推进。**

---

## 二、五种分流状态的完整定义

### RESOLVE —— 可自动处理

**含义**：信号完整且一致，分类明确，结构风险低。系统可以继续自动推进。

**准入条件（全部满足）**：
- signal_completeness > 0.7
- signal_consistency > 0.7
- category_concentration > 0.7
- responsibility_diffusion = low
- irreversibility_potential = low

**输出示例**：
```yaml
triage_status: RESOLVE
confidence: 0.85
primary_label: "个体技能缺口-可训练"
alternative_labels: ["中期职业倦怠-轻度"]
```

### MIXED —— 混合信号

**含义**：信号存在矛盾或分类不集中。可以有限推进，但必须标注混合区域。

**触发条件（满足任一）**：
- signal_consistency 在 0.4-0.7 之间
- category_concentration 在 0.4-0.7 之间
- 两个以上的 primary_label 候选得分接近

**输出示例**：
```yaml
triage_status: MIXED
confidence: 0.55
primary_label: "组织结构模糊-水局倾向"
alternative_labels: ["个体过载-木局倾向", "两种模式混合"]
mixed_areas: ["用户描述同时包含'没人管'和'越做越多'两种信号"]
limited_action_allowed: true
```

### FREEZE —— 冻结

**含义**：结构风险高或触及红线。暂停自动推进，升级人工。

**触发条件（满足任一）**：
- irreversibility_potential = high
- responsibility_diffusion = high AND power_asymmetry = high
- 触及 ASTO 例外标记
- 信号包含以下关键词模式：法律风险、人身安全、自杀、暴力、严重违规

**输出示例**：
```yaml
triage_status: FREEZE
confidence: 0.90
freeze_reason: "结构风险为高不可逆 + 权力严重不对称"
freeze_trigger: "用户描述中包含'被要求承担违法后果'的模式"
escalation_target: HUMAN_REVIEW
```

### UNKNOWN —— 信息不足

**含义**：信号不够做判断。需要补充信息。

**触发条件**：
- signal_completeness < 0.4

**输出示例**：
```yaml
triage_status: UNKNOWN
confidence: 0.30
missing_info_hint: "缺少以下类型的信号：(1) 持续时间 (2) 第三方视角 (3) 具体实例"
suggested_supplement: "建议补充 2-3 个最近发生的事件描述"
```

### REFER —— 转介

**含义**：问题超出 COP 可处理范围。路由到指定目标。

**触发条件（满足任一）**：
- 问题类型属于工程执行 → 转 ODD
- 问题类型属于责任门槛裁决 → 转 TAT
- 问题类型属于治理边界争议 → 转 ECET
- COP 自身置信度 < 0.3 且无法通过补充信息改善

---

## 三、判定矩阵（完整版）

| complete | consist | concentr | resp_diff | power_asym | irrev | → 分流 |
|----------|---------|----------|-----------|------------|-------|--------|
| >0.7 | >0.7 | >0.7 | low | low | low | **RESOLVE** |
| >0.5 | >0.5 | >0.5 | low-med | low-med | low-med | **MIXED** |
| any | any | any | high | high | any | **FREEZE** |
| any | any | any | any | any | high | **FREEZE** |
| <0.4 | any | any | any | any | any | **UNKNOWN** |
| any | any | any | any | any | out_of_scope | **REFER** |

> 注：当多个条件同时触发（如 UNKNOWN + FREEZE），优先取安全等级更高的（FREEZE > REFER > UNKNOWN > MIXED > RESOLVE）。

---

## 四、判定纪律

1. **宁可多冻一次，不可错放一次。** 边缘情况默认 FREEZE。
2. **低置信度不得输出 RESOLVE。** confidence < 0.6 时，最乐观输出为 MIXED。
3. **FREEZE 必须写 freeze_reason。** 不能只标注 FREEZE 不给理由。
4. **REFER 必须写 referral_target。** 不能只转介不说明转给谁。
