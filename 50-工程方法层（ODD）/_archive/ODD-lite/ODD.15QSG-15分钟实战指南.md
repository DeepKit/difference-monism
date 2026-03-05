---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.00入门, ODD.01OVR]
---

# 15 分钟实战指南

## 意向
读完三分钟入门和总览后，你理解了 ODD 的概念——但概念不等于能力。
本文档用两个动手练习，让你在 15 分钟内完成从"知道"到"做到"的跨越。

## 规范
- 练习一（10 分钟）：个人开发者，完成一个产出物的完整封印流程。
- 练习二（+5 分钟）：小团队协作，体验契约对抗和交叉验证。
- 所有 YAML 可直接复制使用，无需额外工具。

## 机制

---

### 练习一：10 分钟 —— 你的第一个封印产出物

**场景**：你要写一个 `format_date` 函数，把 `2026-01-10` 格式化为 `2026年1月10日`。

#### 第 1 步：写契约（2 分钟）

复制以下 YAML，填入你的项目信息：

```yaml
contract:
  id: C-001
  title: "日期格式化函数"
  scope_in: "将 ISO 日期字符串转为中文可读格式"
  scope_out: "不处理时间、不处理时区"
  acceptance_criteria:
    - given: "有效日期 2026-01-10"
      when: "调用 format_date('2026-01-10')"
      then: "返回 '2026年1月10日'"
    - given: "有效日期 2025-12-25"
      when: "调用 format_date('2025-12-25')"
      then: "返回 '2025年12月25日'"
    - given: "无效输入 'not-a-date'"
      when: "调用 format_date('not-a-date')"
      then: "抛出 ValueError，消息包含 'invalid date'"
    - given: "空字符串"
      when: "调用 format_date('')"
      then: "抛出 ValueError"
  boundary_cases:
    - "闰年日期 2024-02-29 → 2024年2月29日"
    - "月份和日期不补零：1月 而非 01月"
  floor: "所有 acceptance_criteria 必须通过"
  red_line: "不得修改输入参数"
  human_confirmed: true
```

**检查点**：你的契约有 4 个验收条件 + 2 个边界用例 + 地板 + 红线。这就是 L2 标准。

#### 第 2 步：创建任务（1 分钟）

```yaml
task:
  id: T-001
  title: "实现 format_date"
  contract_id: C-001
  artifact_type: "function"
  artifact_name: "format_date"
  artifact_path: "src/utils/date.py"
  input_spec: "date_str: str（ISO 格式）"
  output_spec: "str（中文日期）或 ValueError"
  acceptance_criteria:
    - "通过契约 C-001 的全部验收条件"
  error_cases:
    - "无效格式 → ValueError"
    - "空字符串 → ValueError"
  depends_on: []
  task_level: L1
```

#### 第 3 步：执行 + 验证（5 分钟）

写代码（或让 AI 写），然后用契约中的输入输出映射验证：

```
输入: format_date("2026-01-10")  → 期望: "2026年1月10日"     ✅/❌
输入: format_date("2025-12-25")  → 期望: "2025年12月25日"    ✅/❌
输入: format_date("not-a-date")  → 期望: ValueError          ✅/❌
输入: format_date("")            → 期望: ValueError          ✅/❌
输入: format_date("2024-02-29")  → 期望: "2024年2月29日"     ✅/❌
```

全部 ✅ → 进入封存。任何 ❌ → 返工，修复后重新验证。

#### 第 4 步：封存（2 分钟）

```yaml
evidence:
  evidence_type: "output_verification"
  gate: "quality_check"
  result: pass
  summary: "5/5 输入输出映射全部通过"
  contract_id: C-001
  task_id: T-001

seal:
  artifact_version: "1.0.0"
  evidence_bundle: ["evidence-T-001-quality_check"]
  sealed_at: "2026-02-11T15:00:00Z"
  sealed_by: "your_name"
```

**完成！** 你刚刚走完了 ODD 的核心闭环：**约定 → 执行 → 验证 → 封存**。

---

### 练习二：+5 分钟 —— 团队协作完整流程

