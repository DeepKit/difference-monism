---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.03STM, ODD.0F车间]
---

# 智能赛马

## 意向
不是选最好的执行者，而是选够用的执行者。
简单任务用低成本资源，失败后再按需升级——先诊断原因，再决定升级方向。

## 规范

### 核心原则
- 执行者（模型/人）选择 MUST 基于任务复杂度，不得一律使用最强资源。
- 失败后 MUST 先诊断原因，再决定升级路径；盲目升级是反模式。
- 成本 SHOULD 可监控、可预算、可告警。

### 失败诊断优先
失败 MUST 归入以下五类原因之一，对应不同处理路径：
- **上下文不足**：补充上下文 → 同级重试 → 不消耗升级次数。
- **契约模糊**：修正契约/任务描述 → 同级重试 → 不消耗升级次数。
- **测试不合理**：审核测试有效性 → 修正测试 → 不消耗升级次数。
- **执行能力不足**：升级执行者 → 消耗升级次数。
- **未知问题**：升级执行者（保守策略）→ 消耗升级次数。

只有"执行能力不足"和"未知问题"才触发升级。其他原因在同级修正。

### 升级路径
```
初级 ──失败──→ 中级 ──失败──→ 高级 ──失败──→ 人工介入
  │              │               │
  └──成功────────┴──成功─────────┴──成功──→ 完成
```
到达最高级仍失败 MUST 升级人类决策。

---

## 机制

### L1 · 轻量

无正式赛马。执行者固定（人或指定模型）。失败后人工决定是否更换。

---

### L2 · 标准

**任务分级**：根据复杂度预选执行者等级。

分级参考因素：
- 产出物类型（配置 vs 算法）
- 预估代码量（< 50 行 vs > 200 行）
- 依赖数量（0-2 个 vs > 5 个）
- 历史返工率

```yaml
rules:
  - name: 简单任务
    conditions:
      - artifact_type in [config, script, simple_query]
      - estimated_lines < 50
    executor_level: junior

  - name: 标准任务
    conditions:
      - artifact_type in [code_module, api_endpoint]
      - estimated_lines < 200
      - dependencies < 3
    executor_level: standard

  - name: 复杂任务
    conditions:
      - artifact_type in [algorithm, architecture]
      - or: rework_count > 1
    executor_level: senior
```

**失败升级**：按返工次数自动升级。
- 0-1 次返工：初级。
- 2-3 次返工：中级。
- 4-5 次返工：高级。
- ≥6 次返工：触发人类告警（见分级预警文档）。

**诊断**：失败时系统记录失败类型（编译错误/测试失败/验收失败/超时），供人工参考。

---

### L3 · 严格

**智能诊断**：失败后由诊断者（经理 AI 或规则引擎）分析根因，决定处理路径。

```
任务失败
  │
  ├── 原因A: 上下文不足
  │     → 补充上下文（从知识库/功能树/依赖图获取）
  │     → 同级重试
  │     → 不消耗升级次数
  │
  ├── 原因B: 契约模糊
  │     → 触发清晰度重评估（见 CAP 文档）
  │     → 修正后同级重试
  │     → 不消耗升级次数
  │
  ├── 原因C: 测试不合理
  │     → 审核测试有效性（变异测试分数异常低？测试与契约不匹配？）
  │     → 修正测试后同级重试
  │     → 不消耗升级次数
  │
  ├── 原因D: 执行能力不足
  │     → 升级到更高级执行者
  │     → 消耗升级次数
  │
  └── 原因E: 未知问题
        → 升级执行者（保守策略）
        → 消耗升级次数
```

**成本监控**：
- 系统 SHOULD 记录每个任务的执行者等级、调用次数、升级次数。
- 系统 SHOULD 提供聚合视图：一次成功率、升级成功率、人工介入率。
- 升级率 > 30% 时 SHOULD 触发预警，提示检查任务分级规则或契约质量。

**数据结构**：
```yaml
task_execution:
  task_id: string
  executor_level: junior | standard | senior
  rework_count: int
  upgrade_count: int                    # 实际消耗的升级次数
  diagnosis_history:
    - attempt: 1
      failure_type: test_failed
      diagnosis: context_insufficient
      action: inject_context
    - attempt: 2
      failure_type: test_failed
      diagnosis: executor_insufficient
      action: upgrade_executor
  cost: float                           # 执行成本
```

---

## 实践

### 快速选型
- **个人项目** → L1，固定执行者，手动决策。
- **团队项目** → L2，按复杂度分级 + 自动升级。
- **AI 多角色协作** → L3，智能诊断 + 按需升级 + 成本监控。

### 核心原则
- **够用就好**：不是选最强的，而是选最合适的。80% 的任务不需要最强执行者。
- **先诊断再升级**：60% 的失败不是执行者的问题（上下文 60% + 契约 30% + 执行者 10%）。
- **成本可见**：不监控成本就无法优化成本。
