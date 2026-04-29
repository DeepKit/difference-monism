# Progee2 落地优化稿（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：落地稿 / 工程转译件  
> 目的：把 `LMM / COP / TAT / ODD / Harness` 现有接口件，压成 `Progee2` 可直接采用的程序对象、状态、门禁、审计事件与 UI 分层。  
> 边界：本文不是 `Progee2` 的代码设计说明全集，也不替代理论层母文；它只回答“当前最小闭环应该先怎么做、对象怎么落、页面怎么分”。  
>
> 当前纪律：本文是 `Progee2` 现行部署母稿；`API / 数据 / 第一阶段实施` 三份文件默认作为本文的后置补件阅读，不再与本文竞争主位。  

---

## 1. 一句话定位

> **Progee2 不应把所有风险都塞进一个‘质量/审阅’抽象桶，而应把责任裁决、诊断分流、工程门禁、运行时事件拆成四条可独立追溯的链。**

---

## 2. 当前工程目标

当前不追求一次性重构整个系统，

只追求先打通一条窄链：

```text
高风险外部动作
-> Harness 拦截
-> incident_case / rollback_order
-> ODD 审计封存
-> TAT 复审
```

这条链打通后，

再逐步把：

- mutation
- alert
- human decision
- 审批工作流

并回统一治理面。

---

## 3. 角色分工映射到 Progee2

| 理论层 | 在 Progee2 的身份 | 唯一职责 |
|---|---|---|
| `LMM` | `intake / signal capture` | 把问题场显影、弱测量、自测和断链归档送进诊断入口 |
| `COP` | `diagnostic triage service` | 输出 `resolve / mixed / freeze / unknown / refer` 及风险标签 |
| `TAT` | `responsibility ruling service` | 决定 `deny / freeze / allow_with_conditions / limited_pilot / freeze_and_repair` |
| `ODD` | `contract + gate compiler` | 把上游判断压成契约、门禁、证据、封存、回滚策略 |
| `Harness` | `runtime execution kernel` | 拦截高风险动作，签发授权，记录事件，执行回滚 |

最小纪律：

1. `LMM` 不直接进运行时核心
2. `COP` 不直接放行动作
3. `TAT` 不直接写门禁实现
4. `ODD` 不直接执行工具
5. `Harness` 不自行发明合法性

---

## 4. 最小对象模型

## 4.1 Intake 与诊断对象

```yaml
signal_case:
  case_id: string
  source: lmm_intake | selftest | archive
  problem_scene: string
  loss_signals: [string]
  role_map: object
  workflow_status: string
  handoff_intent: bool

cop_assessment:
  assessment_id: string
  case_id: string
  primary_type: string?
  secondary_type: string?
  classification_confidence: float
  structural_risk: LOW | MEDIUM | HIGH
  triage_status: RESOLVE | MIXED | FREEZE | UNKNOWN | REFER
  tags: [string]
  refer_to: [string]
```

## 4.2 责任与工程对象

```yaml
tat_ruling_record:
  ruling_id: string
  case_id: string
  ruling: DENY | FREEZE | ALLOW_WITH_CONDITIONS | LIMITED_PILOT | FREEZE_AND_REPAIR
  r_state: R0 | R1
  max_action_level: none | probe | bounded | pilot | scaled
  appeal_window: int
  rollback_condition: string
  mandatory_audit: [string]

odd_contract:
  contract_id: string
  case_id: string
  contract_family: string
  gate_profile: fast | slow | human_required
  human_only_constraints: [string]
  forbidden_actions: [string]
  evidence_schema: [string]
  rollback_policy: string
```

## 4.3 运行时对象

```yaml
execution_ticket:
  execution_id: string
  contract_id: string
  task_level: L1 | L2 | L3 | L4
  gate_profile: fast | slow | human_required
  hard_constraints: [string]
  freeze_rules: [string]
  rollback_policy: string

capability_grant:
  grant_id: string
  execution_id: string
  permitted_tools: [string]
  permitted_targets: [string]
  forbidden_targets: [string]
  revoke_conditions: [string]

runtime_event:
  event_id: string
  execution_id: string
  event_type: BLOCK | CHALLENGE | ESCALATE | PASS | FAIL | FREEZE | OVERRIDE | SEAL | UNSEAL | ROLLBACK | INCIDENT
  severity: info | warn | high | critical
  reason: string
  evidence_ref: [string]

incident_case:
  incident_id: string
  execution_id: string
  incident_type: unauthorized_action | policy_breach | rollback_failure | dispute
  current_owner: ODD | TAT | Human
  status: open | under_review | closed

rollback_order:
  rollback_id: string
  execution_id: string
  strategy: rollback_all | compensate | partial
  result: pending | success | partial_success | failed
```

---

## 5. 最小状态机

## 5.1 Case 状态

```text
intake
-> cop_assessed
-> tat_pending
-> tat_ruled
-> odd_compiled
-> harness_ready
-> running
-> frozen / incident / sealed / rolled_back
```

## 5.2 诊断状态

```text
resolve | mixed | freeze | unknown | refer
```

纪律：

