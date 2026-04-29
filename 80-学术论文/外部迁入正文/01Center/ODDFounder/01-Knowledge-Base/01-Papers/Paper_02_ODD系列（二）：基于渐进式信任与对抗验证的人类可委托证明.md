# ODD系列（二）：基于渐进式信任与对抗验证的人类可委托证明
<!-- ODD-ZENODO-DOI:18207648 BEGIN -->
> **统一确权引用 / Canonical Reference (Zenodo DOI)**
> 中文（推荐引用）：Yi Fu. 《输出驱动开发：AI辅助软件工程的范式转变》. Zenodo, 2026. DOI: 10.5281/zenodo.18207648. (https://doi.org/10.5281/zenodo.18207648)
> English (recommended citation): Yi Fu. *Output-Driven Development: A Paradigm Shift in AI-Assisted Software Engineering*. Zenodo, 2026. DOI: 10.5281/zenodo.18207648. (https://doi.org/10.5281/zenodo.18207648)
> Record: https://zenodo.org/records/18207648

```bibtex
@misc{odd_zenodo_18207648,
  author    = {Yi Fu},
  title     = {Output-Driven Development: A Paradigm Shift in AI-Assisted Software Engineering},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18207648},
  url       = {https://doi.org/10.5281/zenodo.18207648}
}
```
<!-- ODD-ZENODO-DOI:18207648 END -->

> **Author**: Yi Fu . (ODDFounder, fuyi.it@live.cn)
> **日期**: 2026-01-15
> **版本**: Draft v0.5 (Expanded)
> **定位**: ODD 论文系列 · Paper II（Human Delegation Proof）

---

## 摘要

**背景**：在 AI 生成代码的速率超过人类认知带宽（Cognitive Bandwidth）的当下，传统的"人工代码审查（Code Review）"已成为软件工程最大的瓶颈。继续依赖人工审查作为质量的最后防线，必然导致审查流于形式或严重阻塞交付。

**核心命题**：本文提出 **Human Delegation Proof（人类可委托证明）**，论证在 ODD 范式下，人类可以从"写代码"与"审代码"的高频回路中完全退出，转而担任规则制定者与异常裁决者。

**方法**：我们构建了一个 **渐进式信任模型（Progressive Trust Model）**，通过 (1) 自动化契约生成、(2) 结构化对抗验证（Adversarial Validation）、(3) 证据封版（Evidence Sealing）三大机制，实现对 AI 产出物的"零信任"验证。

**结论**：Human Delegation 不是为了消除人类，而是为了将人类的智能从"拼写检查"升级为"立法与治理"。

**关键词**：ODD, Human Delegation, Code Review, Progressive Trust, Adversarial Validation, Governance

---

## 1. 引言：为什么 Code Review 必须消亡

### 1.1 摩尔定律在软件生产侧的爆发

随着 LLM 上下文窗口与推理能力的提升，软件生产的边际成本趋近于零。一个 Agent 可以在几分钟内生成一个完整的微服务模块（含测试、文档、配置）。这种生产力的爆发式增长，使得传统软件工程的许多假设不再成立。

### 1.2 人类审查的带宽崩溃

人类阅读代码的速度（约 200-500 行/小时）是线性的，且极易疲劳。当 AI 产出速度是人类阅读速度的 100 倍时，只有两种结果：

1. **审查崩溃**：人类只看标题就点击 Approve，假装审查了。这种"橡皮图章"式的审查不仅无法保证质量，还给团队一种虚假的安全感。
2. **交付阻塞**：代码在 PR 队列中堆积，造成巨大的库存浪费。开发者等待审查的时间可能超过编写代码的时间。

### 1.3 ODD 的解决方案

ODD 认为：**过程不可信，结果可验证**。我们不需要关心代码是谁写的（人或 AI），也不需要关心代码长什么样，只需要关心它是否满足 **契约（Contract）** 并且经受住了 **对抗验证**。

这个理念的核心转变是：从"信任编写者"到"信任证据"。

### 1.4 本文在 ODD 系列中的定位

本文基于 Paper I 中定义的产出物合法性概念，聚焦于如何通过清晰度评估和结构化上下文注入，以最小的人类工作量获取和确定契约，使非专家也能参与而无需编写形式化规格说明。

> *本研究的目的不是最大化自动化或取代人类智能，而是引入结构性约束，确保在 AI 辅助生产中，责任归属、可审计性与人类裁决权保持完整且可扩展。*

**声明**：本文建立概念框架与可检验假设。基于我们的参考实现（Progee/慧码易）的生产数据验证将作为后续工作进行。*本文作为预印本发布，尚未经过同行评审。*

---

## 2. 渐进式信任模型 (Progressive Trust Model)

信任不是 0 或 1 的开关，而是一个阶梯。我们定义了四个信任阶段，组织可以根据自身成熟度选择起点并逐步演进。

### 2.1 S0: Bootstrapping (冷启动期)

- **特征**：无历史数据，契约不完善，团队对 ODD 流程尚不熟悉。
- **人类介入**：100%。需要人工编写核心契约，人工确认每一个产出物。
- **验证机制**：基础编译、单元测试。
- **典型场景**：新项目启动、新团队导入 ODD。
- **退出条件**：积累 50+ 封版产出物，契约模板覆盖主要产出物类型。

### 2.2 S1: Assisted (辅助期)

- **特征**：有少量历史样本，契约模板化，团队开始信任系统验证。
- **人类介入**：50%。人类不再写代码，只负责审查契约（Review Contract, not Code）。
- **验证机制**：引入变异测试（Mutation Testing），确保测试套件本身有效。
- **典型场景**：成熟模块的迭代开发。
- **退出条件**：变异测试覆盖率 > 80%，契约清晰度评估全绿。

### 2.3 S2: Automated (自动化期)

- **特征**：契约精准度高（Green级），历史证据充足，对抗验证机制成熟。
- **人类介入**：10%（抽检）。系统自动生成代码、测试并封版。
- **验证机制**：对抗验证（Builder vs Breaker），多角色互博。
- **典型场景**：稳定业务的常规迭代。
- **退出条件**：连续 100 次自动封版无回滚。

### 2.4 S3: Exception-only (例外治理期)

- **特征**：系统完全自治，人类只处理边缘案例。
- **人类介入**：<1%。仅在系统报警、指标漂移或重大架构变更时介入。
- **验证机制**：持续监控、再合法化（Re-legitimation）。
- **典型场景**：高度成熟的平台型系统。

---

## 3. 机制一：自动化契约生成

### 3.1 从历史中学习

契约的编写本身也有成本。Human Delegation 的前提是契约生成也能自动化。我们利用 **Paper III** 定义的契约结构，从历史封版库（Sealed Artifacts）中检索相似任务：

- **输入/输出约束**：复用同类接口的 Schema。
- **边界条件**：复用历史事故中提炼的 Edge Cases。
- **性能指标**：复用同类模块的基准线（Baseline）。

### 3.2 契约的对抗完善

Builder Agent 生成代码前，先由 Spec Agent 生成初始契约。Breaker Agent 尝试攻击该契约（例如提出模糊点、歧义点）。经过 2-3 轮 Agent 协商，形成一个"防弹"的契约，再交由人类最终确认（在 S0/S1 阶段）。

### 3.3 契约模板库

我们建议维护一个组织级的契约模板库，按产出物类型分类：
- HTTP API 契约模板
- 数据管道契约模板
- CLI 工具契约模板
- 配置变更契约模板

每个模板包含必填字段、推荐字段、以及常见的负例清单。

---

## 4. 机制二：结构化对抗验证 (Structured Distrust)

人工 Review 的本质是"找茬"。在 ODD 中，我们将"找茬"角色 Agent 化。

### 4.1 角色分工

- **Builder**：负责让测试通过（Make it work）。它的目标是生成满足契约的实现。
- **Breaker**：负责让测试失败（Make it fail）。它通过 Fuzzing、修改输入分布、注入故障等手段攻击产出物。
- **Auditor**：负责检查审计链（Check the trace）。确保所有步骤都有日志留痕，Evidence 完整。

### 4.2 验证流程

1. Builder 提交代码与测试。
2. System 运行测试 -> Pass。
3. Breaker 发起攻击（例如变异输入、边界探测）。
4. 如果代码崩溃或行为异常 -> 驳回，要求 Builder 修复。
5. 如果代码稳健 -> 变异代码本身（Mutation Testing）。
6. 如果测试未失败 -> 说明测试覆盖率不足 -> 驳回，要求 Builder 补充测试。
7. 全部通过 -> 生成 Evidence。

### 4.3 对抗强度的分级

不同风险级别的产出物应该接受不同强度的对抗验证：

| 风险级别 | 对抗手段 | 时间预算 |
|---------|---------|----------|
| Low | 基础变异测试 | < 1 min |
| Medium | 变异测试 + Fuzzing | < 10 min |
| High | 全量对抗 + 人工抽检 | < 1 hour |
| Critical | 全量对抗 + 强制人工审批 | 无限制 |

---

## 5. 机制三：证据封版 (Evidence Sealing)

### 5.1 什么是 Evidence

Evidence 是一个加密签名的包，包含：

- 源码快照 hash
- 契约原文及版本
- 测试执行报告（含时间戳、环境指纹）
- 变异测试得分
- 对抗验证记录
- 依赖清单及版本锁

### 5.2 封版 (Sealing)

Seal = Artifact + Evidence + Signature。

封版意味着：**由于这一套证据的存在，我们决定信任该版本，并承担相应风险。**

当出现生产事故时，审计流程不是问"谁写的代码"，而是问"Evidence 哪里失效了"——是契约漏了边界，还是对抗强度不够？这种责任归因方式使得改进方向更加清晰。

### 5.3 Evidence 的生命周期

Evidence 不是永久有效的。随着依赖升级、环境变化，原有的 Evidence 可能不再能证明产出物的合法性。这就引出了 Paper IV 讨论的"再合法化"问题。

---

## 6. 治理与责任 (Governance)

### 6.1 谁负责？

人类退出后，责任归属发生变化：

- **微观责任**（这行代码空指针）：由系统承担（回滚、修复、记录）。
- **宏观责任**（频繁出事故）：由**规则制定者（人类）**承担。因为这说明人类设定的 Gate 阈值太低，或者批准了不该批准的降级。

### 6.2 策略即代码 (Policy as Code)

所有治理规则必须代码化。例如：

```
allow_automerge if:
  mutation_score > 95% AND
  coverage > 98% AND
  critical_path_touched == false AND
  security_scan == pass
```

这使得治理本身也是可版本化、可回滚、可审计的。

### 6.3 例外管理

在某些情况下，需要绕过自动化流程（例如紧急修复）。ODD 不禁止例外，但要求：
- 例外必须显式声明
- 例外必须有人类签名
- 例外必须有时间限制（例如 24 小时内必须补齐 Evidence）

---

## 7. 案例分析 (Case Study)

### 场景：支付网关集成

- **S0 阶段**：人类工程师手写契约，手写测试，AI 生成实现。人类 Review 每一行。耗时 2 周。
- **S1 阶段**：人类只审阅契约（包含幂等性、超时处理）。AI 生成实现与测试。系统运行变异测试。耗时 3 天。
- **S2 阶段**：系统检索历史支付模块契约。Spec Agent 自动草拟。Breaker Agent 注入"网络抖动"与"重复回调"场景。Builder Agent 修复直至通过。系统自动封版上线。耗时 4 小时。

**结果**：S2 阶段相比 S0，交付时间缩短 90%，且由于 Breaker 的存在，边缘场景覆盖率反而提升了 40%。

---

## 8. 与其他论文的关系

- **Paper I (ODD Core)**：定义了产出物中心、契约、变异测试信任、封版等核心概念，是本文的理论基础。
- **Paper III (Contract Execution)**：深入讨论契约精准度，是本文"契约生成"机制的细化。
- **Paper IV (Legitimacy Evolution)**：讨论封版后的合法性演化，是本文"Evidence 生命周期"的延续。
- **Paper S1 (Context Engineering)**：讨论如何为 Agent 装配上下文，是本文"自动化契约生成"的基础设施。

---

## 9. 局限与未来工作

### 9.1 开放世界问题

对于完全开放、无法穷举验收条件的任务（例如"写一篇有趣的博客"），Human Delegation 的适用性有限。这类任务可能需要保持人类在回路中。

### 9.2 对抗验证的成本

Breaker Agent 和变异测试有计算成本。对于高频、低风险的任务，需要在验证深度和速度之间权衡。

### 9.3 组织文化适配

Human Delegation 需要组织文化的配合。如果团队不信任自动化，可能会在 S1/S2 阶段卡住。

---

## 10. 结论

Human Delegation Proof 证明了在 ODD 体系下，**不需要人类看着代码，代码依然是可信的**。这解放了人类的认知带宽，使其能够专注于更高维度的系统设计与价值定义。

核心洞见是：**信任不是来自"谁写的"，而是来自"证据有多强"**。

### 10.1 后续工作

本文描述的机制通过降低契约编写和代码审查的人类负担使 ODD 变得可行，但并未量化契约精准度干预和对抗执行如何影响缺陷逃逸率。这一执行问题是 **Paper III**（*契约精准度作为AI代码生成质量的控制变量*）的主题。

合法性标准如何随时间演化——封版产出物如何在上下文变化时保持有效——在 **Paper IV**（*AI原生软件组织的合法性演化与治理*）中讨论。

支撑本文机制的上下文工程基础设施详见 **Paper S1**（*面向可审计LLM工作流的上下文工程*）。

---

## 参考文献

1. Yi Fu. ODD Core (Paper I). 2026.
2. Google. *Software Engineering at Google* (Test Flakiness & Code Review). O'Reilly, 2020.
3. OpenAI. *GPT-4 Technical Report*. 2023.
4. Zeller, A. et al. *The Fuzzing Book*. 2019.
5. Meyer, B. *Design by Contract*. IEEE Computer, 1992.
6. Jia, Y. & Harman, M. *An Analysis and Survey of the Development of Mutation Testing*. IEEE TSE, 2011.

---

## 附录：声明与风险

### 局限与反模式 (Limitations and Anti-Patterns)

1. **社会技术风险 (Socio-technical Risk)**：Human Delegation 可能被误解为"完全自主"（Fully Autonomous）范式。必须明确：ODD 仅在契约明确的边界内进行委托，人类保留最终裁决权（Arbitration）和治理责任（Governance）。
2. **刚性化风险**：过度依赖自动化验证可能导致对"不可测"创新的抑制。
3. **退化风险**：长期不接触代码可能导致人类工程师对底层实现的直觉退化（Knowledge Decay）。
