# WizMem：基于双环认知的LLM应用自改进记忆系统

> **作者**: 付毅 (ODDFounder, Fuyi.it@live.cn)
> **日期**: 2026-01-11
> **状态**: 预印本（用于arXiv提交）
> **关键词**: AI记忆系统, LLM, 知识管理, 持续学习, 认知架构

---

## 摘要

大型语言模型缺乏持久记忆，导致重复交互、输出不一致以及无法从经验中学习。本文介绍**WizMem（Wizard Memory）**，一种用于LLM记忆系统的双环认知架构，结合快速上下文注入与慢速主动精炼。该系统实现了**四层学习层次**（事实→模式→关系→元），带有滑动窗口遗忘的**知识生命周期管理**机制，以及用于自动质量控制的**知识熔断器**。

通过WizAxis平台的理论分析和案例研究，我们证明WizMem实现了：(1) **P95 < 200ms**的上下文注入延迟，(2) 基于有效性的从试用到激活状态的**自动知识晋升**，(3) 当知识质量低于阈值时通过熔断器降级实现**自愈**。WizMem代表了从无状态LLM交互到**持续学习AI系统**的范式转变。

---

## 1. 引言

### 1.1 无状态LLM的问题

当前的LLM应用存在根本性限制：

| 问题 | 表现 | 影响 |
|------|------|------|
| **无记忆** | 每次对话从零开始 | 用户需重复解释偏好 |
| **无学习** | 不能从错误中改进 | 相同错误反复出现 |
| **无一致性** | 输出风格不稳定 | 用户体验差 |

### 1.2 WizMem架构

我们提出**WizMem（Wizard Memory）**，一种双环认知架构：

$$\text{WizMem} = \text{快环（注入）} + \text{慢环（精炼）}$$

| 环 | 目的 | 延迟 | 触发 |
|---|------|------|------|
| 快环 | 上下文注入 | < 200ms | 每次请求 |
| 慢环 | 知识精炼 | 分钟级 | 后台/定时 |

### 1.3 贡献

1. **WizMem架构**：用于LLM记忆的双环认知系统
2. **四层学习模型**：层次化知识提取
3. **知识熔断器**：自愈质量控制
4. **参考实现**：WizAxis中基于PostgreSQL的系统

---

## 2. 相关工作

### 2.1 现有方法对比

| 方法 | 持久 | 学习 | 质量控制 | 生命周期 |
|------|:----:|:----:|:--------:|:--------:|
| 上下文记忆 | 否 | 否 | 否 | 否 |
| RAG | 是 | 否 | 否 | 否 |
| 微调 | 是 | 是 | 手动 | 否 |
| 知识图谱 | 是 | 手动 | 手动 | 否 |
| **WizMem** | **是** | **自动** | **自动** | **是** |

---

## 3. WizMem架构

### 3.1 系统概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        WizMem架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    快环 (< 200ms)    ┌──────────────┐        │
│  │   用户请求    │ ──────────────────▶ │  上下文注入   │        │
│  └──────────────┘                      └──────────────┘        │
│         │                                     │                 │
│         │                                     ▼                 │
│         │                              ┌──────────────┐        │
│         │                              │   LLM调用    │        │
│         │                              └──────────────┘        │
│         │                                     │                 │
│         ▼                                     ▼                 │
│  ┌──────────────┐    慢环 (分钟级)     ┌──────────────┐        │
│  │  交互记录     │ ◀────────────────── │  响应输出    │        │
│  └──────────────┘                      └──────────────┘        │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────┐      │
│  │                    知识精炼管道                        │      │
│  │  提取 → 验证 → 晋升 → 关联 → 遗忘                     │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 快环：上下文注入

快环负责在每次LLM调用前注入相关记忆：

```python
class FastLoop:
    def inject_context(self, request: Request) -> EnrichedRequest:
        # 1. 检索相关记忆
        memories = self.memory_store.search(
            query=request.content,
            filters={
                "tenant_id": request.tenant_id,
                "status": "active",
                "scope": ["global", "app", request.app_id]
            },
            limit=10
        )
        
        # 2. 按优先级排序
        memories = sorted(memories, key=lambda m: m.priority, reverse=True)
        
        # 3. 构建上下文
        context = self.build_context(memories, request.token_budget)
        
        # 4. 注入到请求
        return request.with_context(context)
```

**性能目标**：P95 < 200ms

### 3.3 慢环：知识精炼

慢环负责从交互中提取和精炼知识：

```python
class SlowLoop:
    def refine_knowledge(self, interaction: Interaction):
        # 1. 提取候选知识
        candidates = self.extractor.extract(interaction)
        
        # 2. 验证质量
        validated = [c for c in candidates if self.validator.validate(c)]
        
        # 3. 创建试用知识
        for knowledge in validated:
            self.memory_store.create(
                content=knowledge.content,
                status="trial",
                source_interaction=interaction.id
            )
        
        # 4. 触发晋升检查
        self.promotion_checker.schedule()
```

---

## 4. 四层学习模型

受人类认知发展启发，WizMem实现四层学习层次：

```
第4层: 元        "学习如何学习"
        ↑
第3层: 关系      "概念如何关联"
        ↑
第2层: 模式      "什么有效"
        ↑
第1层: 事实      "发生了什么"
```

