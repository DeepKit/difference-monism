# TAT-ODD 授权编译表（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：接口附录 / 固定编译表  
> 目的：把 `TAT` 的责任裁决档位，固定翻译成 `ODD` 的契约族、门禁链、人工节点、封存、解封与回滚权限。  
> 边界：本文不重写 `TAT` 的门槛裁决，不重写 `ODD` 的完整对象模型，也不替代 `Harness` 的运行时规范；本文只作为 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 中 `接口 B：TAT -> ODD` 的固定展开附录。  

---

## 1. 一句话定位

> **TAT 决定能不能进入动作面，ODD 负责把这个裁决编译成不能偷跑、不能越权、不能失忆的工程门禁链。**

最短归纳：

- `TAT` 给裁决档位
- `ODD` 给工程形态
- `Harness` 执行已编译结果

当前纪律：

> **整条治理/执行链仍按 `LMM -> COP -> TAT -> ODD -> Harness` 理解；若看其中 `COP / TAT / ODD / Harness` 这一段的分工，以 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 为准；本文只负责 `TAT -> ODD` 的授权编译细则。**
>
> **若白皮书与本文出现抽象层表述差异，以白皮书的总定义为准；本文只负责把同一裁决语义展开成固定工程编译结果。**

---

## 2. 本文只处理什么

本文只处理四件事：

1. `TAT -> ODD` 的最小字段映射
2. 五种 `TAT` 裁决档位的固定编译规则
3. 不同裁决下的人工节点、封存、解封与回滚权限
4. 哪些动作在工程层绝不能被放行

本文不处理：

1. `R=0 / R=1` 的上游判定过程
2. `COP` 的分诊与误判学习
3. `Harness` 的对象与事件细节
4. 具体业务契约的完整正文

---

## 3. 三条前置纪律

### 3.1 TAT 裁决不是 ODD 门禁结果

`DENY / FREEZE / ALLOW_WITH_CONDITIONS / LIMITED_PILOT / FREEZE_AND_REPAIR`

这些是：

- 责任门槛裁决
- 扩张资格裁决

不是：

- `PASS / FAIL / FREEZE` 这种工程验证结果

### 3.2 ODD 不得改写 TAT 的裁决含义

`ODD` 可以把裁决翻译成：

- 契约族
- 任务等级
- 门禁链
- 人工节点
- 封存/解封/回滚规则

但不能把：

- `FREEZE_AND_REPAIR` 编译成“先上线再补”
- `LIMITED_PILOT` 编译成“事实量产”
- `DENY` 编译成“内部先偷偷跑一下”

### 3.3 编译的目标不是让流程更顺，而是让越权更难

如果一份编译结果让系统更方便规避：

- 同意
- 复审
- 补偿
- 留痕
- 回滚

那么这份编译结果就是错误的，即使实现上更省事。

---

## 4. 继承输入合同

本文默认逐字继承当前接口白皮书中的 `tat_to_odd` 最小输入，不在此重新定义新版本合同：

```yaml
tat_to_odd:
  case_id: string
  ruling: DENY | FREEZE | ALLOW_WITH_CONDITIONS | LIMITED_PILOT | FREEZE_AND_REPAIR
  r_state: R0 | R1
  consent_required: bool
  required_human_roles: [string]
  review_window_days: int
  appeal_entry: string
  rollback_condition: string
  compensation_profile: string
  max_action_level: none | probe | bounded | pilot | scaled
  mandatory_audits: [string]
```

这份输入在工程层的唯一作用是：

> **限定 ODD 能编译出什么，以及绝不能编译出什么。**

---

## 5. 字段编译表

| TAT 字段 | 编译到 ODD 的落点 | 固定纪律 |
|---|---|---|
| `ruling` | `contract_family / execution_enabled / gate_chain` | 裁决档位优先级最高，其他字段不得反向放宽 |
| `r_state` | `expansion_allowed` | `R0` 不得出现生产放行合同 |
| `consent_required` | `human_only_constraints` | 同意确认必须成为不可绕过节点 |
| `required_human_roles` | `human_review / approval nodes` | 缺少人类角色映射时不得激活执行面 |
| `review_window_days` | `timebox / review_interval / pilot expiry` | 必须变成工程时间窗口，而不是备注 |
| `appeal_entry` | `appeal_trigger / appeal_evidence / escalation route` | 申诉入口必须可定位到证据链 |
| `rollback_condition` | `rollback_policy / rollback_order template` | 必须可执行，不得只写“必要时回滚” |
| `compensation_profile` | `incident handling / compensation evidence requirements` | 不能只放在法务说明，必须可追溯 |
| `max_action_level` | `scope limits / capability limits / contract family upper bound` | 决定执行面的上限，不可被下游扩大 |
| `mandatory_audits` | `gate_chain / evidence_schema / seal prerequisites` | 缺一项都不得生成最终放行封存 |

---

## 6. 五档裁决的固定编译规则

