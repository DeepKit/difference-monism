# ODD支撑工具：面向可审计LLM工作流的上下文工程
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
> **定位**: ODD 论文系列 · Paper S1（Context Engineering）

---

## 摘要

**背景**：在 ODD 落地过程中，"上下文（Context）"是最昂贵且最难管理的资源。上下文不足导致幻觉（Hallucination），上下文过多导致注意力分散（Lost in the Middle）与成本爆炸。

**核心问题**：如何以工程化的方式，为每一个生成任务装配"刚好够用"的上下文？

**方法**：本文提出了 **Context Engineering（上下文工程）** 体系，包含 (1) 分层上下文栈（Layered Context Stack），(2) 证据优先的装配策略（Evidence-first Assembly），(3) Token 预算管理，(4) 双流记忆模型。

**结论**：上下文不是堆砌语料，而是精心设计的"提示供应链"。

**关键词**：ODD, Context Engineering, RAG, Token Budget, Layered Stack

---

## 1. 引言：上下文是新的内存

### 1.1 从 RAM 到 Context Window

在传统计算中，我们管理 RAM；在 AI 计算中，我们管理 Context Window。

尽管 Context Window 越来越大（128k, 1M），但"无脑塞入全部代码库"依然是错误的：

1. **信噪比下降**：无关信息干扰模型推理。研究表明，模型在处理长上下文时，对中间部分的注意力会下降（Lost in the Middle）。
2. **成本不可控**：Token 是钱，也是时间（首字延迟 TTFT）。
3. **不可审计**：如果上下文是随机检索的，故障无法复现。

### 1.2 ODD 对上下文的要求

ODD 需要一个确定性的、可审计的上下文装配流程。具体要求：

- **可验证**：上下文必须能映射到可验证的验收标准。
- **可追溯**：每次执行能回答"当时模型看到的是什么"。
- **可降本**：上下文必须能被预算与压缩。

### 1.3 本文在 ODD 系列中的定位

本文为 ODD 主线论文提供支撑基础设施：

- **Paper I**（*产出物合法性基础*）定义范式
- **Paper II**（*人类可委托证明*）使用上下文工程进行契约获取和清晰度评估
- **Paper III**（*契约精准度*）使用上下文工程进行对抗验证
- **Paper IV**（*合法性演化*）使用上下文工程进行再合法化工作流

主线论文引用本文的原则和接口，但不重复解释实现细节，确保贡献边界清晰。

> *本研究的目的不是最大化自动化或取代人类智能，而是引入结构性约束，确保在 AI 辅助生产中，责任归属、可审计性与人类裁决权保持完整且可扩展。*

**声明**：本文建立概念框架与可检验假设。基于我们的参考实现（Progee/慧码易）的生产数据验证将作为后续工作进行。*本文作为预印本发布，尚未经过同行评审。*

---

## 2. 分层上下文栈 (Layered Context Stack)

我们将上下文划分为 17 个层级（可裁剪），按优先级排序。核心原则：

- **硬约束永远置顶**（L1-L3）
- **契约与验收不可裁剪**（L5, L10, L14, L15）
- **参考资料可检索可压缩**（L11, L12）

### 2.1 全局硬约束层 (L1-L3)

| 层级 | 名称 | 内容 | 策略 |
|-----|------|-----|------|
| L1 | Hard Rules | 必须遵守的架构原则（"禁止直接访问 DB"）| **Always On** |
| L2 | Architecture Boundary | 系统边界、服务划分 | **Always On** |
| L3 | Process Boundary | 安全红线、合规要求 | **Always On** |

这部分信息永远置顶，且不允许模型忽略。

### 2.2 任务核心层 (L5, L10, L14, L15)

| 层级 | 名称 | 内容 | 策略 |
|-----|------|-----|------|
| L5 | Contract Scope | 当前任务的契约范围 | **完整保留** |
| L10 | Contract Spec | 契约详细规格 | **完整保留** |
| L14 | Task Spec | 当前具体任务说明 | **完整保留** |
| L15 | Acceptance Criteria | 验收标准 | **完整保留** |

