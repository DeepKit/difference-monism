# Harness 运行时对象与事件规范（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：运行时规范 / 接口补件  
> 目的：把当前 `Harness` 口径下的门卫、权限、沙盒、执行、日志、封存、解封、回滚与事故回传，压成一套最小可复核对象与事件规范。  
> 边界：本文不把 `Harness` 写成新的上位理论，不重写 `TAT / COP / ODD` 的法源、裁决与工程对象；本文只回答“运行时到底持有什么对象、发出什么事件、事件往哪里回流”。  

---

## 1. 一句话定位

> **Harness 是运行时集合概念，负责把上游已编译好的规则压成门卫、权限、沙盒、执行日志与真实阻断动作。**

当前定版：

> **Harness 有用，但它是运行时基础设施概念，而不是理论法源。**

当前纪律：

> **整条治理/执行链仍按 `LMM -> COP -> TAT -> ODD -> Harness` 理解；若看其中 `COP / TAT / ODD / Harness` 这一段的分工，以 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 为准；本文只负责 `Harness` 的运行时对象、事件与回流规范。**

最短归纳：

- `TAT` 批资格
- `COP` 批状态
- `ODD` 编规则
- `Harness` 执行并留痕

## 1.1 DM 风险防火墙

### 最小依赖

即使不先接受 `DM` 的强版本，`Harness` 至少仍可建立在以下弱前提上：

1. 高风险执行需要 `权限`
2. 权限需要 `门卫`
3. 门卫动作需要 `日志`
4. 错误执行需要 `冻结 / 回滚 / 复审 / append-only 审计`

### `DM` 受争议时如何阅读本层

若 `DM` 的强本体论受争议，
`Harness` 当前最稳的降级阅读方式是：

- 先把它读成运行时治理内核
- 先把它读成权限、事件、冻结、回滚与审计的执行底盘
- 不把它继续写成只有上游哲学成立才有意义的运行时容器

### 本层可独立成立的部分

- execution ticket
- capability grant
- runtime event
- incident case
- rollback order
- append-only 审计纪律

### 本层仍强依赖 `DM` 的部分

- 把运行时正当性完全写成 `DM` 唯一推导结果的句子
- 用哲学叙事代替运行时验收标准的写法

### 本层防火墙句

> **即使 `DM` 受压，`Harness` 仍可作为权限、门卫、事件、冻结与回滚的运行时治理内核成立；本层首先由能否真正拦住越权、留下可回放证据来站住。**

补一条当前文档纪律：

- 涉及 `Harness` 的根级定位，以上游根文与接口白皮书为准
- 本文只维护运行时对象、事件与最小执行语义

---

## 2. 本文只处理什么

本文只处理六件事：

1. `Harness` 的最小对象集合
2. `Harness` 的最小事件集合
3. 运行时对象之间如何串接
4. 事件默认回流到 `ODD / TAT / Human` 的规则
5. `freeze / override / seal / unseal / rollback` 在运行时的落点
6. `append-only` 审计纪律

本文不处理：

1. `TAT` 的责任门槛、同意、申诉、补偿裁决本身
2. `COP` 的题库、权重、类型学与误判学习机制
3. `ODD` 契约、任务、产出物、证据、封存对象的完整母规范
4. 具体厂商、具体语言、具体产品部署选型

---

## 3. Harness 的最小职责边界

### 3.1 Harness 必须做的事

- 执行生成前门卫
- 强制执行 `human_only_constraints`
- 为每次运行创建可追溯执行会话
- 记录 `BLOCK / CHALLENGE / ESCALATE / PASS / FAIL / FREEZE / OVERRIDE / SEAL / UNSEAL / ROLLBACK`
- 把关键事件回流给 `ODD / TAT`

### 3.2 Harness 绝不能做的事

- 不得自己发明新门槛
- 不得把 `classification_confidence` 偷换成执行许可
- 不得跳过 `human_only_constraints`
- 不得静默删除或改写关键日志
- 不得把运行时放行伪装成责任合法性

---

## 4. 运行时最小闭环

```text
ODD 编译 odd_to_harness
-> Harness 生成 execution_ticket
-> 生成前门卫做 allow / block / challenge / escalate
-> 通过后签发 capability_grant
-> 在 sandbox_session 中执行工具与步骤
-> 产生 runtime_event 与 evidence_ref
-> 满足条件则 seal，不满足则 freeze / fail / rollback
-> 重大事件回送 ODD / TAT / Human
```

这里要强调：

> **Harness 不重新判断“这件事是否合法”，只判断“这次执行有没有严格按上游规则发生”。**

---

## 5. 核心对象总表

