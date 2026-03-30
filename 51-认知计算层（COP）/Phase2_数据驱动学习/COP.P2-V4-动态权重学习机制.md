# COP · Phase 2 · V4 — 动态权重学习机制

> **启动条件**：Phase 1 上线并积累 **500+条** 真实用户 `/feedback` 数据后启动
> **核心价值**：让系统从"专家规则"升级为"数据驱动"，精度自动提升

---

## 核心思想

> 哪种判定 → 带来好结果 → 强化对应权重
> 哪种判定 → 带来坏结果 → 削弱对应权重

---

## 一、权重结构（新增可训练层）

每个权重值由两层构成：
```json
{
  "base_weight": 3,      // Phase 1 人工定义的初始值（固定）
  "learned_weight": 1.0  // Phase 2 开始随数据动态修正（初始值 1.0）
}
```
实际生效权重：
```
final_weight = base_weight × learned_weight
```

---

## 二、反馈更新规则

| 用户反馈 | 权重修正量 |
|:---|:---|
| `result = "improved"` | `learned_weight += 0.05` |
| `result = "unchanged"` | `learned_weight -= 0.02` |
| `result = "worse"` | `learned_weight -= 0.07` |

**防崩坏限制**：
```python
learned_weight = clamp(learned_weight, 0.5, 1.5)
```

---

## 三、动作效果学习

每个动作独立维护成功率：
```json
{
  "action": "拉群对撞",
  "success_count": 31,
  "fail_count": 12,
  "success_rate": 0.72
}
```

更新逻辑：
```python
if result == "improved":
    success += 1
else:
    fail += 1
success_rate = success / (success + fail)
```

输出时附带置信度：
```json
"actions": [
  {"name": "拉群对撞", "confidence": 0.72},
  {"name": "引入上级决策", "confidence": 0.58}
]
```

---

## 四、Phase 2 启动检查清单

- [ ] `/feedback` 接口数据积累达到 500+ 条
- [ ] 区分"用户确实执行了动作"与"用户未执行"的数据标注
- [ ] 建立 `learned_weight` 存储层（数据库或配置文件均可）
- [ ] 建立动作成功率统计表
- [ ] 设置定期（每月一次）重新训练调度任务
