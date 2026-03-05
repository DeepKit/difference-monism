---
version: 1.1.0
status: stable
last_updated: 2026-02-11
prerequisites: [ODD.01OVR]
---

# ODD 原生验证

## 意向
不信任 AI 的过程，只信任可验证的结果。
AI 写的代码不可信，AI 写的测试也不可信——但**人类定义的输入输出映射**是可信的。
ODD 原生验证用契约中的输入输出映射直接对比 AI 的输出，不依赖 AI 生成的测试代码。

## 规范

### 核心范式转变（TD-AI）
```
旧思维：如何让 AI 写出好代码？→ 优化输入
新思维：如何让坏代码无法通过？→ 验证输出

旧公式：高质量代码 = 好上下文 + 好契约 + 好模型
新公式：高质量代码 = 好测试 + 通过测试的代码
  其中：好测试 = 好契约 + 测试有效性验证
```

### 六大原则
1. **AI 不可信，测试结果才可信**——不要试图让 AI 写"好代码"，而是建立系统让"坏代码"无法通过。
2. **测试必须由独立来源定义**——契约中的验收标准（人类定义）或经过有效性验证的 AI 测试。
3. **代码是一次性的，测试是永久的**——代码可以重写，测试是质量的定义。
4. **小步快跑，频繁验证**——每写一个函数就测试，不要等到最后。
5. **失败是学习，不是惩罚**——每次失败都记录原因，积累经验（见 ODD.0E法宝-Bug意向图）。
6. **对抗式验证**——测试必须经过"攻击"验证，能被绕过的测试是无效测试。

### AI 不确定性防范策略
1. **输出验证优于代码审查**——不审查 AI 代码逻辑，验证 AI 代码输出。
2. **契约即测试**——契约中的 examples 自动成为测试用例。
3. **小任务原则**——让 AI 生成单个函数（50 行），而非整个模块（500 行）。
4. **幂等重试**——AI 生成失败就重新生成，同一契约多次生成，取通过测试的版本。
5. **隔离不确定性**——确定性边界（契约定义 + 测试执行 + 输出验证）包围不确定的 AI 代码生成区。
6. **人类兜底**——AI 重试 N 次仍失败，升级给人类。

---

## 机制

### L1 · 轻量

**手动验证。** 人工检查 AI 生成的代码是否符合预期。

写完契约后手动跑一遍验证：
- 给定输入 X，实际输出是不是 Y？
- 边界输入有没有异常？

无自动化，靠人工。

---

### L2 · 标准

**ODD 原生验证 = 输入输出映射 + 系统自动对比。**

#### 验证流程
```
人类在契约中定义输入输出映射
  ↓
AI 根据映射生成代码
  ↓
系统用契约中的输入调用代码
  ↓
系统对比实际输出和期望输出
  ├── 匹配 → 通过（quality_check pass）
  └── 不匹配 → 返工
```

#### 四种映射定义方式

**枚举式**（输入空间小、离散）：
```yaml
examples:
  - input: {username: "test", password: "123456"}
    output: {success: true, token: "<UUID>"}
  - input: {username: "test", password: "wrong"}
    output: {success: false, error: "密码错误"}
```

**属性式**（复杂逻辑，验证输出属性而非精确值）：
```yaml
properties:
  - "sort(arr) 的结果 MUST 有序"
  - "sort(arr) 的结果长度 MUST == 原数组长度"
  - "sort(arr) 的结果元素 MUST 是原数组的排列"
```

**示例式**（规律可推断）：
```yaml
examples:
  - input: {date: "2026-01-10"}
    output: "2026年1月10日"
  - input: {date: "2025-12-25"}
    output: "2025年12月25日"
```

**规则式**（有明确数学关系）：
```yaml
rule: "add(a, b) == a + b"
test_cases:
  - {a: 1, b: 2, expected: 3}
  - {a: 0, b: 0, expected: 0}
  - {a: -1, b: 1, expected: 0}
```

#### 四种映射方式的完整端到端示例

以下每个示例展示从契约定义到验证执行的完整流程。

**示例 A：枚举式 —— 用户权限检查**

```yaml
# 1. 契约中定义映射
contract:
  title: "检查用户是否有权访问资源"
  examples:
    - input: {user_role: "admin", resource: "settings"}
      output: {allowed: true}
    - input: {user_role: "guest", resource: "settings"}
      output: {allowed: false, reason: "insufficient_permission"}
    - input: {user_role: "editor", resource: "posts"}
      output: {allowed: true}
    - input: {user_role: "editor", resource: "settings"}
      output: {allowed: false, reason: "insufficient_permission"}
    - input: {user_role: "", resource: "posts"}
      output: {allowed: false, reason: "invalid_role"}

# 2. 系统执行验证
verification_run:
  - call: check_access("admin", "settings")
    actual: {allowed: true}
    expected: {allowed: true}
    result: PASS
  - call: check_access("guest", "settings")
    actual: {allowed: false, reason: "insufficient_permission"}
    expected: {allowed: false, reason: "insufficient_permission"}
    result: PASS
  # ... 其余 3 个同理
  summary: "5/5 PASS"
```

