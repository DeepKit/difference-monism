# Paper II — 人类委托证明

> **英文标题**: Human Delegation Proof: Progressive Trust Transfer from Human Review to Verifiable Mechanisms in AI-Native Software Engineering
> **中文标题**: 人类委托证明：AI 原生软件工程中从人类审查到可验证机制的渐进信任迁移

---

## 元数据

| 字段 | 值 |
|------|------|
| 编号 | Paper II |
| 目标刊/会 | ICSE 2027 或 FSE/ESEC 2027 |
| 级别 | CCF-A |
| 状态 | 📝 提纲阶段 |
| 前置依赖 | Paper I（核心范式） |
| 作者 | Yi Fu |

---

## 核心问题

> 在 AI 辅助开发中，人类如何**证明**自己可以不再写代码、不再审查代码，同时保持问责的可追溯性？

Paper I 建立了"人类是仲裁者而非执行者"的范式。Paper II 回答**如何做到**——通过什么机制，人类可以放心地将执行权委托给 AI？

## 关键素材来源

- Progee: 231 测试全通过、28 bug 由系统审查发现（非人工 Code Review）
- 清晰度评估机制（clarity_detect + clarity_question）
- 诊断优先升级 / 赛马模型（CtrlModelRacing）
- 17 层上下文注入的分级信任策略

## 详细提纲

→ **[提纲.md](提纲.md)**
