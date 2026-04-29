# COP.B02 · 五协议主文

> 定位：COP 核心协议层——五份协议各自独立、互相衔接，共同构成"从复杂现实到可计算诊断"的完整管线。
> 状态：现行母文件
> 作者：Yi Fu（付毅，ODDFounder）

---

## 总论：五协议的关系

五协议不是并列的五个功能模块，而是一条**诊断管线**：

```
输入采样 → 状态编码 → 诊断判定 → 转介与有限干预 → 反馈学习校准
   ↑                                                      │
   └──────────────────────────────────────────────────────┘
                    校准结果回流到采样策略
```

每一步把前一步的输出压得更"可计算"：

| 协议 | 输入 | 输出 | 核心问题 |
|------|------|------|---------|
| P1 输入采样 | 原始现实信号 | 结构化采样帧 | 我们看到了什么 |
| P2 状态编码 | 采样帧 | 编码向量 + 结构标签 | 这属于什么类型的状态 |
| P3 诊断判定 | 编码向量 | 分流状态 + 置信度 | 当前是否清楚、是否安全 |
| P4 转介干预 | 分流状态 | 动作建议 + 转介路由 | 接下来该做什么 |
| P5 反馈校准 | 真实结果 | 协议参数更新 | 我们上次判断对了吗 |

---

## P1 · 输入采样协议

### 1.1 职责

把原始现实信号（自然语言描述、问卷回答、行为日志、指标面板）转换为**结构化采样帧**。

### 1.2 核心原则

- **不在此阶段做判断**：采样只管"收进来"，不管"对不对"
- **信号源显式标注**：每条采样记录必须标注来源、时间、采集方式
- **采样偏倚自报**：采样策略必须说明自己更可能漏掉什么

### 1.3 采样帧结构

```yaml
sampling_frame:
  frame_id: ""
  collected_at: ""
  source_type: questionnaire | log | interview | sensor | document
  source_desc: ""
  signals:
    - signal_id: ""
      content: ""           # 原始内容，不做改写
      modality: text | numeric | categorical | binary
      reliability: high | medium | low | unknown
  sampling_bias_note: ""    # 本帧最可能漏掉什么信号
```

### 1.4 最低采样纪律

1. 每条信号必须保留原始措辞，不做同义改写
2. 不知道的信号写"未知"，不编造
3. 采集方式（用户主动/系统日志/第三方报告）必须标注
4. 采样偏倚声明不得跳过

---

## P2 · 状态编码协议

### 2.1 职责

把采样帧中的原始信号映射到 COP 的编码空间，输出**编码向量 + 结构标签**。

### 2.2 核心原则

- **先继承 ASTO 的结构编码**：在编码前先确认"当前结构处于什么状态/节律/位点"，而不是跳过结构直接从表面标签起步
- **分类集中度与结构风险分开编码**：不要混成一个分数
- **编码不是解释**：编码是"这更接近 X"，不是"这是因为 Y"

### 2.3 编码输出结构

```yaml
encoding_output:
  encoding_id: ""
  source_frame_id: ""
  
  # ASTO 前置编码（必填）
  asto_precoding:
    state_type: ""          # 五态之一
    stage: ""               # 六阶之一
    sequence_type: ""       # 七序之一
    boundary_status: clear | blurred | contested
    exception_flag: false
    
  # COP 核心编码
  clarity_vector:
    signal_completeness: 0-1    # 信号完整度
    signal_consistency: 0-1     # 信号一致度
    category_concentration: 0-1 # 分类集中度
    
  structural_risk_vector:
    responsibility_diffusion: low | medium | high
    power_asymmetry: low | medium | high
    irreversibility_potential: low | medium | high
    
  encoding_confidence: 0-1
  encoding_note: ""         # 编码过程中的不确定性和解释
```

### 2.4 最低编码纪律

1. ASTO 前置编码不得跳过——必须先标五态/六阶/边界
2. 分类集中度与结构风险必须分开输出
3. 编码置信度低于 0.6 时，必须写 `encoding_note`

---

## P3 · 诊断判定协议

### 3.1 职责

基于编码向量和风险向量，输出**分流状态**和**处置建议级别**。

### 3.2 五种分流状态

| 状态 | 含义 | 触发条件 | 默认动作 |
|------|------|---------|---------|
| RESOLVE | 可自动处理 | 信号完整 + 一致 + 分类集中 + 结构风险低 | 允许继续自动推进 |
| MIXED | 混合信号 | 信号不一致 或 分类不集中 | 标注混合区域，有限推进 |
| FREEZE | 冻结 | 结构风险高 或 触及红线 | 暂停自动推进，升级人工 |
| UNKNOWN | 信息不足 | 信号完整度低 | 要求补充信息 |
| REFER | 转介 | 超出 COP 可处理范围 | 转介到 TAT / ODD / 人工 |

