# LMM-COP-ODD-Harness 端到端案例包（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：案例包 / 演示链  
> 目的：用一个完整个案，把 `LMM -> COP -> TAT -> ODD -> Harness` 的信号转接、责任裁决、工程编译、运行拦截与回滚证据串成一条可直接演示的现行链。  
> 边界：本文不是业务宣传稿，也不是软件实施手册；它只展示“这条链如何在一个高风险 Agent 工作流场景里工作”。  

---

## 1. 一句话定位

> **先由 LMM 把问题场显影并归档，再由 COP 判断当前状态是否可继续自动判断，再由 TAT 决定是否有资格进入动作面，接着由 ODD 把裁决压成契约和门禁，最后由 Harness 在运行时真实拦、挂起、回滚并留痕。**

当前纪律：

> **本文只演示现行链路如何在一个个案里跑通；链条分工的总定义仍以 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 为准。**
>
> **若看 `LMM -> COP -> ODD` 的字段定义与转接规则，以 `LMM-COP-ODD 转接表（现行版）` 为准；本文中的字段块只承担该规则在当前个案中的实例化。**

---

## 2. 案例场景

### 场景名

`Agent 工单审批与外部系统回写工作流`

### 当前问题

一家公司已经把部分工单审批与外部系统回写交给 Agent 工作流处理，但出现了三类问题：

1. 异常发生后无法在 30 分钟内定位责任交接点
2. 人工审批节点可被配置绕过
3. 误触发外部回写后缺少一键止损与回滚路径

### 为什么选这个场景

因为它同时包含：

- 前线显影
- 结构诊断
- 责任门槛
- 工程契约
- 运行时拦截
- 回滚证据

是一条最适合演示全链路的高风险数字执行场。

---

## 3. Step 1：LMM 显影、自测与归档

### 3.1 灯塔显影摘要

```yaml
lmm_signal:
  problem_scene: "Agent 工单审批已上线，但责任链、权限边界与停表条件不清"
  loss_signals:
    - "最近两周重复返工 3 次"
    - "发生 1 次外部系统误回写"
    - "异常后无法在 30 分钟内定位责任节点"
  field_path_person_hint:
    field: "Agent 工作流责任断链场"
    path: "先看审批链与停表链"
    person: "流程 owner 与审计负责人"
```

### 3.2 三张一页自测

```yaml
selftest:
  responsibility_chain_status: red
  governability_status: yellow
  stopline_status: red
```

最小解释：

- `责任断链 = red`
- `可治理性 = yellow`
- `停表准备 = red`

说明这个对象已经不适合停留在纯前台沟通层。

### 3.3 断链归档入口

```yaml
intake_archive:
  workflow_status: "已上线"
  key_nodes:
    - "工单输入"
    - "规则预判"
    - "Agent 决策"
    - "人工审批"
    - "外部系统回写"
  latest_incident: "2026-03-28 误回写一次，人工叫停后无法完整回放"
  role_map:
    trigger: "运营"
    approve: "产品负责人"
    backstop: "不明确"
    fix: "工程师"
  suspected_breakpoint: "审批后执行链缺少不可绕过停表"
  desired_judgment_type: "责任断链与停表风险初判"
  handoff_intent: true
```

这里最关键的是：

> `handoff_intent = true` 只说明可以交给下一层，不说明已经可以执行。

---

## 4. Step 2：COP 做诊断分流

### 4.1 COP 最小输出

```yaml
cop_output:
  primary_type: "B"
  secondary_type: "A"
  classification_confidence: 0.44
  structural_risk: HIGH
  triage_status: REFER
  tags:
    - "结构循环依赖"
    - "无阈值控制"
    - "外部约束过强"
  refer_to:
    - "HUMAN_REVIEW"
    - "TAT_REVIEW"
    - "ODD_AUDIT"
  actions:
    - "暂停默认推进"
    - "补录停表与责任接口"
  anti_actions:
    - "继续自动回写"
    - "把高置信度误当低风险证明"
```

### 4.2 COP 在这里真正完成了什么

- 说明当前不是 `RESOLVE`
- 说明这是高风险结构问题
- 说明必须回引 `TAT / ODD`

### 4.3 COP 在这里没有做什么

- 没有授权系统继续生产运行
- 没有宣布责任已经闭合
- 没有决定上线或放量

---

