---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.02OBJ]
---

# 契约对抗生成（CAP）

## 意向
契约写得不好，后面全部白做。
契约生效前必须经过两道关：**清晰度评估**（找出模糊点）和 **对抗生成**（找出漏洞和边界缺失）。

## 规范

### 契约的常见缺陷
- **歧义**："高性能"到底是多快？
- **不完备**：没考虑并发、没考虑空值、没考虑失败场景。
- **恶意合规**：字面上满足契约，实际违背意图（AI 尤其擅长这个）。

### 清晰度评估原则
- 契约草案 MUST 先通过清晰度评估，再进入对抗。
- 模糊项 MUST 分级：🟢清晰 / 🟡有点模糊 / 🔴很模糊。
- 🔴项 MUST 由人类回答后才能继续；🟡项 SHOULD 补充但可忽略。
- 给人类做**选择题**，不做填空题。

### 对抗原则
- 对抗 MUST 在契约生效前完成。
- 对抗过程 MUST 留下记录（pk_history），作为契约证据的一部分。

### 边界声明
每份契约 SHOULD 包含两类边界声明：
- **地板（Floor）**：契约必须满足的最低条件，缺失则系统不可用。
- **红线（Red Line）**：绝不可违反的约束，触碰则立即终止。

地板和红线 MUST 在清晰度评估阶段识别；涉及安全或数据完整性的边界 MUST 标记为红线。

### 攻击策略库
对抗方 SHOULD 从以下三类攻击角度发起挑战：

**逻辑漏洞类**：
- 前置条件和后置条件之间是否有逻辑断层？
- 是否存在一种输入，使得无法满足任何后置条件？
- 约束之间是否有互相矛盾的情况？

**边界条件类**：
- 空值、空串、超长串、特殊字符是否都定义了行为？
- 最大值、最小值、溢出值是否定义了行为？
- 并发、超时、幂等是否有明确约束？

**恶意实现类（精灵效应）**：
- 能否构造一个"偷懒"实现——通过所有验收标准但完全没用？
- 能否构造一个"危险"实现——符合契约但导致数据泄露？
- 能否构造一个"空壳"实现——返回硬编码值通过测试？

---

## 机制

### L1 · 轻量

**清晰度**：自查。写完契约后过一遍检查清单：
- 有没有使用模糊词（"大量""尽快""适当""合理"）？
- 验收条件是否可测试（能写出具体的测试用例）？
- 边界情况是否覆盖（空值、极大值、并发）？
- 有没有"字面合规但不对"的实现方式？
- 地板条件和红线是否声明？

**对抗**：无正式 CAP。自查即可。

---

### L2 · 标准

**清晰度**：系统自动评估 + 人类确认。

模糊类型检测：
- **表达模糊**：命中模糊词列表（规则匹配，低算力）-> 记 1 项。
- **边界缺失**：输入/输出范围、异常处理、幂等/回滚未定义（AI 分析，中算力）-> 记 1 项。
- **依赖缺失**：引用未封存的契约/未定义的外部接口/未定义表结构 -> 记 1 项。
- **逻辑冲突**：前后矛盾、验收标准与描述冲突（**关键项**）-> 记 2 项。
- **安全模糊**：权限/密码/支付/审计未定义策略（**关键项**）-> 记 2 项。

**模糊词检测列表**：
```
数量类: 大量、少量、适当、足够、一些
程度类: 尽快、尽量、合理、适度
范围类: 等等、之类、相关、其他
条件类: 必要时、如果需要、视情况
```

**评分规则**：
- 🟢清晰：0 项模糊。
- 🟡有点模糊：1-2 项且不含关键项。
- 🔴很模糊：>=3 项，或命中关键项（逻辑冲突/安全模糊）。

**评分输出字段**（clarity_detect）：
```yaml
clarity_detect:
  overall: clear | slightly_unclear | very_unclear
  score: 0-5                       # 模糊项累计分
  action: pass | suggest | must_answer
  issues:
    - type: string                 # 模糊类型
      description: string
      severity: green | yellow | red
```

🔴项 MUST 以选择题形式呈现给人类（AI 推荐选项 + 自定义兜底）。

**选择题设计原则**：
- 选择题优先，填空题兜底。人类做选择而非从零定义。
- 每题 SHOULD 包含 3 个 AI 推荐选项 + 1 个"其他"自定义选项。
- AI 根据上下文标记推荐项。

选项生成规则：
| 场景 | 选项来源 |
|------|----------|
| 数值类 | AI 推荐 3 个常见值 + 自定义 |
| 是非类 | 是 / 否 / 视情况 |
| 处理方式 | 拒绝 / 允许 / 警告 / 自定义 |
| 业务逻辑 | 从对话历史提取可能选项 |

**对抗**：另一个人（或 AI）审查契约，SHOULD 从攻击策略库三类角度发起检查。

