# B01: 10分钟从零到CRUD API (演示视频脚本)

> **类型**: 视频脚本
> **时长**: 约10分钟
> **目标受众**: 开发者、技术决策者

---

## 视频概述

本视频演示如何使用 ODD 方法论和 Progee 工具，在 10 分钟内从零开始构建一个完整的 CRUD API，包括数据库、后端接口和测试。

---

## 0:00 - 0:30 [开场]

**(画面)**: 代码编辑器，传统开发场景
**(旁白)**: "传统开发一个 CRUD API 需要多久？创建数据库表、写模型、写路由、写验证、写测试... 少说也要半天。"

**(画面)**: 切换到 Progee 界面
**(旁白)**: "今天，我用 ODD 方法论，10 分钟搞定。"

---

## 0:30 - 2:00 [第一步：Define 定义产出物]

**(画面)**: 打开契约编辑器
**(旁白)**: "ODD 的第一步是 Define——定义你要什么，而不是怎么做。"

**(操作)**: 输入契约定义
```yaml
task: 用户管理 CRUD API
artifacts:
  - type: pg_table
    name: users
    columns: [id, email, name, created_at]
  - type: fastapi_router
    name: user_router
    endpoints: [create, read, update, delete, list]
  - type: pytest_unit
    name: test_user_api
```

**(旁白)**: "看，我只定义了'要什么'——一张表、一组接口、一套测试。具体怎么实现？交给 AI。"

---

## 2:00 - 3:30 [第二步：Decompose 任务分解]

**(画面)**: Progee 自动分解任务
**(旁白)**: "Progee 自动把大任务分解成小任务，每个任务都有明确的输入输出。"

**(展示)**: 任务树
```
用户管理 CRUD API
├── 1. 创建 users 表 (pg_table)
├── 2. 创建 User 模型 (pydantic_model)
├── 3. 创建 CRUD 函数 (python_module)
├── 4. 创建 API 路由 (fastapi_router)
└── 5. 创建单元测试 (pytest_unit)
```

---

## 3:30 - 6:00 [第三步：Execute 执行生成]

**(画面)**: AI 开始生成代码
**(旁白)**: "现在 AI 开始工作。注意，它不是随便生成，而是严格按照契约来。"

**(展示)**: 生成的代码片段
- 数据库迁移脚本
- Pydantic 模型
- CRUD 函数
- FastAPI 路由

**(旁白)**: "每一行代码都有据可查，都能追溯到契约定义。"

---

## 6:00 - 8:00 [第四步：Verify 验证]

**(画面)**: 运行测试
**(旁白)**: "生成完不算完，还要验证。ODD 的核心是'可验证的产出物'。"

**(操作)**: 运行 pytest
```bash
pytest tests/test_user_api.py -v
# 5 passed in 0.8s
```

**(旁白)**: "5 个测试全部通过。这不是巧合，是契约保证的。"

---

## 8:00 - 9:30 [第五步：Seal 封版]

**(画面)**: 提交代码
**(旁白)**: "最后一步，Seal——封版。代码、契约、测试结果，全部归档。"

**(展示)**: 生成的文档
- API 文档 (自动生成)
- 契约记录
- 测试报告

---

## 9:30 - 10:00 [总结]

**(画面)**: 回顾整个流程
**(旁白)**: "10 分钟，从零到一个完整的 CRUD API。这就是 ODD 的力量——不写代码，只定义产出物。"

**(画面)**: Progee Logo
**(字幕)**: "Progee: Don't code. Define."
**(字幕)**: "访问 oddfounder.com 了解更多"

---

## 附录：视频制作清单

- [ ] 录制 Progee 操作画面
- [ ] 准备代码高亮动画
- [ ] 录制旁白
- [ ] 添加字幕
- [ ] 背景音乐
- [ ] 片头片尾动画

---

> **ODD Series | Week 34 . Friday | 40 Weeks Total**
> Previous: "方法论-B03"
> Next: "方法论-B05"