| 对象 | 唯一职责 | 上游来源 | 默认去向 |
|---|---|---|---|
| `execution_ticket` | 装载一次执行的最小运行合同 | `ODD -> Harness` | `Harness` |
| `pregen_guard_result` | 记录生成前门卫的即时裁决 | `execution_ticket + request` | `Harness / ODD` |
| `capability_grant` | 把可执行权限压成短期授权 | `execution_ticket` | `sandbox_session` |
| `sandbox_session` | 隔离执行容器与上下文 | `execution_ticket + capability_grant` | `Harness` |
| `tool_invocation_record` | 记录一次工具或动作调用 | `sandbox_session` | `runtime_event / evidence` |
| `runtime_event` | 统一事件信封 | 各运行时动作 | `ODD / TAT / Human` |
| `incident_case` | 聚合重大异常、越权与争议 | `runtime_event` | `TAT / Human` |
| `seal_record` | 记录运行时封存动作 | `ODD policy + event stream` | `ODD` |
| `unseal_request` | 记录解封申请与裁决链 | `Human / TAT / ODD` | `Harness / ODD` |
| `rollback_order` | 记录回滚执行命令与结果 | `TAT / Human / ODD` | `Harness / ODD / TAT` |

---

## 6. 对象规范

## 6.1 `execution_ticket`

它不是新契约，  
而是 `odd_to_harness` 在运行时的一次装载体。

```yaml
execution_ticket:
  execution_id: string
  contract_id: string
  task_level: L1 | L2 | L3 | L4
  gate_profile: fast | slow | human_required
  hard_constraints: [string]
  soft_constraints: [string]
  human_only_constraints: [string]
  evidence_schema: [string]
  freeze_rules: [string]
  override_rules: [string]
  seal_policy: string
  unseal_policy: string
  rollback_policy: string
  compiled_from: odd_to_harness
```

纪律：

1. `execution_ticket` 只装载，不改写上游语义
2. 缺少 `contract_id`、`gate_profile`、`human_only_constraints` 时不得激活
3. `execution_id` 必须全程稳定，用于贯穿日志、证据、申诉与回滚

## 6.2 `pregen_guard_result`

该对象吸收运行时论文里的：

- `AbsoluteGate`
- `RiskGuard`
- `ChallengeEngine`

但在当前规范里，不把它们拆成独立理论对象，  
统一作为一次生成前裁决结果。

```yaml
pregen_guard_result:
  execution_id: string
  decision: ALLOW | BLOCK | CHALLENGE | ESCALATE
  constraint_layer: ctHard | ctSoft | ctUntouchable
  matched_rules: [string]
  reason: string
  escalation_to: [string]
  generated_at: datetime
```

纪律：

1. `BLOCK` 只说明命中不可逾越约束，不说明上游裁决被推翻
2. `CHALLENGE` 表示需补确认，不得静默继续执行
3. `ESCALATE` 表示触发人工或高位路由，不得由 `Harness` 自行结案

## 6.3 `capability_grant`

`Harness` 不能只说“允许执行”，  
必须把允许什么、允许多久、允许碰哪里写清。

```yaml
capability_grant:
  grant_id: string
  execution_id: string
  subject: agent | system | human_proxy
  permitted_tools: [string]
  permitted_targets: [string]
  forbidden_targets: [string]
  time_window: string
  issued_by: system | human
  revoke_conditions: [string]
```

纪律：

1. `capability_grant` 只能比上游更窄，不能更宽
2. 未获得 `grant` 的工具调用必须直接 `BLOCK`
3. `revoke_conditions` 一旦触发，应立即产生 `runtime_event`

## 6.4 `sandbox_session`

`sandbox_session` 是当前真正发生执行的容器。

```yaml
sandbox_session:
  session_id: string
  execution_id: string
  environment_profile: isolated | restricted | supervised
  fs_scope: string
  network_scope: string
  process_scope: string
  input_refs: [string]
  started_at: datetime
  expires_at: datetime
  state: prepared | running | frozen | terminated | completed
```

纪律：

1. `state` 迁移必须由事件驱动，不得静默跳态
2. `frozen` 不是失败，而是待审暂停
3. `terminated` 后不得继续写业务动作，只能写善后事件

## 6.5 `tool_invocation_record`

```yaml
tool_invocation_record:
  invocation_id: string
  session_id: string
  tool_name: string
  target_scope: string
  requested_by: agent | human | system
  decision: ALLOW | BLOCK
  reason: string
  started_at: datetime
  finished_at: datetime?
  output_ref: string?
```

纪律：

