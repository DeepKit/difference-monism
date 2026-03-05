# ODD — 输出驱动开发 (Output-Driven Development)

> **定义你要什么，验证你得到了什么，锁住已验证的。**
> Define what you want. Verify what you got. Seal what's proven.

```
人类定义 → AI 执行 → 系统验证 → 封存保护
   ↑                                 │
   └──── 新需求 ←────────────────────┘
```

## 快速开始

- **10 秒了解** → [guide/电梯演讲.md](guide/电梯演讲.md)
- **和 TDD 有什么区别？** → [guide/方法论对比.md](guide/方法论对比.md)
- **30 分钟上手** → [guide/快速上手.md](guide/快速上手.md)
- **看真实案例** → [guide/案例-软件工厂.md](guide/案例-软件工厂.md) · [guide/案例-小说创作.md](guide/案例-小说创作.md)

## 项目结构

```
ODD/
├── ODD-main/       # 完整规格（22 篇，中英双语）
│   └── en/         #   英文版
├── paper/          # 学术论文 + 白皮书
├── guide/          # 上手指南 + 案例 + 推广素材
├── tools/          # CLI 工具
└── _archive/       # 旧版归档
```

## 文档导航

### 📖 想了解 ODD 是什么

| 深度 | 文档 | 时间 |
|------|------|------|
| 入门 | [guide/电梯演讲.md](guide/电梯演讲.md) | 10 秒 |
| 对比 | [guide/方法论对比.md](guide/方法论对比.md) | 5 分钟 |
| 上手 | [guide/快速上手.md](guide/快速上手.md) | 30 分钟 |
| 方法论 | [paper/论文-学术版.md](paper/论文-学术版.md) | 1 小时 |
| 白皮书 | [paper/白皮书.md](paper/白皮书.md) | 2 小时 |
| 完整规格 | [ODD-main/ODD.00索引-索引.md](ODD-main/ODD.00索引-索引.md) | 按需 |

### 🔬 想了解哲学基础

ODD 的哲学根基是 ASTO（属集变迁存在论）。

- **溯源指南** → [guide/哲学溯源.md](guide/哲学溯源.md)（ODD 概念 → ASTO 锚点）
- **完整论文** → [ASTO 论文系列](../ASTO/papers/)

### 🏭 想看参考实现

| 领域 | 项目 | ODD 概念落地 |
|------|------|-------------|
| 软件开发 | Progee | 契约+变异测试+封存+赛马+17层上下文 |
| 小说创作 | kiro-gateway | 乐谱+四层校验+九评委+封版+12层上下文 |

## 引用

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

## 许可

Copyright (c) 2026 Yi Fu (ODDFounder). All rights reserved.
