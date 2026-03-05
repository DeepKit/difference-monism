---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.07ART]
---

# Bug 意向图与最佳实践

## 意向
功能树告诉你"做什么"，Bug 意向图告诉你"别踩什么坑"，最佳实践告诉你"怎么做最好"。
三者合称**三大法宝**（功能树 + Bug 意向图 + 最佳实践），在契约生成和代码生成阶段自动注入上下文，把隐式知识变成显式约束。

## 规范

### 三大法宝原则
- 每种产出物类型（artifact_type）SHOULD 关联自己的 Bug 意向图和最佳实践。
- 三大法宝的内容 MUST 作为隐式需求注入契约和任务上下文（详见 ODD.05CTX-上下文工程）。
- Bug 意向图和最佳实践 SHOULD 持续从执行历史中学习和更新，不是静态配置。

### 注入时机
- **契约生成阶段**：Bug 意向图 → 验收条件补充；最佳实践 → 契约约束指导。
- **代码生成阶段**：Bug 意向图 → 对抗测试向量；最佳实践 → 代码生成指导。
- **测试阶段**：Bug 意向图 → 经验库攻击（按历史频率排序）。

---

## 机制

### L1 · 轻量

**手动维护。** 在项目文档或笔记中记录常见坑和推荐做法，开发前人工浏览。

常见坑清单示例：
- 密码明文存储
- 未处理 NULL 输入
- 未考虑并发冲突
- 错误信息泄露内部细节

推荐做法清单示例：
- 密码用 bcrypt/argon2 加密
- 所有输入做边界校验
- 数据库操作做事务保护
- 错误信息统一格式，不暴露堆栈

无自动注入，靠人工记忆和纪律。

---

### L2 · 标准

**结构化存储 + 按类型自动注入。**

#### Bug 意向图

每种产出物类型维护一张 Bug 意向图（Bug Intention Map），记录该类型的历史易错模式。

结构：
```yaml
bug_patterns:
  - id: BP-001
    pattern: "密码明文存储"            # 模式名称
    detection_rule: "stored_password == hash(input_password, salt)"  # 形式化检测规则
    severity: critical                  # 严重性：critical / high / medium / low
    frequency: 127                      # 历史发现次数
    prevention: "使用 bcrypt 或 argon2"  # 预防措施
  - id: BP-002
    pattern: "无登录失败计数"
    detection_rule: "login_attempts >= 5 IMPLIES account_locked == true"
    severity: high
    frequency: 89
    prevention: "实现失败计数 + 账户锁定"
```

注入方式：创建任务时，系统根据 artifact_type 查询对应的 bug_patterns，自动注入到任务上下文的"对抗测试"和"验收条件"中。

#### 最佳实践

每种产出物类型维护一组最佳实践（Best Practices）。

结构：
```yaml
best_practices:
  - id: PR-001
    practice: "使用参数化查询"          # 推荐做法
    rationale: "防止 SQL 注入"          # 原因
    anti_pattern: "字符串拼接 SQL"      # 对应的反模式
    priority: 9                         # 优先级 1-10
    is_mandatory: true                  # 是否强制
  - id: PR-002
    practice: "SECURITY DEFINER 需要固定 search_path"
    rationale: "防止搜索路径注入攻击"
    anti_pattern: "省略 search_path 设置"
    priority: 8
    is_mandatory: true
```

注入方式：代码生成前，系统查询对应的 best_practices，`is_mandatory: true` 的强制注入，其余按 priority 排序注入（受 token 预算裁剪）。

#### 产出物类型标准示例

将三大法宝关联到产出物类型（参考 ODD.07ART-产出物分类体系 L3）：

