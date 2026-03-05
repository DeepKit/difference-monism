---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.07ART]
---

# 功能树

## 意向
产出物不断增长，管道不断编排——但"我想要的那个功能到底在哪？"没人能回答。
功能树是产出物网络的目录：按业务功能分层索引，让任何人都能从功能出发找到对应的产出物、契约和管道，也能在一个产出物变动时立刻知道影响了哪些功能。

## 规范

### 功能树定义
功能树（Functional Tree）= 以业务功能为节点、以"实现/依赖"为边的分层索引。

核心规则：
- 功能树 MUST 覆盖项目所有业务功能，不允许有"无归属"的产出物。
- 每个叶子节点 MUST 映射到至少一个产出物。
- 一个产出物 MAY 被多个功能节点引用（共享组件）。
- 功能树节点的粒度不受代码模块约束——它按业务能力划分，不按目录结构划分。

### 节点结构
```yaml
功能节点:
  id: string              # 唯一标识
  name: string            # 功能名称
  parent: string | null   # 父节点 ID，根节点为 null
  children: [string]      # 子节点 ID 列表
  artifacts: [string]     # 映射的产出物 ID 列表
  owner: string           # 负责人
  status: active | deprecated | planned
```

### 关键操作
- **定位**：给定功能名，查到对应的产出物及其状态。
- **追溯**：给定产出物，查到它属于哪些功能节点。
- **影响分析**：某个产出物变动时，沿功能树 + 依赖图，找出所有受影响的功能。
- **覆盖检查**：检测是否有产出物不属于任何功能节点（孤立产出物）。

### 与管道/依赖图的关系
- 功能树管"业务视角的定位"，依赖图管"技术视角的传导"。
- 影响分析 = 功能树定位 + 依赖图传播：先在依赖图上算出受影响的产出物集合，再在功能树上映射出受影响的功能集合。
- 功能树不替代依赖图，两者互补。

---

## 机制

### L1 · 轻量

功能树 = 一份 Markdown 清单，手动维护。

**做法**：
在项目根目录放一份 `功能树.md`（或嵌在 README 中），按业务功能列出对应的产出物。

```markdown
# 功能树

## 用户管理
- 注册功能 → `user-register` 契约 → 产出物: user-register-api, user-register-test
- 登录功能 → `user-login` 契约 → 产出物: user-login-api, user-login-test

## 订单处理
- 创建订单 → `order-create` 契约 → 产出物: order-create-api, order-create-test
- 支付 → `order-pay` 契约 → 产出物: order-pay-api, payment-gateway-adapter
```

**影响分析**：手动。产出物变动时，在清单中搜索该产出物，看它属于哪些功能。

**覆盖检查**：人工比对产出物列表和功能树，确认没有遗漏。

---

### L2 · 标准

功能树 = 结构化数据，工具可查询。

**节点定义**：
```yaml
functional_tree:
  nodes:
    - id: user-mgmt
      name: 用户管理
      parent: null
      children: [user-register, user-login]
      artifacts: []
      owner: team-a
      status: active

    - id: user-register
      name: 注册功能
      parent: user-mgmt
      children: []
      artifacts: [user-register-api, user-register-test]
      owner: team-a
      status: active
```

**查询能力**：
- `locate(功能名)` → 返回产出物 ID 列表及其当前状态（sealed / stale / in_progress）。
- `trace(产出物ID)` → 返回该产出物所属的功能节点列表。
- `orphans()` → 返回不属于任何功能节点的产出物列表。

**影响分析**：
```
产出物 X 变动
  → 依赖图：找出下游受影响的产出物集合 S
  → 功能树：对 S 中每个产出物调用 trace()，得到受影响功能集合 F
  → 输出：功能列表 F + 每个功能下受影响的产出物
```

**数据结构**：
```yaml
functional_node:
  id: string
  name: string
  parent: string | null
  children: [string]
  artifacts: [artifact_id]
  owner: string
  status: active | deprecated | planned
  updated_at: datetime
```

---

### L3 · 严格

功能树 = 可审计的业务索引，强制覆盖、自动同步、变更留痕。

**强制规则**：
- 每个产出物 MUST 至少归属一个功能节点，否则封存门禁拒绝通过。
- 功能节点变更（新增/移除/重新映射）MUST 记录在审计日志中。
- 功能树版本 MUST 与产出物封存版本对齐——封存时的功能树快照作为证据的一部分。

**自动同步**：
- 新产出物创建时，系统提示归属到功能节点（或拒绝创建）。
- 产出物删除/废弃时，自动从功能树中移除映射，标记孤立节点。

**影响分析增强**：
```
产出物 X 变动
  → 依赖图：级联计算受影响产出物集合 S
  → 功能树：映射出受影响功能集合 F
  → 自动通知 F 中每个功能的 owner
  → 审计日志记录：变更源 → 影响范围 → 通知对象 → 处理结果
```

