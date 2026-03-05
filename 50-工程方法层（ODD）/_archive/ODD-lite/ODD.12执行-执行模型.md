---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.01OVR]
---

# 执行模型

## 意向
ODD 不只是“产出物驱动”，还必须回答：出错怎么办？副作用怎么控？状态如何流转？并发如何约束？事务与补偿如何切分？
执行模型把这些问题前置到契约与管道层，确保“可验证、可恢复、可审计”。

## 规范

### 错误模型
错误必须显式分类与声明：
- **可恢复性**：recoverable / unrecoverable
- **责任归属**：client_error / server_error / external_error
- **传播规则**：上游错误必须被下游声明或转换，不允许静默吞掉

### 副作用模型
- 副作用必须显式声明（effects），并与验证规则绑定。
- 任何外部调用 MUST 标注重试/超时/幂等策略。

### 状态模型
- 状态可显式作为输入/输出传递，或声明为状态容器（reads/writes）。
- 复杂状态 SHOULD 用状态机契约描述。

### 并发模型
- 并发策略 MUST 明确：串行/并行/加锁。
- 幂等性 MUST 声明：幂等键、行为、TTL。

### 事务与补偿
- DB 事务只包含 DB 操作，外部调用必须在事务外。
- 跨步骤失败 MUST 有补偿策略（反向撤销或状态回滚）。

---

## 机制

### L1 · 轻量

**最小化声明**：
- 错误只区分“可恢复/不可恢复”。
- 副作用只做文字描述。
- 并发默认串行。

```yaml
contract:
  errors:
    - code: INVALID_INPUT
      recoverable: false
  effects:
    - type: db_write
      description: "插入用户记录"
```

---

### L2 · 标准

**错误分类 + 明确传播**：
```yaml
errors:
  - code: INVALID_EMAIL
    category: client_error
    recoverable: false
    message: "邮箱格式不正确"
  - code: DB_TIMEOUT
    category: external_error
    recoverable: true
    retry_strategy: exponential_backoff
    max_retries: 3

error_propagation:
  mode: explicit          # explicit | transform
  mapping:
    DB_TIMEOUT -> SERVICE_TEMPORARY_UNAVAILABLE
```

**副作用声明与验证**：
```yaml
effects:
  - type: db_write
    target: users
    operation: insert
  - type: event_emit
    event: user_created

expected_effects:
  - type: db_write
    target: users
    data_match:
      email: "test@example.com"
```

**状态容器**：
```yaml
state_container Session:
  scope: session
  schema:
    user_id: uuid
    token: string

contract GetProfile:
  reads: [Session.user_id]
  output: { profile }
```

**并发与幂等**：
```yaml
concurrency:
  mode: serialized
  lock_key: email
  lock_timeout: 5s

idempotency:
  enabled: true
  key: email
  behavior: return_existing
  ttl: 24h
```

---

### L3 · 严格

**事务边界 + 补偿策略**：
```yaml
transaction:
  isolation: serializable
  timeout: 30s
  steps:
    - contract: CreateOrder
    - contract: ProcessPayment
    - contract: SendConfirmation
  on_failure:
    strategy: rollback_all | compensate
    compensations:
      - CreateOrder: CancelOrder
      - ProcessPayment: RefundPayment
```

**混合管道模式**：
- **编排（Orchestration）**：应用层协调多步骤。
- **事件驱动（Choreography）**：DB 触发事件，应用层响应。
- **Saga**：每步都有补偿，失败时反向执行。

**执行上下文**：
```yaml
execution_context:
  request_id: string
  timestamp: datetime
  errors: [error]
  effects: [effect]
  transaction_id: string?
```

---

## 实践

### 快速选型
- **小项目** → L1，最小错误与副作用声明。
- **团队协作** → L2，错误分类 + 幂等 + 状态容器。
- **关键系统** → L3，事务边界 + 补偿 + Saga。

### 核心原则
- **错误不可隐身**：不声明就等于不存在。
- **副作用必须可验证**：否则无法证明“真的发生”。
- **事务要短、补偿要清晰**：长事务必然锁死系统。
- **并发要可控**：锁与幂等是最低成本保险。