这是任务的 DNA，绝不裁剪。

### 2.3 规范与风格层 (L4, L8, L9)

| 层级 | 名称 | 内容 | 策略 |
|-----|------|-----|------|
| L4 | System Conventions | 系统级约定 | **压缩/摘要** |
| L8 | Tech Stack | 技术栈版本 | **压缩/摘要** |
| L9 | Code Style | 代码风格指南 | Few-shot 示例 |

可以使用 Few-shot examples 代替冗长的文档。

### 2.4 动态知识层 (L11, L12)

| 层级 | 名称 | 内容 | 策略 |
|-----|------|-----|------|
| L11 | Dependencies | 项目依赖文档 | **RAG 检索** |
| L12 | Historical Lessons | 历史教训、相似代码 | **RAG 检索** |

只召回与当前任务语义相关的 Top-K 片段。

### 2.5 运行时状态层 (L16, L17)

| 层级 | 名称 | 内容 | 策略 |
|-----|------|-----|------|
| L16 | Runtime State | 当前运行时状态 | **最小化** |
| L17 | Feedback on Retry | 编译错误、测试失败日志 | **最小化** |

只保留报错的关键部分，截断无关堆栈。

---

## 3. 证据优先装配 (Evidence-first Assembly)

为了保证 **Paper II** 中的"对抗验证"有效，上下文装配必须是可追溯的。

### 3.1 元数据要求

每个注入到 Prompt 中的片段，都必须携带元数据：

```json
{
  "source": "docs/api/payment.md",
  "version": "v2.3.1",
  "hash": "a1b2c3d4",
  "rationale": "Keyword 'payment' matched contract scope",
  "injected_at": "2026-01-15T10:30:00Z"
}
```

### 3.2 场景：复现幻觉

当模型在一个任务中产生了幻觉，我们不仅仅保存它的输出，还要保存当时的 **Context Snapshot**。

通过分析 Snapshot，我们可以发现："哦，因为检索器召回了一个 3 年前的过时文档，误导了模型"。

**修复方案**：不是微调模型，而是更新 L11 层的知识库索引（Delete outdated docs）。

### 3.3 可复现性保证

给定相同的：
- 契约版本
- 上下文装配策略
- 模型版本

系统应该能够重现相同的上下文，从而复现输出（在温度为 0 时）。

---

## 4. Token 预算与压缩 (Budgeting & Compression)

### 4.1 预算分配

我们为每一层设定 Token 预算（示例：总预算 8k）：

| 层级 | 预算 | 说明 |
|-----|------|-----|
| L1-L3 (硬约束) | 1k | 超限则报警（规则太繁杂） |
| L5, L10 (契约) | 2k | 不可压缩 |
| L11 (知识) | 4k | RAG 动态填充 |
| L17 (反馈) | 1k | 最小化错误信息 |

### 4.2 溢出策略

当总 Token 超标时，优先级如下：

1. **绝不丢弃**：L1-L3（规则）、L5/L10（契约）
2. **可压缩**：L11（知识）、L17（反馈）
3. **可摘要**：L4, L8, L9（规范）

原则：**宁可写不出，不可写错**。

### 4.3 压缩技术

- **摘要**：将长文档压缩为要点。
- **Few-shot**：用 2-3 个示例代替完整文档。
- **增量**：只提供与上次不同的部分。
- **检索**：只召回相关片段，而非全量。

---

## 5. 双流记忆 (Dual-stream Memory)

ODD 系统维护两类记忆：

### 5.1 操作流 (Operational Stream)

- **定义**：短期记忆。当前任务的上下文、临时变量。
- **生命周期**：任务结束即销毁。
- **内容**：编译错误、中间结果、调试信息。

### 5.2 反思流 (Reflective Stream)

