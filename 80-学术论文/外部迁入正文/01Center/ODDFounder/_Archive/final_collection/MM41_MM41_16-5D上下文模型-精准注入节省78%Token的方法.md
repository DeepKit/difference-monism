# 5D上下文模型：精准注入节省78%Token的方法

> 你给AI塞了一堆上下文，结果它反而更糊涂了？问题出在"精准"二字。

---

## 一、上下文的"三重困境"

用AI写代码，你一定遇到过这些问题：

**困境1：上下文饥饿**
```
你：帮我写一个登录函数
AI：好的，这是一个通用的登录函数...
你：不对，我们用的是Delphi！
AI：抱歉，这是Delphi版本...
你：我们的数据库是PostgreSQL！
AI：好的，我重新写...
```
来回折腾，浪费时间。

**困境2：上下文爆炸**
```
你：（把整个项目文档都塞进去，5万Token）
AI：（超出上下文限制/账单爆炸）
```

**困境3：上下文污染**
```
你：（塞了一堆"可能有用"的信息）
AI：（被无关信息干扰，输出质量下降）
```

## 二、问题的本质

传统的上下文注入是**一维的**——要么全给，要么不给。

但实际上，上下文应该回答**五个问题**：

| 问题 | 传统方法 | 理想方法 |
|------|----------|----------|
| 给什么？ | 全部 | 按类型筛选 |
| 给多少？ | 固定 | 按范围控制 |
| 怎么给？ | 强制塞入 | 按模式注入 |
| 给谁？ | 所有人 | 按角色区分 |
| 何时给？ | 总是 | 按阶段触发 |

这就是**5D上下文模型**的由来。

## 三、五个维度详解

### D1：内容类型（What）

不是所有信息都同等重要：

| 类型 | 示例 | 优先级 |
|------|------|--------|
| 角色定义 | "你是高级Delphi开发者" | 高 |
| 技术栈 | "PostgreSQL + Redis" | 高 |
| 代码规范 | "函数名用fn_前缀" | 中 |
| 历史Bug | "这个模块容易出N+1查询" | 按需 |
| 参考代码 | "参考fn_register的写法" | 按需 |

**原则**：分类管理，按需注入。

### D2：复用范围（Scope）

上下文有不同的"作用域"：

```
global（全局）
  └── app（应用级）
       └── contract（功能级）
            └── task（任务级）
                 └── stage（阶段级）
```

**示例**：
- 全局："永远不要在日志里打印密码"
- 应用级："Progee项目用Delphi开发"
- 功能级："用户模块遵循MVC模式"
- 任务级："当前任务是实现登录"
- 阶段级："现在是代码审查阶段"

**原则**：窄范围继承宽范围，避免重复。

### D3：注入模式（How）

不同信息有不同的注入策略：

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| force | 强制注入，不可跳过 | 安全规则 |
| conditional | 满足条件才注入 | 特定场景知识 |
| recommend | 推荐注入，可被挤掉 | 最佳实践 |
| searchable | 不主动注入，可检索 | 历史知识库 |
| forbidden | 禁止注入 | 敏感信息 |

**示例**：
```yaml
# 安全规则：永远注入
- content: "密码必须用bcrypt加密"
  mode: force

# 最佳实践：推荐注入
- content: "建议使用连接池"
  mode: recommend
  
# 敏感信息：禁止注入给初级开发者
- content: "生产数据库密码：xxx"
  mode: forbidden
  roles: [junior]
```

### D4：角色（Who）

不同角色需要不同的上下文：

| 角色 | 需要 | 不需要 |
|------|------|--------|
| 架构师 | 设计约束、技术选型 | 具体代码实现 |
| 开发者 | 代码规范、API文档 | 测试策略 |
| 测试员 | 验收标准、边界条件 | 设计原理 |

**原则**：角色隔离，各取所需。

### D5：阶段（When）

开发的不同阶段需要不同信息：

| 阶段 | 典型上下文 |
|------|-----------|
| startup | 完整项目背景（冷启动） |
| coding | 代码规范、API、示例 |
| review | 检查清单、反模式 |
| debug | Bug历史、错误模式 |
| seal | 验收标准、完成检查 |

**关键优化**：冷启动 vs 热启动

```
冷启动（首次）：注入完整上下文 → ~6000 tokens
热启动（后续）：只注入增量 → ~2000 tokens

节省：70%
```

## 四、实际效果

我们在Progee平台上应用5D模型，对比数据：

| 方法 | 10个任务总Token | 输出质量 |
|------|-----------------|----------|
| 全量注入 | 80,000 | 60%相关 |
| RAG检索 | 40,000 | 75%相关 |
| **5D模型** | **21,700** | **95%相关** |

**Token节省：78%**
**质量提升：35%**

## 五、核心算法

```python
def inject_context(request, token_budget):
    # 1. 按角色和阶段过滤
    candidates = filter_by_role_stage(
        all_context, 
        request.role, 
        request.stage
    )
    
    # 2. 分离注入模式
    forced = [c for c in candidates if c.mode == 'force']
    conditional = [c for c in candidates if c.mode == 'conditional' and c.condition_met]
    recommended = [c for c in candidates if c.mode == 'recommend']
    
    # 3. 强制内容必须注入
    result = forced
    remaining_budget = token_budget - sum(c.tokens for c in forced)
    
    # 4. 按优先级填充剩余预算
    for item in sorted(conditional + recommended, key=lambda x: x.priority):
        if item.tokens <= remaining_budget:
            result.append(item)
            remaining_budget -= item.tokens
    
    return result
```

## 六、快速上手

你可以从最简单的版本开始：

```python
# 简化版5D模型
context_config = {
    "global": ["安全规则", "公司规范"],
    "app": ["技术栈", "架构说明"],
    "task": ["当前任务描述"],
}

def get_context(scope, role, stage):
    context = []
    # 继承上层scope
    for s in ["global", "app", scope]:
        context.extend(context_config.get(s, []))
    # 按role和stage过滤
    return filter_by_role_stage(context, role, stage)
```

## 七、总结

5D上下文模型的核心思想：

> **不是给AI更多信息，而是给AI更精准的信息**

五个维度帮你回答：
- **What**：给什么类型的信息
- **Scope**：在什么范围内有效
- **How**：以什么方式注入
- **Who**：给谁看
- **When**：什么时候给

掌握这个模型，你的Token账单和AI输出质量都会有质的飞跃。

---

**下一篇预告**：《知识熔断机制：防止"毒知识"污染AI决策》

*作者：付毅 | ODDFounder | ODD方法论创始人*
