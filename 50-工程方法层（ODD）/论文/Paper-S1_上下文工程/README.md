# Paper S1 — 上下文工程

> **英文标题**: Context Engineering for Output-Driven Development: Layered Assembly, Token Budgets, and Evidence-First Memory
> **中文标题**: 产出物驱动开发的上下文工程：分层组装、Token 预算与证据优先记忆

---

## 元数据

| 字段 | 值 |
|------|------|
| 编号 | Paper S1（支撑论文） |
| 目标刊/会 | ASE 2027 或 ICSE-SEIP 2027 |
| 级别 | CCF-A |
| 状态 | 📝 提纲阶段 |
| 前置依赖 | Paper I |
| 作者 | Yi Fu |

---

## 发布边界

- `当前状态`：Paper S1 仍处于提纲与后续研发阶段，不属于当前 ODD 首轮稳定公开主包
- `适用范围`：路线规划、支撑论文设计、后续投稿准备
- `不是什么`：已经完成正文、可以立即作为正式投稿主对象的声明

---

## 核心问题

> 在 Token 有限、成本敏感的 LLM 环境中，如何**确定性地**为每个任务组装最优上下文？如何保证上下文的可审计性和可复现性？

## 关键素材来源

- Progee: 17 层上下文注入（CtrlContextAssembler + CtrlContextBuilder）
- kiro-gateway: 12 层上下文（从 17 层裁剪：丢弃 4 层，合并 7 组，拆分 2 层）
- 两个系统的 Token 消耗对比数据

## 详细提纲

→ **提纲.md**