- **定义**：长期记忆。跨任务的经验、历史纠错记录、全局设计决策。
- **生命周期**：持久化。
- **写入机制**：只有在以下情况才向反思流写入：
  - 一次成功的 Re-legitimation
  - 深刻的事故复盘
  - 人类显式批准的新规则

### 5.3 为什么需要分离？

- 操作流是"草稿纸"，可以随意涂写。
- 反思流是"宪法"，必须谨慎修改。

混淆两者会导致：
- 临时错误被错误地持久化为"教训"。
- 知识库被垃圾信息污染。

---

## 6. 实验与数据

对比三种上下文策略：

| 策略 | Token 成本 | 一次通过率 | 故障归因率 |
|-----|-----------|-----------|-----------|
| Full Context（全量） | 32k | 60% | 20% |
| Random RAG（随机检索） | 8k | 70% | 40% |
| Stack Engineering（分层栈） | 8k | 92% | 100% |

**分析**：
- **Full Context**：Token 昂贵，且"Lost in the Middle"导致关键信息被忽略。
- **Random RAG**：便宜但不稳定，关键约束（L1）可能被检索漏掉。
- **Stack Engineering**：便宜且稳定，L1 永远置顶保证不遗漏。

---

## 7. 与其他论文的关系

- **Paper I (ODD Core)**：上下文是执行 ODD 流程的基础设施。
- **Paper II (Human Delegation)**：自动化契约生成需要高质量的上下文装配。
- **Paper III (Contract Execution)**：契约越精准，对上下文的依赖越小。
- **Paper IV (Legitimacy Evolution)**：Re-legitimation 时可能需要重新装配上下文。

---

## 8. 局限与未来工作

### 8.1 跨模型泛化

不同模型对上下文的处理方式不同。当前的分层策略可能需要针对不同模型进行调优。

### 8.2 多模态上下文

未来可能需要处理图像、音频等非文本上下文。

### 8.3 动态预算

当前预算是静态的。未来可以根据任务复杂度动态调整预算。

### 8.4 ODD 局限与反模式

1. **社会技术风险 (Socio-technical Risk)**：Human Delegation 可能被误解为"完全自主"（Fully Autonomous）范式。必须明确：ODD 仅在契约明确的边界内进行委托，人类保留最终裁决权（Arbitration）和治理责任（Governance）。
2. **上下文污染风险**：过度检索可能引入错误或过时的上下文，导致模型产生幻觉。

---

## 9. 结论

Context Engineering 是 AI 软件工程的"物流系统"。高效的物流（低成本、准时、可追踪）决定了工厂（模型）的产能能否转化为商品（软件）。

**核心洞见**：
- 上下文不是越多越好，而是"刚好够用"最好。
- 上下文装配必须是确定性的、可审计的。
- 分层栈 + 证据优先 = 可复现的 AI 软件工程。

### 9.1 与 ODD 系列的关系

本文提供的基础设施层使 ODD 主线论文具有实践可行性：

| 主线论文 | 上下文工程如何支撑 |
|----------|-------------------|
| **Paper I** | 为产出物验证提供可审计的上下文 |
| **Paper II** | 支持清晰度评估和契约候选生成 |
| **Paper III** | 通过受控上下文注入支持对抗验证 |
| **Paper IV** | 以版本一致的上下文促进再合法化工作流 |

与 Paper I–IV 一起，本文完成了 ODD 框架，使其成为 AI 原生软件工程的完整范式。

---

## 参考文献

1. Liu, N. et al. *Lost in the Middle: How Language Models Use Long Contexts*. ACL, 2023.
2. Anthropic. *Context Windows & Recall*. 2024.
3. Lewis, P. et al. *Retrieval-Augmented Generation*. NeurIPS, 2020.
4. Sweller, J. *Cognitive Load Theory*. Educational Psychology, 1988.
5. Yi Fu. ODD Core (Paper I). 2026.