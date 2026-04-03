# LMM-COP-ODD 转接表（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：接口补件 / 转接表  
> 目的：把 `LMM -> COP` 的前线信号输入，与 `COP -> ODD` 的诊断输出落点，压成一份可直接复核的现行转接表。  
> 边界：本文不重写 `DM / ASTO / ECET` 法源，不替代 `TAT-COP-ODD-Harness 接口白皮书（现行版）` 的责任裁决顺序，也不展开 `Harness` 的运行时实现。

---

## 1. 一句话定位

> **LMM 负责把现实问题场显影并整理成可诊断输入，COP 负责把输入压成有界状态，ODD 负责把允许进入执行面的状态编译成契约、门禁与证据链。**

---

## 2. 本文只处理什么

本文只处理四件事：

1. `LMM` 哪些信号允许进入 `COP`
2. `LMM` 哪些东西绝不能冒充诊断输入
3. `COP` 输出字段如何落到 `ODD`
4. 不同 `triage_status` 下，`ODD` 允许做什么、不允许做什么

本文不处理：

1. `TAT` 的同意、申诉、补偿与责任闭合裁决
2. `COP` 题库、权重与分类学的全部细节
3. `ODD` 对象模型的完整字段全集
4. `Harness` 的沙盒、权限与遥测实现

---

## 3. 总原则

### 3.1 LMM 到 COP 传的是“结构信号”，不是“成交信号”

能进入 `COP` 的，必须是：

- 问题场摘要
- 自测结果
- 断链归档字段
- 已发生异常与角色链信息

不能进入 `COP` 充当风险依据的，包括：

- 报价意愿
- 预算大小
- 采购时点
- 礼貌性兴趣
- 内容热度与传播反馈

### 3.2 COP 到 ODD 传的是“诊断状态”，不是“执行许可”

`COP` 可以输出：

- 当前状态够不够清楚
- 风险有多高
- 是否应冻结、转介或补采样

`COP` 不可以直接输出：

- 高风险强制动作授权
- 责任已闭合的宣告
- 可以绕过 `TAT` 的上线许可

### 3.3 ODD 接住的是“可工程化约束”，不是全部现实

`ODD` 只接：

- 可写成契约的边界
- 可写成门禁的禁止项
- 可写成证据链的复核要求

`ODD` 不接：

- 纯传播话术
- 未归档的主观直觉
- 没有字段化的港口感受

---

## 4. LMM -> COP：允许进入诊断层的前线信号

### 4.1 允许进入 COP 的四类来源

| LMM 来源 | 当前合法身份 | 进入 COP 的条件 |
|---|---|---|
| `灯塔显影摘要` | 问题场初筛摘要 | 必须已明确问题场、损耗感与对象边界 |
| `一页自测` | 弱测量过滤层 | 必须保留三表结果与关键题命中情况 |
| `断链归档入口` | 结构初判输入 | 必须填写最小字段，不得只留一句模糊抱怨 |
| `港口前确认信号` | 路由许可信号 | 只用于决定是否进入下一层，不得当作风险证据 |

### 4.2 LMM -> COP 最小字段表

| 上游来源 | 规范字段 | 含义 | COP 用途 | 缺失时处理 |
|---|---|---|---|---|
| `灯塔` | `problem_scene` | 当前问题场一句话 | 建立诊断语境 | 缺失则不得正式诊断 |
| `灯塔` | `loss_signals` | 持续损耗、返工、越权、失控等症状 | 辅助判定 `structural_risk` | 只保留“有兴趣”则退回 LMM |
| `灯塔` | `field_path_person_hint` | 场、路、人三点的初步锚定 | 约束诊断对象边界 | 不得由 COP 自行脑补 |
| `自测表一` | `responsibility_chain_status` | 责任断链状态：`green / yellow / red` | 判断责任链是否可解释 | 缺失则至少降为 `UNKNOWN` |
| `自测表二` | `governability_status` | 权限边界与可治理性状态 | 判断是否存在 `ODD_AUDIT` 前提 | 缺失则不得进入执行建议 |
| `自测表三` | `stopline_status` | 停表、回滚、事故处置准备度 | 判断是否命中高风险标签 | 缺失则高风险默认上调 |
| `归档入口` | `workflow_status` | `已上线 / 准上线 / 复盘中` | 决定诊断时态 | 缺失则视为输入不完整 |
| `归档入口` | `key_nodes` | `3-7` 个关键节点 | 形成结构拓扑的最小骨架 | 缺失则不能输出结构型建议 |
| `归档入口` | `latest_incident` | 最近一次异常/返工/越权事件 | 判定风险现实性 | 缺失则只能给弱建议 |
| `归档入口` | `role_map` | `谁触发 / 谁批准 / 谁兜底 / 谁修正` | 判断责任接口是否存在 | 缺失时默认升高责任不确定性 |
| `归档入口` | `suspected_breakpoint` | 当前最怀疑的断链点 | 生成标签与采样重点 | 缺失则不得伪装成已定位 |
| `归档入口` | `desired_judgment_type` | 希望得到的判断类型 | 约束输出范围 | 缺失则按最保守默认处理 |
| `港口前信号` | `handoff_intent` | 是否已出现真实物理接近动作 | 只决定路由，不进风险计算 | 缺失可不影响诊断 |

