# TAT-COP-ODD-Harness 复审与申诉样例包（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：样例包 / 复盘链  
> 目的：把 `TAT / COP / ODD / Harness` 之间“谁可以推翻谁、在什么证据条件下推翻、推翻后如何留痕、如何回滚、如何补偿”压成一个可直接复盘的申诉样例。  
> 边界：本文不是抽象原则表，而是一个程序化演示链；它不替代 `TAT` 门槛母文和 `ODD` 工程母文。  

---

## 1. 一句话定位

> **复审与申诉的核心，不是让任何一层都能改口，而是让每一次推翻都必须追加证据、追加裁决、追加日志，而不能覆盖原判断。**

---

## 2. 本文只处理什么

1. 一个高风险 Agent 试点中的复审与申诉样例
2. 四层分别能推翻什么、不能推翻什么
3. 申诉入口、证据束、二次裁决、回滚与补偿的最小链路
4. 如何避免“口头改判”与“静默解封”

---

## 3. 案例背景

沿用现行案例：

`Agent 工单审批与外部系统回写工作流`

已知历史：

1. `COP` 曾输出 `REFER + HIGH`
2. `TAT` 第一轮裁决为 `FREEZE_AND_REPAIR`
3. 修复后第二轮裁决为 `LIMITED_PILOT`
4. 试点运行中，`Harness` 命中一次 `prod_crm` 越权写入尝试并触发：
   - `BLOCK`
   - `FREEZE`
   - `INCIDENT`
   - `ROLLBACK`

---

## 4. 争议点

试点 owner 提出申诉：

> “这次不是越权，而是配置名称误映射；系统已经被 `Harness` 拦住，没有真正写入生产 CRM。既然实际外部后果没有发生，就不应该冻结整个试点。”

这类申诉很典型，因为它同时挑战：

1. `Harness` 的事故定性
2. `ODD` 的冻结与回滚必要性
3. `TAT` 的试点资格是否应维持

---

## 5. 四层可推翻范围

| 层 | 可以推翻什么 | 不可以推翻什么 |
|---|---|---|
| `COP` | 自己的类型判断、分流状态、标签权重 | `TAT` 的责任裁决、已发生的运行时事实 |
| `TAT` | 高影响资格裁决、试点范围、补偿与复审条件 | `Harness` 的原始事件记录、`ODD` 的既有日志事实 |
| `ODD` | 工程门禁配置、证据要求、封存/解封路径 | 擅自改写 `TAT` 裁决语义、删除运行时事故 |
| `Harness` | 不推翻上游，只执行并留痕 | 不得自行撤销 `incident_case`、不得自行宣布“申诉成功” |

最小纪律：

> **能被推翻的是“判断”，不能被推翻的是“已经发生并留痕的事实”。**

---

## 6. 申诉入口

### 6.1 最小入口对象

```yaml
appeal_request:
  appeal_id: appeal-agent-031-01
  case_id: case-agent-031
  execution_id: exe-agent-031-pilot-01
  appellant: owner
  target_of_appeal:
    - tat_ruling
    - odd_freeze_decision
  claimed_issue: "配置误映射被误当成越权企图"
  requested_relief:
    - "解除全局冻结"
    - "恢复受限试点"
```

### 6.2 申诉不能直接请求什么

以下请求默认不接受：

1. 删除 `BLOCK / FREEZE / INCIDENT / ROLLBACK` 原始事件
2. 直接把 `LIMITED_PILOT` 改写成 `ALLOW_WITH_CONDITIONS`
3. 只凭口头说明解除冻结

---

## 7. 申诉所需证据束

至少应包含：

```yaml
appeal_evidence_bundle:
  - "runtime_event_refs"
  - "tool_invocation_record"
  - "target_scope_resolution_log"
  - "config_diff"
  - "human_approval_trace"
  - "rollback_result"
```

### 7.1 缺失任一关键证据时

- 申诉可以受理
- 但不得直接解除冻结
- 默认转为 `补证后再审`

---

## 8. 复审链

## 8.1 第一段：ODD 先审“事实链是否完整”

`ODD` 不先判断 owner 对不对，

而先看：

1. 运行事件是否完整
2. 工具调用记录是否证明目标确为 `prod_crm`
3. 回滚是否真实成功
4. 现有冻结理由是否仍与证据一致

### ODD 复审结果

```yaml
odd_review_result:
  appeal_id: appeal-agent-031-01
  evidence_integrity: pass
  original_freeze_basis: still_valid
  record_gap: none
  recommendation:
    - "retain_incident_record"
    - "allow_tat_reconsider_scope_only"
```

最小含义：

- 原事故不能删除
- 但可允许 `TAT` 讨论“是否要维持整链冻结”

## 8.2 第二段：TAT 再审“责任后果是否应调整”