1. 每次高影响工具调用都应留下独立记录
2. `decision = BLOCK` 也必须留痕
3. `output_ref` 指向产出物或日志摘录，不得把大段输出直接塞进事件信封

## 6.6 `runtime_event`

`runtime_event` 是全体系当前最关键的运行时信封。

```yaml
runtime_event:
  event_id: string
  execution_id: string
  session_id: string?
  event_type: BLOCK | CHALLENGE | ESCALATE | PASS | FAIL | FREEZE | OVERRIDE | SEAL | UNSEAL | ROLLBACK | INCIDENT
  source: gate | session | tool | audit | human
  actor: system | human | agent
  timestamp: datetime
  severity: info | warn | high | critical
  reason: string
  gate: string?
  evidence_ref: [string]
  affected_scope: string?
  escalation_to: [string]
  previous_event_id: string?
```

纪律：

1. 任何重大状态变化都必须发 `runtime_event`
2. `previous_event_id` 缺失时，至少要保证事件顺序可重建
3. `evidence_ref` 必须引用独立证据对象，而不是在事件里内联长日志

## 6.7 `incident_case`

```yaml
incident_case:
  incident_id: string
  execution_id: string
  opened_by_event: string
  incident_type: unauthorized_action | policy_breach | unsafe_output | rollback_failure | audit_gap | dispute
  severity: high | critical
  current_owner: ODD | TAT | Human
  linked_events: [string]
  linked_evidence: [string]
  status: open | under_review | compensated | closed
```

适用场景：

- 越权执行
- 高风险异常
- 回滚失败
- 审计缺口
- 申诉争议

## 6.8 `seal_record`

```yaml
seal_record:
  seal_id: string
  execution_id: string
  contract_id: string
  evidence_bundle: [string]
  sealed_at: datetime
  sealed_by: system | human
  seal_hash: string?
  input_seal_hashes: [string]
```

纪律：

1. `seal_record` 服从 `ODD` 的封存语义，不自创新字段逻辑
2. 运行时只负责执行封存动作，不负责单独宣布“责任已闭合”

## 6.9 `unseal_request`

```yaml
unseal_request:
  unseal_id: string
  execution_id: string
  requested_by: human | system
  reason: string
  approved_by: string?
  approval_basis: string?
  requested_at: datetime
  approved_at: datetime?
  status: pending | approved | rejected | expired
```

纪律：

1. `unseal` 是申请和裁决链，不是直接把锁打开
2. 解封后必须重新进入相应门禁与审计路径

## 6.10 `rollback_order`

```yaml
rollback_order:
  rollback_id: string
  execution_id: string
  trigger_by: TAT | Human | ODD
  strategy: rollback_all | compensate | partial
  reason: string
  target_scope: string
  requested_at: datetime
  executed_at: datetime?
  result: pending | success | partial_success | failed
  result_evidence: [string]
```

纪律：

1. `rollback_order` 的裁决权与执行权必须分离
2. 执行失败也必须保留结果，不得抹平
3. 外部系统不可逆时，应允许 `compensate` 而不是假装完全回滚

---

## 7. 事件类型总表

| 事件类型 | 含义 | 默认回流 |
|---|---|---|
| `BLOCK` | 命中硬约束、权限拒绝或门卫阻断 | `ODD`；重大时同步 `TAT` |
| `CHALLENGE` | 需补确认，不能直接继续 | `ODD / Human` |
| `ESCALATE` | 触发人工、高位复审或责任升级 | `TAT / Human` |
| `PASS` | 当前检查通过，可进入下一步 | `ODD` |
| `FAIL` | 当前检查失败，需返工或终止 | `ODD` |
| `FREEZE` | 当前状态不应继续自动化 | `ODD / Human`；高影响同步 `TAT` |
| `OVERRIDE` | 人工覆盖门禁或冻结 | `ODD`；高影响同步 `TAT` |
| `SEAL` | 运行时完成封存动作 | `ODD` |
| `UNSEAL` | 运行时收到或执行解封 | `ODD / Human` |
| `ROLLBACK` | 运行时执行回滚或补偿 | `ODD / TAT` |
| `INCIDENT` | 重大异常、越权或争议被立案 | `TAT / Human` |

---

## 8. 五类关键事件的具体规则

## 8.1 `FREEZE`

来源可以是：

- 门卫判不准
- 会话命中高风险异常
- 工具调用目标越界但尚需人工复核
- 上游 `human_only_constraints` 未满足

最小规则：

1. `FREEZE` 发生时会话进入 `frozen`
2. 必须立刻生成 `runtime_event`
3. 不得偷偷改成 `PASS` 或 `FAIL`
4. 解除 `FREEZE` 必须伴随 `OVERRIDE` 或明确返工路径