**示例 B：属性式 —— 列表去重**

```yaml
# 1. 契约中定义属性
contract:
  title: "列表去重函数"
  properties:
    - "unique(arr) 的结果不含重复元素"
    - "unique(arr) 的结果是原数组的子集"
    - "unique(arr) 保持元素首次出现的顺序"
    - "unique([]) == []"
    - "unique(arr) 的长度 <= 原数组长度"

# 2. 系统生成随机测试用例并验证属性
verification_run:
  test_cases_generated: 100        # 随机生成 100 个输入
  properties_checked:
    - property: "无重复元素"
      method: "len(result) == len(set(result))"
      pass_count: 100
    - property: "原数组子集"
      method: "all(x in arr for x in result)"
      pass_count: 100
    - property: "保持顺序"
      method: "比较元素在原数组中的索引顺序"
      pass_count: 100
    - property: "空数组"
      method: "unique([]) == []"
      pass_count: 1
    - property: "长度约束"
      method: "len(result) <= len(arr)"
      pass_count: 100
  summary: "5 属性 x 100 用例 = 500 检查，全部 PASS"
```

**示例 C：示例式 —— 手机号脱敏**

```yaml
# 1. 契约中用少量示例展示规律
contract:
  title: "手机号脱敏：中间 4 位替换为 ****"
  examples:
    - input: {phone: "13812345678"}
      output: "138****5678"
    - input: {phone: "19900001111"}
      output: "199****1111"
    - input: {phone: "12345"}          # 非标准长度
      output: {error: "invalid_phone"}

# 2. 系统从示例推断规律后生成更多用例验证
verification_run:
  inferred_rule: "phone[:3] + '****' + phone[7:]"
  contract_examples:
    - call: mask_phone("13812345678")
      actual: "138****5678"
      expected: "138****5678"
      result: PASS
    - call: mask_phone("19900001111")
      actual: "199****1111"
      expected: "199****1111"
      result: PASS
    - call: mask_phone("12345")
      actual: {error: "invalid_phone"}
      expected: {error: "invalid_phone"}
      result: PASS
  generated_examples:                  # 系统自动补充
    - call: mask_phone("18688889999")
      actual: "186****9999"
      rule_check: PASS
    - call: mask_phone("01012345678")
      actual: {error: "invalid_phone"}
      rule_check: PASS
  summary: "3 契约示例 + 2 生成示例 = 5/5 PASS"
```

**示例 D：规则式 —— 折扣计算**

```yaml
# 1. 契约中定义数学规则
contract:
  title: "计算折后价格"
  rule: "discount_price(price, rate) == round(price * (1 - rate), 2)"
  constraints:
    - "price >= 0"
    - "0 <= rate <= 1"
    - "结果精确到分（Decimal）"
  test_cases:
    - {price: 100.00, rate: 0.1, expected: 90.00}
    - {price: 100.00, rate: 0.0, expected: 100.00}
    - {price: 100.00, rate: 1.0, expected: 0.00}
    - {price: 0.01, rate: 0.5, expected: 0.01}   # round(0.005, 2)
    - {price: 99.99, rate: 0.15, expected: 84.99} # round(84.9915, 2)

# 2. 系统执行验证
verification_run:
  contract_cases:
    - call: discount_price(100.00, 0.1)
      actual: 90.00
      expected: 90.00
      result: PASS
    - call: discount_price(100.00, 0.0)
      actual: 100.00
      expected: 100.00
      result: PASS
    - call: discount_price(100.00, 1.0)
      actual: 0.00
      expected: 0.00
      result: PASS
    - call: discount_price(0.01, 0.5)
      actual: 0.01
      expected: 0.01
      result: PASS
    - call: discount_price(99.99, 0.15)
      actual: 84.99
      expected: 84.99
      result: PASS
  rule_fuzz:                           # 规则模糊测试
    random_cases: 200
    formula_check: "actual == round(price * (1 - rate), 2)"
    pass_count: 200
  summary: "5 契约用例 + 200 随机用例 = 205/205 PASS"
```

#### 动态值匹配
输出中包含 UUID、时间戳等动态值时，不能精确匹配，需用模式匹配：