```yaml
artifact_types:
  auth_login:
    # 功能树模板（见 ODD.0B功树-功能树）
    feature_tree_template:
      - auth_login.validate_input
      - auth_login.check_credentials
      - auth_login.generate_token
      - auth_login.record_audit
      - auth_login.handle_failure

    # Bug 意向图
    bug_patterns:
      - {pattern: "密码明文存储", severity: critical, frequency: 127}
      - {pattern: "无登录失败计数", severity: high, frequency: 89}
      - {pattern: "Token无过期时间", severity: high, frequency: 76}
      - {pattern: "错误信息泄露用户存在", severity: medium, frequency: 234}

    # 最佳实践
    best_practices:
      - {practice: "bcrypt/argon2 加密密码", rationale: "抗彩虹表", mandatory: true}
      - {practice: "登录失败延迟响应", rationale: "防时序攻击", mandatory: false}
      - {practice: "Token 用 JWT 或安全随机数", rationale: "防伪造", mandatory: true}

    # 隐式需求（自动注入契约验收标准）
    implicit_requirements:
      - "密码必须加密存储"
      - "防止暴力破解"
      - "记录登录审计日志"
      - "处理网络超时"

  api_endpoint:
    feature_tree_template:
      - api.validate_request
      - api.authorize
      - api.execute_logic
      - api.format_response
      - api.handle_error

    bug_patterns:
      - {pattern: "SQL 注入", severity: critical, frequency: 312}
      - {pattern: "未验证输入长度/类型", severity: high, frequency: 267}
      - {pattern: "无认证/鉴权检查", severity: critical, frequency: 198}
      - {pattern: "错误响应泄露内部堆栈", severity: medium, frequency: 156}
      - {pattern: "无限流导致 DDoS", severity: high, frequency: 91}
      - {pattern: "返回数据未脱敏", severity: high, frequency: 134}

    best_practices:
      - {practice: "参数化查询", rationale: "防 SQL 注入", mandatory: true}
      - {practice: "统一错误响应格式 {code, message, request_id}", rationale: "可追踪 + 不泄露内部", mandatory: true}
      - {practice: "请求速率限制", rationale: "防滥用", mandatory: false}
      - {practice: "响应字段白名单（不返回未声明字段）", rationale: "防数据泄露", mandatory: true}

    implicit_requirements:
      - "输入必须校验类型和范围"
      - "返回统一错误格式"
      - "记录访问日志"
      - "处理超时和服务不可用"

  db_migration:
    feature_tree_template:
      - migration.validate_schema
      - migration.apply_changes
      - migration.verify_data
      - migration.rollback

    bug_patterns:
      - {pattern: "无回滚脚本", severity: critical, frequency: 203}
      - {pattern: "键删列未备份数据", severity: critical, frequency: 87}
      - {pattern: "迁移顺序依赖异常", severity: high, frequency: 156}
      - {pattern: "大表 ALTER 锁表导致停机", severity: critical, frequency: 67}
      - {pattern: "NOT NULL 新列未设默认值", severity: high, frequency: 189}
      - {pattern: "索引缺失导致慢查询", severity: medium, frequency: 245}

    best_practices:
      - {practice: "每次迁移必须配对回滚脚本", rationale: "可恢复性", mandatory: true}
      - {practice: "先加列后删列（两步迁移）", rationale: "避免破坏性变更", mandatory: false}
      - {practice: "大表用 pt-online-schema-change / pg_repack", rationale: "避免锁表", mandatory: true}
      - {practice: "迁移前备份受影响的表", rationale: "数据安全网", mandatory: true}

    implicit_requirements:
      - "必须有回滚方案"
      - "不得在高峰期执行"
      - "迁移前后数据完整性校验"
      - "记录迁移耗时和影响行数"

  config_file:
    feature_tree_template:
      - config.load
      - config.validate_schema
      - config.apply
      - config.hot_reload

    bug_patterns:
      - {pattern: "密钥/密码硬编码", severity: critical, frequency: 278}
      - {pattern: "无模式校验，拼写错误静默失败", severity: high, frequency: 312}
      - {pattern: "环境差异未处理（dev/staging/prod 配置混用）", severity: high, frequency: 167}
      - {pattern: "配置变更未重启服务（缓存旧值）", severity: medium, frequency: 198}
      - {pattern: "缺少默认值导致启动崩溃", severity: high, frequency: 145}

    best_practices:
      - {practice: "敏感信息从环境变量/密钥管理器读取", rationale: "不入库", mandatory: true}
      - {practice: "配置文件必须有 JSON Schema / YAML Schema 校验", rationale: "早期发现错误", mandatory: true}
      - {practice: "每个字段有默认值或标记 required", rationale: "防缺失崩溃", mandatory: false}
      - {practice: "配置变更记录审计日志", rationale: "可追溯", mandatory: false}

    implicit_requirements:
      - "不得包含明文密钥"
      - "必须有模式校验"
      - "支持多环境覆盖"
      - "变更后有生效机制说明"
```

