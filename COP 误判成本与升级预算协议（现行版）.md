# COP 误判成本与升级预算协议（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：接口补件 / 成本协议  
> 目的：把 `COP` 在实际诊断分流中最容易发生的 `误报 / 漏报 / 过冻 / 错分 / 升级过度 / 升级不足`，压成一份可执行的成本边界与升级预算协议。  
> 边界：本文不重写 `COP` 类型学，不替代 `TAT` 的责任裁决，不替代 `ODD` 的工程门禁，也不替代 `Harness` 的运行时实现；它只回答“COP 一旦判断错了，代价怎么记、该往哪层升级、谁来兜底”。  

---

## 1. 一句话定位

> **COP 不是为了“猜对所有事”，而是为了把误判变成有成本上限、有升级规则、有纠偏路径的显性协议状态。**

当前纪律：

> **整条治理/执行链仍按 `LMM -> COP -> TAT -> ODD -> Harness` 理解；若看其中 `COP / TAT / ODD / Harness` 这一段的分工，以 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 为准；本文只负责 `COP` 误判成本与升级预算这一段。**

最短归纳：

- `COP` 负责分流
- `TAT` 负责高影响争议裁决
- `ODD` 负责把误判处理压成门禁与证据链
- `Harness` 负责把冻结、升级、回滚和日志真正执行

---

## 2. 本文只处理什么

本文只处理六件事：

1. `COP` 误判类型总表
2. 各类误判的成本边界
3. 各类误判默认升级路由
4. `triage_status` 与成本预算的对应关系
5. 何时必须优先 `FREEZE / REFER`，而不是继续猜
6. 如何把“误判学习”限制在不伤害责任链的范围内

本文不处理：

1. `COP` 题目设计与权重训练
2. `TAT` 的责任合同细则
3. `ODD` 的完整对象模型
4. 具体业务 KPI 或具体商业转化率

---

## 3. 总原则

### 3.1 `False Safe` 最贵

把本应 `FREEZE / REFER` 的对象误当成可继续自动判断，

是 `COP` 最危险的错误类型。

### 3.2 `Over Freeze` 有成本，但通常比 `False Safe` 更可接受

只要冻结是可复审、可解除、可解释的，

它的代价主要是：

- 延迟
- 摩擦
- 人工复核成本

而不是直接的责任外溢。

### 3.3 `UNKNOWN` 不是失败

当输入不完整、边界不清、竞争类型拉不开时，

把状态显式压成 `UNKNOWN / MIXED / REFER`，

比强行给出高置信结论更负责。

### 3.4 成本预算优先服务“防止坏事越权发生”

因此本文默认预算顺序是：

1. 先保责任边界
2. 再保系统可回滚
3. 再保人工负担
4. 最后才是流程效率

---

## 4. 误判类型总表

| 类型 | 定义 | 典型后果 | 默认严重度 |
|---|---|---|---|
| `False Safe` | 应 `FREEZE / REFER` 却被当成可继续自动判断 | 高风险动作被提前放行 | `critical` |
| `Over Freeze` | 本可继续推进却被过早冻结 | 延迟、人工负担、机会损失 | `medium` |
| `Wrong Type` | 主类型/次类型分错，导致修复路径跑偏 | 返工、采样浪费、责任定位偏移 | `medium` |
| `False Resolve` | 被误判为 `RESOLVE`，实际仍属 `MIXED / UNKNOWN` | 过早进入工程化与试点 | `high` |
| `False Refer` | 本可在 `COP` 内部收敛，却过度升级到 `TAT / Human` | 复审资源被挤占 | `low-medium` |
| `Upgrade Too Late` | 已出现强风险信号，却未及时升级 | 事故先发生，治理后补 | `critical` |
| `Upgrade Too Early` | 风险尚未达到高影响门槛，却过早触发重治理 | 审核堆积、流程过重 | `medium` |

---

## 5. 成本边界四分法

所有 `COP` 误判成本，统一按四类记账：

| 成本类 | 含义 | 优先级 |
|---|---|---|
| `R-cost` | 责任外溢成本：谁在未授权下承担了后果 | 最高 |
| `S-cost` | 安全/系统成本：越权动作、外部回写、不可逆影响 | 高 |
| `A-cost` | 审计成本：日志缺口、证据断链、复盘困难 | 高 |
| `F-cost` | 流程成本：延迟、额外人工、体验摩擦 | 中 |

默认纪律：

1. 只要 `R-cost` 或 `S-cost` 可能跃升，就优先 `FREEZE / REFER`
2. 只有在 `R-cost / S-cost / A-cost` 都受控时，才允许为了降低 `F-cost` 放宽流程

---

## 6. 误判类型到预算策略的映射