### 4.3 绝不能进入 COP 风险计算的字段

以下字段即使存在，也不得参与 `classification_confidence`、`structural_risk` 或 `triage_status`：

- `budget_range`
- `purchase_timeline`
- `decision_maker_name_chain`
- `phone / wechat`
- `content_heat`
- `礼貌兴趣`
- `报价询问本身`

这些东西最多只属于：

- 港口排程
- 人工承接
- 后续商务动作

不属于：

- 结构诊断证据
- 风险等级证据
- 自动执行许可

### 4.4 LMM -> COP 最小转接包

```json
{
  "problem_scene": "Agent 工作流已上线，但责任链、权限边界与停表条件不清",
  "loss_signals": [
    "最近两周重复返工 3 次",
    "出现一次越权调用",
    "异常后无法在 30 分钟内定位责任节点"
  ],
  "selftest": {
    "responsibility_chain_status": "red",
    "governability_status": "yellow",
    "stopline_status": "red"
  },
  "workflow_status": "已上线",
  "key_nodes": ["输入采集", "规则判断", "Agent 执行", "人工审批", "外部系统回写"],
  "latest_incident": "2026-03-28 出现误触发，人工叫停后无法完整回放",
  "role_map": {
    "trigger": "运营",
    "approve": "产品负责人",
    "backstop": "不明确",
    "fix": "工程师"
  },
  "suspected_breakpoint": "审批后执行链缺少停表与回滚接口",
  "desired_judgment_type": "先做责任断链与停表风险初判",
  "handoff_intent": true
}
```

最小纪律：

1. `handoff_intent = true` 不代表可以跳过 `COP`
2. 三张自测只给 `green / yellow / red`，不直接冒充 `COP` 类型学
3. `role_map.backstop` 若不明确，默认提高责任不确定性，不得替系统补位

---

## 5. COP -> ODD：诊断输出如何落到工程协议

### 5.1 必须原样保真的 COP 字段

| COP 字段 | ODD 落点 | 纪律 |
|---|---|---|
| `primary_type` | `contract.context.cop_primary_type` | 只作诊断快照，不作放行凭证 |
| `secondary_type` | `contract.context.cop_secondary_type` | 仅在存在竞争候选时保留 |
| `classification_confidence` | `gate.freeze_conditions` | 只判断“像不像”，不得代替风险 |
| `structural_risk` | `contract.risk_level` / `gate_strength` | 决定门禁强度与证据等级 |
| `triage_status` | `pre_gate_state` | 决定能否进入契约编译 |
| `tags` | `red_lines` / `focus_checks` | 转成红线、停表点、审计点 |
| `refer_to` | `human_review_nodes` | 直接决定是否必须回引 `TAT / HUMAN / ODD_AUDIT` |
| `actions` | `repair_objectives` | 只转成允许动作候选，不得跳过契约化 |
| `anti_actions` | `forbidden_actions` | 直接进入禁止动作清单 |

### 5.2 COP 状态到 ODD 的默认路由

| `triage_status` | 风险条件 | ODD 允许生成什么 | 默认门禁动作 |
|---|---|---|---|
| `RESOLVE` | `LOW` | `repair_contract / pilot_contract / production_contract` | 进入正常 `PASS / FREEZE / FAIL` 门禁链 |
| `RESOLVE` | `MEDIUM` | `repair_contract / audit_contract` | 先补证据，再决定是否放行 |
| `MIXED` | 任意 | `branch_compare_contract / sampling_contract` | 默认 `FREEZE`，不得直接生产放行 |
| `FREEZE` | 任意 | `freeze_record / human_review_record` | 停在待审，不生成执行型契约 |
| `UNKNOWN` | 任意 | `resample_contract / intake_repair_contract` | 只能补采样，不能推进执行 |
| `REFER` + `TAT_REVIEW` | 任意 | `audit_placeholder_contract` | 先回引 `TAT`，不得越层执行 |
| `REFER` + `ODD_AUDIT` | `MEDIUM / HIGH` | `audit_contract / repair_contract` | 先审计可追溯性、停表与回滚接口 |

最短判断：

