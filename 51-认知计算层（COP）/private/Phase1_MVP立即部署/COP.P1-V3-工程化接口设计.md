# COP · Phase 1 · V3 — 工程化接口设计

> **可立即部署**：开发团队拿到这份文件，即可开始工程实现
>
> **目标产品**：任何调用 COP `Phase 1` 协议的前台，都应以本接口为准
>
> **本轮变化**：输出字段从“一个类型 + 一个风险值”升级为“类型候选 + 分类集中度 + 结构风险 + 分流状态 + 转介接口”

---

## 一、数据结构

### 1. 用户输入结构（Request Body）

```json
{
  "answers": {
    "Q1": "B",
    "Q2": "A",
    "Q3": "C",
    "Q4": "C",
    "Q5": "B",
    "Q6": "D",
    "Q7": "C",
    "Q8": "D",
    "Q9": "C"
  }
}
```

### 2. 标准输出结构（Response Body）

```json
{
  "primary_type": "A",
  "secondary_type": "B",
  "score": {
    "A": 8,
    "B": 11,
    "C": 3,
    "D": 5
  },
  "classification_confidence": 0.41,
  "structural_risk": "HIGH",
  "triage_status": "REFER",
  "tags": ["结构循环依赖", "信息失真"],
  "refer_to": ["HUMAN_REVIEW", "TAT_REVIEW"],
  "actions": [
    "暂停自动闭环",
    "升级人工复核",
    "补录责任接口与阈值信息"
  ],
  "anti_actions": [
    "直接执行高强度动作",
    "把分类集中度当成低风险证明"
  ]
}
```

### 3. 权重矩阵配置

权重矩阵必须外置为配置文件，不能写死在代码里。

```json
{
  "Q1": {
    "A": {"A":0,"B":0,"C":0,"D":0},
    "B": {"A":2,"B":1,"C":0,"D":0},
    "C": {"A":2,"B":3,"C":0,"D":0},
    "D": {"A":3,"B":2,"C":0,"D":0}
  },
  "Q2": {
    "A": {"A":4,"B":0,"C":0,"D":0},
    "B": {"A":0,"B":4,"C":0,"D":0},
    "C": {"A":0,"B":0,"C":4,"D":0},
    "D": {"A":0,"B":0,"C":0,"D":4}
  }
}
```

> 完整矩阵见 `COP.P1-V2-加权判定引擎.md`

---

## 二、核心算法伪代码

```python
score = {"A": 0, "B": 0, "C": 0, "D": 0}

# Step 1：累积分数
for q, selected in answers.items():
    weights = WEIGHT_MATRIX[q][selected]
    for t in ["A", "B", "C", "D"]:
        score[t] += weights[t]

# Step 2：基础排序
sorted_types = sorted(score, key=score.get, reverse=True)
primary = sorted_types[0]
secondary = sorted_types[1]
primary_score = score[primary]
secondary_score = score[secondary]
total_score = sum(score.values())

# Step 3：硬规则
hard_rule_hits = 0
if answers["Q4"] == "D":
    primary = "B"
    hard_rule_hits += 1
if answers["Q5"] == "D" and answers["Q2"] == "D":
    primary = "D"
    hard_rule_hits += 1
if answers["Q2"] == "A" and answers["Q3"] in ["C", "D"]:
    primary = "A"
    hard_rule_hits += 1

primary_score = score[primary]

# Step 4：副类型
if secondary_score < 0.60 * primary_score:
    secondary = None

# Step 5：分类集中度
classification_confidence = primary_score / total_score if total_score > 0 else 0

# Step 6：结构风险
risk_points = 0
for q in ["Q2", "Q3", "Q4", "Q5", "Q7", "Q8", "Q9"]:
    if answers[q] in ["C", "D"]:
        risk_points += 1
if answers["Q4"] == "D":
    risk_points += 1
if answers["Q5"] == "D" and answers["Q2"] == "D":
    risk_points += 1

if answers["Q4"] == "D" or (answers["Q5"] == "D" and answers["Q2"] == "D") or risk_points >= 4:
    structural_risk = "HIGH"
elif risk_points >= 2:
    structural_risk = "MEDIUM"
else:
    structural_risk = "LOW"

# Step 7：分流状态
if total_score < 6:
    triage_status = "UNKNOWN"
    primary = None
    secondary = None
elif hard_rule_hits >= 2 or (classification_confidence < 0.40 and structural_risk == "HIGH"):
    triage_status = "FREEZE"
    primary = None
    secondary = None
elif structural_risk == "HIGH" or answers["Q8"] in ["C", "D"] or answers["Q9"] == "D":
    triage_status = "REFER"
elif secondary is not None and secondary_score >= 0.85 * primary_score:
    triage_status = "MIXED"
else:
    triage_status = "RESOLVE"

# Step 8：标签
tags = []
if answers["Q4"] in ["C", "D"]:
    tags.append("结构循环依赖")
if answers["Q3"] in ["C", "D"]:
    tags.append("信息失真")
if answers["Q5"] in ["C", "D"]:
    tags.append("时间轴污染")
if answers["Q7"] in ["C", "D"]:
    tags.append("系统被套利")
if answers["Q6"] in ["C", "D"]:
    tags.append("样本偏差")
if answers["Q8"] in ["C", "D"]:
    tags.append("无阈值控制")
if answers["Q9"] in ["C", "D"]:
    tags.append("外部约束过强")

# Step 9：转介接口
refer_to = []
if triage_status in ["FREEZE", "UNKNOWN", "REFER"]:
    refer_to.append("HUMAN_REVIEW")
if structural_risk == "HIGH":
    refer_to.append("TAT_REVIEW")
if answers["Q8"] in ["C", "D"] or answers["Q9"] == "D":
    refer_to.append("ODD_AUDIT")
```

