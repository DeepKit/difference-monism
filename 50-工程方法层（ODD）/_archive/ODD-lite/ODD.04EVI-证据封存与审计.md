---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.02OBJ]
---

# 证据封存与审计

## 意向
说“做完了”不够，要拿得出证据。
证据是门禁的产物，封存是证据的终点，审计是不可篡改的记录。

## 规范

### 证据优先原则
- 所有门禁结论 MUST 有证据可复验。
- 长输出（日志、测试报告、终端会话）MUST 下沉为证据对象，不得内联在上下文中。
- 上下文 MUST 只注入：摘要 + evidence_ref。

### 封存规则
- 封存 MUST 绑定：产出物版本 + 证据集合。
- 封存后产出物 MUST 不可变；任何修改 MUST 先解封。
- 解封 MUST 记录原因、操作者、时间，并触发下游重新验证。

### 审计规则
- 审计记录 MUST 不可被执行者篡改。
- 任何结论进入知识库 MUST 带来源引用（task_id / evidence_ref / version）。

---

## 机制

### L1 · 轻量

**证据**：产出物本身就是证据。测试通过的报告 = 证据。
```yaml
evidence:
  type: test_report
  result: pass | fail
  summary: string
```

**封存**：产出物归档即视为封存。无额外流程。

**审计**：无正式审计。产出物的版本控制历史（如 git log）即为记录。

---

### L2 · 标准

**证据**：结构化记录，每条证据关联门禁和任务。
```yaml
evidence:
  id: string
  evidence_type: test_report | coverage_report | lint_report | review_record
  gate: string                        # 关联哪个门禁
  result: pass | fail
  summary: string
  storage_ref: string                 # 存储位置
  sha256: string
  contract_id: string
  task_id: string
```

**封存**：显式绑定产出物 + 证据集合。
```yaml
seal:
  artifact_version: string
  evidence_bundle: [evidence_id]
  sealed_at: datetime
  sealed_by: string
```

**解封**：
```yaml
unseal:
  reason: string
  by: string
  at: datetime
```
解封后，下游依赖的产出物自动标记为 stale。

**审计日志**：记录关键操作（封存、解封、门禁结果）。
```yaml
audit_log:
  action: seal | unseal | gate_pass | gate_fail
  target_id: string
  by: string
  at: datetime
  details: string
```

**证据检索**：系统 SHOULD 提供按需查询能力（tail / grep / slice）。

---

### L3 · 严格

**证据增强**：
- 增加变异测试、对抗测试、交叉审查、人工审查等证据类型。
- 证据对象 MUST 包含 workshop_id（来源车间）。

**封存增强**：
- 生成 seal_hash（产出物内容 + 证据集合的哈希），不可篡改。
- 包含所有输入产出物的 seal_hash（证据链传递）。
- sealed 状态不可逆（与 L2 的可解封不同）。如需修改，必须创建新版本。

```yaml
seal:
  seal_hash: string
  input_seal_hashes: [string]         # 上游产出物的 seal_hash
  evidence_refs: [string]
  gate_results: [evidence_ref]
  sealed_at: datetime
  audit_record_ref: string
```

**审计增强**：
- 审计日志 MUST 不可篡改（append-only）。
- 每条审计记录包含前一条的 hash（链式完整性）。
- 解封操作 MUST 记录累计次数，异常解封 SHOULD 触发告警。

---

## 实践

### 快速选型
- **小项目** → L1，测试报告就是证据，归档就是封存。
- **团队项目** → L2，结构化证据 + 审计日志 + 可解封。
- **关键系统** → L3，不可篡改的审计链 + 证据链传递 + 封存不可逆。

### 核心原则
- **证据不内联**：长内容下沉为证据对象，上下文只用引用。
- **封存是终点**：封存后的产出物是确定的、可信赖的。
- **审计不可篡改**：执行者不能修改自己的审计记录。
