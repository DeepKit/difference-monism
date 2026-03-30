# COP · Phase 1 · V3 — 工程化接口设计

> **可立即部署**：开发团队拿到这份文件，即可开始工程实现
> **目标产品**：`asto.cc/diag` 的后端计算服务

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
  "confidence": 0.61,
  "risk_level": "HIGH",
  "tags": ["结构循环依赖", "信息失真"],
  "actions": [
    "投放负向探针",
    "私下验证真实意见",
    "书面确认责任"
  ],
  "anti_actions": [
    "继续沉默",
    "默认共识"
  ]
}
```

### 3. 权重矩阵配置（必须外置为配置文件，不能写死在代码里）
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
> ⚠️ 完整权重矩阵见 `COP.P1-V2-加权判定引擎.md`

---

## 二、核心算法伪代码

```python
# Step 1：初始化
score = {"A": 0, "B": 0, "C": 0, "D": 0}

# Step 2：遍历所有问题
for q in answers:
    selected = answers[q]
    weights = WEIGHT_MATRIX[q][selected]
    for t in ["A","B","C","D"]:
        score[t] += weights[t]

# Step 3：冲突规则（优先级覆盖）
if answers["Q4"] == "D":
    primary = "B"                         # 死锁优先
elif answers["Q5"] == "D" and answers["Q2"] == "D":
    primary = "D"                         # 沉没成本锁定
elif answers["Q2"] == "A" and answers["Q3"] in ["C","D"]:
    primary = "A"                         # 共识幻觉覆盖
else:
    primary = max(score, key=score.get)   # 取最高分

# Step 4：副类型
sorted_types = sorted(score, key=score.get, reverse=True)
secondary = sorted_types[1]
if score[secondary] < 0.6 * score[primary]:
    secondary = None

# Step 5：风险等级
total = sum(score.values())
confidence = score[primary] / total if total > 0 else 0
risk = "HIGH" if confidence > 0.6 else ("MEDIUM" if confidence > 0.4 else "LOW")

# Step 6：副标签生成
tags = []
if answers["Q4"] in ["C","D"]: tags.append("结构循环依赖")
if answers["Q3"] in ["C","D"]: tags.append("信息失真")
if answers["Q5"] in ["C","D"]: tags.append("时间轴污染")
if answers["Q7"] in ["C","D"]: tags.append("系统被套利")
if answers["Q6"] in ["C","D"]: tags.append("样本偏差")
if answers["Q8"] in ["C","D"]: tags.append("无阈值控制")
```

---

## 三、API 接口规范

### POST `/analyze`
**功能**：提交 9 题答案，返回结构诊断结果

**请求示例**：
```json
POST https://api.asto.cc/analyze
Content-Type: application/json

{
  "answers": { "Q1":"C","Q2":"B","Q3":"D","Q4":"C","Q5":"B","Q6":"C","Q7":"B","Q8":"C","Q9":"C" }
}
```

**返回示例**：
```json
{
  "primary_type": "B",
  "secondary_type": "A",
  "confidence": 0.67,
  "risk_level": "HIGH",
  "tags": ["结构循环依赖","信息失真"],
  "actions": ["拉所有相关方进同一沟通场","明确指出依赖冲突","引入上级强制决策"],
  "anti_actions": ["单点沟通","继续当中间人"]
}
```

---

### POST `/feedback`（Phase 2 预留接口）
**功能**：收集用户执行动作后的真实结果，为 V4 动态权重训练提供数据燃料

```json
POST /feedback
{
  "user_id": "xxx",
  "primary_type": "B",
  "action_taken": true,
  "which_action": "拉群对撞",
  "result": "improved"  // improved | unchanged | worse
}
```

> ⚠️ 此接口在 Phase 1 可以仅做数据记录，Phase 2 启动后开始触发权重修正逻辑

---

## 四、动作映射配置（外置，可热更新）

```json
{
  "A": {
    "actions": ["投放负向探针","私下验证真实意见","书面确认责任"],
    "anti": ["继续沉默","顺从共识"]
  },
  "B": {
    "actions": ["拉所有相关方进同一沟通场","明确指出依赖冲突","引入上级强制决策"],
    "anti": ["单点沟通","继续当中间人"]
  },
  "C": {
    "actions": ["立即设定硬停止条件","新增需求必须交换代价","强制封板当前版本"],
    "anti": ["接受顺手改一下","等待临界点"]
  },
  "D": {
    "actions": ["强制归零（假设从未投入）","只计算未来收益","设定退出触发点"],
    "anti": ["因已投入继续决策","用未来填补过去"]
  }
}
```

---

## 五、MVP 上线检查清单

- [ ] 前端：9题问卷页面（单选，禁止多选）
- [ ] 前端：结果展示页（类型 + 副标签 + 风险等级 + 动作指令）
- [ ] 后端：权重矩阵配置文件（JSON，外置）
- [ ] 后端：`/analyze` 接口（Python/Node.js 均可）
- [ ] 后端：`/feedback` 接口（Phase2预留，先只存数据）
- [ ] 结果页底部：《TAT首诊申请表》硬植入入口
- [ ] 权限限制：申请表限"一号位"才能提交（选否则跳出页面）
