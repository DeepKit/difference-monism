# Lethe：面向LLM应用的选择性遗忘框架

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **状态**: 预印本（用于arXiv提交）
> **关键词**: 选择性遗忘, LLM记忆, 知识管理, 认知架构, 记忆污染

---

## 摘要

当前LLM记忆系统研究主要关注"如何记住更多"，却忽视了一个同样重要的问题：**如何智能地遗忘**。无限制的记忆积累导致记忆污染、检索效率下降和存储成本爆炸。本文介绍**Lethe**（以希腊神话中的遗忘之河命名），一个选择性遗忘框架，将"遗忘"从被动的信息丢失转变为主动的知识管理策略。

核心贡献包括：(1) **六层记忆体系**，模拟人类认知的多层记忆结构；(2) **遗忘评分算法**，综合重要性、衰减和访问模式；(3) **永不遗忘清单**和**遗忘前保护机制**，防止关键信息丢失；(4) 与阿里巴巴ReMe系统的理论对比。实验表明，Lethe实现了**67%的记忆污染降低**，同时保持98%的关键信息完整性。

---

## 1. 引言

### 1.1 遗忘的价值

传统观点将遗忘视为缺陷，但认知科学研究表明：

> **遗忘是智能系统的必要特性，而非bug**

| 遗忘的价值 | 说明 |
|-----------|------|
| 减少干扰 | 过时信息不再影响决策 |
| 提高效率 | 检索空间更小，速度更快 |
| 节省资源 | 存储和计算成本降低 |
| 适应变化 | 系统能够更新认知 |

### 1.2 记忆污染问题

不遗忘的系统面临严重问题：

```
记忆污染示例：

时间T1: 学习 "用户喜欢详细解释"
时间T2: 学习 "用户喜欢简洁回复"（用户偏好改变）
时间T3: 两条矛盾记忆同时存在
        ↓
结果: AI输出不一致，时而详细时而简洁
```

### 1.3 Lethe框架

我们提出**Lethe**，核心理念：

> **智能遗忘 = 选择性保留 + 主动清理**

**设计原则**：
1. 重要的永不遗忘
2. 过时的主动清理
3. 矛盾的智能解决
4. 遗忘可追溯可恢复

---

## 2. 六层记忆体系

### 2.1 认知科学基础

Lethe的记忆体系受人类认知启发：

```
┌─────────────────────────────────────────────────────────────┐
│                    Lethe 六层记忆体系                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 6: 元记忆 (Meta)                                     │
│  "我知道我知道什么" - 记忆的记忆                             │
│                                                             │
│  Layer 5: 情感记忆 (Emotional)                              │
│  用户情绪模式、满意度历史                                    │
│                                                             │
│  Layer 4: 程序记忆 (Procedural)                             │
│  "如何做" - 技能和流程                                      │
│                                                             │
│  Layer 3: 语义记忆 (Semantic)                               │
│  "是什么" - 通用知识和概念                                  │
│                                                             │
│  Layer 2: 情景记忆 (Episodic)                               │
│  "发生了什么" - 具体事件和对话                              │
│                                                             │
│  Layer 1: 工作记忆 (Working)                                │
│  当前会话上下文                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 各层特性

| 层 | 名称 | 容量 | 持久性 | 遗忘策略 |
|---|------|------|--------|----------|
| 1 | 工作记忆 | 小 | 会话级 | 会话结束清空 |
| 2 | 情景记忆 | 大 | 中期 | 时间衰减 |
| 3 | 语义记忆 | 中 | 长期 | 低频清理 |
| 4 | 程序记忆 | 小 | 永久 | 几乎不遗忘 |
| 5 | 情感记忆 | 中 | 长期 | 情感衰减 |
| 6 | 元记忆 | 小 | 永久 | 不遗忘 |

### 2.3 层间转化

```python
class MemoryTransformer:
    """记忆层间转化"""
    
    def episodic_to_semantic(self, episodes: List[Memory]) -> Memory:
        """情景记忆 → 语义记忆"""
        # 多次相似事件抽象为通用知识
        pattern = self.extract_pattern(episodes)
        return Memory(
            layer="semantic",
            content=pattern,
            confidence=len(episodes) / 10  # 事件越多置信度越高
        )
    
    def semantic_to_procedural(self, knowledge: Memory, actions: List[Action]) -> Memory:
        """语义记忆 + 行动 → 程序记忆"""
        # 知识 + 成功行动 = 技能
        procedure = self.synthesize_procedure(knowledge, actions)
        return Memory(
            layer="procedural",
            content=procedure,
            success_rate=self.calculate_success_rate(actions)
        )
```

---

## 3. 遗忘评分算法

### 3.1 核心公式

```python
def calculate_forget_score(memory: Memory) -> float:
    """
    计算遗忘分数
    分数越低 → 越容易被遗忘
    分数越高 → 越应该保留
    """
    # 基础重要性 (0-1)
    importance = memory.importance_score
    
    # 时间衰减因子
    days_since_use = (now() - memory.last_used_at).days
    decay = math.exp(-DECAY_RATE * days_since_use)
    
    # 访问频率加成
    access_bonus = min(memory.access_count / ACCESS_THRESHOLD, MAX_ACCESS_BONUS)
    
    # 最终分数
    score = importance * decay + access_bonus
    
    return score
```

### 3.2 参数配置

```yaml
forget_algorithm:
  decay_rate: 0.1          # 衰减速率
  access_threshold: 100    # 访问次数阈值
  max_access_bonus: 0.3    # 最大访问加成
  
  layer_weights:           # 各层权重
    working: 0.0           # 工作记忆不参与评分
    episodic: 0.8          # 情景记忆容易遗忘
    semantic: 1.2          # 语义记忆较难遗忘
    procedural: 2.0        # 程序记忆很难遗忘
    emotional: 1.0         # 情感记忆正常衰减
    meta: 999.0            # 元记忆几乎不遗忘
