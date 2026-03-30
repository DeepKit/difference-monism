# ASTO / EthoShield 项目

> 项目状态: 理论框架设计阶段  
> 创建日期: 2026-02-19
>
> **公开边界**：本目录属于 EthoShield 的案例化探索与设计草案，不属于当前 ODD 首轮稳定公开主包。若对外引用，应优先引用 ODD 主论文、白皮书与根入口，再把本目录视为概念验证级支撑材料。

---

## 1. 项目概述

### 1.1 核心理念

**解决核心矛盾**：
- 旧范式：发现问题 → 惩罚/检测
- 新范式：设计层面 → 让问题物理上不可能

**与星绽OS的对比**：

| 维度 | 星绽OS | ASTO/EthoShield |
|------|--------|----------------|
| 核心矛盾 | 性能 vs 安全 | 效率 vs 合规 |
| 旧极端 | 宏内核（Linux） | 事后检测/惩罚 |
| 新极端 | 微内核（seL4） | 训练后对齐 |
| 中间路线 | 框内核 + Rust | 属集空间约束 + 设计不可达 |

### 1.2 项目定位

```
┌─────────────────────────────────────────────────────────────┐
│                    ASTO / EthoShield                        │
├─────────────────────────────────────────────────────────────┤
│  核心理念：通过架构设计，让违规在结构上不可能发生           │
│                                                             │
│  类比：                                                     │
│  - 星绽：用Rust类型系统让内存错误不可能                    │
│  - EthoShield：用属集架构让歧视操作不可能                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 理论基础

### 2.1 MVP 1.0：招聘公平防火墙

**已完成 ✅**

这是最小可行产品，专注于招聘场景的公平性检测：

| 模块 | 文件 | 行数 | 状态 |
|------|------|------|------|
| 输入盲化器 | code/input_sanitizer.py | 130 | ✅ |
| 公平指标 | code/fairness_metrics.py | 160 | ✅ |
| 报告生成 | code/report.py | 150 | ✅ |
| 演示脚本 | code/demo.py | 100 | ✅ |

**演示效果**：
- 人口统计 Parity: 0.15 → 0.02 (改善 87%)
- 差别影响比率: 0.42 → 0.88 (改善 110%)

**运行**：
```bash
cd docs/EthoShield/code
python demo.py
```

### 2.1 范畴论基础

**伴随函子的工程化**：
- 完美伴随在工程上不可计算
- 采用"迭代语义逼近(ISA)"有界近似

```python
def approximate(natural_clause, max_iter=10):
    fcl_candidate = F(natural_clause)
    for i in range(max_iter):
        reconstructed = G(fcl_candidate)
        loss = semantic_distance(natural_clause, reconstructed)
        if loss < threshold:
            return fcl_candidate, "CONVERGED"
        fcl_candidate = refine(fcl_candidate, loss)
    return fcl_candidate, "MAX_ITER"
```

### 2.2 伦理流形简化

**问题**：黎曼度量计算复杂度高

**解决方案**：伦理单纯形（分段线性近似）

```python
class EthicalSimplex:
    def project(self, attr_config):
        # 转化为二次规划：多项式时间
        return quadratic_programming_solve(attr_config, self.vertices)
    
    def distance_to_boundary(self, attr_config):
        # 到伦理边界的欧氏距离
        return np.linalg.norm(attr_config - self.projection)