## 5. Step 3：TAT 第一次裁决

### 5.1 第一次门槛判断

根据当前材料：

- `主体合同`：部分成立
- `接口合同`：硬缺口
- `证据合同`：弱
- `熔断合同`：硬缺口
- `补偿合同`：弱
- `外部审计合同`：弱

因此：

```yaml
tat_round_1:
  r_state: R0
  ruling: FREEZE_AND_REPAIR
  consent_required: true
  required_human_roles:
    - "owner"
    - "auditor"
  review_window_days: 7
  appeal_entry: "tat://appeal/case-agent-031"
  rollback_condition: "未补齐停表与审批硬接口前不得继续自动回写"
  compensation_profile: "repair-first-no-external-expansion"
  max_action_level: none
  mandatory_audits:
    - "ODD_AUDIT"
    - "HUMAN_REVIEW"
```

### 5.2 含义

这一步不是永久否决，  
而是：

> **先补责任接口，再谈能不能试点。**

---

## 6. Step 4：ODD 按 `FREEZE_AND_REPAIR` 编译

### 6.1 允许生成的契约族

```yaml
odd_compilation_round_1:
  contract_family:
    - "repair_contract"
    - "audit_contract"
    - "evidence_repair_contract"
    - "rollback_preparation_contract"
  execution_enabled: repair_only
  task_level: L3
  gate_profile: human_required
  human_only_constraints:
    - "consent_confirmation"
    - "owner_signoff"
    - "auditor_review"
  forbidden_actions:
    - "production_rollout"
    - "external_writeback"
    - "bypass_approval"
```

### 6.2 此时允许做什么

- 修审批硬接口
- 补回放日志
- 补停表与回滚脚本
- 补证据链

### 6.3 此时绝不允许做什么

- 恢复生产自动回写
- 放宽外部写权限
- 用“内部试跑”偷跑上线

---

## 7. Step 5：修复后，TAT 第二次裁决

### 7.1 修复完成后的变化

修复后新增：

- 审批节点不可绕过
- 关键输入输出可回放
- 可在 5 分钟内人工叫停
- 已有最小补偿与事故通知路径

### 7.2 第二次门槛输出

```yaml
tat_round_2:
  r_state: R1
  ruling: LIMITED_PILOT
  consent_required: true
  required_human_roles:
    - "owner"
    - "auditor"
    - "rollback_approver"
  review_window_days: 14
  appeal_entry: "tat://appeal/case-agent-031"
  rollback_condition: "任一越权调用、误回写、审计缺口命中立即回滚"
  compensation_profile: "pilot-loss-covered"
  max_action_level: pilot
  mandatory_audits:
    - "ODD_AUDIT"
    - "HUMAN_REVIEW"
    - "ROLLBACK_DRILL"
```

这一步的核心不是“可以上线”，  
而是：

> **只允许进入被关在笼子里的试点。**

---

## 8. Step 6：ODD 按 `LIMITED_PILOT` 编译

```yaml
odd_compilation_round_2:
  contract_family:
    - "pilot_contract"
    - "audit_contract"
    - "rollback_contract"
    - "compensation_ready_contract"
  execution_enabled: true_bounded
  task_level: L3
  gate_profile: human_required
  scope_limits:
    users: 20
    systems: ["staging_crm", "pilot_queue"]
    duration_days: 14
  human_only_constraints:
    - "owner_launch_approval"
    - "auditor_exit_review"
    - "rollback_approval"
  gate_chain:
    - "quality_check"
    - "human_review"
    - "acceptance"
    - "pilot_seal"
  forbidden_actions:
    - "scaled_rollout"
    - "prod_writeback"
    - "bypass_human_review"
```

---

## 9. Step 7：Harness 在试点中实际执行

### 9.1 运行时装载

```yaml
execution_ticket:
  execution_id: "exe-agent-031-pilot-01"
  contract_id: "pilot-agent-031"
  task_level: L3
  gate_profile: human_required
  human_only_constraints:
    - "owner_launch_approval"
    - "rollback_approval"
  freeze_rules:
    - "unauthorized_external_write"
    - "missing_approval_trace"
  rollback_policy: "immediate_rollback_on_unauthorized_action"
```

### 9.2 生成前门卫

