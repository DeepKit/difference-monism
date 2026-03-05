---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.02OBJ]
---

# 状态机与门禁

## 意向
每一次状态迁移都必须有理由、有证据、有记录。
没有通过门禁的产出物，不允许流向下游。

## 规范

### 基本定义
- **状态（State）**：产出物在生命周期中的位置标识。
- **门禁（Gate）**：状态之间的检查点，决定是否允许迁移。
- **证据绑定（Evidence Binding）**：每次通过门禁 MUST 关联至少一条证据记录。
- **返工（Rework）**：门禁未通过时的回退路径，MUST 携带 failure_context。

### 状态迁移规则
- 迁移 = 门禁检查 + 证据绑定 + 审计记录，三者缺一不可。
- failure_context MUST 引用证据对象（evidence_ref），不得内联大段日志。
- task_level 决定需要经过哪些门禁；人工覆盖 MUST 只能升级，不能降级。

---

## 机制

### L1 · 轻量

**状态机**：
```
pending → in_progress → review → done
           ↖── rework ──↙
```

**门禁**：只有一道——`review`。
- 通过条件：自动测试全部通过。
- 证据：测试报告（通过/失败 + 覆盖率）。
- 失败处理：回到 `in_progress`，附带失败原因摘要。

**最小数据结构**：
```yaml
task:
  id: string
  state: pending | in_progress | review | done | rework
  evidence:
    - type: test_report
      result: pass | fail
      summary: string
```

---

### L2 · 标准

**状态机**：在 L1 基础上增加 `blocked` 和 `quality_check`。
```
blocked → pending → in_progress → quality_check → acceptance → done
                      ↖──────── rework ────────↙
```

**门禁**：两道——`quality_check` + `acceptance`。
- `quality_check`（自动）：
  - 通过条件：测试通过 + 覆盖率 ≥ 阈值 + 静态分析无严重项。
  - 证据：测试报告 + 覆盖率报告 + lint 报告。
- `acceptance`（人工）：
  - 通过条件：审查者确认产出物符合契约验收条件。
  - 证据：审查记录（审查者ID + 结论 + 备注）。

**返工增强**：
- rework 记录包含：触发门禁、失败证据引用、返工次数。
- 返工次数 ≥ 3 时，SHOULD 自动升级 task_level。

**数据结构增量**：
```yaml
task:
  # ...L1 字段...
  state: blocked | pending | in_progress | quality_check | acceptance | done | rework
  task_level: L1 | L2
  rework_count: int
  evidence:
    - type: test_report | coverage_report | lint_report | review_record
      gate: quality_check | acceptance
      result: pass | fail
      reviewer_id: string?      # 人工门禁时填写
      failure_context:
        evidence_ref: string    # 指向具体证据ID
        summary: string
```

---

### L3 · 严格

**状态机**：在 L2 基础上增加风险驱动的动态门禁链。
```
blocked → pending → in_progress → quality_check
  → [mutation_test] → [adversarial_test] → [cross_review] → [human_review]
  → acceptance → sealed
       ↖──────────────── rework ────────────────↙
```

方括号 = 按 task_level 动态插入：
- L1 任务：跳过所有扩展门禁。
- L2 任务：插入 mutation_test。
- L3 任务：插入 mutation_test + adversarial_test。
- L4 任务：全部插入，含 human_review。

**门禁详细**：
- `mutation_test`：
  - 通过条件：mutation_score ≥ 阈值（建议 80%）。
  - 证据：变异测试报告（存活变异体列表 + 总分）。
- `adversarial_test`：
  - 通过条件：无高危漏洞存活。
  - 证据：漏洞列表 + 复现实验记录。
- `cross_review`：
  - 通过条件：多方审查者共识（≥ 2/3 通过）。
  - 证据：各方意见 + 裁决依据。
  - 报告结构：
    ```yaml
    cross_review_report:
      reviewers: [workshop_id]       # 参与审查的车间
      opinions:
        - reviewer: workshop_id
          verdict: pass | fail | concern
          comments: [string]
      consensus: bool                # 是否达成共识
      escalated: bool                # 是否升级人类
      escalation_reason: string?     # 分歧描述
    ```