审查结果记录：
```yaml
clarity:
  overall: clear | slightly_unclear | very_unclear
  issues: [{type, description, severity}]
  human_answers: [{issue_id, choice}]
review:
  reviewer: string
  attack_vectors_checked: [logic | boundary | malicious]
  issues_found: [string]
  resolved: bool
```

---

### L3 · 严格

**清晰度**：在 L2 基础上增加**双 AI 对抗检测**——两个 AI（或同模型不同 prompt）分别找模糊点，取严格者，差异项追加为必须澄清。命中关键项时切换不同模型对抗。

**对抗：完整 CAP（Contract Adversarial Protocol）——多角色对抗循环。**

**角色**（可映射到军帐五角色或独立分配）：
- **Proposer（提案者）**：将人类意图转化为契约草案，并根据攻击修复。
- **Challenger（挑战者）**：从逻辑漏洞和边界条件角度攻击。
- **Attacker（攻击者）**：从恶意实现角度攻击——构造字面合规但违背意图的实现。
- **Arbiter（裁决者）**：判断攻击是否有效，决定继续 PK 还是通过/升级人类。

**流程**：
```
人类意图 → Proposer 出草案 V1
  ↓
Challenger + Attacker 攻击 V1
  ↓
漏洞存在？ → Yes → Proposer 修复 → V2 → 再攻击（循环）
  ↓ No
Arbiter 最终审查 → 通过 → 人类确认
```
- MUST 有最大回合数（建议 3 轮）。
- 超限未收敛 MUST 升级人类裁决，标注争议点。

**证据沉淀**：
```yaml
pk_history:
  - round: 1
    attacker: Challenger
    attack_vector: boundary
    issue: "未定义并发场景下的行为"
    fix: "增加并发边界用例，定义锁策略"
    verdict: pass
  - round: 2
    attacker: Attacker
    attack_vector: malicious
    issue: "可以返回空数据来'通过'验收"
    fix: "验收条件增加最小数据量要求"
    verdict: pass
  - round: 3
    attacker: Challenger
    attack_vector: logic
    issue: "前置条件与后置条件存在逻辑断层"
    fix: "补充中间状态约束"
    verdict: pass
```

pk_history 作为契约证据的一部分，参与封存和审计。

---

### 完整对抗对话示例

以下 3 个示例展示 CAP 在不同场景下的实际运作。

#### 示例 1：用户注册 API（逻辑漏洞攻击）

**人类意图**："用户注册接口，接受邮箱和密码，创建账户。"

```
[Proposer] 契约草案 V1：
  title: 用户注册
  acceptance_criteria:
    - given: 有效邮箱和密码
      when: POST /register {email, password}
      then: 返回 201 + user_id
    - given: 邮箱已注册
      when: POST /register {email, password}
      then: 返回 409 Conflict
  floor: 注册成功后可登录
  red_line: 密码不得明文存储

[Challenger] 攻击（逻辑漏洞）：
  "密码强度没有任何约束。用户可以用空密码或 '1' 注册。
   这不违反契约，但违背安全意图。"

[Arbiter] 裁决：攻击有效。密码约束是安全基线。

[Proposer] 修复 → V2：
  + boundary_cases:
    - "密码长度 < 8 → 返回 400，提示 'password too short'"
    - "密码长度 > 128 → 返回 400，提示 'password too long'"
  + acceptance_criteria:
    - given: 密码为空
      when: POST /register {email, password: ""}
      then: 返回 400

[Attacker] 攻击（恶意实现）：
  "我可以用 MD5 存密码，技术上不是'明文'，但极不安全。
   红线只说'不得明文存储'，没说用什么算法。"

[Arbiter] 裁决：攻击有效。红线需要更精确。

[Proposer] 修复 → V3：
  red_line: "密码 MUST 使用 bcrypt/argon2/scrypt 存储，不得使用 MD5/SHA1/SHA256"

[Arbiter] 最终审查：V3 通过。提交人类确认。
```

pk_history 记录：
```yaml
pk_history:
  - round: 1
    attacker: Challenger
    attack_vector: logic
    issue: "无密码强度约束，空密码可注册"
    fix: "增加密码长度验证 8-128 + 空密码边界"
    verdict: pass
  - round: 2
    attacker: Attacker
    attack_vector: malicious
    issue: "MD5 不算明文但不安全，红线定义不精确"
    fix: "红线明确 MUST bcrypt/argon2/scrypt"
    verdict: pass
```

#### 示例 2：订单金额计算（边界条件攻击）

**人类意图**："计算订单总金额，含折扣和税。"