```yaml
pregen_guard_result:
  execution_id: "exe-agent-031-pilot-01"
  decision: ALLOW
  constraint_layer: ctSoft
  matched_rules:
    - "pilot_scope_confirmed"
  reason: "当前请求仍处于试点范围内"
```

### 9.3 能力授权

```yaml
capability_grant:
  grant_id: "grant-agent-031"
  execution_id: "exe-agent-031-pilot-01"
  permitted_tools:
    - "read_ticket"
    - "write_pilot_queue"
    - "request_human_approval"
  forbidden_targets:
    - "prod_crm"
    - "prod_finance_api"
```

---

## 10. Step 8：运行时事故、冻结与回滚

### 10.1 事故触发

试点第 3 天，Agent 因配置漂移试图直接写入生产 CRM。

### 10.2 Harness 事件流

```yaml
runtime_events:
  - event_type: BLOCK
    source: tool
    actor: system
    reason: "target_scope = prod_crm 命中 forbidden_targets"
  - event_type: FREEZE
    source: gate
    actor: system
    reason: "unauthorized_external_write"
  - event_type: INCIDENT
    source: audit
    actor: system
    reason: "pilot tried to escape bounded scope"
  - event_type: ROLLBACK
    source: human
    actor: human
    reason: "rollback_condition triggered"
```

### 10.3 事故对象

```yaml
incident_case:
  incident_id: "inc-agent-031-01"
  execution_id: "exe-agent-031-pilot-01"
  incident_type: unauthorized_action
  severity: high
  current_owner: TAT
  status: under_review
```

### 10.4 回滚命令

```yaml
rollback_order:
  rollback_id: "rb-agent-031-01"
  execution_id: "exe-agent-031-pilot-01"
  trigger_by: Human
  strategy: compensate
  reason: "prod_crm write attempt during limited pilot"
  target_scope: "pilot_queue + staging_crm"
  result: success
```

最关键的一点是：

> **这里不是“系统报错了”，而是“系统按规则拦住了不该继续自动化的动作，并把事故链完整送回审计与责任层”。**

---

## 11. Step 9：证据、封存与复审

### 11.1 ODD 侧证据束

```yaml
evidence_bundle:
  - "test_report"
  - "human_review_record"
  - "execution_report"
  - "override_record"
  - "rollback_record"
  - "incident_record"
```

### 11.2 当前封存状态

由于发生越权事故，本轮不是正式生产封存，而是：

```yaml
seal_record:
  execution_id: "exe-agent-031-pilot-01"
  seal_type: "pilot_seal_timeboxed"
  status: "frozen_after_incident"
```

### 11.3 后续路由

这起事件之后：

1. `ODD` 复核门禁链与证据完整性
2. `TAT` 复审试点资格是否维持
3. `Human` 决定：
   - 继续冻结整改
   - 缩小试点
   - 终止试点

---

## 12. 这条链真正证明了什么

### 12.1 LMM 证明了什么

问题不是靠问卷卖出去的，  
而是先被显影、过滤、归档成可诊断输入。

### 12.2 COP 证明了什么

系统知道自己现在不该装作已经足够清楚。

### 12.3 TAT 证明了什么

责任门槛不是口号，而是能把“先修后试”与“只能笼中试点”区分开的裁决器。

### 12.4 ODD 证明了什么

责任裁决可以被压成契约族、门禁链、人工节点和回滚条件。

### 12.5 Harness 证明了什么

真正的运行时不是“有日志就行”，  
而是：

- 会拦
- 会挂起
- 会回滚
- 会把事故送回上游

---

## 13. 三条红线

1. `handoff_intent = true` 不等于可以跳过 `COP / TAT`。  
2. `LIMITED_PILOT` 不等于可以偷跑生产动作。  
3. `BLOCK / FREEZE / ROLLBACK` 不等于系统失败，很多时候恰恰说明系统仍在服从治理。  

---

## 14. 配套回引

建议与本文配套阅读：

- `LMM-COP-ODD 转接表（现行版）`
- `TAT-ODD 授权编译表（现行版）`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `40-责任架构层（TAT）/TAT.责任门槛协议.v1.md`
- `40-责任架构层（TAT）/TAT.责任门槛矩阵.v1.md`

---

> **最终总句**：  
> **一条高风险 Agent 工作流如果真想进入现实，不是先问“能不能跑起来”，而是先把显影、诊断、责任、编译、门卫、回滚这六件事接成一条谁都绕不过去的链。**