- `human_review`：
  - 触发条件：cross_review 产生分歧，或 task_level = L4。
  - 证据：人类裁决记录 + 理由。

**封存（Sealed）**：
- `done` 升级为 `sealed`——状态不可逆，证据链冻结。
- sealed MUST 生成 seal_hash，绑定全部 evidence_ref。

**数据结构增量**：
```yaml
task:
  # ...L2 字段...
  state: ...L2状态... | mutation_test | adversarial_test | cross_review | human_review | sealed
  task_level: L1 | L2 | L3 | L4
  gate_chain: [string]           # 动态生成的门禁序列
  seal:
    seal_hash: string
    sealed_at: datetime
    evidence_refs: [string]      # 全部证据ID
  evidence:
    - type: ...L2类型... | mutation_report | adversarial_report | cross_review_record | human_review_record
      gate: string
      result: pass | fail
      mutation_score: float?
      vulnerability_count: int?
      reviewers: [string]?
      consensus: bool?
```

---

## 实践

### 快速选型指南
- **我一个人写个小工具** → 用 L1，4 个状态够了。
- **团队协作、有代码审查流程** → 用 L2，加上人工验收门禁。
- **AI 多角色协作、关键系统** → 用 L3，上动态门禁链和封存。

### task_level 分级算法

AI 自动分级 + 人类可覆盖。任务创建时自动完成，人类确认后保存。

**四维度评分**：
| 维度 | L1 (1分) | L2 (2分) | L3 (3分) | L4 (4分) |
|------|----------|----------|----------|----------|
| 预估代码行数 | < 30 | 30-100 | 100-300 | > 300 |
| 功能复杂度 | 单表 CRUD | 多表关联 | 复杂算法 | 分布式/并发 |
| 安全敏感度 | 无 | 低（日志） | 中（用户数据） | 高（认证/支付） |
| 外部依赖数 | 0 | 1-2 | 3-5 | > 5 |

**计算规则**：`最终级别 = MAX(各维度级别)` —— 短板原则，任何单一高风险维度不会被其他低风险维度稀释。

**人类覆盖规则**：
- 人类可手动调整级别，**只能升级，不能降级**。
- 降级需要输入理由并记录审计日志。

### 验证策略分类

artifact_type 决定验证策略，验证策略决定跳过哪些状态：

| 策略 | quality_check | acceptance | mutation_test | 适用 |
|------|--------------|------------|---------------|------|
| automated | 自动单元测试 | 自动集成测试 | 执行 | 代码类 |
| executed | 执行验证 | 效果验证 | 跳过 | 数据库/行为类 |
| reviewed | 格式检查 | 人工审核 | 跳过 | 文档类 |
| single | 跳过 | 合并验证 | 跳过 | 简单配置 |
| none | 跳过 | 跳过 | 跳过 | 注释/日志 |

### 外部显示标签

内部状态统一，外部按产出物类别显示专业术语：

| 内部状态 | 代码类 | 数据库类 | 行为类 | 文档类 | 配置类 |
|----------|--------|----------|--------|--------|--------|
| in_progress | 开发中 | 开发中 | 开发中 | 编写中 | 配置中 |
| quality_check | 单元测试中 | DDL执行中 | 触发验证中 | 格式检查中 | 语法验证中 |
| acceptance | 集成测试中 | 数据验证中 | 效果验证中 | 内容审核中 | 生效验证中 |
| mutation_test | 变异测试中 | 变异测试中 | 变异测试中 | 跳过 | 跳过 |

未列出的状态（blocked/pending/sealed/rework）各类别标签相同。

### 适配建议
- 可以按模块混用等级：核心模块 L3，工具脚本 L1。
- 门禁阈值（覆盖率、mutation_score 等）由项目自行设定，ODD 不规定具体数值。