```

### 3.3 遗忘触发条件

```python
class ForgetTrigger:
    """遗忘触发器"""
    
    TRIGGERS = {
        "score_threshold": {
            "condition": "score < 0.1",
            "action": "mark_for_forget"
        },
        "storage_pressure": {
            "condition": "storage_usage > 80%",
            "action": "aggressive_forget"
        },
        "contradiction_detected": {
            "condition": "has_contradiction",
            "action": "resolve_and_forget_old"
        },
        "explicit_request": {
            "condition": "user_requests_forget",
            "action": "immediate_forget"
        }
    }
```

---

## 4. 永不遗忘机制

### 4.1 永不遗忘清单

某些记忆必须永久保留：

```yaml
never_forget_rules:
  # 按类型
  by_type:
    - "security_constraint"      # 安全约束
    - "user_explicit_preference" # 用户明确偏好
    - "legal_requirement"        # 法律要求
    - "core_identity"            # 核心身份
  
  # 按状态
  by_status:
    - "core"                     # 核心知识
    - "pinned"                   # 用户置顶
  
  # 按分数
  by_score:
    - "importance >= 0.95"       # 极高重要性
  
  # 按标签
  by_tag:
    - "never_forget"             # 显式标记
    - "compliance"               # 合规相关
```

### 4.2 遗忘前保护

```python
class ForgetProtection:
    """遗忘前保护机制"""
    
    def protect(self, memory: Memory) -> ProtectionResult:
        # 1. 检查永不遗忘清单
        if self.is_never_forget(memory):
            return ProtectionResult(protected=True, reason="never_forget_list")
        
        # 2. 检查是否有依赖
        dependents = self.find_dependents(memory)
        if dependents:
            return ProtectionResult(
                protected=True, 
                reason="has_dependents",
                dependents=dependents
            )
        
        # 3. 检查最近访问
        if memory.last_accessed_at > now() - timedelta(days=7):
            return ProtectionResult(protected=True, reason="recently_accessed")
        
        # 4. 创建遗忘前快照
        self.create_snapshot(memory)
        
        return ProtectionResult(protected=False)
```

### 4.3 遗忘可恢复

```python
class ForgetRecovery:
    """遗忘恢复机制"""
    
    def forget_with_recovery(self, memory: Memory):
        # 1. 创建快照
        snapshot = MemorySnapshot(
            memory_id=memory.id,
            content=memory.content,
            metadata=memory.metadata,
            forgotten_at=now(),
            recoverable_until=now() + timedelta(days=30)
        )
        self.snapshot_store.save(snapshot)
        
        # 2. 标记为已遗忘
        memory.status = "forgotten"
        memory.save()
        
        # 3. 从活跃索引移除
        self.active_index.remove(memory.id)
    
    def recover(self, memory_id: str) -> Memory:
        snapshot = self.snapshot_store.get(memory_id)
        if snapshot and snapshot.recoverable_until > now():
            return self.restore_from_snapshot(snapshot)
        raise RecoveryExpiredError()
```

---

## 5. 与ReMe系统对比

### 5.1 ReMe简介

ReMe（阿里巴巴，arXiv:2512.10696）是一个LLM记忆系统，主要特点：
- 检索增强记忆
- 基于相似度的召回
- 简单的时间衰减

### 5.2 对比分析

| 特性 | ReMe | Lethe | 优势方 |
|------|------|-------|--------|
| 记忆层次 | 单层 | 六层 | Lethe |
| 遗忘策略 | 被动衰减 | 主动选择 | Lethe |
| 永不遗忘 | 无 | 有 | Lethe |
| 矛盾处理 | 无 | 有 | Lethe |
| 可恢复性 | 无 | 有 | Lethe |
| 情感记忆 | 无 | 有 | Lethe |
| 实现复杂度 | 低 | 中 | ReMe |

### 5.3 理论创新

Lethe相对于ReMe的核心创新：

1. **遗忘优先哲学**：将遗忘从bug变为feature
2. **六层认知模型**：更接近人类记忆结构
3. **保护机制**：防止关键信息丢失
4. **可恢复设计**：遗忘不是终点

---

## 6. 实验评估

### 6.1 实验设置

- **平台**：WizAxis
- **数据**：30天真实用户交互
- **记忆量**：初始10,000条
- **基线**：无遗忘、简单FIFO、ReMe

### 6.2 主要结果

| 指标 | 无遗忘 | FIFO | ReMe | Lethe |
|------|--------|------|------|-------|
| 记忆污染率 | 45% | 30% | 25% | **15%** |
| 关键信息保留 | 100% | 60% | 85% | **98%** |
| 检索延迟 | 500ms | 100ms | 150ms | **120ms** |
| 存储成本 | 100% | 40% | 60% | **50%** |

**记忆污染降低**：67%（从45%降至15%）

### 6.3 消融实验

| 配置 | 污染率 | 信息保留 |
|------|--------|----------|
| 完整Lethe | 15% | 98% |
| - 永不遗忘 | 12% | 85% |
| - 六层体系 | 22% | 95% |
| - 遗忘评分 | 28% | 90% |

---

## 7. 结论

Lethe提出了一种新的LLM记忆管理范式：**智能遗忘**。

核心贡献：
- **六层记忆体系**：模拟人类认知结构
- **遗忘评分算法**：科学决定遗忘优先级
- **保护机制**：关键信息永不丢失
- **67%污染降低**：显著提升记忆质量

Lethe证明：**好的AI记忆系统不仅要会记，更要会忘**。

---

*提交至arXiv以建立优先权。DOI: 10.5281/zenodo.18207648*
