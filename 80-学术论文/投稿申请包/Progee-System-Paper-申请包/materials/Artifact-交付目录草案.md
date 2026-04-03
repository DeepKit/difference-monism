# Progee Artifact 交付目录草案

## 作用

本文件把 `Progee` 的 supplement / artifact 从“有个最小运行模板”推进为“可对外打包的目录骨架”。

## 建议对外交付目录

```text
artifact/
  README.md
  RUN.md
  ENVIRONMENT.md
  outputs/
    dunitx-results.xml
    eval/
  appendices/
    结果与主张映射表.md
    审稿人最小复核路径.md
    附录与实现锚点表.md
```

## 每部分最少应放什么

| 目录或文件 | 最低内容 | 当前对应入口 |
| --- | --- | --- |
| `README.md` | artifact 身份、主张边界、运行前提、输出物总览 | `Artifact-最小执行模板.md` |
| `RUN.md` | 最小执行步骤、命令、失败时先看什么 | `审稿人最小复核路径.md` |
| `ENVIRONMENT.md` | Windows、PowerShell、PostgreSQL test DB、安全保险丝 | `Artifact-最小执行模板.md` |
| `outputs/dunitx-results.xml` | 最小可核输出物 | `bin/dunitx-results.xml` |
| `outputs/eval/` | 可选表图导出 `csv` | `eval/*.csv` |
| `appendices/` | 主张-证据-实现锚点的补充说明 | 本目录下三份补充文档 |

## 当前默认打包原则

1. 只交付最小可复现路径，不把整仓直接压进投稿包。
2. 只支撑“状态机治理、证据优先持久化、最小复现评估路径”三项主张。
3. 输出物优先选 `XML / CSV / 说明文档`，避免把 artifact 写成宣传册。
4. 正式 venue 未锁定前，附件文件名尽量保持中性，避免过早绑定会务体例。
