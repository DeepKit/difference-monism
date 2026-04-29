# COP.B02-P2 · 状态编码协议详细版

> 定位：COP 诊断管线第二协议——如何把采样帧映射到编码空间。本文件是 B02 五协议主文中 P2 的完整展开。
> 作者：Yi Fu（付毅，ODDFounder）

---

## 一、P2 在诊断管线中的位置

```
输入采样(P1) → 状态编码(P2) → 诊断判定(P3) → 转介干预(P4) → 反馈校准(P5)
```

P2 是从"原始信号"到"可计算状态"的关键转换。不跳过 P2 直接做诊断——否则诊断就是基于表面标签的猜测。

---

## 二、编码流程：两步走

### 第一步：ASTO 前置编码（必填，不可跳过）

在进入 COP 核心编码之前，必须先继承 ASTO 的结构编码：

```yaml
asto_precoding:
  state_type: 自在 | 共识 | 编码 | 物化 | 定向
  stage: 潜伏 | 显性 | 扩散 | 峰值 | 衰减 | 残留
  sequence_position: 识别 | 定位 | 分析 | 设计 | 执行 | 验证 | 迭代
  boundary_status: clear | blurred | contested
  exception_flag: false | true
  exception_detail: ""       # exception_flag=true 时必填
```

### ASTO 前置编码的快速判断法

**五态判断**：
- "大家隐约觉得不对但说不清" → 自在
- "大家都知道有问题但没写成规则" → 共识
- "已经有明确的规则/流程/SOP" → 编码
- "规则已经被系统/工具强制执行" → 物化
- "系统能自己判断什么时候该改规则" → 定向

**六阶判断**：
- "才刚开始出现苗头" → 潜伏
- "已经能稳定观察到" → 显性
- "开始影响其他部分" → 扩散
- "现在是最严重的时候" → 峰值
- "在好转/收敛" → 衰减
- "基本平息但留了尾巴" → 残留

**边界判断**：
- "所有人都同意这个边界在哪" → clear
- "有人说不清这个边界" → blurred
- "有人在主动挑战这个边界" → contested

---

## 三、COP 核心编码

### 清晰度向量（clarity_vector）

| 维度 | 含义 | 评分指南 |
|------|------|---------|
| signal_completeness (0-1) | 信号够不够做判断 | 0.8+: 各通道信号齐全；0.4-0.7: 有部分通道缺失；<0.4: 关键通道空白 |
| signal_consistency (0-1) | 不同来源的信号是否一致 | 0.8+: 多源交叉验证一致；0.4-0.7: 部分矛盾；<0.4: 严重矛盾 |
| category_concentration (0-1) | 信号是否集中在单一类型 | 0.8+: 信号明确指向某一类型；0.4-0.7: 混合信号；<0.4: 分散到无法归类 |

### 结构风险向量（structural_risk_vector）

| 维度 | 含义 | 评分指南 |
|------|------|---------|
| responsibility_diffusion | 责任扩散程度 | high: 没人能说出谁在负责；medium: 有人负责但授权不清晰；low: 责任主体明确 |
| power_asymmetry | 权力不对称程度 | high: 承压点与决策点完全分离；medium: 有一定不对称；low: 权责基本匹配 |
| irreversibility_potential | 不可逆潜力 | high: 下一步动作可能有不可逆后果；medium: 可逆但有成本；low: 低风险动作 |

---

## 四、编码输出完整结构

```yaml
encoding_output:
  encoding_id: ""
  source_frame_id: ""
  
  asto_precoding: { ... }     # 见上
  
  clarity_vector:
    signal_completeness: 0.0-1.0
    signal_consistency: 0.0-1.0
    category_concentration: 0.0-1.0
    
  structural_risk_vector:
    responsibility_diffusion: low | medium | high
    power_asymmetry: low | medium | high
    irreversibility_potential: low | medium | high
    
  encoding_confidence: 0.0-1.0
  encoding_note: ""
  
  # 低置信度时的必填项
  low_confidence_reasons: []  # encoding_confidence < 0.6 时填写
```

---

## 五、编码不做什么

- 不跳过 ASTO 前置编码直接从表面标签起步
- 不把"这个人看起来很焦虑"编码为"火局"——需要走判局流程
- 不把分类集中度与结构风险混成一个分数——必须分开输出
- 不把编码当作解释——"这更接近 X"不等于"这是因为 Y"