## 6.1 `DENY`

### 责任语义

- 当前没有进入动作面的资格
- 不允许试点、灰跑、内部先上

### ODD 编译结果

| 项目 | 固定结果 |
|---|---|
| `execution_enabled` | `false` |
| `allowed_contract_family` | `deny_record / appeal_record / responsibility_gap_report` |
| `default_task_level` | `none` |
| `gate_profile` | `none` |
| `required_human_nodes` | `appeal_only` |
| `seal_mode` | `case_seal_only` |
| `unseal_condition` | `new_evidence or successful appeal` |
| `rollback_authority` | `n/a` |

### 工程纪律

1. 不得生成任何执行型契约
2. 不得签发 `odd_to_harness`
3. 只能生成拒绝记录、责任缺口报告与申诉入口

## 6.2 `FREEZE`

### 责任语义

- 当前不应继续推进
- 但不是永久否决，通常意味着信息不足、争议未决或需复审

### ODD 编译结果

| 项目 | 固定结果 |
|---|---|
| `execution_enabled` | `false` |
| `allowed_contract_family` | `freeze_record / supplement_request / review_contract` |
| `default_task_level` | `L2` |
| `gate_profile` | `human_required` |
| `required_human_nodes` | `independent_review + dispute_review` |
| `seal_mode` | `freeze_seal` |
| `unseal_condition` | `review_passed and missing_fields_completed` |
| `rollback_authority` | `n/a` |

### 工程纪律

1. 不得把 `FREEZE` 编译成可执行试点
2. 只能补信息、补证据、补复审
3. 解除冻结必须留下 `override` 或复审通过证据

## 6.3 `FREEZE_AND_REPAIR`

### 责任语义

- 责任门槛尚未满足放行
- 但允许围绕修复责任结构本身开展有限工程工作

### ODD 编译结果

| 项目 | 固定结果 |
|---|---|
| `execution_enabled` | `repair_only` |
| `allowed_contract_family` | `repair_contract / audit_contract / evidence_repair_contract / rollback_preparation_contract` |
| `default_task_level` | `L3` |
| `gate_profile` | `human_required` |
| `required_human_nodes` | `TAT_review + ODD_audit + owner_signoff` |
| `seal_mode` | `repair_seal_only` |
| `unseal_condition` | `repair_items_passed and TAT_recheck_completed` |
| `rollback_authority` | `TAT/Human decide, Harness execute, ODD record` |

### 工程纪律

1. 允许修责任接口，不允许放量上线
2. 所有契约都应围绕：
   - 证据补齐
   - 熔断补齐
   - 补偿准备
   - 回滚准备
3. 只能生成修复封存，不得生成生产封存

## 6.4 `LIMITED_PILOT`

### 责任语义

- 允许进入试点
- 但必须限域、限量、限时、可回滚、可复审

### ODD 编译结果

| 项目 | 固定结果 |
|---|---|
| `execution_enabled` | `true_bounded` |
| `allowed_contract_family` | `pilot_contract / audit_contract / rollback_contract / compensation_ready_contract` |
| `default_task_level` | `L3`；公共高影响场景可升 `L4` |
| `gate_profile` | `human_required` |
| `required_human_nodes` | `launch_approval + in_window_review + exit_review` |
| `seal_mode` | `pilot_seal_timeboxed` |
| `unseal_condition` | `pilot_scope_change or review_window_hit or appeal_accepted` |
| `rollback_authority` | `TAT/Human/threshold trigger, Harness execute, ODD seal rollback evidence` |

### 工程纪律

1. 必须写明试点范围、人数、系统边界与期限
2. 必须存在可执行回滚或补偿路径
3. `scaled` 级动作在 `LIMITED_PILOT` 下默认禁止
4. 任何超范围动作都应直接触发 `FREEZE / INCIDENT`

## 6.5 `ALLOW_WITH_CONDITIONS`

### 责任语义

- 允许执行
- 但仍处在条件放行状态，而不是“从此无需复审”

### ODD 编译结果

| 项目 | 固定结果 |
|---|---|
| `execution_enabled` | `true_conditioned` |
| `allowed_contract_family` | `bounded_production_contract / audit_contract / review_contract / rollback_contract` |
| `default_task_level` | `L2-L3`，高外溢场景不低于 `L3` |
| `gate_profile` | `slow`；若含强人工条款则 `human_required` |
| `required_human_nodes` | `consent/review/appeal nodes as declared` |
| `seal_mode` | `formal_seal_with_revalidation` |
| `unseal_condition` | `contract_change or audit_failure or accepted_appeal` |
| `rollback_authority` | `as declared by TAT/Human, mandatory executable path retained` |

### 工程纪律

1. 条件放行不等于永久豁免
2. 复审窗口、申诉入口、审计要求必须转成门禁链
3. 若 `max_action_level = scaled`，仍必须保留周期性复核与回滚路径

---

## 7. `max_action_level` 的固定上限映射