### 3.3 判定规则（简化矩阵）

| 信号完整度 | 分类集中度 | 结构风险 | → 分流状态 |
|-----------|-----------|---------|------------|
| >0.7 | >0.7 | low | RESOLVE |
| >0.5 | >0.5 | low-medium | MIXED |
| any | any | high | FREEZE |
| <0.4 | any | any | UNKNOWN |
| any | any | out_of_scope | REFER |

> 注：这是概念级矩阵，实际判定权重由 `COP.诊断协议.v1.md` 和 `COP.校准样本协议.v1.md` 详细定义。

### 3.4 诊断判定输出

```yaml
diagnostic_output:
  diagnosis_id: ""
  source_encoding_id: ""
  
  triage_status: RESOLVE | MIXED | FREEZE | UNKNOWN | REFER
  confidence: 0-1
  primary_label: ""
  alternative_labels: []
  
  freeze_reason: ""         # triage_status=FREEZE 时必填
  referral_target: ""       # triage_status=REFER 时必填
  missing_info_hint: ""     # triage_status=UNKNOWN 时建议补充的信息
  
  diagnosis_note: ""
```

---

## P4 · 转介与有限干预协议

### 4.1 职责

基于分流状态，生成**下一步动作建议**和**转介路由**。

### 4.2 五种分流→动作映射

| 分流状态 | 动作类型 | 具体动作 |
|---------|---------|---------|
| RESOLVE | 放行 | 允许进入 RT6 完整六步流程，附带诊断摘要 |
| MIXED | 有限放行 | 进入 RT6，但标注混合信号区域供步骤 2 额外关注 |
| FREEZE | 冻结 + 升级 | 停止自动推进；路由到人工复审或 TAT 评审 |
| UNKNOWN | 补充采样 | 向用户或系统请求指定类型的额外信息 |
| REFER | 转介 | 生成转介摘要，路由到指定目标（TAT/ODD/ECET/人工） |

### 4.3 有限干预原则

COP 可以做：
- 基于规则的有限建议（不涉及高风险强制动作）
- 转介路由选择（根据问题类型匹配目标层）
- 信息补充请求（明确请求什么类型的信息）

COP 不得做：
- 强制性高风险动作授权
- 行为锁定的最终裁决
- 同意、申诉、补偿结构定义（这些必须回引 TAT）

### 4.4 转介路由

| 问题类型 | 转介目标 | 转介内容 |
|---------|---------|---------|
| 触及责任门槛 | TAT | 诊断摘要 + 风险向量 + 触发信号 |
| 契约/门禁/证据问题 | ODD | 诊断摘要 + 涉及的产出物引用 |
| 治理边界争议 | ECET | 诊断摘要 + 治理约束分析 |
| COP 自身无法判断 | 人工复审 | 完整诊断链 + 无法判断的原因 |

---

## P5 · 反馈学习校准协议

### 5.1 职责

收集诊断后的真实结果，对比诊断结论与实际情况，校准协议参数。

### 5.2 校准数据采集

每次诊断后，在以下时点采集校准信号：

| 时点 | 采集内容 |
|------|---------|
| 即时反馈 | 用户/系统对诊断的反应 |
| RT6 步骤 2 反馈 | 扫描诊断是否与 COP 诊断一致 |
| RT6 步骤 6 反馈 | 复诊时发现的问题是否与初始诊断匹配 |
| 事故回溯 | FREEZE/REFER 后被证实为正确的冻结（避免了一次损害）或错误的冻结（阻碍了本可进行的处理） |

### 5.3 三类误判的校准

| 误判类型 | 定义 | 校准动作 |
|----------|------|---------|
| False Safe | 判定为 RESOLVE，实则不应推进 | 提高该类型的分类集中度阈值或结构风险敏感度 |
| Over Freeze | 判定为 FREEZE，实则本可推进 | 下调该类型的冻结触发阈值 |
| Wrong Type | 分流方向正确但分类标签错误 | 调整该信号模式的编码映射 |

### 5.4 校准输出

```yaml
calibration_output:
  calibration_id: ""
  source_diagnosis_id: ""
  
  actual_outcome: ""        # 真实发生了什么
  diagnosis_accurate: true | false | partial
  misclass_type: false_safe | over_freeze | wrong_type | none
  
  parameter_adjustments:
    - parameter: ""         # 哪个参数需要调整
      direction: up | down
      magnitude: minor | moderate | major
      reason: ""
```

---

## 跨协议纪律

1. **协议不可跳过**：不得从采样直接跳到判定（跳过编码），也不得从判定直接跳到校准（跳过转介）
2. **不安全的输出必须 FREEZE 或 REFER**：宁可多冻一次，不可错放一次
3. **校准必须闭环**：每次误判必须在误判样本库中留档
4. **ASTO 前置编码不可省略**：这是防止 COP 退化为"表面分类器"的关键机制
