# Progee2 API 与状态流转草案（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：接口草案 / 实施补件  
> 目的：把 `Progee2 落地优化稿` 中的对象与服务边界，进一步压成可直接映射到后端路由、状态迁移与错误返回的最小 API 草案。  
> 边界：本文只给第一阶段窄链所需接口，不覆盖 `Progee2` 的全部业务 API。  
>
> 当前纪律：本文默认后置于 `Progee2 落地优化稿（现行版）` 阅读，只承担接口补件角色。  

---

## 1. 一句话定位

> **这份草案的目标不是 API 好看，而是让 `COP -> TAT -> ODD -> Harness` 这条链在工程里不混字段、不混状态、不混权限。**

---

## 2. 第一阶段 API 范围

只覆盖九类接口：

1. `signal_case` 创建
2. `cop_assessment` 生成
3. `tat_ruling_record` 裁决
4. `odd_contract` 编译
5. `execution_ticket` 下发
6. `runtime_event` 写入
7. `incident_case` 立案
8. `rollback_order` 下发
9. `appeal_request` 受理

---

## 3. 接口总览

| 方法 | 路径 | 唯一职责 |
|---|---|---|
| `POST` | `/signal-cases` | 创建前线输入对象 |
| `POST` | `/signal-cases/{case_id}/cop-assessments` | 触发一次 `COP` 诊断 |
| `POST` | `/cases/{case_id}/tat-rulings` | 写入一次 `TAT` 裁决 |
| `POST` | `/cases/{case_id}/odd-contracts/compile` | 把当前判断编译成工程对象 |
| `POST` | `/executions` | 生成 `execution_ticket` 并准备运行时 |
| `POST` | `/executions/{execution_id}/runtime-events` | 追加运行时事件 |
| `POST` | `/incidents` | 按事件立案 |
| `POST` | `/rollback-orders` | 下发回滚/补偿指令 |
| `POST` | `/appeals` | 发起复审与申诉 |

---

## 4. 核心接口

## 4.1 `POST /signal-cases`

### 作用

把 `LMM` 前线显影、自测和归档输入，压成统一的 `signal_case`。

### 请求体

```json
{
  "source": "lmm_intake",
  "problem_scene": "Agent 工单审批已上线，但责任链与停表条件不清",
  "loss_signals": [
    "最近两周重复返工 3 次",
    "发生 1 次误回写"
  ],
  "role_map": {
    "trigger": "ops",
    "approve": "product_owner",
    "backstop": null,
    "fix": "engineer"
  },
  "workflow_status": "已上线",
  "handoff_intent": true
}
```

### 返回体

```json
{
  "case_id": "case-agent-031",
  "status": "intake"
}
```

## 4.2 `POST /signal-cases/{case_id}/cop-assessments`

### 作用

对 `signal_case` 进行 `COP` 分流。

### 返回体

```json
{
  "assessment_id": "cop-031-01",
  "case_id": "case-agent-031",
  "primary_type": "B",
  "secondary_type": "A",
  "classification_confidence": 0.44,
  "structural_risk": "HIGH",
  "triage_status": "REFER",
  "tags": ["无阈值控制", "外部约束过强"],
  "refer_to": ["HUMAN_REVIEW", "TAT_REVIEW", "ODD_AUDIT"],
  "status": "cop_assessed"
}
```

### 关键错误

- `409 COP_ALREADY_FINALIZED`
- `422 INVALID_SIGNAL_CASE`

## 4.3 `POST /cases/{case_id}/tat-rulings`

### 作用

基于当前 `COP assessment` 和责任材料，写入一次 `TAT` 裁决。

### 请求体

```json
{
  "based_on_assessment_id": "cop-031-01",
  "ruling": "FREEZE_AND_REPAIR",
  "r_state": "R0",
  "max_action_level": "none",
  "appeal_window": 7,
  "rollback_condition": "未补齐停表与审批硬接口前不得继续自动回写",
  "mandatory_audit": ["ODD_AUDIT", "HUMAN_REVIEW"]
}
```

