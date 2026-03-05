---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.02OBJ]
---

# 产出物分类体系

## 意向
用类型把“作文题”变成“填空题”。
每个任务只生产一个产出物，类型明确就知道该交付什么、怎么测试。

## 规范

### 分类原则
- 每个产出物 MUST 有明确的类型（artifact_type）。
- 类型决定了产出物的结构、必填字段、测试策略。
- 每个任务 MUST 只产出一个产出物（原子化）。

---

## 机制

### L1 · 轻量

**自由命名。** 产出物类型用自然语言描述即可。

常见类型示例：
- `code` — 代码文件
- `test` — 测试文件
- `doc` — 文档
- `config` — 配置文件
- `sql` — 数据库脚本

无强制规范，命名一致就好。

---

### L2 · 标准

**受控类型表。** 项目维护一张类型表，每种类型定义模板。

```yaml
artifact_types:
  pg_function:
    title_template: "创建函数 {name}"
    required_fields: [name, params, return_type]
    test_strategy: pgTAP
  python_module:
    title_template: "实现模块 {name}"
    required_fields: [name, input_spec, output_spec]
    test_strategy: pytest
  api_endpoint:
    title_template: "实现接口 {method} {path}"
    required_fields: [method, path, request_schema, response_schema]
    test_strategy: integration_test
  document:
    title_template: "编写 {name}"
    required_fields: [name, audience]
    test_strategy: review
```

**测试策略自动关联**：类型确定后，测试策略自动填充，无需每次手动指定。

---

### L3 · 严格

**标准库（数据库为真相源）**：在 L2 类型表基础上，每种类型附带完整标准库字段。

标准库字段（建议最小集）：
- input_spec_template / output_spec_template（结构模板）
- side_effects_template（副作用模板）
- implicit_requirements（隐式需求）
- common_knowledge（常识库）
- adversarial_tests（对抗测试向量）
- bug_patterns（历史易错模式）
- best_practices（推荐做法）
- feature_tree_template（功能树模板）
- temporal_defaults（时间维度默认值）
- test_strategy（默认验证策略）

```yaml
artifact_types:
  pg_function:
    # ...L2 字段...
    input_spec_template: { params: [], return_type: "" }
    output_spec_template: { success: {}, error: {} }
    side_effects_template: [db_write]
    implicit_requirements:
      - "必须处理 NULL 输入"
    common_knowledge:
      - "默认事务隔离级别为 read_committed"
    adversarial_tests:
      - "SQL 注入"
    bug_patterns:
      - "未关闭游标"
    best_practices:
      - "使用参数化查询"
    feature_tree_template:
      - "pg_function.validate_input"
    temporal_defaults:
      lifecycle: medium_term
      data_growth: linear
      concurrency: 10-100
    test_strategy: pgTAP
```

**知识注入流程**：
1. 识别 artifact_type → 加载标准库。
2. implicit_requirements → 注入契约验收标准。
3. common_knowledge / best_practices → 注入上下文与生成约束。
4. adversarial_tests / bug_patterns → 注入对抗与测试策略。
5. temporal_defaults → 填充 temporal_config（可一键确认）。

---

## 实践

### 快速选型
- **小项目** → L1，自由命名，保持一致即可。
- **团队项目** → L2，维护类型表，测试策略自动关联。
- **关键系统** → L3，标准库 + 知识自动注入。

### 核心原则
- **一个任务一个产出物**：原子化是蜂巢的基础。
- **类型决定模板**：类型明确后，该交什么、怎么测试都是确定的。
