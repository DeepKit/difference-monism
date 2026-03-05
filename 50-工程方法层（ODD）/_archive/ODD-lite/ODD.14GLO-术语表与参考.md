---
version: 1.0.0
status: stable
last_updated: 2026-02-11
prerequisites: [无]
---

# 术语表与参考

## 意向
ODD 文档集使用大量专有术语和缩写。本文档提供中英文对照、概念关系图和学术引用，便于快速查阅和外部沟通。

## 规范
- 新增术语 MUST 同步更新本文档和 `ODD.00IDX-索引.md`。
- 术语定义以本文档为权威来源，索引中的定义为简版。

## 机制

### 核心术语中英文对照

#### 五大支柱
- 契约 — Contract
- 产出物 — Artifact
- 门禁 — Gate
- 证据 — Evidence
- 封存 — Seal

#### 对象与结构
- 任务 — Task
- 管道 — Pipeline
- 功能树 — Functional Tree
- 依赖图 — Dependency Graph
- 功能节点 — Functional Node
- 产出物类型 — Artifact Type
- 产出物标准库 — Artifact Standard Library

#### 状态与流转
- 状态机 — State Machine
- 返工 — Rework
- 解封 — Unseal
- 封版 — Sealed（状态）
- 阻塞 — Blocked
- 废弃 — Deprecated
- 外部显示标签 — External Display Label

#### 质量与验证
- 清晰度评估 — Clarity Assessment
- 对抗生成 — Adversarial Generation
- 契约对抗协议 — Contract Adversarial Protocol (CAP)
- 地板 — Floor（最低条件）
- 红线 — Red Line（不可违反约束）
- 变异测试 — Mutation Testing
- 变异体 — Mutant
- 变异分数 — Mutation Score
- ODD 原生验证 — ODD Native Verification
- TD-AI — Test-Driven AI（测试驱动 AI 范式）
- 输入输出映射 — Input-Output Mapping
- 动态值匹配 — Dynamic Value Matching

#### 上下文与知识
- 上下文工程 — Context Engineering
- 情报官 — Intelligence Officer
- 17 层上下文 — 17-Layer Context Model
- 隐式需求 — Implicit Requirements
- 常识库 — Common Knowledge Base
- Token 预算 — Token Budget
- 预置参数组 — Preset Parameter Set
- 提示词存库 — Prompt Repository

#### 执行与管理
- 车间 — Workshop
- 车间池 — Workshop Pool
- 赛马 — Racing（任务分级匹配）
- 红绿灯 — Traffic Light（分级预警）
- 三大法宝 — Three Treasures（功能树 + Bug 意向图 + 最佳实践）
- Bug 意向图 — Bug Intention Map
- 最佳实践 — Best Practices
- 反模式 — Anti-Pattern
- 交叉审核 — Cross-Review

#### 版本与迁移
- 契约版本迁移 — Contract Version Migration
- 语义化版本 — Semantic Versioning (SemVer)
- 兼容性规则 — Compatibility Rules
- 版本生命周期 — Version Lifecycle

#### 执行模型
- 幂等性 — Idempotency
- 补偿 — Compensation
- 副作用声明 — Side-Effect Declaration
- 事务边界 — Transaction Boundary
- 管道边界原则 — Pipeline Boundary Principle

#### 角色
- 提案者 — Proposer
- 挑战者 — Challenger
- 攻击者 — Attacker
- 裁决者 — Arbiter

#### 等级体系
- L1 · 轻量 — L1 · Lightweight
- L2 · 标准 — L2 · Standard
- L3 · 严格 — L3 · Strict
- L4 · 人工审查 — L4 · Human Review（仅任务等级）

#### 缩写速查
- ODD — Outcome-Driven Development（产出物驱动开发）
- CAP — Contract Adversarial Protocol（契约对抗协议）
- TD-AI — Test-Driven AI（测试驱动 AI）
- ES — Empirically Settled（经验可判定）
- NES — Not Empirically Settled（经验不可判定）
- DAG — Directed Acyclic Graph（有向无环图）
- SemVer — Semantic Versioning（语义化版本）

### 核心概念关系图

```
                        ┌─────────┐
                        │  人类意图  │
                        └────┬────┘
                             ▼
                    ┌─────────────────┐
                    │    契约 Contract   │◄── 清晰度评估 + CAP 对抗
                    └────────┬────────┘
                             │ 分解
                    ┌────────▼────────┐
                    │    任务 Task      │◄── 赛马分级 + 车间分配
                    └────────┬────────┘
                             │ 执行
                    ┌────────▼────────┐
                    │  产出物 Artifact  │◄── 三大法宝注入（功能树+Bug图+最佳实践）
                    └────────┬────────┘
                             │ 验证
                    ┌────────▼────────┐
                    │   门禁 Gate       │◄── ODD 原生验证 + 变异测试
                    └────────┬────────┘
                             │ 通过
                    ┌────────▼────────┐
                    │   证据 Evidence   │
                    └────────┬────────┘
                             │ 绑定
                    ┌────────▼────────┐
                    │   封存 Seal       │
                    └────────┬────────┘
                             │ 输入
                    ┌────────▼────────┐
                    │   管道 Pipeline   │──→ 擢升为新产出物 → 循环
                    └─────────────────┘

    横向关系：
    功能树 ←→ 产出物（业务定位）
    依赖图 ←→ 产出物（技术传导）
    上下文工程 → 情报官 → 17 层上下文 → 模型调用
    产出物标准库 → 隐式需求 + 常识库 → 注入契约/任务
```

### 学术引用与理论基础

**契约式编程（Design by Contract）**
- Bertrand Meyer, "Applying Design by Contract", IEEE Computer, 1992
- ODD 的契约概念扩展了 Meyer 的前置/后置条件模型，增加了对抗生成和清晰度评估

**变异测试（Mutation Testing）**
- Richard Lipton, "Fault Diagnosis of Computer Programs", PhD Thesis, Carnegie Mellon, 1971
- Jia & Harman, "An Analysis and Survey of the Development of Mutation Testing", IEEE TSE, 2011
- ODD 将变异测试从代码验证扩展到契约验证层

**基于属性的测试（Property-Based Testing）**
- Claessen & Hughes, "QuickCheck: A Lightweight Tool for Random Testing", ICFP, 2000
- ODD 的属性式映射直接借鉴了属性测试的理念

**管道架构（Pipeline Architecture）**
- Martin Fowler, "Pipes and Filters", Enterprise Integration Patterns
- ODD 管道强调契约边界和封存传递，不同于传统数据流管道

**状态机与形式化验证**
- David Harel, "Statecharts: A Visual Formalism for Complex Systems", Science of Computer Programming, 1987
- ODD 状态机为工程简化版本，用门禁替代完整形式化验证

**语义化版本控制**
- Tom Preston-Werner, "Semantic Versioning 2.0.0", semver.org
- ODD 的契约版本迁移直接采用 SemVer 规范

**测试金字塔**
- Mike Cohn, "Succeeding with Agile", 2009
- ODD 的 70/25/5 比例来源于此经典模型

---

## 实践
- 沟通中使用中文术语为主，括号标注英文缩写。
- 对外文档和 API 设计使用英文术语。
- 不确定术语含义时以本文档为准，而非索引中的简版定义。