| `max_action_level` | ODD 允许编译的最大执行范围 | 默认禁止 |
|---|---|---|
| `none` | 不生成执行型契约 | 任何上线、试点、自动动作 |
| `probe` | 只允许读、查、采样、诊断 | 写操作、外部后果动作 |
| `bounded` | 允许受限内部动作 | 大规模外放、不可逆动作 |
| `pilot` | 允许限域试点 | 量产扩容、无限期运行 |
| `scaled` | 允许条件化规模运行 | 绕过复审与回滚的无限放量 |

最小纪律：

1. `max_action_level` 是上限，不是承诺一定放到该级
2. 下游可以更保守，不能更激进

---

## 8. 人工节点编译规则

### 8.1 `consent_required = true`

必须编译成：

- `human_only_constraints += consent_confirmation`
- 未完成同意确认前不得放行执行

### 8.2 `required_human_roles`

必须编译成明确节点，而不是备注文字：

- `launch_approval`
- `human_review`
- `appeal_review`
- `rollback_approval`
- `compensation_ack`

### 8.3 `review_window_days`

必须至少落成一项：

- `pilot_expiry`
- `review_interval_days`
- `override_expiry`

不得只保留在文书说明里。

---

## 9. 封存、解封、回滚的编译规则

## 9.1 封存

| 裁决 | 允许的封存类型 |
|---|---|
| `DENY` | `case_seal_only` |
| `FREEZE` | `freeze_seal` |
| `FREEZE_AND_REPAIR` | `repair_seal_only` |
| `LIMITED_PILOT` | `pilot_seal_timeboxed` |
| `ALLOW_WITH_CONDITIONS` | `formal_seal_with_revalidation` |

红线：

- `DENY / FREEZE / FREEZE_AND_REPAIR` 不得生成生产终态封存

## 9.2 解封

`unseal` 只能发生在：

- 新证据进入
- 复审通过
- 契约被合法修订
- 申诉成功

不得因为“业务很急”直接跳过。

## 9.3 回滚

| 裁决 | 回滚要求 |
|---|---|
| `DENY` | 无执行面，回滚不适用 |
| `FREEZE` | 无执行面，回滚不适用 |
| `FREEZE_AND_REPAIR` | 修复型动作若改变系统状态，必须预写回滚 |
| `LIMITED_PILOT` | 回滚或补偿路径必须先于试点存在 |
| `ALLOW_WITH_CONDITIONS` | 只要有现实后果动作，就必须保留回滚/补偿路径 |

---

## 10. 一个最小编译样例

### 输入

```yaml
tat_to_odd:
  case_id: case-agent-031
  ruling: LIMITED_PILOT
  r_state: R1
  consent_required: true
  required_human_roles: [owner, auditor]
  review_window_days: 14
  appeal_entry: "tat://appeal/case-agent-031"
  rollback_condition: "任一越权调用或高风险异常触发立即回滚"
  compensation_profile: "pilot-loss-covered"
  max_action_level: pilot
  mandatory_audits: [ODD_AUDIT, HUMAN_REVIEW]
```

### 编译后 ODD 结果

```yaml
odd_compilation:
  case_id: case-agent-031
  contract_family: pilot_contract
  execution_enabled: true_bounded
  task_level: L3
  gate_profile: human_required
  human_only_constraints:
    - consent_confirmation
    - owner_launch_approval
    - auditor_exit_review
  gate_chain:
    - quality_check
    - human_review
    - acceptance
    - pilot_seal
  review_interval_days: 14
  appeal_trigger: "tat://appeal/case-agent-031"
  rollback_policy: "immediate_rollback_on_unauthorized_action"
  forbidden_actions:
    - scaled_rollout
    - bypass_human_review
```

这个例子的重点是：

> **`LIMITED_PILOT` 到工程层后，必须看起来像“被关在笼子里的试点”，而不是“换个名字的正式上线”。**

---

## 11. 三条最关键红线

1. `DENY / FREEZE` 绝不能被工程便利偷换成“内部先运行一下”。  
2. `LIMITED_PILOT` 绝不能被产品压力偷换成“先量产再补手续”。  
3. `ALLOW_WITH_CONDITIONS` 绝不能被运维惯性偷换成“永久放行、不再复审”。  

---

## 12. 配套回引

建议与本文配套阅读：

- `TAT.责任门槛协议.v1.md`
- `TAT.责任门槛矩阵.v1.md`
- `责任架构理论宣言与白皮书.md`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `50-工程方法层（ODD）/ODD-main/docs/C11.工程_对象模型与标准规范.md`
- `50-工程方法层（ODD）/ODD-main/docs/C13.工程_验证_门禁_状态机.md`

---

> **最终总句**：  
> **TAT 不负责替你写门禁，但它负责规定哪种门禁才算没有背叛责任裁决；ODD 不负责重判责任，但它负责把责任裁决编译成不能偷跑的工程现实。**
