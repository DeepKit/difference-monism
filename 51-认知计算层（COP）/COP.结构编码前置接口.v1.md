# COP.结构编码前置接口 v1

> **定位**：本文把 `COP` 在给出 `RESOLVE / MIXED / FREEZE / UNKNOWN / REFER` 之前，必须保留的 `ASTO` 结构编码压成最小前置接口。  
> **用途**：防止 `COP` 的分流状态变成黑箱结果，而没有可复核的结构病历。

---

## 一、接口原则

`COP` 的价值不在于总能给答案，
而在于能承认未知、及时冻结并控制误判成本。

但若 `COP` 只输出分流状态，
而不说明当前对象处于什么结构成熟度、什么演化节律、什么责任流向模式，
就会削弱其可复核性。

因此 `COP` 正式分流前，
应先写出一层 `ASTO` 结构编码。

---

## 二、正式分流前的最小字段

| 字段 | 说明 |
|:---|:---|
| `state_form` | 当前结构成熟度 |
| `dynamic_stage` | 当前节律位置 |
| `action_step` | 当前动作位点 |
| `primary_break_order` | 当前主断裂行动位点 |
| `secondary_break_order` | 当前次断裂行动位点 |
| `boundary_status` | 当前边界清晰度 |
| `exception_flag` | 当前是否触发例外或红线 |
| `responsibility_flow_pattern` | 当前责任异常模式 |

这些字段不是为了替代 `COP` 的诊断结果，
而是为了说明：

> **`COP` 是在什么结构前提下给出本次冻结、混合、未知或转介判断的。**

---

## 三、从结构编码到分流的最小规则

### 1. `FREEZE`

若同时出现以下特征，优先考虑 `FREEZE`：

- `dynamic_stage = 脉冲 / 崩解`
- `boundary_status = 模糊 / 可争议`
- `exception_flag = 高阶例外 / 禁行红线`

### 2. `UNKNOWN`

若输入不足且：

- `state_form` 无法稳定判断
- `responsibility_flow_pattern` 无法辨识

则应允许 `UNKNOWN`，不得伪装成已有明确结论。

### 3. `REFER`

若结构编码已显示：

- 高责任争议
- 高影响后果
- 高工程执行风险

则即使分类集中，也应优先 `REFER` 至 `TAT / ODD / HUMAN_REVIEW`。

### 4. `MIXED`

若当前存在多个竞争性结构模式，
例如同时出现 `沉积 + 割裂`、`蔓生 + 下滑`，
则允许 `MIXED`，不必强压单一主型。

---

## 四、推荐输出格式

```text
ASTO 前置编码：
- state_form:
- dynamic_stage:
- action_step:
- primary_break_order:
- secondary_break_order:
- boundary_status:
- exception_flag:
- responsibility_flow_pattern:

COP 输出：
- triage_status:
- evidence_gap:
- classification_confidence:
- structural_risk:
- refer_to:
```

---

## 五、最短句

> **`COP` 的分流结果之前，应该先有一张结构编码卡；先说明系统怎么坏，再决定该不该继续自动判断。**