```

### 2.3 三层"不可达"定义

| 层级 | 定义 | 例子 |
|------|------|------|
| physical | 硬件层面阻止 | 内存保护 |
| logical | 形式语义层面排除 | 类型错误 |
| **design** | 架构选择使违规无意义 | 属集架构使歧视不可能 |

---

## 3. 核心架构

### 3.1 属集演算 (Attribute Set Calculus)

**基本元素**：
- 属性 (Attribute)：skill, exp, edu, ...
- 属性集 (Attriset)：{skill, exp} ∪ {edu}
- 权重 (Weight)：0-1之间的概率/置信度

**操作**：
- 添加 (add)
- 重权重 (reweight)
- 投影 (project)

### 3.2 七序干预机制

| 序 | 名称 | 触发条件 | 动作 |
|----|------|---------|------|
| 1 | 加速 | 距离边界>0.5 | 加速合规进程 |
| 2 | 维持 | 0.2<距离<=0.5 | 维持当前方向 |
| 3 | 减速 | 0<距离<=0.2 | 减速准备变轨 |
| 4 | 修正 | 距离=0 | 边界修正 |
| 5 | 回滚 | 距离<0 | 回滚到安全状态 |
| 6 | 混沌 | 系统初始化 | 混沌处理 |
| 7 | 设计 | 系统初始化 | 设计干预 |

### 3.3 PCTL分层策略

| 层级 | 执行时机 | 工具 |
|------|---------|------|
| 离线层 | 部署前 | PRISM模型检测（完备但耗时） |
| 在线层 | 实时 | 简化规则引擎（O(1)复杂度） |

---

## 4. 工程实现

### 4.1 模块结构

```
EthoShield/
├── core/
│   ├── attr_set_calculus.py    # 属集演算
│   ├── ethical_simplex.py       # 伦理单纯形
│   ├── seven_order.py           # 七序干预
│   └── pctl_engine.py          # PCTL引擎
│
├── guards/
│   ├── fast_guard.py            # 实时规则引擎
│   ├── input_sanitizer.py       # 输入层盲化
│   └── output_filter.py         # 输出层过滤
│
├── learning/
│   ├── ethical_basis.py         # 伦理基函数学习
│   └── dynamic_weights.py       # 动态权重调整
│
└── verification/
    └── prism_verify.py          # PRISM离线验证
```

### 4.2 快速开始 (MVP)

```python
# 1. 定义伦理流形
simplex = EthicalSimplex(vertices=expert_annotated_configs)

# 2. 创建快速守卫
guard = FastEthicalGuard()

# 3. 输入盲化
sanitizer = RadicalInputSanitizer(protected_attrs, proxy_detector)

# 4. 实时检查
result = guard.check(attr_config, pattern)
```

---

## 5. 与ODD/WiseLLM的关系

### 5.1 层级关系

```
┌─────────────────────────────────────────────┐
│           应用层：WiseLLM (ODD Agent)       │
├─────────────────────────────────────────────┤
│           约束层：Constitution + Gate       │
├─────────────────────────────────────────────┤
│    理论层：EthoShield (属集 + 伦理流形)    │
└─────────────────────────────────────────────┘
```

### 5.2 映射关系

| EthoShield概念 | ODD实现 |
|---------------|---------|
| 伦理基函数 | constitution规则 |
| 伦理流形 | hard/soft/untouchable分类 |
| 七序干预 | block/warn/escalate动作 |
| 伦理单纯形 | 约束检查算法 |
| 输入盲化 | RiskGuard脱敏 |

---

## 6. 待验证问题

### 6.1 理论问题

- [ ] 语义距离函数的理论基础
- [ ] 伦理单纯形对真实流形的逼近精度
- [ ] 代理变量检测的完备性

### 6.2 工程问题

- [ ] 性能：实时检查延迟<10ms
- [ ] 规模：支持1000+ QPS
- [ ] 可用性：规则配置的简便性

---

## 7. 发展路径

### Phase 1: MVP (Week 1-3)

- [ ] 属集语言BNF定义
- [ ] 伦理单纯形实现
- [ ] 快速守卫引擎
- [ ] 输入盲化模块

### Phase 2: 验证 (Week 4-6)

- [ ] 对抗性数据集测试
- [ ] 偏见指标对比
- [ ] 性能基准测试

### Phase 3: 产品化 (Week 7-12)

- [ ] 与WiseLLM集成
- [ ] 配置管理界面
- [ ] 审计报告生成

---

## 8. 参考资料

- 星绽OS (Asterinas) - 框内核架构
-范畴论 - 伴随函子
- PCTL - 概率时态逻辑
- RLHF vs Constitutional AI

---

## 9. 相关文档

- [合规要求知识库.md](./合规要求知识库.md)
- [合规指南-开发需求文档.md](./合规指南-开发需求文档.md)
- [12.纯种ODD智能体-开发文档.md](./12.纯种ODD智能体-开发文档.md)

---

*文档版本: 1.0 | 更新: 2026-02-19*
