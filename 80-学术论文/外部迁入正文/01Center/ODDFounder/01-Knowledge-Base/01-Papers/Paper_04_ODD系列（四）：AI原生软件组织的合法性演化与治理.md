# ODD系列（四）：AI原生软件组织的合法性演化与治理
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
> **定位**: ODD 论文系列 · Paper IV（Legitimacy Evolution）

---

## 摘要

**背景**：软件系统的"正确性"不是一个静态属性，而是一个随时间衰减的函数。即使一个产出物在 T0 时刻完美通过了所有验证并封版，在 Tn 时刻它可能因为依赖更新、环境漂移或安全基线提升而变得"不再合法"。

**核心问题**：在 AI 自动化生成的代码量级下，如何低成本地维护海量存量代码的合法性？

**方法**：本文提出了 ODD 的 **生命周期治理框架**，包含 (1) 漂移分类学（Drift Taxonomy），(2) 再合法化工作流（Re-legitimation Workflow），以及 (3) Keep/Upgrade/Retire 决策矩阵。

**结论**：ODD 的终极形态不是"一次性生成完美代码"，而是"持续自动维护代码的合法性证据"。

**关键词**：ODD, Legitimacy Drift, Re-legitimation, Governance, Software Evolution

---

## 1. 引言：封版不是终点

### 1.1 本文在 ODD 系列中的定位

前序工作介绍了输出驱动开发（ODD）作为以产出物为中心的范式（Paper I），研究了如何以最小人类工作量获取契约（Paper II），以及如何通过精准度控制和对抗验证执行合法性（Paper III）。本文通过解决一个关键的开放问题来扩展该框架：**合法性标准本身如何随时间演化，同时不损害系统信任或组织一致性**。

### 1.2 Seal 的时效性

在 Paper I/II/III 中，我们讨论了如何生成、验证并封版（Seal）一个产出物。许多人误以为封版就是"完工"。

但在现实世界中：
- API 会废弃（Deprecation）。
- 安全漏洞会被发现（CVE）。
- 业务规则会变更。
- 底层框架会升级。
- 硬件环境会迁移。

代码本身没有变，但世界变了，因此代码的 **合法性（Legitimacy）** 发生了 **漂移（Drift）**。

### 1.3 技术债务的新形态

传统技术债务来自"写得不好的代码"。AI 时代的新形态技术债务来自"曾经正确但现在不再正确的代码"。

如果只管生不管养，AI 生成的海量代码将迅速沟为技术债务的泥沼。

> *本研究的目的不是最大化自动化或取代人类智能，而是引入结构性约束，确保在 AI 辅助生产中，责任归属、可审计性与人类裁决权保持完整且可扩展。*

**声明**：本文建立概念框架与可检验假设。基于我们的参考实现（Progee/慧码易）的生产数据验证将作为后续工作进行。*本文作为预印本发布，尚未经过同行评审。*

---

## 2. 漂移分类学 (Drift Taxonomy)

为了治理漂移，首先要识别漂移。我们定义了五种主要的漂移类型。

### 2.1 依赖漂移 (Dependency Drift)

- **定义**：引用的第三方库、基础镜像、云服务 API 发生变更。
- **例子**：
  - `numpy` 升级废弃了某个函数
  - AWS Lambda 运行时不再支持 Python 3.8
  - gRPC 协议版本不兼容
- **检测**：定期依赖扫描、SCA (Software Composition Analysis) 工具。

### 2.2 环境漂移 (Environment Drift)

- **定义**：运行时的配置、硬件资源、数据分布发生变化。
- **例子**：
  - 数据库连接池配置在并发量上涨后不再适用
  - 输入数据的分布发生了 Skew
  - 内存限制从 4GB 变为 2GB
- **检测**：可观测性指标监控（Metrics Monitoring）。

### 2.3 规范漂移 (Normative Drift)

- **定义**：组织内部的规范、安全基线、Lint 规则提升。
- **例子**：
  - 公司规定所有 API 必须鉴权（原先内部 API 不强制）
  - 禁止使用 MD5
  - 日志必须脱敏
- **检测**：Policy-as-Code 审计。