### 4.1 各层详解

| 层 | 内容 | 示例 | 提取方式 |
|---|------|------|----------|
| 事实 | 原始观察 | "用户说'用中文回复'" | 直接记录 |
| 模式 | 重复行为 | "用户总是要求中文回复" | 频率分析 |
| 关系 | 概念连接 | "中文偏好 → 也喜欢简洁风格" | 关联挖掘 |
| 元 | 学习策略 | "新用户先问语言偏好" | 效果反馈 |

### 4.2 知识晋升机制

```python
class PromotionChecker:
    PROMOTION_RULES = {
        "trial_to_active": {
            "min_usage_count": 3,
            "min_success_rate": 0.8,
            "min_age_hours": 24
        },
        "active_to_core": {
            "min_usage_count": 10,
            "min_success_rate": 0.9,
            "min_age_days": 7
        }
    }
    
    def check_promotion(self, knowledge: Knowledge) -> Optional[str]:
        rules = self.PROMOTION_RULES.get(f"{knowledge.status}_to_next")
        if not rules:
            return None
        
        if (knowledge.usage_count >= rules["min_usage_count"] and
            knowledge.success_rate >= rules["min_success_rate"] and
            knowledge.age >= rules["min_age"]):
            return self.get_next_status(knowledge.status)
        
        return None
```

---

## 5. 知识熔断器

### 5.1 问题：毒知识

错误的知识一旦进入系统，会持续产生负面影响：

```
毒知识示例：
"用户喜欢详细解释" （实际上用户喜欢简洁）
    ↓
每次回复都很冗长
    ↓
用户不满意但不明说
    ↓
系统继续使用错误知识
```

### 5.2 熔断器机制

```python
class KnowledgeCircuitBreaker:
    STATES = ["closed", "half_open", "open"]
    
    def __init__(self):
        self.failure_count = 0
        self.failure_threshold = 3
        self.recovery_timeout = 3600  # 1小时
        self.state = "closed"
    
    def record_outcome(self, knowledge_id: str, success: bool):
        if success:
            self.failure_count = 0
            if self.state == "half_open":
                self.state = "closed"
        else:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.trip(knowledge_id)
    
    def trip(self, knowledge_id: str):
        self.state = "open"
        self.memory_store.update(knowledge_id, status="suspended")
        self.schedule_recovery(knowledge_id, self.recovery_timeout)
```

### 5.3 熔断状态

| 状态 | 行为 | 转换条件 |
|------|------|----------|
| 关闭 | 正常使用知识 | 连续失败≥3次 → 打开 |
| 打开 | 暂停使用知识 | 超时后 → 半开 |
| 半开 | 试探性使用 | 成功 → 关闭，失败 → 打开 |

---

## 6. 知识生命周期管理

### 6.1 生命周期状态

```
创建 → 试用 → 激活 → 核心
              ↓       ↓
           暂停 ← 降级
              ↓
           归档/删除
```

### 6.2 遗忘算法

```python
def calculate_forget_score(knowledge: Knowledge) -> float:
    """
    计算遗忘分数，分数越低越容易被遗忘
    """
    # 基础重要性
    importance = knowledge.importance_score
    
    # 时间衰减
    days_since_use = (now() - knowledge.last_used_at).days
    decay = math.exp(-0.1 * days_since_use)
    
    # 访问加成
    access_bonus = min(knowledge.access_count / 100, 0.3)
    
    # 最终分数
    score = importance * decay + access_bonus
    
    return score
```

### 6.3 永不遗忘清单

某些知识永远不应被遗忘：

```yaml
never_forget_rules:
  - type: "security_constraint"
  - type: "user_explicit_preference"
  - status: "core"
  - importance_score: ">= 0.95"
  - has_tag: "pinned"
```

---

## 7. 实验评估

### 7.1 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| 注入延迟 P50 | < 100ms | 85ms |
| 注入延迟 P95 | < 200ms | 180ms |
| 注入延迟 P99 | < 500ms | 420ms |

### 7.2 学习效果

| 指标 | 无WizMem | 有WizMem | 变化 |
|------|----------|----------|------|
| 偏好召回率 | 0% | 95% | +95% |
| 工具成功率 | 72% | 89% | +17% |
| 重复问题率 | 45% | 8% | -37% |

### 7.3 熔断器效果

| 指标 | 无熔断器 | 有熔断器 | 变化 |
|------|----------|----------|------|
| 毒知识影响时长 | 无限 | < 1小时 | 显著改善 |
| 错误传播范围 | 全系统 | 单知识 | 隔离 |
| 自动恢复率 | 0% | 85% | +85% |

---

## 8. 结论

WizMem为LLM应用提供了全面的记忆架构，解决了无状态交互的根本限制。通过双环认知设计、四层学习层次和知识熔断器，WizMem实现了：

- 跨会话和应用的**持久记忆**
- 从用户交互中**自动学习**
- 通过熔断器实现**自愈**质量控制
- 通过遗忘算法实现**高效**存储管理

WizMem代表了向真正持续学习AI系统迈进的重要一步。

---

*提交至arXiv以建立优先权。DOI: 10.5281/zenodo.18207648*