---

## 三、API 接口规范

### POST `/analyze`

**功能**：提交 9 题答案，返回结构诊断结果

**请求示例**

```json
POST https://api.asto.cc/analyze
Content-Type: application/json

{
  "answers": {
    "Q1": "C",
    "Q2": "B",
    "Q3": "D",
    "Q4": "C",
    "Q5": "B",
    "Q6": "C",
    "Q7": "B",
    "Q8": "C",
    "Q9": "C"
  }
}
```

**返回示例**

```json
{
  "primary_type": "B",
  "secondary_type": "A",
  "classification_confidence": 0.52,
  "structural_risk": "HIGH",
  "triage_status": "REFER",
  "tags": ["结构循环依赖", "信息失真", "无阈值控制"],
  "refer_to": ["HUMAN_REVIEW", "TAT_REVIEW", "ODD_AUDIT"],
  "actions": [
    "暂停默认推进",
    "转人工复核依赖链",
    "补录阈值控制与责任接口"
  ],
  "anti_actions": [
    "把分类结果直接当作执行许可",
    "在高风险下继续自动推进"
  ]
}
```

### POST `/feedback`

**功能**：收集用户执行动作后的真实结果，为 `Phase 2` 提供训练素材

```json
POST /feedback
{
  "user_id": "xxx",
  "primary_type": "B",
  "triage_status": "REFER",
  "action_taken": true,
  "which_action": "升级人工复核",
  "result": "improved"
}
```

> `Phase 1` 只做数据记录；在补齐标签质量控制、版本回滚和对照规则前，不自动进入权重更新。

---

## 四、动作映射规则

### 1. `RESOLVE`

允许返回类型相关的有限动作集。

### 2. `MIXED`

动作集必须收缩为低强度探针，例如：

- 补充信息
- 对撞验证
- 小步试探

### 3. `FREEZE / UNKNOWN / REFER`

优先返回安全动作，而不是强处置动作：

```json
{
  "safe_actions": [
    "暂停自动闭环",
    "转人工复核",
    "补录缺失信息",
    "回接责任门槛与工程审计"
  ],
  "anti": [
    "直接执行高强度动作",
    "省略复核与升级接口"
  ]
}
```

---

## 五、MVP 上线检查清单

- [ ] 前端：9题问卷页面
- [ ] 前端：结果展示页显示 `classification_confidence / structural_risk / triage_status`
- [ ] 后端：权重矩阵配置文件外置
- [ ] 后端：`/analyze` 接口返回 `refer_to`
- [ ] 后端：`/feedback` 接口只记录，不自动改权重
- [ ] 高风险结果默认触发 `HUMAN_REVIEW`
- [ ] 命中 `Q8/Q9` 的高风险结果默认附带 `TAT_REVIEW / ODD_AUDIT`

---

## 六、最短压缩句

1. `V3 不是把 V2 包成 API，而是把“允许停止自动化”写进接口。`
2. `只要进入高风险现实，API 就必须会说：请升级，不要自动闭环。`