**数据结构增量**：
```yaml
functional_node:
  # ...L2 字段...
  version: integer                    # 节点版本号
  change_log:
    - changed_at: datetime
      change_type: add_artifact | remove_artifact | remap | deprecate
      detail: string
      operator: string

functional_tree_snapshot:
  snapshot_id: string
  tree_version: integer
  taken_at: datetime
  triggered_by: string                # 哪次封存触发的快照
  nodes: [functional_node]
```

---

### 完整示例：电商系统功能树

以下展示一个典型电商系统的功能树结构、产出物映射和影响分析。

#### 功能树结构

```
电商平台 (root)
├── 用户管理 (user-mgmt)
│   ├── 注册 (user-register)
│   ├── 登录 (user-login)
│   └── 个人信息 (user-profile)
├── 商品管理 (product-mgmt)
│   ├── 商品列表 (product-list)
│   ├── 商品搜索 (product-search)
│   └── 库存管理 (inventory)
├── 订单管理 (order-mgmt)
│   ├── 创建订单 (order-create)
│   ├── 支付 (order-pay)
│   └── 退款 (order-refund)
└── 通知系统 (notification)
    ├── 邮件通知 (notify-email)
    └── 站内消息 (notify-inbox)
```

#### L2 结构化数据（节选）

```yaml
functional_tree:
  nodes:
    - id: root
      name: 电商平台
      parent: null
      children: [user-mgmt, product-mgmt, order-mgmt, notification]
      artifacts: []
      owner: platform-team
      status: active

    - id: order-mgmt
      name: 订单管理
      parent: root
      children: [order-create, order-pay, order-refund]
      artifacts: []
      owner: order-team
      status: active

    - id: order-create
      name: 创建订单
      parent: order-mgmt
      children: []
      artifacts:
        - order-create-api          # REST API 产出物
        - order-create-validator    # 输入校验产出物
        - order-create-test         # 测试产出物
      owner: order-team
      status: active

    - id: order-pay
      name: 支付
      parent: order-mgmt
      children: []
      artifacts:
        - payment-gateway-adapter   # 支付网关适配器
        - payment-callback-handler  # 回调处理器
        - payment-test              # 支付测试
      owner: order-team
      status: active

    - id: order-refund
      name: 退款
      parent: order-mgmt
      children: []
      artifacts:
        - refund-processor          # 退款处理器
        - refund-policy-engine      # 退款策略引擎
      owner: order-team
      status: active

    - id: inventory
      name: 库存管理
      parent: product-mgmt
      children: []
      artifacts:
        - inventory-service         # 库存服务
        - inventory-lock            # 库存锁定机制
      owner: product-team
      status: active
```

#### 影响分析演示

**场景**：`payment-gateway-adapter` 产出物变更（支付网关升级）。

```
第 1 步：依赖图传播
  payment-gateway-adapter 变更
    → payment-callback-handler（直接依赖）
    → refund-processor（调用支付接口做退款）
    → order-create-api（调用支付接口做扣款）
  受影响产出物集合 S = {
    payment-callback-handler,
    refund-processor,
    order-create-api
  }

第 2 步：功能树映射
  trace(payment-callback-handler) → 支付 (order-pay)
  trace(refund-processor)          → 退款 (order-refund)
  trace(order-create-api)          → 创建订单 (order-create)
  受影响功能集合 F = {支付, 退款, 创建订单}

第 3 步：输出
  受影响功能   │ 受影响产出物              │ 负责人
  ──────────┼─────────────────────────┼──────────
  支付         │ payment-callback-handler  │ order-team
  退款         │ refund-processor          │ order-team
  创建订单     │ order-create-api          │ order-team

  → 通知 order-team：3 个功能受影响，需重新验证下游产出物。
```

#### 覆盖检查示例

```
orphans() → 返回: [logging-middleware]

→ 发现孤立产出物: logging-middleware 不属于任何功能节点。
→ 处理: 归属到“基础设施”功能节点，或确认是废弃产出物后标记 deprecated。
```

---

## 实践

### 快速选型指南
- **产出物 < 20 个** → L1，一份 Markdown 清单足矣。
- **多团队协作、产出物持续增长** → L2，结构化数据 + 查询能力。
- **需要合规审计、不允许孤立产出物** → L3，强制覆盖 + 版本快照 + 变更审计。

### 核心原则
- **功能视角优先**：功能树按"用户要什么"组织，不按"代码怎么分"组织。
- **零孤立**：每个产出物都能从功能树上找到归属，没有"幽灵产出物"。
- **双视角互补**：功能树 = 业务地图，依赖图 = 技术传导路径。两者结合才能回答"改了这里，影响了哪些业务"。
