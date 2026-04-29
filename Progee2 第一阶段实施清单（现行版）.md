# Progee2 第一阶段实施清单（现行版）

> 版本：v1.0  
> 日期：2026-03-31  
> 性质：实施清单 / 收口件  
> 目的：把 `Progee2` 第一阶段窄链的实现顺序、验收标准、风险点和禁止偷跑项压成一份可以直接照着推进的清单。  
> 边界：本文只覆盖第一阶段，不规划完整大重构。  
>
> 当前纪律：本文默认后置于 `Progee2 落地优化稿（现行版）`、`API` 与 `数据` 两份补件之后阅读，只承担实施收口角色。  

---

## 1. 一句话定位

> **第一阶段不是做“完整新系统”，而是先让四类高风险动作具备被拦、被立案、被回滚、被复审的最小能力。**

---

## 2. 第一阶段范围

只覆盖四类动作：

1. `外部写回`
2. `数据库破坏性操作`
3. `文件覆盖或删除`
4. `自动批准`

---

## 3. 实施顺序

## Step 1：落表与索引

目标：

- 建立 `signal_cases / cop_assessments / tat_rulings / odd_contracts / execution_tickets / runtime_events / incident_cases / rollback_orders / appeal_requests`

完成标准：

1. 能插入最小样例数据
2. 能按 `case_id / execution_id` 回放
3. `runtime_events` 只追加

## Step 2：打通 `execution_ticket`

目标：

- 高风险动作前必须先拿到 `execution_ticket`

完成标准：

1. 没票据不能执行
2. 票据内能看到 `gate_profile / freeze_rules / rollback_policy`

## Step 3：补 `capability_grant`

目标：

- 明确允许什么工具、什么目标、什么时间窗

完成标准：

1. 没授权一定被拦
2. 命中 `forbidden_targets` 一定生成 `BLOCK`

## Step 4：统一 `runtime_event`

目标：

- 所有高风险动作都必须写标准事件

完成标准：

1. 至少支持 `BLOCK / FREEZE / INCIDENT / ROLLBACK`
2. 每个事件都带 `execution_id`

## Step 5：立 `incident_case`

目标：

- 把事故从“技术异常”变成治理对象

完成标准：

1. 越权动作一定能立案
2. 立案后能挂 owner：`ODD / TAT / Human`

## Step 6：打 `rollback_order`

目标：

- 出事后不只报警，还能真正回滚或补偿

完成标准：

1. 至少支持 `rollback_all / compensate / partial`
2. 回滚结果必须留痕

## Step 7：补 `appeal_request`

目标：

- 支持试点冻结后的复审与申诉

完成标准：

1. 申诉不能抹掉原事故
2. 申诉成功也只能追加新裁决

---

## 4. 页面最小改造

### Dashboard

必须看到四块：

1. `责任裁决`
2. `诊断分流`
3. `工程门禁`
4. `运行时事件`

### Review

必须拆页签：

1. `COP`
2. `TAT`
3. `ODD`
4. `Runtime`

### Task Detail

至少新增：

1. `max_action_level`
2. `appeal_window`
3. `rollback_condition`
4. `latest_runtime_event`

---

## 5. 最小验收标准

只要以下六条同时成立，第一阶段就算过线：

1. 四类高风险动作都要先拿 `execution_ticket`
2. 没 `capability_grant` 就一定被拦
3. 被拦后一定生成 `runtime_event`
4. 命中严重规则后一定能立 `incident_case`
5. 事故后一定能下 `rollback_order`
6. 全链路能被 `case_id / execution_id` 回放

---

## 6. 禁止偷跑项

以下事情第一阶段不要做：

1. 不要先重做全部 UI
2. 不要先拆微服务
3. 不要先做复杂 BI 看板
4. 不要把 `COP` 权重学习自动化
5. 不要在没有回滚能力前放开高风险执行

---

## 7. 当前最高风险

| 风险 | 说明 | 对策 |
|---|---|---|
| 状态混线 | `triage_status` 和 `ruling` 被前后端混成一个字段 | 明确双字段，双视图 |
| 日志退化 | `runtime_event` 被当普通技术日志 | 单独事件表，append-only |
| 回滚空转 | UI 有“回滚”按钮，但底层无 `rollback_order` | 先做后端对象，再做前台按钮 |
| 申诉抹历史 | 为了体验，把事故和冻结直接覆盖 | 只允许追加，不允许覆盖 |

---

## 8. 第一阶段完成后的下一步

第一阶段过线后，再继续：

1. `COP` 误判预算入库
2. `override_expiry`
3. `UNSEAL / RE-SEAL` UI
4. mutation / alert / human decision 并轨

---

## 9. 配套回引

- `Progee2 落地优化稿（现行版）`
- `Progee2 API 与状态流转草案（现行版）`
- `Progee2 数据对象与审计索引（现行版）`
- `COP 误判成本与升级预算协议（现行版）`
- `TAT-COP-ODD-Harness 复审与申诉样例包（现行版）`

---

> **最终总句**：  
> **Progee2 第一阶段的成功，不看功能多不多，只看高风险动作是不是终于有了票据、授权、事件、事故、回滚和复审这六个硬接口。**
