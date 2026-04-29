# SlideFold：面向LLM应用的多级滑动窗口记忆压缩技术

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **状态**: 预印本（用于arXiv提交）
> **关键词**: 记忆压缩, LLM, 滑动窗口, Token优化, 上下文管理

---

## 摘要

LLM应用中的记忆管理面临根本性挑战：对话历史和知识库随时间无限增长，而上下文窗口和Token预算有限。现有方法要么简单截断（丢失重要信息），要么全量保留（成本爆炸）。本文介绍**SlideFold**，一种多级滑动窗口压缩技术，通过N级递归压缩实现理论上无限的记忆容量。

核心创新包括：(1) **N级滑动压缩**架构，每级压缩比可配置；(2) **Hot/Warm/Cold三级存储**策略，按访问频率分层；(3) **情景→语义记忆转化**机制，将具体事件抽象为通用知识。在WizAxis平台的实验中，SlideFold实现了**73%的Token节省**，同时保持95%的关键信息召回率。

---

## 1. 引言

### 1.1 记忆增长问题

LLM应用的记忆随使用时间线性增长：

```
第1天:   100条记忆 →   50K tokens
第30天:  3000条记忆 → 1.5M tokens
第365天: 36000条记忆 → 18M tokens
```

**问题**：
- 上下文窗口有限（128K-200K tokens）
- Token成本随记忆量线性增长
- 检索延迟随数据量增加

### 1.2 现有方法的局限

| 方法 | 描述 | 问题 |
|------|------|------|
| 简单截断 | 保留最近N条 | 丢失重要历史 |
| 全量保留 | 保留所有记忆 | 成本爆炸 |
| 固定摘要 | 定期生成摘要 | 信息损失不可控 |
| FIFO队列 | 先进先出 | 不考虑重要性 |

### 1.3 SlideFold方案

我们提出**SlideFold**，核心思想：

> **不是删除旧记忆，而是压缩旧记忆**

```
原始记忆 → 一级压缩 → 二级压缩 → ... → N级压缩
(详细)      (摘要)      (要点)          (精华)
```

**关键特性**：
- 理论上无限级压缩
- 每级压缩比可配置
- 重要信息永不丢失

---

## 2. SlideFold架构

### 2.1 多级压缩模型

```
┌─────────────────────────────────────────────────────────────┐
│                    SlideFold 多级压缩                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Level 0 (原始)     Level 1 (压缩)    Level 2 (高度压缩)    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │ 完整对话    │   │ 对话摘要    │   │ 关键要点    │       │
│  │ 100% tokens │──▶│ 30% tokens  │──▶│ 10% tokens  │       │
│  │ 最近7天     │   │ 7-30天      │   │ 30天以上    │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│                                                             │
│  压缩触发: 窗口满 → 滑动 → 压缩最旧部分 → 推入下一级        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 滑动窗口机制

```python
class SlidingWindow:
    def __init__(self, level: int, config: WindowConfig):
        self.level = level
        self.max_items = config.max_items[level]
        self.compression_ratio = config.compression_ratio[level]
        self.items = []
    
    def add(self, item: MemoryItem):
        self.items.append(item)
        
        if len(self.items) > self.max_items:
            self.slide()
    
    def slide(self):
        # 取出最旧的一批
        to_compress = self.items[:self.batch_size]
        self.items = self.items[self.batch_size:]
        
        # 压缩并推入下一级
        compressed = self.compress(to_compress)
        self.next_level.add(compressed)
    
    def compress(self, items: List[MemoryItem]) -> MemoryItem:
        # 使用LLM进行压缩
        prompt = f"将以下{len(items)}条记忆压缩为一条摘要，保留关键信息：\n"
        prompt += "\n".join([item.content for item in items])
        
        summary = self.llm.generate(prompt, max_tokens=self.target_tokens)
        
        return MemoryItem(
            content=summary,
            level=self.level + 1,
            source_count=len(items),
            importance=max(item.importance for item in items)
        )
```

### 2.3 压缩配置示例

```yaml
slidefold_config:
  levels:
    - level: 0
      name: "原始"
      max_items: 100
      max_age_days: 7
      compression_ratio: 1.0
      
    - level: 1
      name: "摘要"
      max_items: 50
      max_age_days: 30
      compression_ratio: 0.3
      
    - level: 2
      name: "要点"
      max_items: 20
      max_age_days: 90
      compression_ratio: 0.1
      
    - level: 3
      name: "精华"
      max_items: 10
      max_age_days: null  # 永久
      compression_ratio: 0.03
