# ODD 论文系列（ODD Paper Series）

> **作者**: Yi Fu (ODDFounder, fuyi.it@live.cn)
> **语言策略**: 中文先行，写好后翻译为英文投稿
> **Paper I 已发布**: [Zenodo DOI: 10.5281/zenodo.18207648](https://doi.org/10.5281/zenodo.18207648)

---

## 系列总览

| 编号 | 标题 | 目标刊/会 | 级别 | 状态 |
|------|------|-----------|------|------|
| **I** | 产出物合法性基础 (Artifact Legitimacy) | ICSE 2027 / TSE | CCF-A | ✅ 初稿完成 |
| **II** | 人类委托证明 (Human Delegation Proof) | ICSE 2027 / FSE 2027 | CCF-A | 📝 提纲 |
| **III** | 契约精度 (Contract Precision) | FSE 2027 / TOSEM | CCF-A | 📝 提纲 |
| **IV** | 合法性演化 (Legitimacy Evolution) | TSE / TOSEM | CCF-A | 📝 提纲 |
| **S1** | 上下文工程 (Context Engineering) | ASE 2027 / ICSE-SEIP | CCF-A | 📝 提纲 |
| **E1** | 实证：一人软件工厂 (Empirical: Software Factory) | ICSE-SEIP / ESEM | — | 📝 提纲 |
| **E2** | 领域迁移：ODD 超越软件 (Domain Adaptation) | ASE 2027 / AAAI 2027 | CCF-A | 📝 提纲 |

---

## 论文间逻辑关系

```
Paper I ─── 核心范式（产出物、契约、变异测试、封存）
  │
  ├── Paper II ─── 人如何退出执行循环？（委托证明）
  │
  ├── Paper III ── 契约如何决定产出质量？（精度度量与对抗）
  │
  ├── Paper IV ── 合法性如何随时间演化？（生命周期治理）
  │
  ├── Paper S1 ── 上下文工程如何支撑规模化？（工程基础设施）
  │
  ├── Paper E1 ── Progee 案例（软件工程实证）
  │
  └── Paper E2 ── kiro-gateway 案例（领域无关性实证）
```

---

## 建议投稿顺序

1. **Paper I** → 打磨格式，投 ICSE 2027 或 TSE（优先）
2. **Paper E1** → 实证数据最充分，可独立投稿
3. **Paper II** → 理论核心延伸，与 Paper I 形成组合拳
4. **Paper III + E2** → 契约精度理论 + 跨领域实证互为支撑
5. **Paper S1** → 工程实践，适合 SEIP track
6. **Paper IV** → 需要更多纵向数据积累

---

## 目录结构

```
paper/
├── README.md                              ← 你在这里
├── 白皮书.md                               (完整技术参考)
├── 论文-学术版.md                           (Paper I 正文)
├── Paper-I_产出物合法性/
├── Paper-II_人类委托证明/
├── Paper-III_契约精度/
├── Paper-IV_合法性演化/
├── Paper-S1_上下文工程/
├── Paper-E1_实证-软件工厂/
└── Paper-E2_领域迁移/
```

---

## 目标顶刊/会议

| 缩写 | 全称 | 级别 | 类型 |
|------|------|------|------|
| ICSE | International Conference on Software Engineering | CCF-A | 会议 |
| FSE/ESEC | Foundations of Software Engineering | CCF-A | 会议 |
| ASE | Automated Software Engineering | CCF-A | 会议 |
| TSE | IEEE Transactions on Software Engineering | CCF-A | 期刊 |
| TOSEM | ACM Trans. on Software Engineering and Methodology | CCF-A | 期刊 |
| ICSE-SEIP | ICSE Software Engineering in Practice | — | Track |
| ESEM | Empirical Software Engineering and Measurement | — | 会议 |
| AAAI | AAAI Conference on Artificial Intelligence | CCF-A | 会议 |