- `mixed / freeze / unknown / refer` 不得被 UI 简化成“待处理”一个词
- 必须保留原始诊断状态

## 5.3 责任状态

```text
deny | freeze | allow_with_conditions | limited_pilot | freeze_and_repair
```

纪律：

- `TAT` 状态与 `COP triage_status` 平行存在
- 不得互相覆盖

## 5.4 运行状态

```text
prepared | running | frozen | terminated | completed
```

---

## 6. 页面分层

## 6.1 Dashboard

不再只显示“质量/审阅”，

而改成四块：

1. `责任裁决`
   - 当前 `TAT ruling`
   - 申诉窗口
   - 强制审计项
2. `诊断分流`
   - `triage_status`
   - `structural_risk`
   - `tags`
3. `工程门禁`
   - `gate_profile`
   - `human_only_constraints`
   - `forbidden_actions`
4. `运行时事件`
   - 最新 `BLOCK / FREEZE / INCIDENT / ROLLBACK`

## 6.2 Review 页面

默认拆成四个页签：

1. `COP Assessment`
2. `TAT Ruling`
3. `ODD Contract`
4. `Runtime / Incident`

这样做的目的不是页面好看，

而是防止：

- 诊断争议被误当成责任争议
- 工程失败被误当成认知不清
- 运行时事故被误当成单纯代码 bug

## 6.3 Task Detail 页面

在任务页中至少增加：

1. `max_action_level`
2. `appeal_window`
3. `mandatory_audit`
4. `rollback_condition`
5. `human_only_constraints`
6. `latest_runtime_event`

---

## 7. 最小服务切分

建议最小先切四个服务边界：

| 服务 | 先做什么 |
|---|---|
| `cop-triage` | 接收 `signal_case`，吐 `cop_assessment` |
| `tat-ruling` | 接收 `cop_assessment`，吐 `tat_ruling_record` |
| `odd-compiler` | 接收 `tat_ruling_record + cop_assessment`，吐 `odd_contract + execution_ticket` |
| `harness-runtime` | 接收 `execution_ticket`，管理 `capability_grant / runtime_event / incident_case / rollback_order` |

当前不必先物理拆微服务，

但逻辑边界必须先拆出来。

---

## 8. 第一阶段只落哪条链

### 8.1 范围

只覆盖四类动作：

1. `外部写回`
2. `数据库破坏性操作`
3. `文件覆盖或删除`
4. `自动批准`

### 8.2 为什么只选这四类

因为它们最容易同时击穿：

- 责任边界
- 回滚能力
- 审计能力

且最能体现 `Harness` 的真实价值。

### 8.3 第一阶段结果标准

只要做到以下四件事，就算第一阶段成功：

1. 高风险动作执行前一定拿到 `execution_ticket`
2. 没有 `capability_grant` 就一定被拦
3. 出事后一定生成 `incident_case + rollback_order`
4. 事件链一定能回到 `ODD / TAT`

---

## 9. 最小接口示意

```yaml
api_flow:
  POST /signal-cases
  -> POST /cop/assessments
  -> POST /tat/rulings
  -> POST /odd/contracts/compile
  -> POST /harness/executions
  -> POST /harness/events
  -> POST /incidents
  -> POST /rollback-orders
```

当前不要先追求接口优雅，

先保证：

- 字段不混
- 状态不混
- 权限不混

---

## 10. 一个最小 UI 文案示例

### Dashboard 卡片

```text
责任裁决：LIMITED_PILOT
诊断分流：REFER / HIGH
工程门禁：human_required
运行时状态：FROZEN_AFTER_INCIDENT
```

### Incident 卡片

```text
事件：unauthorized_external_write
来源：Harness BLOCK
当前 owner：TAT
回滚：success
申诉窗口：剩余 5 天
```

这种文案比“质量风险：高”更有治理意义。

---

## 11. 第二阶段再做什么

第一阶段窄链打通后，

再逐步补：

1. `COP 误判预算`
2. `TAT 申诉样例`
3. `override_expiry`
4. `seal / unseal` 的完整 UI
5. mutation / alert / human decision 的并轨

---

## 12. 三条红线

1. 不得把 `COP triage_status` 和 `TAT ruling` 混成一个字段。  
2. 不得把 `Harness runtime_event` 只当作技术日志，而不回流治理链。  
3. 不得在没有 `rollback_order` 能力前，放开高风险外部动作。  

---

## 13. 配套回引

建议与本文配套阅读：

- `一元论八层统一架构图（现行版）`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `COP 误判成本与升级预算协议（现行版）`
- `TAT-COP-ODD-Harness 复审与申诉样例包（现行版）`
- `Progee2 API 与状态流转草案（现行版）`
- `Progee2 数据对象与审计索引（现行版）`
- `Progee2 第一阶段实施清单（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `TAT-ODD 授权编译表（现行版）`
- `LMM-COP-ODD-Harness 端到端案例包（现行版）`

---

> **最终总句**：  
> **Progee2 的下一步，不是继续往“更聪明的 AI 工作台”堆功能，而是先把责任裁决、诊断分流、工程门禁和运行时事件接成一条真正能拦住坏事的窄链。**