---

### L3 · 严格

**在 L2 基础上增加：自动学习 + 双流沉淀 + 度量闭环。**

#### Bug 意向图的学习循环

Bug 意向图不是静态配置，而是从执行历史中持续学习：

```
返工发生 → 提取失败原因 → 匹配已有模式？
  ├── 是 → frequency +1，更新 severity
  └── 否 → 创建新模式，标记 source_task_id
           ↓
新模式积累 → 达到阈值 → 晋升为标准库模式
           ↓
下次同类型任务 → 自动注入新模式 → 预防同类错误
```

学习来源：
- **返工记录**：任务失败后自动提取 Bug 模式（语义记忆沉淀）。
- **对抗测试结果**：攻击成功的向量自动加入 Bug 意向图。
- **人类反馈**：人类在审查中标记的问题。

#### 最佳实践的学习循环

```
任务成功封存 → 提取代码模式 → 评估可复用性
  ├── 高复用性 → 创建最佳实践条目
  └── 低复用性 → 存入车间知识库（不升级为标准）
```

#### 反模式库

与最佳实践对应，维护一组反模式（Anti-Patterns），每个反模式 SHOULD 包含：

```yaml
anti_patterns:
  - id: AP-001
    name: "契约定义模糊"
    symptoms:                           # 症状
      - "契约只有一句话描述"
      - "没有明确验收标准"
      - "ES/NES 混为一谈"
    consequences:                       # 后果
      - "AI 生成不符预期"
      - "反复返工"
      - "无法封存"
    solutions:                          # 解决方案
      - "使用契约模板"
      - "强制验收标准 >= 3 个边界用例 + 1 个错误用例"
      - "必须经过 CAP 验证"
  - id: AP-002
    name: "车间隔离不当"
    symptoms:
      - "车间共享数据库连接"
      - "一个车间崩溃影响其他车间"
    consequences:
      - "故障扩散"
      - "无法热启动"
    solutions:
      - "每个车间独立连接"
      - "故障隔离机制"
  - id: AP-003
    name: "NES 伪装成 ES"
    symptoms:
      - "用工具检测「代码质量」"
      - "指标绿了但实际有问题"
    consequences:
      - "虚假安全感"
      - "质量失控"
    solutions:
      - "明确 ES/NES 边界"
      - "工具只检测可客观判定的事项"
      - "人工审查 NES 项"
```

#### 度量指标

**过程指标**：
- 契约定义时间：目标 < 2 天（从 Draft 到 Ready）
- 返工率：目标 < 10%（验证失败次数 / 总任务数）
- 封存时间：目标 < 1 周（从 Ready 到 Sealed）
- 车间利用率：目标 70–90%（活跃车间 / 总车间数）

**结果指标**：
- 生产缺陷率：目标 < 5%（生产环境 bug / 功能点数）
- 技术债增速：目标线性（维护成本占比）
- 知识复用率：目标 > 70%（热启动复用知识占比）
- Bug 意向图命中率：目标 > 60%（预防的 bug / 实际发现的 bug）

---

## 实践

### 快速选型
- **小项目** → L1，手动维护常见坑和推荐做法清单。
- **团队项目** → L2，结构化存储 + 按 artifact_type 自动注入。
- **关键系统** → L3，自动学习 + 反模式库 + 度量闭环。

### 核心原则
- **历史即教训**：Bug 意向图是前人踩过的坑，必须注入上下文让执行者绕开。
- **实践即捷径**：最佳实践是验证过的路，复用优于从零开始。
- **三大法宝协同**：功能树定位"在哪"，Bug 意向图防"踩坑"，最佳实践指"怎么做"——缺一不可。
- **学习闭环**：静态配置会过时，从执行历史中持续学习才是长期价值。
