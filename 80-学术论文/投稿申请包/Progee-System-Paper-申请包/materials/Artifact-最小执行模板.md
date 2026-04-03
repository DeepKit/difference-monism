# Progee Artifact 最小执行模板

## 1. Artifact 身份

- 论文：`Progee v2`
- 类型：系统 / 工具论文最小复现附件
- 目标：支撑“状态机治理 + 证据优先持久化 + 最小可复现评估路径”三项主张

## 2. 仓库与入口

- 代码主位：`<repo-root>/`
- 复现指南：`docs/Replication.md`
- E2E 脚本：`scripts/run_e2e_tests.ps1`
- 表图导出脚本：`scripts/export_eval_metrics.ps1`

## 3. 最小运行前提

1. Windows + PowerShell
2. 已构建 `bin\ProgeeTests.exe`
3. PostgreSQL test database
4. 已设置测试环境变量，尤其是：
   - `PROGEE_ALLOW_DESTRUCTIVE_TESTS=1`
   - `PROGEE_TEST_DB_NAME` 含 `_test`
   - `PROGEE_TEST_DB_PASSWORD`

## 4. 最小执行步骤

1. 准备测试数据库与账户。
2. 在当前 shell 中设置环境变量。
3. 运行：

```powershell
.\scripts\run_e2e_tests.ps1
```

4. 如需表格 / 图的数据，再运行：

```powershell
.\scripts\export_eval_metrics.ps1
```

## 5. 预期输出

最小输出：

- `bin/dunitx-results.xml`

可选输出：

- `eval/evidence_counts.csv`
- `eval/tasks_rework_distribution.csv`
- 其他 `eval/*.csv`

## 6. 审稿人最该核什么

1. 脚本是否真的能把主张绑定到可检查输出物。
2. 输出物是否与论文中的评估叙述一致。
3. 边界说明是否诚实写明 destructive tests 与环境前提。

## 7. 不应误写的地方

- 不把“可复现路径存在”写成“外部有效性已经闭合”。
- 不把“最小路径可运行”写成“整仓全部路径都稳定复现”。
- 不把 artifact 附件写成性能宣传材料。
