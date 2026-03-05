# odd-hub

> **AI writes code. ODD takes responsibility.**

---

## 一句话定位

**ODD 是一场技术思想运动。**

不是框架。不是工具。是一个关于"谁对软件负责"的根本性重构。

---

## 核心命题

> AI 不会取代程序员。
> 但不会定义契约的程序员会被淘汰。

当 AI 生成代码的成本趋近于零，人类的价值从"执行"转移到"决策与问责"。
软件工程的核心问题不再是"如何写代码"，而是：

- **谁定义了什么算做好？**（契约）
- **谁为结果负责？**（问责）
- **机器如何验证机器的产出？**（验证）

ODD 回答这三个问题。

---

## 战略路径

```
短期：技术思想运动    → 让开发者认同"契约优先"
中期：工程风险控制    → 让团队用 ODD 降低 AI 代码风险
长期：软件生产关系重构 → 重新定义人与 AI 的协作边界
```

---

## 产品矩阵（完整转化链）

```
相信  →  odd-demo      概念验证，5分钟看懂 ODD 是什么
体验  →  ProgeeLite    桌面工具，真实感受 ODD 工作流
使用  →  odd-core      CLI 工具，在真实项目中持续使用
付费  →  WiseLLM Cloud 团队服务，省心用 ODD 并为此付费
```

> WiseLLM 不是附属工具。它是 ODD 的现实放大器。
> 没有 WiseLLM，odd-hub 只是方法论仓库。

---

## 实证数据

- 172 个任务对照实验
- 缺陷率降低 **59.5%**（p=0.029）
- 代码审查负荷降低 **40%**

---

## 目录结构

```
odd-hub/
├── docs/
│   └── 产品愿景.md
├── odd-demo/                ← 概念验证（Python）
│   ├── docs/                ← 三套受众文档 + 社交媒体文案 + 验证报告
│   └── papers/              ← 学术论文 + 白皮书
├── odd-core/                ← CLI 工具（Python，MIT 开源）
│   ├── src/odd/
│   ├── templates/           ← 内置契约模板（15个）
│   └── tests/
└── assets/                  ← Logo、截图、品牌资源
```

---

## 推广材料

面向三类受众：

- [开发者版](odd-demo/docs/demo-explained-for-developers_CN.md) — "从砌砖工人到建筑监理"
- [管理者版](odd-demo/docs/demo-explained-for-managers_CN.md) — 效率提升 36-72 倍 + 风险可控
- [决策者版](odd-demo/docs/demo-explained-for-executives_CN.md) — 生产关系重构 + 合规价值
- [社交媒体文案](odd-demo/docs/SOCIAL_MEDIA_POSTS.md)
- [概念验证报告](odd-demo/docs/ODD_Validation_Report.md)

---

## 相关项目

| 项目 | 说明 |
|------|------|
| [ODD 方法论](../../01Center/ODD/ODD-main/docs/) | 理论体系（A01-E25） |
| [ProgeeLite](../progeeLite/) | Delphi 桌面验证工具 |
| [WiseLLM](../WiseLLM/) | LLM API 中台，ODD 现实放大器 |
| [BetterCiv](../../01Center/BetterCiv/) | 三大理论统一对外门户 |

---

## 许可证

- ODD 方法论：免费开放
- odd-core：MIT License
- WiseLLM Cloud：商业服务
