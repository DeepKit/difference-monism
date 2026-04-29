# COP.B03 · 诊断走通示例：从采样到校准

> 定位：COP 五协议诊断管线的端到端走通示例——展示一例完整信号如何经过 P1→P2→P3→P4→P5。
> 作者：Yi Fu（付毅，ODDFounder）

---

## 场景

一位 42 岁的中层管理者，在一家 500 人制造企业负责生产调度。最近一年持续感到"被夹在中间"——上级给目标但不给资源，下级抱怨目标不合理但自己无法向上推动。他在考虑辞职，但不确定是"真的该走"还是"只是太累了"。

---

## P1：输入采样

### 采样帧

```yaml
sampling_frame:
  frame_id: "MFG-MGR-2026-001"
  collected_at: "2026-04-28"
  source_type: questionnaire
  source_desc: "用户主动填写的9题诊断问卷+2道开放题"
  
  channels:
    - channel_id: "self-report"
      modality: text
      signals:
        - signal_id: "S1"
          raw_content: "我被要求对生产线的效率负责，但我没有权限调整排班表"
          reliability: high
          reliability_basis: "这是对具体工作流程的描述，不是感受表达"
          
        - signal_id: "S2"
          raw_content: "每次我跟上面要人，就说让我自己想办法"
          reliability: medium
          reliability_basis: "这包含感受成分——'每次'可能不是字面的每次"
          
        - signal_id: "S3"
          raw_content: "连续三个季度考核拿了C——不是因为效率没达标，是因为上级说我执行力度不够"
          reliability: high
          reliability_basis: "可核实的事实陈述"

  sampling_bias_note: "本帧信号全部来自用户单方面描述。最可能漏掉：上级视角的叙述、同级别管理者的比较信息、组织架构的正式文件。"
  
  completeness_self_assessment:
    signal_density: moderate
    blind_spots: ["上级视角缺失", "组织架构正式文件未获取"]
    recommended_supplement: "建议补充一份组织架构图和该岗位的正式职责说明"
```

---

## P2：状态编码

### ASTO 前置编码

```yaml
asto_precoding:
  state_type: 共识       # 大家都知道有问题，但没写成规则
  stage: 显性            # 问题已稳定可观察（连续三个C考核）
  sequence_position: 定位 # 在"这是什么问题"的阶段
  boundary_status: blurred  # 职责边界模糊——"对效率负责但不控制排班"
  exception_flag: false
```

### COP 核心编码

```yaml
encoding_output:
  encoding_id: "MFG-MGR-2026-001-ENC"
  source_frame_id: "MFG-MGR-2026-001"
  
  clarity_vector:
    signal_completeness: 0.6    # 三个信号明确但全部来自单方面
    signal_consistency: 0.9     # 三个信号高度一致
    category_concentration: 0.8 # 明确指向"权责割裂"类型
    
  structural_risk_vector:
    responsibility_diffusion: medium   # 有明确责任人但授权不清晰
    power_asymmetry: high              # 有责无权
    irreversibility_potential: medium  # 辞职是重要的但非不可逆
    
  encoding_confidence: 0.75
  encoding_note: "信号高度一致指向金局（权责割裂）。置信度中等偏离因为缺少第三方视角验证。"
```

---

## P3：诊断判定

### 判定矩阵计算

| 维度 | 值 | 阈值 | 结果 |
|------|-----|------|------|
| completeness | 0.6 | >0.5 ✓ | 通过 |
| consistency | 0.9 | >0.5 ✓ | 通过 |
| concentration | 0.8 | >0.5 ✓ | 通过 |
| power_asymmetry | high | — | 关注 |
| irreversibility | medium | — | 关注 |

→ 判定：**MIXED**（信号虽一致但来自单方面，权力不对称高）

```yaml
diagnostic_output:
  triage_status: MIXED
  confidence: 0.75
  primary_label: "金局-权责割裂（中层管理者典型模式）"
  alternative_labels: ["火局-责任引爆（三个C考核=起火信号）"]
  
  mixed_areas: ["信号全部来自用户方，缺少上级视角和组织结构文件"]
  limited_action_allowed: true
```

---

## P4：转介与有限干预

```yaml
action:
  type: PROCEED_WITH_CAUTION
  target: RT6
  
  payload:
    diagnostic_summary: "用户处于典型中层管理者权责割裂状态（金局），伴有火局早期信号（连续考核C=正在被点燃）。结构风险：中等偏离。"
    confidence: 0.75
    mixed_areas: ["缺少第三方视角验证"]
    step_2_extra_attention: "RT6步骤2建议加入'组织架构对比'——用户的正式职责 vs 实际被问责的内容"
    review_required_after_step: 2
    
    # RT6不启动的备选路径
    suggested_escalation_if_declines: "如果用户在步骤3说不进入处理——暂时不启动RT6，但建议一个月后复诊"
```

---

## P5：反馈校准（假设的后续）

### 假定结果：四个月后

用户在 RT6 的支持下做了一个决定：不是辞职，而是向上级做了一次"责任边界对话"——要求明确"我对什么有决定权"和"我只对什么负责"。上级部分同意了。

### 校准评估

```yaml
calibration:
  diagnosis_accurate: true
  actual_outcome: "用户通过结构对话缓解了权责割裂——验证了COP的诊断方向正确"
  
  # COP没有误判——金局+火局早期信号是正确的
  # 但有一个可以改进的地方：
  improvement_note: "在P2编码中，signal_completeness被标记为0.6因为只有用户视角。但本案例中用户视角最终被证明是准确的。这提示：对于'权责割裂'这类结构性明显的信号，单方面信号也可能足够可靠——阈值可以微调。"
```

### 如果诊断错了

替代场景：如果用户实际上不是权责割裂，而是"自己的执行确实有问题，上级的批评是合理的"（即诊断过度归因于结构而忽略了个人因素）——这就是一个 False Safe 误判（COP让用户相信是结构问题，但实际上用户自己的执行也有责任）。

在这种情况下，校准动作是：**提高 power_asymmetry 从 medium 到 high 的判断标准**——需要至少两个独立来源确认"有责无权"才标注为 high。

---

## 走通总结

这个示例展示了 COP 诊断管线最重要的纪律：

1. **P1 采样时不编造**——缺少上级视角就标注"缺少"，不推测上级在想什么
2. **P2 编码前先做 ASTO 前置**——五态/六阶/边界一个不跳
3. **P3 判定时宁可保守**——即使信号一致，因为来源单一，只给 MIXED 不给 RESOLVE
4. **P4 转介时标注混合区域**——让 RT6 在步骤 2 做额外验证
5. **P5 校准时区分"诊断对了"和"可以微调阈值"**——不因为一次正确就过度自信
