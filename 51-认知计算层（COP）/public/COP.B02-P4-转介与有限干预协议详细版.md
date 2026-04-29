# COP.B02-P4 · 转介与有限干预协议详细版

> 定位：COP 诊断管线第四协议——基于分流状态生成下一步动作与转介路由。本文件是 B02 五协议主文中 P4 的完整展开。
> 作者：Yi Fu（付毅，ODDFounder）

---

## 一、P4 在诊断管线中的位置

```
输入采样(P1) → 状态编码(P2) → 诊断判定(P3) → 转介干预(P4) → 反馈校准(P5)
```

P3 判定"什么状态"，P4 决定"接下来做什么"。

---

## 二、五种分流 → 动作映射

### RESOLVE → 放行

```yaml
action:
  type: PROCEED
  target: RT6
  payload:
    diagnostic_summary: ""      # 诊断摘要
    confidence: 0.85
    recommended_starting_step: 1  # RT6 六步中的建议起点
    attention_areas: []          # 需要注意但不足以阻止的区域
```

### MIXED → 有限放行

```yaml
action:
  type: PROCEED_WITH_CAUTION
  target: RT6 | LMM
  payload:
    diagnostic_summary: ""
    confidence: 0.55
    mixed_areas: []             # 需要额外关注的混合信号区域
    step_2_extra_attention: ""  # RT6 步骤 2（扫描诊断）需额外关注的问题
    review_required_after_step: 2  # 在哪一步之后必须回看
```

### FREEZE → 冻结+升级

```yaml
action:
  type: FREEZE_AND_ESCALATE
  target: HUMAN_REVIEW | TAT_REVIEW
  payload:
    freeze_reason: ""
    freeze_trigger_signals: []  # 触发冻结的具体信号
    diagnostic_chain: ""        # 完整诊断链（采样→编码→判定）
    recommended_question_for_human: ""  # 建议人类回答的核心问题
    minimum_wait: ""            # 在人类回复前至少等待多久
```

### UNKNOWN → 补充采样

```yaml
action:
  type: SUPPLEMENT
  target: ORIGINAL_CHANNEL     # 回到原采样通道
  payload:
    missing_info_hint: ""
    suggested_questions: []     # 建议追问的具体问题
    suggested_channels: []      # 建议从哪些通道补充
    max_supplement_rounds: 2    # 最多补充几轮
```

### REFER → 转介

```yaml
action:
  type: REFER
  target: TAT | ODD | ECET | HUMAN
  payload:
    referral_reason: ""
    diagnostic_summary: ""
    triage_chain: ""            # 完整分流链
    urgency: routine | elevated | urgent
```

---

## 三、转介路由详细规则

### 转 TAT

**触发条件**（满足任一）：
- 涉及责任门槛（谁承接高影响后果）
- 用户明确申诉
- FREEZE 原因涉及权力不对称导致的不可逆后果
- 需要同意/补偿/熔断结构判断

**转介包内容**：诊断摘要 + 风险向量 + 触发信号 + COP 自身置信度

### 转 ODD

**触发条件**：
- 问题涉及契约/验证/门禁/证据/封存
- 产出物质量争议
- 审计追溯需求

**转介包内容**：涉及的 artifact_id + 契约链 + 门禁日志

### 转 ECET

**触发条件**：
- 治理边界争议（多头管理、影子主权）
- 元治理条件问题（"谁来治理治理者"）
- 跨文明比较需求

### 转人工

**触发条件**：
- COP 自身判定置信度 < 0.3
- 三个转介目标都不适用
- 人类明确要求人工接手

---

## 四、COP 可以做与不可以做

### COP 可以做
- 基于规则的建议（不涉及高风险强制动作）
- 转介路由选择
- 信息补充请求
- 有限动作建议（标注置信度和边界）

### COP 不可以做
- 强制性高风险动作授权
- 行为锁定的最终裁决
- 同意、申诉、补偿结构定义 → 回引 TAT
- 绕过 ODD 直接修改契约/门禁/封存
- 在 FREEZE 状态下仍输出 PROCEED