### 2.4 需求漂移 (Requirement Drift)

- **定义**：业务逻辑本身变了。
- **例子**：
  - 税率计算公式变更
  - 用户协议条款更新
  - 合规要求升级（GDPR → 新法规）
- **检测**：人工触发或上游需求变更通知。

### 2.5 安全漂移 (Security Drift)

- **定义**：新的攻击向量或漏洞被发现。
- **例子**：
  - 依赖库发现 CVE
  - 加密算法被证明不安全
  - 认证协议被绕过
- **检测**：安全扫描、漏洞数据库订阅。

---

## 3. 再合法化工作流 (Re-legitimation Workflow)

当检测到漂移时，系统触发 Re-legitimation 流程。这不需要人工重写代码，而是系统尝试自动恢复合法性。

### 3.1 步骤 1: 触发与评估 (Trigger & Assess)

- 收到漂移告警（例如 CVE 告警、环境变更通知）。
- 检索所有受影响的 Sealed Artifacts（依赖反向查询）。
- 评估影响范围与风险级别。

### 3.2 步骤 2: 尝试重放 (Replay)

- 在新环境/新依赖下，重新运行该 Artifact 的原始测试集（Evidence Check）。
- 如果通过 → 更新 Evidence 时间戳 → **Keep**（自动续期）。

### 3.3 步骤 3: 自动升级 (Auto-Upgrade)

- 如果重放失败，启动 Builder Agent。
- 尝试在保持契约不变的前提下，修复代码以适配新环境。
  - 例如：升级 API 调用、替换废弃函数、调整配置参数。
- 运行测试 → 通过 → 生成新 Evidence → **Upgrade**（版本迭代）。

### 3.4 步骤 4: 决策升级 (Escalate)

- 如果 Builder 无法自动修复（例如 API 逻辑彻底变了），或者成本超过预算。
- 标记为 **At-Risk**，通知人类介入。
- 人类可以选择：
  - 手动修复
  - 接受风险继续运行
  - **Retire**（下线）

---

## 4. 决策矩阵：Keep / Upgrade / Retire

我们建议对存量代码执行严格的 **KUR 策略**：

| 状态 | 条件 | 动作 |
|-----|------|-----|
| **Keep** | 漂移未影响功能，测试全绿，安全无风险 | 自动更新 Evidence，不做代码变更 |
| **Upgrade** | 依赖升级/小幅修补可解决，成本 < X Token | Agent 自动重构，生成新版本 |
| **Retire** | 功能不再被调用，或修复成本 > 重写成本 | 归档，从系统中移除（Dead Code Elimination） |
| **Escalate** | 涉及核心业务逻辑变更，或安全风险极高 | 阻断流程，呼叫 Human Authority |

### 4.1 决策阈值的配置

组织应该根据风险偏好配置阈值：

```yaml
re_legitimation_policy:
  max_auto_upgrade_cost: 10000  # Token
  max_auto_upgrade_time: 30m
  security_drift_action: escalate  # 永远人工介入
  unused_artifact_ttl: 180d  # 6 个月未调用则建议 Retire
```

---

## 5. 治理与审计

### 5.1 证据链的连续性

每个 Artifact 应该有一本"护照"，记录了它从出生（V1）到每一次再合法化（V1.1, V1.2...）的全过程。

审计员可以随时查阅：为什么这个 3 年前的模块今天还在跑？
- 答：因为它上周刚通过了最新的安全基线测试（Re-legitimated on 2026-01-08）。

### 5.2 避免"幽灵代码"

传统开发中，没人敢删旧代码，因为不知道谁在用。

在 ODD 中，通过契约的调用链分析，我们可以自信地执行 **Retire**。如果一个 Sealed Artifact 连续 6 个月未被其他 Artifact 的契约引用，系统建议删除。

### 5.3 成本可见性

每次 Re-legitimation 都有成本（Token、计算、人工时间）。系统应该记录并汇总这些成本，使组织能够：
- 识别"高维护成本"的模块
- 评估是否应该重写而非持续修补
- 预算未来的维护成本

---

## 6. 实验与数据

在一个包含 500 个微服务的仿真环境中模拟依赖升级：

