# LLM计费预占用：流式输出的计费难题解决方案

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **标签**: 计费系统, LLM, 预占用, 事务一致性, Billing

---

## 摘要

在 LLM 应用中，计费面临一个独特的挑战：**流式输出 (Streaming)**。用户发起请求时，我们不知道由于会生成多少 Token，也就不知道该扣多少钱。如果等生成完了再扣，用户可能余额不足；如果先扣一个大数，用户体验差。Billing 系统引入了 **"预占用 (Reserve) -> 结算 (Settle) -> 冲正 (Revert)"** 的三阶段事务机制，完美解决了这一难题。

---

## 一、流式计费的死锁

*   **场景**：用户余额 10 元。Advanced Model 价格 0.1元/千Token。
*   **问题**：用户发了一个请求。
    *   *方案A（后付费）*：让用户先用。结果AI输出了 20万 Token（20元）。用户欠费 10 元跑路。
    *   *方案B（预付费）*：先扣 100元。用户只有 10 元，直接被拒，但其实他只打算生成一句话（0.01元）。

我们需要一种**动态的、乐观的、但有底线**的计费方式。

---

## 二、三阶段生命周期

Billing 系统借鉴了数据库事务和酒店预授权的思路。

### 2.1 阶段一：预占用 (Reserve)

当请求到达网关（Gateway）时，还没转发给 LLM。
*   **计算**：估算 Input Token（如 1000） + 预设 Output 缓冲区（如 1000）。
*   **动作**：在用户钱包中**冻结 (Freeze)** 对应金额（不是扣除，是冻结）。
*   **检查**：如果余额 < 冻结额，拒绝请求。
*   **输出**：生成一个 `TransactionID`，状态 `PENDING`。

### 2.2 阶段二：实时结算 (Incremental Settle) - 可选

对于超长会话，网关可以每隔 10秒 汇报一次当前生成的 Token 数。
*   **动作**：追加冻结额度。
*   **风控**：如果追加失败（余额耗尽），网关立即切断 LLM 连接，停止生成。

### 2.3 阶段三：最终结算与冲正 (Commit & Revert)

请求结束（Finish/Error）。
*   **场景A：成功**
    *   实际消耗：Input 1000 + Output 500 = 1500 Token。
    *   **动作**：
        1.  解冻所有预占用金额。
        2.  实际扣除 1500 Token 对应的费用。
        3.  Transaction 状态变更为 `SUCCESS`。
*   **场景B：失败**（如 LLM 报错）
    *   **动作**：
        1.  解冻所有预占用金额。
        2.  Transaction 状态变更为 `FAILED`。
        3.  用户一分钱不花，余额自动恢复。

---

## 三、工程实现

在 `Billing` 系统的 `cost_service.py` 中，我们使用了 **Redis Lua 脚本** 来保证操作的原子性。

```lua
-- Lua Pseudo-code for Reserve
local balance = redis.call('HGET', user_key, 'balance')
local frozen = redis.call('HGET', user_key, 'frozen')
local available = balance - frozen

if available >= request_amount then
    redis.call('HINCRBY', user_key, 'frozen', request_amount)
    return 'OK'
else
    return 'INSUFFICIENT_FUNDS'
end
```

这种设计确保了在高并发下（用户开了10个窗口同时刷），余额永远不会扣成负数。

---

## 四、多租户与配额

除了余额，Billing 系统还支持 **Quota (配额)** 管理。
*   Progee 团队每月有 10000 刀额度。
*   Solvit 团队每月有 5000 刀额度。

配额的逻辑与余额完全一致，只是数据源不同。这种**统一钱包架构**使得我们可以灵活地为不同层级的对象（用户、应用、租户）应用相同的计费策略。

---

## 五、总结

LLM 的计费系统比传统 SaaS 复杂，因为它的**边际成本是动态的**。
通过**预占用机制**，Billing 系统实现了风控与体验的平衡：
*   对平台：保证了**实收实付**，没有坏账。
*   对用户：保证了**按量付费**，没有多扣。

这是构建可持续商业化 AI 产品的基石。

---

*（本系列工程实践文章更新完毕）*
