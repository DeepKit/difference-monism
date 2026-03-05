---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.01OVR]
---

# 对象模型

## 意向
ODD 的所有工程活动围绕五个核心对象运转：契约、任务、产出物、证据、封存。
它们的复杂度随项目等级伸缩，但核心关系不变：契约定义任务，任务产出产出物，门禁产生证据，证据支撑封存。

## 规范

### 对象关系图
```
契约 ──定义──→ 任务 ──产出──→ 产出物
                    │                │
                门禁检查            封存锁定
                    │                │
                    └──产生──→ 证据 ──绑定──┘
```

### 1. 契约（Contract）
对一件工作的明确约定。契约 MUST 在动工前定义清楚。

### 2. 任务（Task）
契约下的具体工作项。每个任务产出一个产出物。

### 3. 产出物（Artifact）
可验证的具体交付物（代码、文档、配置、测试报告等）。产出物 MUST 可被定位和版本化。

### 4. 证据（Evidence）
门禁检查的结果记录。长内容 MUST 下沉为证据对象，上下文中只注入摘要 + evidence_ref。

### 5. 封存（Seal）
将产出物 + 证据集合锁定。封存后不可变；任何修改 MUST 先解封，解封 MUST 记录原因并触发审计。

---

## 机制

### L1 · 轻量

每个对象只保留最小必要字段。

**契约**：
```yaml
contract:
  id: string
  title: string
  acceptance_criteria: [string]     # 至少 1 条
  boundary_cases: [string]          # 至少 1 条
```

**任务**：
```yaml
task:
  id: string
  contract_id: string
  title: string
  state: pending | in_progress | review | done | rework
  acceptance_criteria: [string]
  depends_on: [task_id]
```

**产出物**：
```yaml
artifact:
  id: string
  task_id: string
  type: string                      # 自由命名
  path: string                      # 定位用
  depends_on: [artifact_id]
```

**证据**：
```yaml
evidence:
  type: test_report
  result: pass | fail
  summary: string
```

**封存**：产出物归档即视为封存，无额外字段。

---

### L2 · 标准

在 L1 基础上增加质量控制和审计字段。

**契约增量**：
```yaml
contract:
  # ...L1 字段...
  scope_in: string                  # 做什么
  scope_out: string                 # 不做什么
  error_cases: [{code, description}]
  quality_score: int                # 质量评分（0-100）
  quality_details: object           # 评分明细
  human_confirmed: bool             # 关键契约人工确认
```

**契约质量评分规则**：
| 检查项 | 分值 | 说明 |
|--------|------|------|
| 标题清晰度 | 10 | ≥ 10 字符且无歧义 |
| 描述完整度 | 15 | ≥ 50 字符，含背景和目标 |
| 验收标准数量 | 20 | ≥ 3 条得满分 |
| 验收标准可验证性 | 15 | 每条有明确 Given-When-Then |
| 边界情况覆盖 | 20 | ≥ 3 条，覆盖最小/最大/空值 |
| 异常情况定义 | 15 | ≥ 1 条，有明确错误码 |
| 安全级别标注 | 5 | 已标注安全级别 |

**激活阈值**：
- ≥ 80 分：可直接激活
- 60-79 分：警告，建议补充
- < 60 分：禁止激活，必须补充

**任务增量**：
```yaml
task:
  # ...L1 字段...
  state: blocked | pending | in_progress | quality_check | acceptance | done | rework
  task_level: L1 | L2
  artifact_type: string
  input_spec: string
  output_spec: string
  side_effects:                     # 行为类产出物必填
    - type: string                  # 副作用类型
      target: string                # 影响目标
      description: string
  expected_effects:                 # 对副作用的可验证声明（可选）
    - type: string
      target: string
      data_match: object?           # 期望匹配的字段/值
  rework_count: int
  failure_context:
    evidence_ref: string
    summary: string
```

**副作用类型**：
| 类型 | 说明 |
|------|------|
| db_read / db_write | 数据库读写 |
| cache_read / cache_write | 缓存读写 |
| data_insert / data_update / data_delete | 数据变更（显式） |
| event_emission | 发送事件 |
| message_publish / message_send | 发布/发送消息 |
| notification_email / notification_sms | 发送通知 |
| http_request / external_call | 外部调用 |
| file_read / file_write / file_create | 文件操作 |
| log_write | 日志记录 |
| time_get / random_generate | 非确定性来源 |