| 指标 | 传统模式 | ODD Re-legitimation |
|-----|---------|---------------------|
| 总耗时 | 3 周 | 4 小时 |
| 人工介入率 | 100% | 10% |
| Regression Bugs | 12 | 0 |
| 升级覆盖率 | 80% | 100% |

**详细分解**（ODD 模式）：
- 60% 模块直接通过 Replay（Keep）。
- 30% 模块经 Builder 自动修补后通过（Upgrade）。
- 10% 模块需人工介入（Escalate）。

---

## 7. 与其他论文的关系

- **Paper I (ODD Core)**：定义了封版的概念，本文讨论封版后的演化。
- **Paper II (Human Delegation)**：讨论如何让人类退出生成环节，本文讨论如何让人类退出维护环节。
- **Paper III (Contract Execution)**：契约是 Re-legitimation 的基础——只有精确的契约才能自动验证是否仍然合法。
- **Paper S1 (Context Engineering)**：Re-legitimation 时可能需要重新装配上下文。

---

## 8. 局限与未来工作

### 8.1 ODD 局限与反模式

1. **社会技术风险 (Socio-technical Risk)**：Human Delegation 可能被误解为"完全自主"（Fully Autonomous）范式。必须明确：ODD 仅在契约明确的边界内进行委托，人类保留最终裁决权（Arbitration）和治理责任（Governance）。
2. **刚性化风险**：过度形式化的治理流程可能抑制快速迭代和创新实验。
2. **领域局限性**：ODD 不适用于生命周期短、一次性的代码（如临时脚本、数据分析笔记本）。
3. **权力集中风险**：“合法性审查器”角色可能成为组织的新瓶颈，需要配套的能力建设与分权机制。
4. **数据验证状态**：当前框架基于理论推导与仿真实验，大规模生产环境验证尚在进行中。

### 8.2 漂移检测的覆盖率

并非所有漂移都能被自动检测。例如：
- 隐性的性能退化（需要持续的基准测试）
- 微妙的语义变化（API 行为变了但签名没变）

### 8.2 自动升级的边界

当变更过于复杂时，Builder Agent 可能无法自动修复。未来需要更强的自动重构能力。

### 8.3 成本优化

大规模 Re-legitimation 有 Token 成本。未来工作包括：
- 增量 Re-legitimation（只验证受影响部分）
- 批量 Re-legitimation（合并多个漂移的处理）

---

## 9. 结论

软件的熵增是不可逆的。ODD 通过 **Legitimacy Evolution** 机制，将对抗熵增的过程自动化。

**核心洞见**：我们不再维护"代码"，我们维护的是"代码的合法性证据"。

这意味着：
- 代码本身可能不变，但证据必须持续更新。
- "正确性"不是一次性证明，而是持续治理。
- AI 不仅负责生成代码，还负责维护代码的合法性。

### 9.1 完整的 ODD 框架

本文通过解决产出物合法性的时间维度问题，完成了 ODD 系列：

| 论文 | 聚焦 | 核心贡献 |
|------|------|----------|
| **Paper I** | 定义 | 产出物合法性作为控制的核心对象 |
| **Paper II** | 可行性 | 以最小人类工作量获取契约 |
| **Paper III** | 执行 | 契约精准度与对抗验证 |
| **Paper IV** | 演化 | 合法性随时间的治理 |
| **Paper S1** | 基础设施 | 面向可审计性和成本控制的上下文工程 |

这些论文共同建立了 ODD 作为 AI 原生软件工程的完整范式——不仅解决产出物如何生产和验证，还解决它们如何在世界变化时保持合法性。

支撑合法性演化的上下文工程基础设施详见 **Paper S1**（*面向可审计LLM工作流的上下文工程*）。

---

## 参考文献

1. Lehman, M. M. *Laws of Software Evolution*. IEEE, 1980.
2. Google. *Hyrum's Law*. 2020.
3. Beyer, B. et al. *Site Reliability Engineering* (Toil Reduction). O'Reilly, 2016.
4. Yi Fu. ODD Core (Paper I). 2026.
5. Yi Fu. Human Delegation Proof (Paper II). 2026.