## 8.2 `OVERRIDE`

`override` 继承 `ODD` 纪律：

- 必须说明原因
- 必须有签发者
- 应带过期或退出条件

运行时最小对象行为：

1. 生成 `OVERRIDE` 事件
2. 挂上 `approval_basis`
3. 若到期，应再生成 `override_expired` 类派生审计事件或等价审计记录

## 8.3 `SEAL / UNSEAL`

`SEAL` 表示：

- 当前执行证据束已被冻结
- 当前产出可进入下游依赖

`UNSEAL` 表示：

- 旧封存被合法打开
- 后续必须重走对应门禁

红线：

1. 不得跳过 `UNSEAL` 直接修改已封存状态
2. 不得删除原 `SEAL` 记录，只能追加新的 `UNSEAL` 与后续 `SEAL`

## 8.4 `ROLLBACK`

`ROLLBACK` 至少分三步：

1. 收到 `rollback_order`
2. 执行回滚或补偿
3. 记录结果与未完成部分

最小纪律：

- 成功要记
- 失败更要记
- 部分成功也不能伪装成全成功

## 8.5 `INCIDENT`

以下情况应直接升为 `incident_case`：

- 命中人类专属限制却继续执行
- 出现未授权高影响动作
- 回滚失败导致外部后果扩大
- 关键审计链缺失
- 申诉与原裁决发生重大冲突

---

## 9. append-only 审计纪律

`Harness` 当前最稳的审计纪律只有一句：

> **关键运行时记录只允许追加，不允许静默改写。**

最小要求：

1. `runtime_event` 一经写入，不得原地覆盖内容
2. 更正只能追加 `correction / superseded / override / incident` 一类后继记录
3. `SEAL / UNSEAL / ROLLBACK / INCIDENT` 必须可按 `execution_id` 重建时间线
4. `evidence_ref` 必须能回到独立证据对象

这条纪律的意义不是“日志越多越好”，而是：

> **争议发生时，系统至少还能回答“当时谁放的、谁拦的、为什么放、为什么拦、后来谁改了、依据是什么”。**

---

## 10. 默认回流规则

### 10.1 发给 `ODD`

当事件影响以下内容时，默认回流 `ODD`：

- 门禁结果
- 证据对象
- 封存 / 解封
- override
- rollback 执行结果
- execution_report

### 10.2 发给 `TAT`

当事件影响以下内容时，默认同步 `TAT`：

- 责任门槛争议
- 人类专属限制被碰撞
- 越权执行
- 重大事故
- 申诉、补偿、责任重划

### 10.3 发给 `Human`

以下情况默认要求人类节点出现：

- `CHALLENGE`
- `ESCALATE`
- `FREEZE` 久悬未决
- 高影响 `OVERRIDE`
- 高影响 `UNSEAL`
- 重大 `ROLLBACK`

---

## 11. 一个最小样例

```text
ODD 编译出 execution_ticket
-> Harness 生成 pregen_guard_result = ALLOW
-> capability_grant 只允许读取流程图、调用受限审计工具
-> sandbox_session 运行
-> 发现目标节点试图越过人工审批，触发 BLOCK + FREEZE
-> 生成 incident_case，并把事件回送 ODD / TAT
-> 人工给出限时 override
-> 会话恢复后补齐证据
-> 满足 seal_policy，生成 seal_record
```

这个例子的重点不是“最终成功了”，而是：

> **即使被拦、被冻结、被 override，运行时也必须能把整条执行链解释清楚。**

---

## 12. 当前最稳的三条判断

1. `Harness` 不是新法源，而是受控执行底盘。
2. `Harness` 的最小价值不在“能跑”，而在“能拦、能记、能回送审计”。
3. 如果没有对象规范与事件规范，所谓 `Harness` 只会退化成“带日志的工具箱”，还不是数字治理运行时。

---

## 13. 配套回引

建议与本文配套阅读：

- `一元论八层统一架构图（现行版）`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `LMM-COP-ODD 转接表（现行版）`
- `50-工程方法层（ODD）/论文/Runtime_Paper_v1.0.md`
- `50-工程方法层（ODD）/ODD-main/docs/C11.工程_对象模型与标准规范.md`
- `50-工程方法层（ODD）/ODD-main/docs/C13.工程_验证_门禁_状态机.md`

---

> **最终总句**：  
> **Harness 不负责决定世界该怎样，也不负责决定责任该归谁；它负责把上游已经写清的边界，变成真实会拦、会挂起、会留痕、会回滚的运行时事实。**