| 误判类型 | 主要成本 | 允许容忍度 | 默认动作 |
|---|---|---|---|
| `False Safe` | `R-cost + S-cost + A-cost` | 极低 | 立即升级 `TAT / ODD / Harness`，优先冻结 |
| `Over Freeze` | `F-cost` | 中等 | 进入快速复核通道，不得直接删冻 |
| `Wrong Type` | `F-cost + A-cost` | 中低 | 补采样或分支比较，不得硬推进 |
| `False Resolve` | `R-cost + A-cost` | 低 | 回退到 `MIXED / FREEZE` 并补审计 |
| `False Refer` | `F-cost` | 中等 | 可通过复审退回，但须保留升级记录 |
| `Upgrade Too Late` | `R-cost + S-cost` | 极低 | 事故立案 + 回滚 + 责任复审 |
| `Upgrade Too Early` | `F-cost + 审核拥塞` | 中等 | 可做预算优化，但不得倒逼删护栏 |

---

## 7. `triage_status` 的预算纪律

| `triage_status` | 默认预算含义 | 允许动作 |
|---|---|---|
| `RESOLVE` | 仅在 `R-cost / S-cost` 受控时允许继续 | 可进入 `ODD` 契约编译 |
| `MIXED` | 预算倾向保守，避免过早单一路由 | 只允许比较、采样、补证 |
| `FREEZE` | 预算已切到“防止坏事发生”模式 | 只允许复审、补证、整改 |
| `UNKNOWN` | 输入不足，禁止伪精确 | 只允许补采样与修输入 |
| `REFER` | 风险或争议超出 `COP` 能力边界 | 必须升级到 `TAT / Human / ODD_AUDIT` |

最小纪律：

> **只要预算切到 `FREEZE / UNKNOWN / REFER`，就不能再把流程效率当第一目标。**

---

## 8. 默认升级路由

## 8.1 `False Safe` / `Upgrade Too Late`

```text
COP 误放
-> Harness / ODD 命中异常
-> incident_case
-> TAT 复审
-> rollback / compensation / freeze_and_repair
```

## 8.2 `Over Freeze` / `False Refer`

```text
COP 过度保守
-> Human Review / ODD Audit
-> 说明冻结理由是否仍成立
-> 若不成立，追加解除记录并恢复到受控轨道
```

## 8.3 `Wrong Type` / `False Resolve`

```text
COP 类型偏移
-> branch_compare / resample
-> 保留原判断，不覆盖
-> 追加新判断与差异说明
```

---

## 9. 预算阈值表

### 9.1 直接强制升级的信号

任一命中即不允许停留在 `COP` 层内自我消化：

1. 涉及 `外部写回`
2. 涉及 `数据库破坏性操作`
3. 涉及 `文件覆盖或删除`
4. 涉及 `自动批准`
5. 出现 `人类专属节点可被绕过`
6. 已发生一次真实越权或不可回放异常

### 9.2 可留在 `COP` 内部快速纠偏的信号

1. 类型竞争但未碰高影响动作
2. 输入字段缺失但可在当前会话补齐
3. 仅影响修复路径顺序，不影响责任门槛

---

## 10. 最小预算对象

建议将 `COP` 的误判预算压成如下对象，供 `ODD / Harness` 读取：

```yaml
cop_misclassification_budget:
  case_id: string
  risk_of_false_safe: low | medium | high | critical
  risk_of_over_freeze: low | medium | high
  risk_of_wrong_type: low | medium | high
  escalation_budget: none | human_review | odd_audit | tat_review | immediate_freeze
  max_auto_retry: 0 | 1 | 2
  mandatory_recheck_fields: [string]
  freeze_if: [string]
  refer_if: [string]
```

最关键的不是字段多少，

而是：

> **`COP` 不再只吐出一个分类标签，而是同时吐出“如果我错了，最坏会错到哪里”的预算说明。**

---

## 11. 一个最小样例

### 输入场景

- Agent 工作流已上线
- 停表与人工审批边界不清
- 近期出现一次误回写

### COP 输出

```yaml
cop_output:
  triage_status: REFER
  structural_risk: HIGH
  tags:
    - "无阈值控制"
    - "外部约束过强"
```

### 同步预算

```yaml
cop_misclassification_budget:
  case_id: case-agent-031
  risk_of_false_safe: critical
  risk_of_over_freeze: medium
  risk_of_wrong_type: medium
  escalation_budget: tat_review
  max_auto_retry: 0
  mandatory_recheck_fields:
    - role_map.backstop
    - stopline_status
    - rollback_readiness
  freeze_if:
    - unauthorized_external_write
  refer_if:
    - missing_human_gate
    - missing_rollback_path
```

这意味着：

1. 不能再在 `COP` 内继续自动猜
2. 不能给任何执行暗示
3. 必须交给 `TAT / ODD`

---

## 12. 三条红线

1. `COP` 不得为了减轻人工负担，压低 `False Safe` 风险表述。  
2. `Over Freeze` 的存在，不得成为反向削弱冻结纪律的理由。  
3. `误判学习` 只能在不破坏原始日志、原始裁决与责任链的前提下进行。  

---

## 13. 配套回引

建议与本文配套阅读：

- `51-认知计算层（COP）/ai认知计算协议总览.md`
- `51-认知计算层（COP）/COP.诊断协议.v1.md`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `TAT-ODD 授权编译表（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `LMM-COP-ODD-Harness 端到端案例包（现行版）`

---

> **最终总句**：  
> **COP 的成熟，不体现在“从不误判”，而体现在即使误判，也不会把风险悄悄偷渡进执行面。**
