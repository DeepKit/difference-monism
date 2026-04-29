# ADD 论文摘要（中英）

**论文题目**：Arbitration-Driven Development: A Governance Framework for Trustworthy AI-Assisted Software Engineering

---

## 中文摘要
随着大语言模型（LLM）在软件工程中的广泛应用，生产力的瓶颈已从“代码生成（Generation）”转移至“代码治理（Governance）”。现有的开发范式（如 TDD、ODD）侧重于描述“如何构建”，却未能有效解决“如何确信”的问题。在 AI 生成代码的速度远超人类审查能力的今天，传统的“人机回环（Human-in-the-loop）”模式正因认知过载而失效。
本文提出了 **Arbitration-Driven Development (ADD，仲裁者驱动开发)**。这是一种独立于生成模型的元治理框架，旨在将工程师的角色从“创作者（Author）”重塑为“仲裁者（Arbiter）”。ADD 建立了以**“责任守恒定律”**为核心的哲学基础，并通过**动态风险分级**、**契约对抗生成机制（CAP）**以及**状态机确权体系**，构建了一个零信任的治理环境。通过在 **Progee** 系统中的参考实现以及一个“积分兑换”功能的英雄之旅案例，我们展示了 ADD 如何通过前置冲突（Engineering Conflict）和分级治理，在不牺牲核心安全性的前提下，驾驭 AI 的无限生产力。

---

## English Abstract
As large language models (LLMs) become widely adopted in software engineering, the primary bottleneck has shifted from *code generation* to *governance and assurance*. Existing methodologies (e.g., TDD, ODD) mainly describe **how to build**, but often leave unresolved the question of **how to trust** what has been built—especially when AI can produce large code changes faster than humans can reliably review.

This paper proposes **Arbitration-Driven Development (ADD)**, a model-agnostic governance framework that redefines the engineer’s role from *author* to **arbiter**. ADD is grounded in a “conservation of accountability” premise: regardless of how much work AI performs, accountability cannot be automated away and must ultimately be assumed by humans. To operationalize this premise, ADD introduces (1) **risk-proportional governance** via L1–L4 grading, (2) a **Contract Adversarial Protocol (CAP)** that engineers conflict before code is produced, and (3) a **state-machine-based authority boundary** centered on sealing/unsealing.

We present a reference implementation in the **Progee** system and a narrative case study (points redemption) to illustrate how ADD surfaces ambiguity early, concentrates human attention on high-impact decisions, and establishes a clear audit trail for responsibility.
