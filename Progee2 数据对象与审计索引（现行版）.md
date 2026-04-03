# Progee2 数据对象与审计索引（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：数据草案 / 审计补件  
> 目的：把 `signal_case / cop_assessment / tat_ruling_record / odd_contract / execution_ticket / runtime_event / incident_case / rollback_order / appeal_request` 压成可落表、可索引、可回放的最小数据结构。  
> 边界：本文只处理第一阶段窄链所需数据对象，不覆盖 `Progee2` 全仓业务表。  

---

## 1. 一句话定位

> **这份数据草案首先服务“谁放的、谁拦的、为什么拦、后来谁改了”，而不是先服务 BI 和报表。**

---

## 2. 第一阶段核心表

建议第一阶段至少有九张核心表：

1. `signal_cases`
2. `cop_assessments`
3. `tat_rulings`
4. `odd_contracts`
5. `execution_tickets`
6. `capability_grants`
7. `runtime_events`
8. `incident_cases`
9. `rollback_orders`
10. `appeal_requests`

---

## 3. 表结构草案

## 3.1 `signal_cases`

```sql
signal_cases(
  case_id varchar primary key,
  source varchar not null,
  problem_scene text not null,
  loss_signals_json text not null,
  role_map_json text not null,
  workflow_status varchar not null,
  handoff_intent boolean not null,
  created_at datetime not null
)
```

## 3.2 `cop_assessments`

```sql
cop_assessments(
  assessment_id varchar primary key,
  case_id varchar not null,
  primary_type varchar null,
  secondary_type varchar null,
  classification_confidence decimal(5,4) not null,
  structural_risk varchar not null,
  triage_status varchar not null,
  tags_json text not null,
  refer_to_json text not null,
  created_at datetime not null
)
```

## 3.3 `tat_rulings`

```sql
tat_rulings(
  ruling_id varchar primary key,
  case_id varchar not null,
  based_on_assessment_id varchar not null,
  ruling varchar not null,
  r_state varchar not null,
  max_action_level varchar not null,
  appeal_window int not null,
  rollback_condition text not null,
  mandatory_audit_json text not null,
  created_at datetime not null
)
```

## 3.4 `odd_contracts`

```sql
odd_contracts(
  contract_id varchar primary key,
  case_id varchar not null,
  based_on_ruling_id varchar not null,
  contract_family varchar not null,
  gate_profile varchar not null,
  human_only_constraints_json text not null,
  forbidden_actions_json text not null,
  evidence_schema_json text not null,
  rollback_policy text not null,
  created_at datetime not null
)
```

## 3.5 `execution_tickets`

```sql
execution_tickets(
  execution_id varchar primary key,
  contract_id varchar not null,
  task_level varchar not null,
  gate_profile varchar not null,
  hard_constraints_json text not null,
  freeze_rules_json text not null,
  rollback_policy text not null,
  state varchar not null,
  created_at datetime not null
)
```

## 3.6 `capability_grants`

```sql
capability_grants(
  grant_id varchar primary key,
  execution_id varchar not null,
  permitted_tools_json text not null,
  permitted_targets_json text not null,
  forbidden_targets_json text not null,
  revoke_conditions_json text not null,
  created_at datetime not null
)
```

## 3.7 `runtime_events`

```sql
runtime_events(
  event_id varchar primary key,
  execution_id varchar not null,
  previous_event_id varchar null,
  event_type varchar not null,
  source varchar not null,
  actor varchar not null,
  severity varchar not null,
  reason text not null,
  evidence_ref_json text not null,
  created_at datetime not null
)
```

## 3.8 `incident_cases`

```sql
incident_cases(
  incident_id varchar primary key,
  execution_id varchar not null,
  opened_by_event varchar not null,
  incident_type varchar not null,
  severity varchar not null,
  current_owner varchar not null,
  status varchar not null,
  created_at datetime not null
)
```

## 3.9 `rollback_orders`

```sql
rollback_orders(
  rollback_id varchar primary key,
  execution_id varchar not null,
  trigger_by varchar not null,
  strategy varchar not null,
  reason text not null,
  target_scope text not null,
  result varchar not null,
  created_at datetime not null
)
```

## 3.10 `appeal_requests`

```sql
appeal_requests(
  appeal_id varchar primary key,
  case_id varchar not null,
  execution_id varchar not null,
  appellant varchar not null,
  target_of_appeal_json text not null,
  claimed_issue text not null,
  status varchar not null,
  created_at datetime not null
)
```

---

## 4. 关键索引

优先建立以下索引：

```sql
create index idx_cop_assessments_case_id on cop_assessments(case_id);
create index idx_tat_rulings_case_id on tat_rulings(case_id);
create index idx_odd_contracts_case_id on odd_contracts(case_id);
create index idx_execution_tickets_contract_id on execution_tickets(contract_id);
create index idx_runtime_events_execution_id_created_at on runtime_events(execution_id, created_at);
create index idx_incident_cases_execution_id on incident_cases(execution_id);
create index idx_rollback_orders_execution_id on rollback_orders(execution_id);
create index idx_appeal_requests_case_id on appeal_requests(case_id);
```

最关键的是：

- `runtime_events(execution_id, created_at)`
- `incident_cases(execution_id)`
- `appeal_requests(case_id)`

因为三者决定能不能回放治理链。

---

## 5. append-only 审计规则

### 5.1 只追加，不覆盖

以下表默认禁止 `update` 语义覆盖核心记录：

1. `runtime_events`
2. `incident_cases`
3. `rollback_orders`
4. `appeal_requests`

### 5.2 如何修正

修正只能通过：

1. 新增后继事件
2. 新增新裁决
3. 新增 superseded 标识字段或关系表

不能直接改旧行内容。

---

## 6. 最小回放查询

### 6.1 某次执行的完整事件流

```sql
select *
from runtime_events
where execution_id = :execution_id
order by created_at asc;
```

### 6.2 某案例的完整治理链

```sql
select *
from signal_cases sc
left join cop_assessments ca on ca.case_id = sc.case_id
left join tat_rulings tr on tr.case_id = sc.case_id
left join odd_contracts oc on oc.case_id = sc.case_id
where sc.case_id = :case_id;
```

### 6.3 某事故后的申诉与回滚链

```sql
select *
from incident_cases ic
left join rollback_orders ro on ro.execution_id = ic.execution_id
left join appeal_requests ar on ar.execution_id = ic.execution_id
where ic.incident_id = :incident_id;
```

---

## 7. 最小 UI 读模型

可派生三类只读视图：

1. `v_case_governance_summary`
2. `v_execution_runtime_timeline`
3. `v_incident_appeal_summary`

这些视图服务 Dashboard / Review / Incident 页面，

不要让前端自己拼所有底层表。

---

## 8. 三条红线

1. 不得让 `runtime_events` 变成可覆盖更新的普通日志表。  
2. 不得把 `triage_status` 与 `ruling` 塞进同一列。  
3. 不得只存最终状态而丢掉中间冻结、回滚、申诉记录。  

---

## 9. 配套回引

- `Progee2 落地优化稿（现行版）`
- `Progee2 API 与状态流转草案（现行版）`
- `Harness 运行时对象与事件规范（现行版）`
- `TAT-COP-ODD-Harness 复审与申诉样例包（现行版）`

---

> **最终总句**：  
> **Progee2 的第一阶段数据层，首先要能回答责任链怎么走过，其次才是把数据喂给报表。**
