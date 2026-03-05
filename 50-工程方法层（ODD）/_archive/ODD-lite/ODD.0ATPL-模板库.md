---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [无]
---

# 模板库

## 意向
复制→填空→开工。按等级选模板，不用从零开始。

## 规范
- 选用与项目等级一致的模板，不跨级套用。
- 模板字段可增补，不得删除必填字段。
- 先填清验收与边界，再进入实现。

## 机制

---

## L1 · 轻量模板

### 契约
```yaml
contract:
  title: ""
  acceptance_criteria:
    - ""
  boundary_cases:
    - ""
```

### 任务
```yaml
task:
  title: ""
  contract_id: ""
  acceptance_criteria:
    - ""
  depends_on: []
```

### 产出物
```yaml
artifact:
  type: ""
  path: ""
  depends_on: []
```

---

## L2 · 标准模板

### 契约
```yaml
contract:
  title: ""
  scope_in: ""
  scope_out: ""
  acceptance_criteria:
    - given: ""
      when: ""
      then: ""
  boundary_cases:
    - ""
  error_cases:
    - code: ""
      description: ""
  human_confirmed: false
```

### 任务
```yaml
task:
  title: ""
  contract_id: ""
  artifact_type: ""
  artifact_name: ""
  artifact_path: ""
  input_spec: ""
  output_spec: ""
  acceptance_criteria:
    - ""
  error_cases:
    - ""
  depends_on: []
  task_level: L1
```

### 证据
```yaml
evidence:
  evidence_type: ""
  gate: ""
  result: pass | fail
  summary: ""
  storage_ref: ""
  sha256: ""
  contract_id: ""
  task_id: ""
```

### 封存
```yaml
seal:
  artifact_version: ""
  evidence_bundle: []
  sealed_at: ""
  sealed_by: ""
```

### 返工上下文（rework 时必填）
```yaml
failure_context:
  rework_number: 1
  from_status: ""
  failure_reason: ""
  failure_evidence_refs: []
  previous_attempts:
    - ""
```

---

## L3 · 严格模板

### 契约（在 L2 基础上增加）
```yaml
contract:
  # ...L2 字段...
  formal_spec:
    preconditions: []
    postconditions: []
    invariants: []
  temporal_config:
    lifecycle: ""
    data_growth: ""
    concurrency: ""
  pk_history:
    - round: 1
      issue: ""
      fix: ""
      verdict: ""
```

### 任务（在 L2 基础上增加）
```yaml
task:
  # ...L2 字段...
  task_level: L1 | L2 | L3 | L4
  gate_chain: []
  developed_by_workshop_id: ""
```

### 封存（在 L2 基础上增加）
```yaml
seal:
  # ...L2 字段...
  seal_hash: ""
  input_seal_hashes: []
  gate_results: []
  audit_record_ref: ""
```

### 审计日志
```yaml
audit_log:
  action: seal | unseal | gate_pass | gate_fail
  target_id: ""
  by: ""
  at: ""
  previous_hash: ""
  details: ""
```

---

## 通用模板（跨等级）

### 管道
```yaml
pipeline:
  id: ""
  name: ""
  description: ""
  inputs:                              # 已封存产出物
    - artifact_id: ""
      seal_version: ""
  stages:
    - name: ""
      contract_id: ""
      task_ids: []
  output:
    artifact_id: ""
    artifact_type: ""
  depends_on_pipelines: []
```

### 功能节点
```yaml
functional_node:
  id: ""
  name: ""
  parent: ""                           # null 为根节点
  children: []
  artifacts: []                        # 映射的产出物 ID
  owner: ""
  status: active | deprecated | planned
```

### CAP 对抗记录
```yaml
cap_record:
  contract_id: ""
  clarity_detect:
    overall: clear | slightly_unclear | very_unclear
    score: 0
    action: pass | suggest | must_answer
    issues:
      - type: ""
        description: ""
        severity: green | yellow | red
    human_answers: []
  pk_history:
    - round: 1
      attacker: Challenger | Attacker
      attack_vector: logic | boundary | malicious
      issue: ""
      fix: ""
      verdict: pass | escalate
```

### Bug 模式条目
```yaml
bug_pattern:
  id: ""
  artifact_type: ""
  pattern: ""
  detection_rule: ""
  severity: critical | high | medium | low
  frequency: 0
  prevention: ""
  source_task_id: ""                   # 首次发现的任务
```

### 最佳实践条目
```yaml
best_practice:
  id: ""
  artifact_type: ""
  practice: ""
  rationale: ""
  anti_pattern: ""
  priority: 1                          # 1-10
  is_mandatory: false
```

### 车间
```yaml
workshop:
  id: ""
  contract_id: ""
  status: idle | active | paused | failed | completed
  assigned_to: ""                      # 执行者（人类/AI）
  task_ids: []
  knowledge_cache: []                  # 车间级知识缓存
  created_at: ""
  last_active_at: ""
```

### 预警事件
```yaml
alert:
  id: ""
  level: green | yellow | red
  source: ""
  message: ""
  triggered_at: ""
  acknowledged_by: ""
  resolution: ""                       # 处理结果
```

### 赛马任务分配
```yaml
racing_assignment:
  task_id: ""
  task_grade: L1 | L2 | L3 | L4
  assigned_level: ""
  attempt: 1
  max_attempts: 3
  failure_diagnosis: ""
  escalated: false
  escalated_to: ""
```

---

## 实践
- 小项目：直接用 L1。
- 团队协作：从 L2 起步，按需选用通用模板。
- 关键系统：使用 L3 并补充 formal_spec 与 temporal_config，配套使用全部通用模板。
