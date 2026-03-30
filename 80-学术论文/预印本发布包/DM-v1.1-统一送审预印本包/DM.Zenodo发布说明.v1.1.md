# DM Zenodo 发布说明（v1.1）

> **适用场景**：把 DM 作为 `Zenodo / 预印本 / 征评版` 公开发布时使用。
>
> **当前推荐口径**：`统一送审版 / 征评版 / 预印本`
>
> **不推荐口径**：`最终定稿 / 已完成同行评审 / 闭合成熟理论`
>
> **作者 / Author**：Yi Fu（付毅，ODDFounder，fuyi.it@live.cn）

---

## 1. 推荐发布对象

当前最适合上传的主对象是：

1. [DM.统一送审包.v1.1](./DM.统一送审包.v1.1.md)

若 Zenodo 允许附带补充材料，建议同时附上：

2. [DM.理论定位申明](./DM.理论定位申明.md)
3. [Glossary](./Glossary.md)
4. [DM.全栈术语映射与命名关系表](./DM.全栈术语映射与命名关系表.md)

不建议第一次公开就把全仓库所有层级文档打包为同一个外部对象。

---

## 2. 推荐标题

中文标题建议：

> **《差异一元论（DM）：统一送审版 v1.1》**

英文标题建议：

> **Difference Monism (DM): Unified Send-for-Review Package v1.1**

如果你希望更学术一点，也可用：

> **Difference Monism (DM): A Unified Research Program in Ontology, Mind, Knowledge, and Normativity**

---

## 3. 推荐摘要

中文摘要建议：

> 差异一元论（Difference Monism, DM）是一套以“差异、结构、边界、继承与层级涌现”为统一语法的哲学研究纲领。它试图在不预设实体本体论、心物二元论或终极目的论的前提下，重写存在、时间、规律、因果、意识、认识与规范之间的连续主链。当前版本 `v1.1` 为统一送审版：已形成可连续阅读的主干、明确的失败条件接口与最小外部征评包，但仍处于公开征评、批评吸收与长期验证阶段，不应被表述为最终成熟定稿。

英文摘要建议：

> Difference Monism (DM) is a philosophical research program that uses difference, structure, boundary, inheritance, and layered emergence as a unified grammar across ontology, mind, knowledge, and normativity. It aims to reconstruct the continuity between existence, time, lawfulness, causality, consciousness, cognition, and institutional order without presupposing substance metaphysics, mind-body dualism, or teleological closure. Version `v1.1` is the unified send-for-review edition: it already provides a readable main chain, explicit failure conditions, and a minimal external review package, but it remains a public review edition rather than a finalized, externally validated theory.

---

## 4. 推荐关键词

中文关键词建议：

- 差异一元论
- 结构本体论
- 层级涌现
- 意识哲学
- 认识论
- 规范生成
- 文明韧性

英文关键词建议：

- Difference Monism
- structural ontology
- layered emergence
- philosophy of mind
- epistemology
- normativity
- civilizational resilience

---

## 5. 推荐引用格式

在 DOI 尚未生成前，可先写成：

> Yi Fu. 《差异一元论（DM）：统一送审版 v1.1》. Zenodo, 2026. DOI 待生成.

或：

```bibtex
@misc{dm_zenodo_v11,
  author    = {Yi Fu},
  title     = {Difference Monism (DM): Unified Send-for-Review Package v1.1},
  year      = {2026},
  publisher = {Zenodo},
  note      = {Public review edition; DOI pending}
}
```

生成 DOI 后，把 `note` 改成正式 `doi` 与 `url` 即可。

---

## 6. 版本声明

公开说明建议固定为：

> **DM 当前处于 `v1.1 统一送审版`。它已经适合公开征评、公开比较与预印本式发布，但仍保留开放边界，不应被包装为已经完成同行评审的终局理论。**

---

## 7. 第一次发布的最小纪律

- 只发一个主入口，不要同时抛出多个并列版本。
- 明确写出 `v1.1 统一送审版 / 征评版`。
- 标出这是“研究纲领偏上”的送审型理论包，而不是终局真理。
- 若附带补充材料，优先放定位申明和术语表，不优先放大量内部工作流文档。
- 若同时附 `supplements/`，应按主文已经写明的三域公开引用优先序使用案例：第一层案例可作限定性主论证，第二层/第三层案例不进入公开主引文区。
- 若读者在仓库或补充材料中看到 `RM / Resonance Monism / 共振一元论 / 共扰一元论`，应按早期命名阶段材料理解；当前公开主链以 `DM -> ASTO -> ECET -> TAT -> ODD` 为准。