**场景**：在练习一的基础上，你需要一个 `format_date_range` 函数，把两个日期格式化为区间。

#### 第 1 步：写契约草案（1 分钟）

```yaml
contract:
  id: C-002
  title: "日期区间格式化"
  scope_in: "将两个 ISO 日期转为中文区间表示"
  scope_out: "不处理跨年缩写"
  acceptance_criteria:
    - given: "正常区间"
      when: "调用 format_date_range('2026-01-01', '2026-01-31')"
      then: "返回 '2026年1月1日 — 2026年1月31日'"
    - given: "同一天"
      when: "调用 format_date_range('2026-01-01', '2026-01-01')"
      then: "返回 '2026年1月1日'"
    - given: "开始日期晚于结束日期"
      when: "调用 format_date_range('2026-02-01', '2026-01-01')"
      then: "抛出 ValueError，消息包含 'start > end'"
  boundary_cases:
    - "跨年: 2025-12-31 到 2026-01-01"
  floor: "所有 acceptance_criteria 必须通过"
  red_line: "不得修改输入参数；必须复用已封存的 format_date"
  depends_on: [C-001]
  human_confirmed: false        # ← 还没确认，先走对抗
```

#### 第 2 步：清晰度评估（1 分钟）

扮演评估者，检查契约：

```yaml
clarity_detect:
  overall: slightly_unclear
  score: 1
  action: suggest
  issues:
    - type: "边界缺失"
      description: "未定义 null 输入行为"
      severity: yellow
```

发现 🟡 项：null 输入未定义。补充：

```yaml
    - given: "null 输入"
      when: "调用 format_date_range(null, '2026-01-01')"
      then: "抛出 ValueError"
```

#### 第 3 步：简易对抗（2 分钟）

扮演 Challenger 攻击契约：

```
Challenger: "如果两个日期格式不同呢？比如 '2026/01/01' 和 '2026-01-01'？"
→ 修复：scope_in 明确 "两个参数均为 ISO 8601 格式（YYYY-MM-DD）"

Challenger: "依赖的 format_date 未封存怎么办？"
→ 回答：已封存（练习一完成），depends_on: [C-001] 指向封存版本。

Attacker: "我可以返回硬编码字符串通过测试。"
→ 修复：补充随机日期对的属性验证——结果 MUST 包含两个输入日期的中文格式。
```

记录对抗证据：
```yaml
pk_history:
  - round: 1
    attacker: Challenger
    attack_vector: boundary
    issue: "未限制输入格式"
    fix: "scope_in 增加 ISO 8601 约束"
    verdict: pass
  - round: 2
    attacker: Attacker
    attack_vector: malicious
    issue: "可硬编码通过"
    fix: "增加属性验证"
    verdict: pass
```

将 `human_confirmed` 改为 `true`。

#### 第 4 步：执行 + 封存（1 分钟）

复用练习一的流程：写代码 → 输入输出验证 → 封存。

```yaml
seal:
  artifact_version: "1.0.0"
  evidence_bundle:
    - "evidence-T-002-quality_check"
    - "evidence-T-002-pk_history"
  sealed_at: "2026-02-11T15:10:00Z"
  sealed_by: "your_name"
  input_seal_hashes:
    - "seal-C-001-v1.0.0"      # 依赖练习一的封存
```

**完成！** 你体验了：契约依赖、清晰度评估、对抗生成、证据沉淀——这就是 L2 团队协作流程。

---

## 实践

### 下一步
- 想深入契约设计 → `ODD.06CAP-契约对抗生成.md`
- 想了解状态流转 → `ODD.03STM-状态机与门禁.md`
- 想用更多模板 → `ODD.0ATPL-模板库.md`
- 想理解验证原理 → `ODD.10验证-ODD原生验证.md`

### 核心原则
- **先约定再动手**：没有契约就没有方向，没有验收条件就无法判断完成。
- **小步封存**：一个函数一个封印，不要等到"全部写完"再验证。
- **对抗不是找茬**：对抗是在执行前发现问题，成本远低于执行后返工。
- **依赖必须封存**：上游未封存，下游不开工——这是管道的基本纪律。