```

---

## 3. Hot/Warm/Cold存储策略

### 3.1 三级存储模型

| 层级 | 温度 | 存储位置 | 访问延迟 | 成本 |
|------|------|----------|----------|------|
| Hot | 热 | 内存/Redis | < 10ms | 高 |
| Warm | 温 | PostgreSQL | < 100ms | 中 |
| Cold | 冷 | 对象存储 | < 1s | 低 |

### 3.2 温度计算

```python
def calculate_temperature(memory: Memory) -> str:
    # 基于访问频率和时间
    recency_score = 1.0 / (1 + days_since_access(memory))
    frequency_score = min(memory.access_count / 10, 1.0)
    importance_score = memory.importance
    
    temperature = (
        recency_score * 0.4 +
        frequency_score * 0.3 +
        importance_score * 0.3
    )
    
    if temperature > 0.7:
        return "hot"
    elif temperature > 0.3:
        return "warm"
    else:
        return "cold"
```

### 3.3 自动迁移

```python
class TemperatureMigrator:
    def migrate(self):
        # Hot → Warm: 7天未访问
        hot_memories = self.get_hot_memories()
        for memory in hot_memories:
            if days_since_access(memory) > 7:
                self.move_to_warm(memory)
        
        # Warm → Cold: 30天未访问
        warm_memories = self.get_warm_memories()
        for memory in warm_memories:
            if days_since_access(memory) > 30:
                self.move_to_cold(memory)
        
        # Cold → Warm: 被访问时自动升温
        # (在查询时处理)
```

---

## 4. 情景→语义记忆转化

### 4.1 认知科学基础

人类记忆分为：
- **情景记忆**：具体事件（"昨天我吃了披萨"）
- **语义记忆**：通用知识（"披萨是意大利食物"）

SlideFold模拟这一过程：

```
情景记忆（Level 0-1）→ 语义记忆（Level 2+）

示例：
情景: "2026-01-05 用户要求用中文回复"
情景: "2026-01-06 用户再次要求中文"
情景: "2026-01-07 用户说'请用中文'"
      ↓ 压缩转化
语义: "用户偏好中文回复"
```

### 4.2 转化算法

```python
class EpisodicToSemanticConverter:
    def convert(self, episodes: List[Memory]) -> Memory:
        # 1. 提取共同模式
        patterns = self.extract_patterns(episodes)
        
        # 2. 生成语义知识
        prompt = f"""
        分析以下{len(episodes)}条情景记忆，提取通用知识：
        
        {self.format_episodes(episodes)}
        
        输出格式：
        - 通用知识点（不含具体时间/地点）
        - 置信度（基于出现频率）
        """
        
        semantic = self.llm.generate(prompt)
        
        return Memory(
            content=semantic,
            type="semantic",
            confidence=self.calculate_confidence(episodes),
            source_episodes=len(episodes)
        )
```

---

## 5. 实验评估

### 5.1 实验设置

- **数据集**：WizAxis平台30天真实对话数据
- **记忆量**：初始5000条，约2.5M tokens
- **基线方法**：简单截断、FIFO、固定摘要

### 5.2 Token节省

| 方法 | 保留Token | 节省率 | 信息召回 |
|------|-----------|--------|----------|
| 全量保留 | 2.5M | 0% | 100% |
| 简单截断 | 500K | 80% | 45% |
| FIFO | 500K | 80% | 52% |
| 固定摘要 | 600K | 76% | 78% |
| **SlideFold** | **675K** | **73%** | **95%** |

### 5.3 关键发现

1. **73%Token节省**：从2.5M降至675K
2. **95%信息召回**：关键信息几乎无损
3. **压缩质量**：LLM压缩优于规则压缩
4. **分层效果**：Hot/Warm/Cold显著降低延迟

---

## 6. 结论

SlideFold提供了一种实用的LLM记忆压缩方案：

- **多级滑动压缩**：理论上无限容量
- **三级存储策略**：平衡性能与成本
- **情景→语义转化**：模拟人类记忆机制
- **73%Token节省**：显著降低运营成本

该技术已在WizAxis平台生产环境部署，服务1200+日活用户。

---

*提交至arXiv以建立优先权。DOI: 10.5281/zenodo.18207648*