1. `FREEZE / UNKNOWN / REFER` 不是“坏结果”，而是“不允许装作已经能执行”
2. `MIXED` 可以生成比较型或采样型契约，但不能伪装成单一确定方案
3. `HIGH structural_risk` 下，`ODD` 的首要任务通常不是放行，而是补门禁、补证据、补回滚

### 5.3 COP 标签到 ODD 关注项的最小映射

| COP 标签 | ODD 应新增的约束 |
|---|---|
| `结构循环依赖` | 增加跨节点断环验证与人工确认点 |
| `信息失真` | 增加输入输出可追溯与对账验收条目 |
| `时间轴污染` | 增加版本、时序、重放一致性检查 |
| `系统被套利` | 增加对抗验证与异常滥用样本 |
| `样本偏差` | 增加覆盖边界、抽样说明与外推限制 |
| `无阈值控制` | 强制写入停表、熔断、人工接管条件 |
| `外部约束过强` | 强制写入回滚、补偿、外部依赖失败策略 |

### 5.4 ODD 侧最小合同骨架

```yaml
contract:
  id: agent-workflow-breakpoint-repair
  title: "Agent 工作流责任断链修复"
  context:
    cop_primary_type: "B"
    cop_secondary_type: "A"
    structural_risk: "HIGH"
    triage_status: "REFER"
    tags:
      - "结构循环依赖"
      - "无阈值控制"
  human_review_nodes:
    - "HUMAN_REVIEW"
    - "TAT_REVIEW"
    - "ODD_AUDIT"
  forbidden_actions:
    - "在未补停表条件前继续自动推进"
    - "把分类集中度当成低风险证明"
  acceptance_criteria:
    - criterion: "任意一次完整执行都能回放关键输入、关键输出与审批节点"
      hardness: hard
      executability: EN
    - criterion: "异常发生时可在 5 分钟内人工暂停，并保留执行证据"
      hardness: hard
      executability: EN
  evidence_policy:
    required:
      - output_verification
      - execution_report
      - human_review_record
      - override
  rollback_policy:
    enabled: true
```

这段骨架只说明一件事：

> **ODD 接住 COP 后，不是“把诊断结论贴到看板上”，而是把诊断结论压成可验证、可冻结、可回滚、可封存的工程对象。**

---

## 6. 三条跨层红线

### 红线 1：LMM 的港口热度不能冒充 COP 的结构风险

“对方很想聊”“对方在催报价”只能说明：

- 接近动作出现了
- 人工承接时机可能到了

不能说明：

- 结构已经清楚
- 风险已经可控
- 可以跳过诊断或责任审查

### 红线 2：COP 的分类集中度不能冒充 ODD 的放行证明

`classification_confidence` 高，只说明：

- 当前像某一类

不说明：

- 这条工作流已经安全
- 契约已经充分
- 可以不上停表、回滚与证据链

### 红线 3：ODD 的 PASS 不能反向证明上游已经合法

`ODD PASS` 只说明：

- 产出物通过了当前契约

不说明：

- `TAT` 的同意与责任门槛已经解决
- `LMM` 的前线承接就是正当的
- `COP` 先前遗漏的现实变量已经消失

---

## 7. 最短执行顺序

```text
LMM 显影问题场
-> 自测与归档把问题写成字段
-> COP 判断现在能不能继续自动判断
-> TAT 在高影响处决定能不能进入动作面
-> ODD 把允许进入的部分压成契约、门禁、证据与回滚
```

---

## 8. 配套回引

建议与本文配套阅读：

- `一元论八层统一架构图（现行版）`
- `TAT-COP-ODD-Harness 接口白皮书（现行版）`
- `52-认知方法层（LMM）/01.LMM理论/LMM.理论.003-理论基础与系统架构.md`
- `52-认知方法层（LMM）/04.产品打造/Agentic-AI子场/LMM.产品-AI.007-一页自测与断链归档入口.md`
- `52-认知方法层（LMM）/05.理论变现/LMM.变现.007-主战线港口承接与报价SOP.md`
- `51-认知计算层（COP）/README-COP总架构说明.md`
- `51-认知计算层（COP）/COP.诊断协议.v1.md`
- `51-认知计算层（COP）/Phase1_MVP立即部署/COP.P1-V3-工程化接口设计.md`
- `50-工程方法层（ODD）/ODD-main/docs/C09.工程_契约_产出物_证据.md`
- `50-工程方法层（ODD）/ODD-main/docs/C13.工程_验证_门禁_状态机.md`

---

> **最终总句**：  
> **LMM 把现实写成可诊断输入，COP 把输入压成有界状态，ODD 把允许执行的状态压成可验证契约；这三层一旦混线，不是误诊，就是越权，要么就是把责任重新打回黑箱。**