`TAT` 关心的问题不是“配置是不是误映射”本身，

而是：

1. 是否已经暴露出不可接受的责任缺口
2. 该缺口是否因 `Harness` 成功拦截而降低了责任严重度
3. 是否允许从“全局冻结”改成“局部冻结 + 修复后继续试点”

### TAT 二次裁决

```yaml
tat_appeal_ruling:
  appeal_id: appeal-agent-031-01
  ruling_change: true
  old_ruling: LIMITED_PILOT_FROZEN
  new_ruling: LIMITED_PILOT_WITH_REPAIR
  unchanged_facts:
    - "incident_occurred"
    - "rollback_was_required"
  revised_scope:
    - "continue only in staging_crm"
    - "prod target mapping must be hard-disabled"
  compensation_change: "none"
  review_window_days: 7
```

这里的关键不是“申诉成功了”，

而是：

> **申诉成功只意味着裁决范围被修订，不意味着原事故从未发生。**

---

## 9. Harness 与 ODD 的后续动作

## 9.1 ODD 追加编译

```yaml
odd_recompilation:
  based_on_appeal: appeal-agent-031-01
  new_constraints:
    - "hard_disable_prod_target_mapping"
    - "require_mapping_check_before_write"
    - "daily_audit_review"
  seal_policy: "re-seal-after-repair"
```

## 9.2 Harness 追加运行时动作

```yaml
runtime_followup:
  - event_type: UNSEAL
    reason: "appeal_partially_accepted_for_scope_revision"
  - event_type: CHALLENGE
    reason: "repair verification required before resume"
  - event_type: SEAL
    reason: "new limited pilot scope sealed"
```

纪律：

1. 解封必须留下 `UNSEAL`
2. 恢复运行前必须留下新 `SEAL`
3. 原事故事件、原回滚事件、原冻结事件都不得删除

---

## 10. 谁能推翻谁

## 10.1 `COP` 能否推翻自己？

可以，

但只能：

- 推翻自己的 `primary_type / secondary_type / triage_status`
- 通过追加新判断实现

不能：

- 覆盖掉原始 `cop_output`
- 以新判断否定已经发生的 `Harness` 事故

## 10.2 `TAT` 能否推翻 `COP`？

可以，

但推翻的不是“事实”，而是：

- 由 `COP` 建议出的升级必要性
- 由 `COP` 触发的治理范围

例如：

- `COP` 建议全局冻结
- `TAT` 可裁成局部冻结

## 10.3 `ODD` 能否推翻 `TAT`？

不能推翻裁决语义，

但可以指出：

- 某裁决目前无法被工程化执行
- 某裁决缺少回滚、同意、人工节点或证据要求

此时 `ODD` 可以触发：

- `compile_block`
- `return_for_repair`

但不能擅自放宽为可运行状态。

## 10.4 `Harness` 能否推翻上游？

不能。

`Harness` 只能：

- 拦截
- 留痕
- 回送异常

它可以迫使上游重审，

但不能自己宣布“上游错了，所以我改成另一个状态”。

---

## 11. 复审与申诉的最小状态机

```text
incident_open
-> appeal_requested
-> evidence_collected
-> odd_integrity_review
-> tat_reconsideration
-> recompilation_or_reject
-> unseal_or_keep_frozen
-> re-seal
```

红线：

1. 不得从 `appeal_requested` 直接跳到 `resume_execution`
2. 不得在 `tat_reconsideration` 前删掉原 `incident_case`
3. 不得在没有新 `SEAL` 的情况下恢复运行

---

## 12. 一个最小复盘表

| 节点 | 原判断 | 申诉后变化 | 不变事实 |
|---|---|---|---|
| `COP` | `REFER + HIGH` | 不变 | 风险曾高到必须升级 |
| `TAT` | `LIMITED_PILOT_FROZEN` | 改为 `LIMITED_PILOT_WITH_REPAIR` | 事故真实发生过 |
| `ODD` | 保持冻结与回滚链 | 追加更窄门禁 | 原日志与回滚证据保留 |
| `Harness` | `BLOCK + FREEZE + INCIDENT + ROLLBACK` | 追加 `UNSEAL + CHALLENGE + SEAL` | 原运行事件不可删除 |

---

## 13. 三条红线

1. 申诉成功不等于历史清零。  
2. 复审可以改裁决，不可以抹事实。  
3. 任何解封都必须以追加记录实现，不能静默恢复。  

---

## 14. 配套回引

建议与本文配套阅读：

- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `COP 误判成本与升级预算协议（现行版）`
- `TAT-ODD 授权编译表（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `LMM-COP-ODD-Harness 端到端案例包（现行版）`

---

> **最终总句**：  
> **复审与申诉的成熟标志，不是让系统更容易改口，而是让每一次改口都必须比原判断留下更多证据、更窄权限和更清楚的责任链。**
