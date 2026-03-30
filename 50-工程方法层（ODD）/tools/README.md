# ODD CLI 工具

> **状态**: 存根 — 最小可用工具，让人 5 分钟体验 ODD

> **公开边界**：本目录属于 ODD 的工程辅助工具探索，不是当前首轮公开主包，也不应被误读为 ODD 已完成稳定官方 CLI 发布。

---

## 当前定位

- `适用范围`：本地体验、原型工具、工程辅助验证
- `不是什么`：稳定发行版、首轮公开主对象、ODD 理论主文
- `与主包关系`：若对外公开，优先引用 ODD 主论文与白皮书；本目录仅作为补充性工具探索说明

## 目标命令

```bash
odd init          # 生成 outcome spec 模板（YAML）
odd verify        # 跑测试 + 变异测试，输出 mutation score
odd seal          # 打 git tag + 记录 score + 生成 seal record
odd status        # 查看当前项目的 ODD 状态（已封存/待验证/...）
```

## 技术选型（待定）

| 方案 | 优点 | 缺点 |
|------|------|------|
| Python + Click | 生态好，跨平台 | 需装 Python |
| Node + Commander | npm 分发方便 | 需装 Node |
| Go 单二进制 | 零依赖分发 | 开发成本稍高 |
| Shell 脚本 | 零成本启动 | Windows 兼容性差 |

## 最小 MVP

Phase 1: Shell/PowerShell 脚本包装（`odd init` + `odd seal`）
Phase 2: 集成 Stryker/mutmut（`odd verify`）
Phase 3: 独立二进制或 npm 包

## 待办

- [ ] 确定技术选型
- [ ] 实现 `odd init`（生成 outcome-spec.yaml 模板）
- [ ] 实现 `odd seal`（git tag + seal record JSON）
- [ ] 集成至少一个变异测试工具