**产出物增量**：
```yaml
artifact:
  # ...L1 字段...
  state: sealed | stale
  dependency_graph:
    upstream: [artifact_id]
    downstream: [artifact_id]
```

**证据增量**：
```yaml
evidence:
  # ...L1 字段...
  evidence_type: test_report | coverage_report | lint_report | review_record
  storage_ref: string
  sha256: string
  gate: string                      # 关联的门禁
  contract_id: string
  task_id: string
```

**封存增量**：
```yaml
seal:
  artifact_version: string
  evidence_bundle: [evidence_ref]
  sealed_at: datetime
  sealed_by: string
```

---

### L3 · 严格

在 L2 基础上增加对抗生成、动态门禁链、不可变封存。

**契约增量**：
```yaml
contract:
  # ...L2 字段...
  formal_spec:                      # 形式化规格
    preconditions: [string]
    postconditions: [string]
    invariants: [string]
  temporal_config:                  # 时间维度
    lifecycle: string
    data_growth: string
    concurrency: string
    considerations: [string]?
    confirmed_by_human: bool?
  pk_history:                       # 对抗生成记录
    - round: int
      issue: string
      fix: string
      verdict: string

**形式化语法规则（简版）**：
- 允许：`== != > >= < <=`、`AND/OR/NOT`、`len()`、`regex_match()`、`in`、`IMPLIES`。
- 约束必须可验证，避免主观词（如“快速”“优秀”）。

**形式化示例**：
```yaml
formal_spec:
  preconditions:
    - "username != null"
    - "len(username) >= 3"
    - "regex_match(email, '.*@.*')"
  postconditions:
    - "result.success == true OR result.error != null"
    - "result.success == true IMPLIES result.token != null"
  invariants:
    - "user.password_hash != user.password_plain"
```

**时间维度默认值**（可直接确认）：
- lifecycle: temporary | short_term | medium_term | long_term（默认 medium_term）
- data_growth: stable | linear | exponential（默认 linear）
- concurrency: <10 | 10-100 | 100-1000 | >1000（默认 10-100）
- considerations: i18n | multi_timezone | data_migration | offline_support（可选）

人类确认规则：
- 若使用默认值，可一键确认。
- 若修改默认值，MUST 记录 confirmed_by_human。

```

**任务增量**：
```yaml
task:
  # ...L2 字段...
  task_level: L1 | L2 | L3 | L4
  gate_chain: [string]              # 动态门禁序列
  developed_by_workshop_id: string  # 交叉审核用
```

**产出物增量**：
```yaml
artifact:
  # ...L2 字段...
  seal_hash: string                 # 指向 seal 记录的哈希
```
产出物上只保留 seal_hash 作为指向，完整的封存记录见下方独立的 seal 对象。

**证据增量**：
```yaml
evidence:
  # ...L2 字段...
  evidence_type: ...L2类型... | mutation_report | adversarial_report | cross_review_record | human_review_record
  mutation_score: float?
  vulnerability_count: int?
  reviewers: [string]?
  consensus: bool?
  workshop_id: string
```

**封存增量**：
```yaml
seal:
  # ...L2 字段...
  seal_hash: string                 # 不可篡改的哈希
  input_seal_hashes: [string]       # 上游产出物的 seal_hash
  gate_results: [evidence_ref]      # 所有门禁证据
  audit_record_ref: string

unseal:
  reason: string                    # 解封原因（bug 描述）
  by: string                        # 解封授权人（必须是人类）
  at: datetime
  count: int                        # 累计解封次数
```

**解封规则**：
- 只有人类可以授权解封，AI 不得自行解封。
- MUST 填写解封原因。
- 解封后状态变为 rework，原封版代码自动归档。
- 解封次数累加，用于质量分析（频繁解封提示契约或测试质量问题）。

**解封流程**：
```
发现 bug → 人类发起解封请求（填写原因）
  → 系统记录审计日志
  → 原封版代码归档
  → 状态 sealed → rework
  → unseal_count + 1
  → 正常返工流程
```

---

## 实践

### 快速选型
- **一个人写小工具** → L1，每个对象 3-5 个字段就够。
- **团队协作** → L2，加上质量控制和依赖跟踪。
- **关键系统 / AI 协作** → L3，完整的形式化规格、对抗生成、证据链。

### 核心原则
- 对象字段是累加的：L2 是 L1 的超集，L3 是 L2 的超集。
- 关系是不变的：无论哪个等级，“契约→任务→产出物→证据→封存”的链条不变。