| 动态值类型 | 期望输出写法 | 匹配方式 |
|------------|-------------|----------|
| UUID | `<UUID>` | 正则 `^[0-9a-f]{8}-...` |
| 时间戳 | `<TIMESTAMP>` | 执行时间 ±5 秒 |
| 自增 ID | `<INT>` | 正整数 |
| 随机字符串 | `<TOKEN:32>` | 长度 32 的字符串 |
| 浮点数 | `<FLOAT:0.01>` | 误差 ≤ 0.01 |
| 固定值 | 直接写值 | 精确匹配 |

期望输出示例：
```json
{
  "id": "<UUID>",
  "created_at": "<TIMESTAMP>",
  "token": "<TOKEN:64>",
  "score": "<FLOAT:0.001>",
  "name": "固定值直接对比"
}
```

---

### L3 · 严格

**在 L2 基础上增加：验证器自测 + 变异测试 + 对抗验证。**

#### 验证器自身测试
ODD 验证器本身 MUST 有完整测试覆盖：

| 测试类别 | 要求 |
|----------|------|
| 正向测试：正确输出应通过验证 | 100% 覆盖 |
| 负向测试：错误输出应被拒绝 | 100% 覆盖 |
| 边界测试：空值、极值、特殊字符 | ≥ 90% 覆盖 |
| 动态值测试：UUID、时间戳、随机数 | 100% 覆盖 |

#### 变异测试验证测试有效性
测试通过不代表测试有效——变异测试验证测试质量：
```
代码生成 → 单元测试通过 → 变异测试
  → 在代码中故意引入 bug（变异体）
  → 检查测试是否能发现
  → 能发现 = 测试有效（变异体被"杀死"）
  → 不能发现 = 测试无效（需补充测试）
  → 变异分数 = 杀死数 / (总数 - 等价数) ≥ 80%
```

六类变异算子：
| 算子 | 示例 |
|------|------|
| 算术运算符替换（AOR） | `+` → `-`, `*` → `/` |
| 关系运算符替换（ROR） | `>` → `>=`, `=` → `<>` |
| 逻辑运算符替换（LOR） | `and` → `or`, `not` → 删除 |
| 常量替换（COR） | `0` → `1`, `True` → `False` |
| 语句删除（SDL） | 删除赋值语句、删除 return |
| 条件边界（CBM） | `x > 0` → `x >= 0` |

#### 管道测试策略（补充）

**测试金字塔**：
- 70% 单元测试（单管道，事务回滚隔离）
- 25% 集成测试（真实 DB + mock 外部依赖）
- 5% E2E 测试（完整流程）

**契约驱动测试**：
- 由 examples 自动生成正向测试。
- 由 input/output 约束生成边界测试。

**事务回滚隔离**：
```yaml
test_isolation:
  mode: transaction_rollback
  reason: "测试结束自动回滚，避免清理成本"
```

**外部依赖 Mock & 补偿验证**：
- 外部调用必须 mock，验证补偿逻辑（退款/释放库存）。
- 失败路径与补偿路径必须有测试。

**隔离策略**（按复杂度选择）：
- 事务隔离（推荐）
- Schema 隔离（并行测试）
- 快照恢复（复杂场景）

#### 对抗式验证
```
AI-A（开发者）：写代码 + 写测试
AI-B（攻击者）：尝试写能通过测试但有 bug 的代码

AI-B 能通过？→ 测试不够严格 → AI-A 补充测试
AI-B 不能通过？→ 测试有效
```

#### 完整质量保证流程
```
[阶段1: 测试定义] — 人类/契约
  ↓ 契约中定义验收标准 + 边界条件
[阶段2: 代码生成] — AI
  ↓ AI 根据契约生成代码
[阶段3: 输出验证] — 系统（quality_check）
  ↓ 用契约输入调用代码，对比输出
[阶段4: 集成验证] — 其他车间（acceptance）
  ↓ 多产出物组合 + 边界测试
[阶段5: 变异测试] — 系统（mutation_test）
  ↓ 验证测试有效性 ≥ 80%
[阶段6: 对抗测试] — 系统（adversarial_test，L3+）
  ↓ 攻击代码发现漏洞
[阶段7: 交叉审核] — 其他车间（cross_review，L4）
  ↓ 多方审核 + 分歧上报人类
[阶段8: 封版] — 自动
```

---

## 实践

### 快速选型
- **小项目** → L1，手动验证。
- **团队项目** → L2，ODD 原生验证 + 动态值匹配。
- **关键系统** → L3，验证器自测 + 变异测试 + 对抗验证。

### 核心原则
- **输出对比优于测试代码**：不写测试代码，用契约中的输入输出映射直接对比。
- **人类定义标准，机器执行验证**：测试标准来自契约（人类确认），不来自 AI。
- **动态值不精确匹配**：UUID、时间戳等用模式匹配，避免误报。
- **验证器也要测试**：验证器本身有 bug，一切都不可信。
