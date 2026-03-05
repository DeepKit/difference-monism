# 写作策略：规范可执行化 (Executable Normativity)

**目标期刊**: *IEEE Software / ACM TSE*
**定位**: 模块 E（技术难题攻关）
**核心任务**: 解决“如何把自然语言规范转化为代码约束”的方法论问题。

---

## 1. 核心论点 (The One Thing)
**"Normativity must be compiled into constraints; a specification that is not executable is merely a suggestion."**
（规范性必须被编译为约束；不可执行的规范仅仅是建议。）

## 2. 避坑指南 (Anti-Patterns)
*   **不要** 陷入自然语言处理 (NLP) 的技术细节。
*   **不要** 忽视“人”的因素（解释权）。
*   **ASTO** 不出现。

## 3. 结构大纲 (Structure)
1.  **The Problem**: 需求文档与代码实现的脱节（Drift）。
2.  **The Concept**: "Executable Specification" 的再定义 —— 不仅仅是测试用例，而是治理契约。
3.  **The Method**: 展示一个从 "Policy" 到 "Code Guardrail" 的转换流程。
4.  **The Tooling**: 简要介绍支持工具（如 DSL, Linters, CI/CD Gates）。
5.  **Evaluation**: 效率与合规性的平衡。

## 4. 写作战术 (Tactics)
*   **对话对象**: 软件工程研究者、工具开发者。
*   **语气**: 技术硬核、方法论导向。
*   **关键词**: Traceability, Compliance as Code, DevOps.