```
[Proposer] 契约草案 V1：
  title: 订单金额计算
  acceptance_criteria:
    - given: 商品 100 元，折扣 10%，税率 13%
      when: calculate_total(100, 0.1, 0.13)
      then: 返回 101.70
  floor: 计算结果精确到分
  red_line: 金额不得为负

[Challenger] 攻击（边界条件）：
  "1. 折扣 > 100% 会怎样？折扣 = 1.5 意味着倒贴钱？
   2. 商品价格 = 0 呢？
   3. 浮点精度：0.1 + 0.2 ≠ 0.3，怎么处理？"

[Arbiter] 裁决：三个攻击均有效。

[Proposer] 修复 → V2：
  + boundary_cases:
    - "折扣范围 [0, 1.0]，超出 → ValueError"
    - "价格 = 0 → 返回 0.00"
    - "价格 < 0 → ValueError"
  + acceptance_criteria:
    - given: 浮点精度
      when: calculate_total(0.1, 0, 0)
      then: 返回 0.10（Decimal 运算，非 float）
  + 规范补充: "内部使用 Decimal 类型，避免浮点误差"

[Attacker] 攻击（恶意实现）：
  "我可以把所有金额都返回 0.00，
   因为 floor 只说'精确到分'，0.00 精确到分了。"

[Arbiter] 裁决：攻击有效。floor 需要和验收条件联动。

[Proposer] 修复 → V3：
  floor: "所有 acceptance_criteria MUST 通过 + 计算结果精确到分"

[Arbiter] 最终审查：V3 通过。提交人类确认。
```

pk_history 记录：
```yaml
pk_history:
  - round: 1
    attacker: Challenger
    attack_vector: boundary
    issue: "折扣范围/零价格/浮点精度均未定义"
    fix: "限制折扣 [0,1.0]，零价格返回 0.00，改用 Decimal"
    verdict: pass
  - round: 2
    attacker: Attacker
    attack_vector: malicious
    issue: "全返回 0.00 满足 floor '精确到分'"
    fix: "floor 与 acceptance_criteria 联动"
    verdict: pass
```

#### 示例 3：文件导出（精灵效应攻击）

**人类意图**："把用户列表导出为 CSV 文件。"

```
[Proposer] 契约草案 V1：
  title: 用户列表 CSV 导出
  acceptance_criteria:
    - given: 3 个用户
      when: export_csv(users)
      then: 生成包含 3 行数据的 CSV 文件
    - given: 0 个用户
      when: export_csv([])
      then: 生成只有表头的 CSV 文件
  floor: 文件可被 Excel 正确打开
  red_line: 不得导出密码字段

[Attacker] 攻击（精灵效应）：
  "我可以生成一个 3 行的 CSV，每行只写 'data,data,data'。
   满足 '3 行数据'，但内容完全无意义。"

[Arbiter] 裁决：攻击有效。验收条件只验行数，不验内容。

[Proposer] 修复 → V2：
  acceptance_criteria 修改:
    - given: 用户 [{name: "张三", email: "z@test.com"}]
      when: export_csv(users)
      then: |
        CSV 包含表头行: name,email,created_at
        数据行包含: 张三,z@test.com,<TIMESTAMP>
  + boundary_cases:
    - "用户名含逗号 → 字段用双引号包裹"
    - "用户名含双引号 → 双引号转义"
    - "10000 个用户 → 文件大小 < 50MB，耗时 < 10s"

[Challenger] 攻击（逻辑漏洞）：
  "CSV 编码呢？中文用户名在 Excel 里会乱码。
   UTF-8 BOM 还是 GBK？"

[Arbiter] 裁决：攻击有效。编码是 CSV 的经典坑。

[Proposer] 修复 → V3：
  + 规范补充: "编码 MUST 为 UTF-8 with BOM（Excel 兼容）"
  + acceptance_criteria:
    - given: 中文用户名 "张三"
      when: export_csv 后用 Excel 打开
      then: 显示 "张三" 而非乱码

[Arbiter] 最终审查：V3 通过。提交人类确认。
```

pk_history 记录：
```yaml
pk_history:
  - round: 1
    attacker: Attacker
    attack_vector: malicious
    issue: "可生成无意义数据满足行数要求"
    fix: "验收条件验证具体字段内容"
    verdict: pass
  - round: 2
    attacker: Challenger
    attack_vector: boundary
    issue: "CSV 编码未定义，中文会乱码"
    fix: "强制 UTF-8 with BOM + Excel 可读性验收"
    verdict: pass
```

---

## 实践

### 快速选型
- **小项目** → L1，自查清单 + 声明地板/红线。
- **团队项目** → L2，清晰度评估 + 人工审查。
- **关键系统** → L3，双 AI 清晰度 + 完整 CAP 对抗循环。

### 核心原则
- **契约质量决定一切**：契约写得不好，后续所有门禁都没有意义。
- **先评估再对抗**：清晰度评估消除模糊，对抗消除漏洞，两步不可跳过。
- **选择题优于填空题**：让人类做选择而不是从零开始定义，降低认知负担。
- **AI 尤其需要对抗**：AI 很擅长"字面合规"，攻击策略库是拦截这类问题的最低成本方式。
- **地板和红线必须声明**：地板缺失 = 系统不可用；红线触碰 = 立即终止。