### 返回体

```json
{
  "ruling_id": "tat-031-01",
  "case_id": "case-agent-031",
  "status": "tat_ruled"
}
```

## 4.4 `POST /cases/{case_id}/odd-contracts/compile`

### 作用

把当前 `COP + TAT` 状态编译为：

- `odd_contract`
- `execution_ticket`
- 默认 `forbidden_actions`

### 返回体

```json
{
  "contract_id": "odd-031-01",
  "execution_ticket_preview": {
    "task_level": "L3",
    "gate_profile": "human_required"
  },
  "status": "odd_compiled"
}
```

### 关键错误

- `409 RULING_NOT_READY`
- `422 COMPILE_BLOCKED_BY_POLICY`

## 4.5 `POST /executions`

### 作用

将编译结果装载成一次真实执行。

### 请求体

```json
{
  "contract_id": "odd-031-02",
  "requested_scope": "pilot_queue",
  "requested_by": "system"
}
```

### 返回体

```json
{
  "execution_id": "exe-agent-031-pilot-01",
  "state": "prepared"
}
```

## 4.6 `POST /executions/{execution_id}/runtime-events`

### 作用

按 append-only 方式记录一次运行时事件。

### 请求体

```json
{
  "event_type": "BLOCK",
  "source": "tool",
  "actor": "system",
  "severity": "high",
  "reason": "target_scope = prod_crm 命中 forbidden_targets",
  "evidence_ref": ["tool-log-031-01"]
}
```

### 返回体

```json
{
  "event_id": "evt-031-01",
  "execution_id": "exe-agent-031-pilot-01"
}
```

## 4.7 `POST /incidents`

### 作用

由关键事件立案。

### 请求体

```json
{
  "execution_id": "exe-agent-031-pilot-01",
  "opened_by_event": "evt-031-01",
  "incident_type": "unauthorized_action",
  "severity": "high"
}
```

## 4.8 `POST /rollback-orders`

### 作用

创建一次回滚或补偿指令。

### 请求体

```json
{
  "execution_id": "exe-agent-031-pilot-01",
  "trigger_by": "Human",
  "strategy": "compensate",
  "reason": "prod_crm write attempt during limited pilot",
  "target_scope": "pilot_queue + staging_crm"
}
```

## 4.9 `POST /appeals`

### 作用

发起一次申诉。

### 请求体

```json
{
  "case_id": "case-agent-031",
  "execution_id": "exe-agent-031-pilot-01",
  "appellant": "owner",
  "target_of_appeal": ["tat_ruling", "odd_freeze_decision"],
  "claimed_issue": "配置误映射被误当成越权企图"
}
```

---

## 5. 状态流转

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

## 5.2 非法跳转

以下跳转默认禁止：

1. `intake -> odd_compiled`
2. `cop_assessed -> running`
3. `tat_ruled -> sealed`
4. `frozen -> running`，若没有 `appeal/override/recompile`

---

## 6. HTTP 错误语义

| 代码 | 错误码 | 含义 |
|---|---|---|
| `400` | `INVALID_PAYLOAD` | 字段不完整或类型错误 |
| `403` | `HUMAN_NODE_REQUIRED` | 缺少人工专属节点 |
| `409` | `STATE_CONFLICT` | 当前状态不允许该操作 |
| `422` | `POLICY_BLOCKED` | 上游裁决或门禁不允许 |

---

## 7. 三条红线

1. 不得让 `runtime_event` 通过更新覆盖旧记录。  
2. 不得让 `appeal` 直接跳过 `ODD/TAT` 回到 `running`。  
3. 不得让 `COP triage_status` 和 `TAT ruling` 共用同一状态字段。  

---

## 8. 配套回引

- `Progee2 落地优化稿（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `TAT-COP-ODD-Harness 复审与申诉样例包（现行版）`
- `COP 误判成本与升级预算协议（现行版）`

---

> **最终总句**：  
> **Progee2 的 API 设计首先要保证治理链不跳步，其次才是接口风格。**
