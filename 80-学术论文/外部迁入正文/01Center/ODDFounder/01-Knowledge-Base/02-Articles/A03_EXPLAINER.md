# A03: 698种产出物分类法详解 (The Taxonomy of 698 Artifacts)

> **作者**: Yi Fu (ODDFounder  fuyi.it@live.cn)
> **日期**: 2026-01-15
> **标签**: ODD, 产出物分类, 软件工程, AI开发

---

## 摘要

软件开发的本质是生产**产出物 (Artifact)**。ODD 方法论将软件开发中所有可能的产出物系统化为 **698 种类型**，分布在 **14 大类别**中。本文详细解读这套分类体系，帮助开发者精确定义 AI 任务。

---

## 1. 为什么需要产出物分类？

### 1.1 问题：模糊的需求导致模糊的输出

```
你：帮我实现用户登录功能
AI：好的，这是登录代码...

问题来了：
- 你要的是数据库表？还是 API 接口？还是前端界面？
- 需要单元测试吗？集成测试呢？
- 配置文件要不要？文档呢？
```

**根本原因**：缺乏精确的"产出物词汇表"。

### 1.2 解决方案：元素周期表思维

就像化学有元素周期表，软件开发也需要一个完整的产出物分类体系。

**698 种产出物** = 软件开发的"元素周期表"

---

## 2. 14 大类别概览

| 类别 | 英文 | 数量 | 说明 |
|------|------|:----:|------|
| 代码 | code | 205 | 22个子类别，覆盖主流语言 |
| 数据库 | database | 117 | 表、视图、函数、触发器等 |
| 配置 | config | 25 | 构建配置、运行时配置 |
| 基础设施 | infrastructure | 95 | Docker、K8s、Terraform等 |
| 文档 | document | 31 | API文档、用户手册等 |
| 测试 | test | 38 | 单元、集成、E2E测试 |
| 行为 | behavior | 45 | 工作流、状态机、规则 |
| 安全 | security | 20 | 证书、策略、审计报告 |
| API | api | 22 | REST、GraphQL、gRPC |
| 设计 | design | 21 | UI设计、架构图、规范 |
| 资源 | asset | 27 | 图片、字体、多媒体 |
| AI/ML | ml | 24 | 模型、数据集、Prompt |
| 构建 | build | 18 | 包、镜像、归档文件 |
| 数据 | data | 10 | 迁移脚本、ETL流程 |
| **总计** | - | **698** | **14大类别** |

---

## 3. 代码类详解 (205种)

代码类是最大的类别，包含 22 个子类别：

```
代码类子类别：
├── Delphi (13种): unit, form, frame, datamodule, package...
├── C#/.NET (12种): class, interface, controller, blazor...
├── Python (10种): module, class, fastapi, django...
├── TypeScript (12种): module, class, react, vue, angular...
├── Java (10种): class, interface, spring, android...
├── Go (8种): package, struct, interface, handler...
├── Rust (8种): module, struct, trait, macro...
├── C/C++ (10种): header, source, class, template...
├── 游戏开发 (14种): unity, unreal, godot, cocos...
├── 嵌入式 (10种): firmware, driver, arduino, esp-idf...
├── 硬件描述 (6种): verilog, vhdl, systemverilog...
├── 区块链 (10种): solidity, vyper, move, cairo...
├── 函数式 (10种): elixir, erlang, haskell, scala...
├── 科学计算 (10种): r, julia, matlab, jupyter...
├── 遗留系统 (10种): cobol, fortran, ada, abap...
└── 低代码 (8种): bpmn, dmn, rule engine...
```

---

## 4. 数据库类详解 (117种)

```
数据库类子类别：
├── PostgreSQL (25种): table, view, function, trigger, index...
├── MySQL (20种): table, view, procedure, event...
├── SQLite (15种): table, view, trigger, index...
├── MongoDB (12种): collection, index, aggregation...
├── Redis (10种): string, hash, list, set, stream...
├── Elasticsearch (10种): index, mapping, query...
├── 时序数据库 (10种): influxdb, timescaledb...
├── 图数据库 (8种): neo4j, dgraph...
└── 向量数据库 (7种): pinecone, milvus, qdrant...
```

---

## 5. 如何使用产出物分类

### 5.1 精确定义任务

**模糊定义**：
```
帮我写一个用户管理功能
```

**精确定义**：
```yaml
artifacts:
  - type: pg_table
    name: users
  - type: pg_function
    name: create_user
  - type: fastapi_router
    name: user_router
  - type: pytest_unit
    name: test_user_service
```

### 5.2 契约驱动开发

每种产出物都有对应的**契约模板**：

```yaml
# pg_function 契约模板
contract:
  type: pg_function
  name: transfer_money
  input:
    - from_account: uuid
    - to_account: uuid
    - amount: decimal
  output:
    - success: boolean
    - transaction_id: uuid
  preconditions:
    - from_account.balance >= amount
  postconditions:
    - from_account.balance = old.balance - amount
    - to_account.balance = old.balance + amount
```

---

## 6. 总结

698 种产出物分类是 ODD 方法论的基石：

1. **精确性**：消除需求模糊性
2. **可验证性**：每种产出物都有明确的验收标准
3. **可复用性**：契约模板可以跨项目复用
4. **AI友好**：为 AI 提供精确的"词汇表"

**记住**：不要告诉 AI "怎么做"，而是告诉它 "做出什么"。

---

*附件：完整的 698 种产出物列表请参考配套的 JSON 文件。*
*下一篇：《ODD开发周期：Define→Decompose→Execute→Verify→Seal》*

---

> **ODD Series | Week 35 . Friday | 40 Weeks Total**
> Previous: "学术论文-A05"
> Next: "老兵心法-从石斧到AI：人类工具史的终局是心想事成"
