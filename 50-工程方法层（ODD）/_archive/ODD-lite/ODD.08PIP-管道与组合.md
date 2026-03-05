---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.01OVR]
---

# 管道与组合

## 意向
产出物不是孤立的。原子产出物通过管道组合擢升为新产出物，这是蜂巢生长的方式。
管道是有契约的组装线——它声明接收什么、产出什么、怎样算成功。

## 规范

### 管道定义
管道（Pipeline）= 可复用的“输入产出物 → 转换 → 输出产出物”单元。
每个管道 MUST 拥有自己的契约，声明：
- 输入：接收哪些产出物（类型 + 状态要求）
- 输出：产生什么产出物
- 验收：输出满足什么条件算成功

### 产出物依赖规则
- 管道输入 MUST 引用已封存的产出物，不得引用未封存的中间状态。
- 产出物之间的依赖关系 MUST 显式声明，不得隐式依赖。
- 依赖图 MUST 为有向无环图（DAG），禁止循环依赖。
- 当某个产出物被替换时，所有依赖它的下游管道 MUST 重新验证。

### 组合模式
- 串联：A >> B（A 的输出作为 B 的输入）
- 并联：A || B（同时执行，结果合并）
- 条件：cond ? A : B（按条件选路径）
- 循环：A * n（重复执行，带上限）
- 聚合：A + B → C（多个产出物合并为一个）

### 管道边界原则（DB 层 vs 应用层）
- **能在 DB 完成的就放 DB**：数据变形、聚合、约束、状态机转换。
- **必须出 DB 的放应用层**：外部调用、文件 IO、AI 推理、人机交互。
- **混合管道**：DB 负责数据，应用负责副作用与外部交互。

**决策树（简化）**：
```
外部调用？是 → 应用层
否 → 纯数据变形？是 → DB 层
否 → 复杂业务/需要人类？是 → 应用层
否 → DB 层
```

**事务边界**：
- DB 事务只包含 DB 操作，外部调用必须在事务外。
- 外部失败必须有补偿（释放库存/取消订单）。

**协调模式**：
- 编排（Orchestration）：应用层显式编排步骤。
- 事件驱动（Choreography）：DB 触发事件，应用层监听响应。
- Saga：每步有补偿，失败时反向执行补偿。

### 组合抽象机制
- **泛型**：以类型参数复用契约（CRUD<T, ID>）。
- **继承**：公共错误/中间件/头部在基类定义。
- **模板**：结构复用（分页列表、批处理）。
- **Mixin**：可审计/可缓存等横切能力组合。

### 组合安全规则
- 类型兼容 MUST 检查：A.output 的类型可赋给 B.input。
- 错误传播 MUST 声明：组合契约必须覆盖子契约的所有错误情况。
- 封存约束 MUST 传递：组合产出物的 seal MUST 包含所有输入产出物的 evidence_ref。

---

## 机制

### L1 · 轻量

管道 = 手动组合。不需要正式的管道定义，但产出物之间的依赖关系要记录清楚。

**依赖管理**：
- 在产出物的 metadata 中记录 `depends_on`（列出依赖的产出物 ID）。
- 人工确认依赖关系正确即可。

```yaml
artifact:
  id: string
  depends_on: [string]   # 依赖的产出物 ID 列表
  produced_by: string    # 哪个契约/任务产生的
```

**组合方式**：手动指定输入产出物，手动验证输出。

---

### L2 · 标准

管道 = 有契约的组装单元，依赖关系由系统维护。

**管道定义**：
```yaml
pipeline:
  id: string
  name: string
  contract:
    inputs:
      - artifact_type: code_module
        state: sealed               # MUST 已封存
      - artifact_type: test_suite
        state: sealed
    output:
      artifact_type: integrated_module
    acceptance: string              # 验收条件
    error_handling: string          # 错误处理策略
```

**依赖管理**：
- 系统维护产出物依赖图（DAG）。
- 执行管道前自动检查：所有输入产出物是否已封存。
- 当输入产出物被替换时，系统标记下游管道为“待重新验证”。

**影响分析**：
```
产出物 X 被替换
  → 查询依赖图：哪些管道的输入包含 X？
  → 标记这些管道的输出产出物为 stale
  → 递归向下：这些 stale 产出物又被谁依赖？
  → 直到没有更多下游
```

**数据结构**：
```yaml
artifact:
  # ...L1 字段...
  state: sealed | stale            # stale = 依赖已变，需重新验证
  dependency_graph:
    upstream: [artifact_id]         # 我依赖谁
    downstream: [artifact_id]       # 谁依赖我
```

---

### L3 · 严格

管道 = 可审计的自动化组装线，依赖关系强制执行、自动级联。

**管道增强**：
- 管道执行 MUST 产生完整的审计日志（输入产出物ID + 输出产出物ID + 门禁结果 + 时间戳）。
- 组合产出物的 seal MUST 包含所有输入产出物的 seal_hash（证据链传递）。
- 组合抽象（泛型/继承/模板/Mixin）MUST 在最终实例化时落地为明确的输入输出与错误声明。

**依赖管理增强**：
- 产出物替换时，系统自动触发下游重新验证（级联重验）。
- 重验失败的下游产出物自动进入 rework。
- 依赖图变更 MUST 记录在审计日志中。

**并行编排**：
- 无依赖关系的管道可以并行执行（由调度器根据 DAG 自动判断）。
- 有依赖关系的管道严格按拓扑序执行。

**数据结构增量**：
```yaml
pipeline_execution:
  pipeline_id: string
  inputs: [{artifact_id, seal_hash}]   # 输入快照
  output: {artifact_id, seal_hash}     # 输出快照
  gate_results: [evidence_ref]         # 门禁证据
  executed_at: datetime
  triggered_by: string                 # 手动 | 级联重验 | 调度

artifact:
  # ...L2 字段...
  seal:
    seal_hash: string
    input_seal_hashes: [string]        # 所有输入产出物的 seal_hash
    sealed_at: datetime
```

---

## 实践

### 快速选型指南
- **产出物很少、依赖简单** → L1，记录 depends_on 就够了。
- **多人协作、产出物之间有明确依赖** → L2，系统维护依赖图，自动标记 stale。
- **关键系统、需要完整审计链** → L3，级联重验 + 封存链传递 + 自动并行编排。

### 依赖管理核心原则
- **只依赖已封存的东西**：不确定的产出物不能被引用，这是质量的根基。
- **依赖必须显式**：“我依赖谁”写在明处，不能靠猜。
- **变动必须传导**：上游变了，下游必须知道并重新验证。
