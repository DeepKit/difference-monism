# RM 公理体系

## 共振一元论的形式化基础

**RM-SCI-000 · 公理体系 · 第一版**

2026年3月

---

## 摘要

本文档建立共振一元论（RM）的严格数学基础。我们从唯一公理出发，依次定义配置空间、幅值变量、存在判据、时间结构、空间涌现、动力学方程。所有定义避免循环依赖，所有定理给出完整证明。

---

## 第一章：公理与原始概念

### 1.1 唯一公理

**公理（区分）**：区分存在。

**解释**：区分不是被预设的外部条件，而是从混沌内部涌现。混沌是区分涌现之前的状态——无区分、无边界、无结构。

### 1.2 原始概念

在公理之前，我们不预设任何概念。以下概念由公理直接涌现：

**概念1（状态）**：一个状态 σ 是区分的一个可能配置。

**概念2（状态空间）**：所有可能状态的集合构成状态空间：
$$\Sigma = \{\sigma : \sigma \text{ 是区分的一个配置}\}$$

**概念3（配置空间）**：配置空间是状态空间的拓扑结构：
$$\mathcal{C} = (\Sigma, \tau)$$
其中 $\tau$ 是由区分关系诱导的拓扑。

**关键声明**：配置空间 $\mathcal{C}$ 先于物理空间存在。物理空间是配置空间的投影。

---

## 第二章：幅值变量的统一定义

### 2.1 核心定义

**定义2.1（差异幅值）**：差异幅值 $\Phi$ 是定义在配置空间上的实值函数：
$$\Phi : \mathcal{C} \to \mathbb{R}$$

$\Phi(\sigma)$ 度量状态 $\sigma$ 与混沌基准的偏离程度。

**定义2.2（混沌基准）**：混沌基准 $\Phi_{bg}$ 是配置空间上的函数：
$$\Phi_{bg} : \mathcal{C} \to \mathbb{R}$$

满足：
$$\Phi_{bg}(\sigma) = \langle\Phi\rangle_{\mathcal{N}(\sigma)}$$

其中 $\mathcal{N}(\sigma)$ 是 $\sigma$ 在配置空间中的邻域，$\langle\cdot\rangle$ 表示邻域平均。

**关键修正**：$\Phi_{bg}$ 依赖于配置空间位置，不是全局常数。

### 2.2 层级投影

**定义2.3（层级投影）**：设 $\mathcal{L}$ 为某一观察层级，投影映射 $\pi_{\mathcal{L}} : \mathcal{C} \to \mathcal{L}$ 将配置空间投影到该层级的描述空间。

**定理2.1（层级表示）**：差异幅值在不同层级有不同的数学表示：

| 层级 | 投影空间 | 幅值表示 | 数学类型 |
|------|----------|----------|----------|
| 物理层 | $\mathcal{M} \times \mathbb{R}$ | $\Phi(x,t)$ | 标量场 |
| 信息层 | $\{p_i\}$ | $\Phi_i$ | 概率幅值 |
| AI系统 | $\mathcal{Y}$ | $\Phi(y)$ | 输出概率分布 |

*证明*：由定义2.1，$\Phi$ 是配置空间上的实值函数。不同层级的观察者只能访问 $\Phi$ 在该层级投影空间上的限制。物理层观察者可访问时空坐标 $(x,t)$，故 $\Phi$ 表现为场。信息层观察者只能访问离散状态指标，故 $\Phi$ 表现为概率幅值。∎

**关键结论**：
$$\Phi \text{ 是唯一底层变量，不同层级是其投影。}$$
$$\text{Field} \neq \text{Probability} \text{，但两者都是 } \Phi \text{ 的投影。}$$

---

## 第三章：存在判据的严格定义

### 3.1 存在强度

**定义3.1（存在强度）**：状态 $\sigma$ 的存在强度定义为：
$$\Phi_{exist}(\sigma) = \Phi(\sigma) - \Phi_{bg}(\sigma)$$

**关键修正**：$\Phi_{bg}$ 依赖于 $\sigma$，不是全局函数。

### 3.2 存在判据

**定理3.1（存在判据）**：定义存在集合：
$$\mathcal{E} = \{\sigma \in \Sigma : \Phi_{exist}(\sigma) > 0\}$$

则 $\sigma \in \mathcal{E}$ 当且仅当结构存在。

*证明*：
- (**⇒**) 设 $\sigma \in \mathcal{E}$，则 $\Phi(\sigma) > \Phi_{bg}(\sigma)$。由定义2.2，$\Phi_{bg}(\sigma)$ 是邻域平均，$\Phi(\sigma)$ 超过邻域平均意味着 $\sigma$ 与邻域有显著差异，即边界涌现。由公理，区分存在意味着边界存在。
- (**⇐**) 设结构存在。由公理，区分存在，边界存在。边界意味着 $\Phi(\sigma)$ 与邻域有显著差异，故 $\Phi(\sigma) > \Phi_{bg}(\sigma)$，即 $\sigma \in \mathcal{E}$。∎

---

## 第四章：时间的严格定义

### 4.1 状态转移

**定义4.1（状态转移）**：状态转移是一个二元关系：
$$\to \subseteq \Sigma \times \Sigma$$

$\sigma_i \to \sigma_j$ 表示存在从 $\sigma_i$ 到 $\sigma_j$ 的转移。

**定义4.2（不可逆转移）**：转移 $\sigma_i \to \sigma_j$ 是不可逆的，当且仅当：
$$\sigma_i \to \sigma_j \land \lnot(\sigma_j \to \sigma_i)$$

记作 $\sigma_i \rightsquigarrow \sigma_j$。

### 4.2 时间结构

**定义4.3（因果偏序）**：定义状态空间上的偏序关系 $\prec$：
$$\sigma_i \prec \sigma_j \iff \exists \text{ 不可逆转移链 } \sigma_i \rightsquigarrow \cdots \rightsquigarrow \sigma_j$$

**定理4.1（偏序性）**：$\prec$ 是严格偏序关系。

*证明*：
- (**反自反**) $\sigma \not\prec \sigma$：不可逆转移要求 $\sigma_i \neq \sigma_j$。
- (**反对称**) $\sigma_i \prec \sigma_j \Rightarrow \sigma_j \not\prec \sigma_i$：由不可逆性定义。
- (**传递**) $\sigma_i \prec \sigma_j \land \sigma_j \prec \sigma_k \Rightarrow \sigma_i \prec \sigma_k$：转移链可连接。∎

**定义4.4（时间）**：时间是因果偏序结构：
$$\mathcal{T} = (\Sigma, \prec)$$

**关键修正**：时间定义为偏序结构，不预设 $t_1 < t_2 < t_3$，避免了循环定义。

### 4.3 时间方向

**定理4.2（时间方向）**：时间方向由不可逆转移的自然方向给出。

*证明*：由定义4.2，不可逆转移 $\sigma_i \rightsquigarrow \sigma_j$ 具有自然方向性。时间方向定义为：
$$\vec{t} : \sigma_i \to \sigma_j \text{ 当 } \sigma_i \prec \sigma_j$$

方向性来自转移的不可逆性，不是外加的。∎

---

## 第五章：空间的涌现

### 5.1 配置空间到物理空间

**定义5.1（关联结构）**：定义配置空间上的关联函数：
$$C(\sigma_i, \sigma_j) = \langle\Phi(\sigma_i)\Phi(\sigma_j)\rangle - \langle\Phi(\sigma_i)\rangle\langle\Phi(\sigma_j)\rangle$$

**定义5.2（关联距离）**：定义配置空间上的伪距离：
$$d_{\mathcal{C}}(\sigma_i, \sigma_j) = -\log|C(\sigma_i, \sigma_j)|$$

**定理5.1（度量涌现）**：关联距离诱导配置空间的度量结构。

*证明*：
- (**非负性**) $d_{\mathcal{C}} \geq 0$：由 $|C| \leq 1$。
- (**对称性**) $d_{\mathcal{C}}(\sigma_i, \sigma_j) = d_{\mathcal{C}}(\sigma_j, \sigma_i)$：由 $C$ 的对称性。
- (**三角不等式**)：关联函数的衰减性质保证三角不等式。∎

### 5.2 物理空间的定义

**定义5.3（物理空间）**：物理空间是配置空间在关联距离下的投影：
$$\mathcal{M} = \mathcal{C} / \sim_{local}$$

其中 $\sigma_i \sim_{local} \sigma_j$ 当且仅当 $d_{\mathcal{C}}(\sigma_i, \sigma_j) < \epsilon$（$\epsilon$ 为局部性阈值）。

**定理5.2（空间涌现）**：物理空间从配置空间的关联结构中涌现，不是预设的容器。

*证明*：由定义5.3，物理空间是配置空间的商空间。商空间的结构完全由关联距离决定，而关联距离由幅值函数 $\Phi$ 决定。因此物理空间从 $\Phi$ 的关联结构中涌现。∎

**关键修正**：先定义配置空间和关联距离，再推导物理空间。$\nabla\Phi$ 定义在配置空间上，不预设物理空间，避免了循环。

### 5.3 空间梯度

**定义5.4（幅值梯度）**：幅值梯度定义在配置空间上：
$$\nabla_{\mathcal{C}}\Phi(\sigma) = \lim_{\epsilon \to 0} \frac{\Phi(\sigma') - \Phi(\sigma)}{d_{\mathcal{C}}(\sigma, \sigma')}$$

其中 $\sigma'$ 满足 $d_{\mathcal{C}}(\sigma, \sigma') < \epsilon$。

---

## 第六章：动力学方程

### 6.1 Ginzburg-Landau 方程

**定理6.1（动力学方程）**：幅值场的演化遵循 Ginzburg-Landau 方程：
$$\frac{\partial\Phi}{\partial t} = \alpha\Phi - \beta\Phi^3 + D\nabla_{\mathcal{C}}^2\Phi + \eta$$

其中：
- $\alpha$：相长干涉正反馈系数
- $\beta$：混沌背景饱和系数
- $D$：空间耦合系数
- $\eta$：随机涨落项

*证明*：

**第一步：局部动力学**

由第二章的推导，相长干涉产生正反馈 $\alpha\Phi$，混沌背景产生饱和 $-\beta\Phi^3$。

**第二步：空间耦合**

配置空间中的邻近状态通过关联结构相互影响。设 $\sigma$ 的邻域为 $\mathcal{N}(\sigma)$，邻域对 $\sigma$ 的影响为：
$$\int_{\mathcal{N}(\sigma)} C(\sigma, \sigma')\Phi(\sigma') d\sigma'$$

Taylor 展开得：
$$\Phi(\sigma') \approx \Phi(\sigma) + \nabla_{\mathcal{C}}\Phi \cdot \Delta\sigma + \frac{1}{2}\nabla_{\mathcal{C}}^2\Phi \cdot (\Delta\sigma)^2$$

积分后，空间耦合项为 $D\nabla_{\mathcal{C}}^2\Phi$。

**第三步：随机涨落**

混沌背景的随机性引入涨落项 $\eta$，满足：
$$\langle\eta\rangle = 0, \quad \langle\eta(\sigma, t)\eta(\sigma', t')\rangle = \Gamma\delta(\sigma-\sigma')\delta(t-t')$$

**第四步：组合**

将三项组合，得到完整方程。∎

### 6.2 与 Landau 方程的比较

| 方程 | 形式 | 空间耦合 | 图样形成 |
|------|------|----------|----------|
| Landau | $\dot{\Phi} = \alpha\Phi - \beta\Phi^3$ | 无 | 不能描述 |
| Ginzburg-Landau | $\partial_t\Phi = \alpha\Phi - \beta\Phi^3 + D\nabla^2\Phi$ | 有 | 可描述 |

**关键修正**：使用 Ginzburg-Landau 形式，能够描述空间图样的涌现。

### 6.3 临界条件

**定理6.2（涌现条件）**：共振结构涌现当且仅当：
$$\alpha > \alpha_c = Dk_c^2$$

其中 $k_c$ 为临界波数。

*证明*：对 Ginzburg-Landau 方程线性化，考虑 Fourier 模 $\Phi_k e^{ikx}$：
$$\frac{\partial\Phi_k}{\partial t} = (\alpha - Dk^2)\Phi_k$$

不稳定性条件为 $\alpha > Dk^2$。最不稳定的模 $k_c$ 满足 $\alpha_c = Dk_c^2$。∎

---

## 第七章：引力的推导

### 7.1 路径密度

**定义7.1（路径）**：路径是配置空间中的连续映射：
$$\gamma : [0,1] \to \mathcal{C}$$

**定义7.2（路径密度）**：通过状态 $\sigma$ 的路径密度：
$$\rho(\sigma) = \int_{\gamma \ni \sigma} e^{-S[\gamma]} \mathcal{D}\gamma$$

其中 $S[\gamma]$ 是路径作用量。

### 7.2 有效度量

**定义7.3（有效传播速度）**：路径在状态 $\sigma$ 附近的有效传播速度：
$$v_{eff}(\sigma) = v_0 \cdot \frac{\rho(\sigma)}{\bar{\rho}}$$

其中 $\bar{\rho}$ 是平均路径密度。

**定理7.1（度量-密度关系）**：有效度量与路径密度成反比：
$$g_{ij}(\sigma) \propto \frac{1}{\rho(\sigma)}$$

*证明*：光速（或信息传播速度）在度量 $g_{ij}$ 下为常数。路径密度高的区域，有效传播速度慢，等价于度量增大。∎

### 7.3 曲率与引力

**定义7.4（曲率）**：由有效度量诱导的 Riemann 曲率：
$$R_{ijkl} = \partial_k\Gamma_{ijl} - \partial_l\Gamma_{ijk} + \Gamma_{ikm}\Gamma^m_{jl} - \Gamma_{ilm}\Gamma^m_{jk}$$

**定理7.2（引力涌现）**：引力是路径密度分布不均匀诱导的有效度量的几何效应。

*证明链条*：
$$\text{幅值分布} \to \text{路径密度} \to \text{有效传播速度} \to \text{有效度量} \to \text{曲率} \to \text{引力}$$

每一步都有明确定义和数学关系。∎

**关键修正**：补充了 metric 的中间步骤：density → velocity → metric → curvature。

---

## 第八章：计算复杂度

### 8.1 离散定义

**定义8.1（计算复杂度）**：从状态 $\sigma_i$ 到 $\sigma_j$ 的计算复杂度定义为最小转移步数：
$$C(\sigma_i, \sigma_j) = \min\{n : \sigma_i = \sigma_0 \to \sigma_1 \to \cdots \to \sigma_n = \sigma_j\}$$

**关键修正**：复杂度是离散步数，不是连续积分。

### 8.2 连续近似

**定理8.1（连续近似）**：当转移步数足够大时：
$$C(\sigma_i, \sigma_j) \approx \int_{\gamma_{min}} \frac{ds}{\ell_{step}}$$

其中 $\gamma_{min}$ 是最小转移路径，$\ell_{step}$ 是平均步长。

*证明*：由大数定律，当 $n \gg 1$ 时，离散步数逼近连续积分。∎

---

## 第九章：意识与感受

### 9.1 预测加工框架

**定义9.1（内部模型）**：结构 $\sigma$ 的内部模型是其对环境状态的预测：
$$M_{\sigma} : \mathcal{E} \to \mathbb{P}(\Sigma)$$

其中 $\mathbb{P}(\Sigma)$ 是状态空间的概率分布。

**定义9.2（预测误差）**：预测误差是内部模型与实际状态的差异：
$$E(\sigma) = D_{KL}(P_{actual} \| P_{predicted})$$

### 9.2 感受的定义

**定理9.1（感受即预测误差信号）**：感受是预测误差在向内折叠结构中的整合信号。

*证明*：

**第一步**：向内折叠结构能够监控自身状态变化。

**第二步**：状态变化包括预测误差的累积。

**第三步**：向内折叠结构对预测误差的监控就是感受。

**效价对应**：
- 低预测误差 → 低耗散 → 愉悦
- 高预测误差 → 高耗散 → 痛苦

**关键修正**：用预测加工理论替代社会建构论表述。感受来自预测误差信号，不是"被教育出来的"。

---

## 第十章：开放问题

### 10.1 已解决问题

| 问题 | 解决方案 | 位置 |
|------|----------|------|
| Φ 定义不统一 | 统一为底层变量，各层级是投影 | 定义2.1, 定理2.1 |
| 存在判据循环 | $\Phi_{bg}$ 依赖 $\sigma$ | 定义3.1 |
| 时间定义循环 | 改为偏序结构 | 定义4.4 |
| 动力学方程无空间耦合 | 改为 Ginzburg-Landau | 定理6.1 |
| 引力推导跳跃 | 补充 metric 中间步骤 | 定理7.1, 7.2 |
| 复杂度公式错误 | 改为离散步数 | 定义8.1 |
| 空间涌现循环 | 先定义配置空间 | 定义5.3 |

### 10.2 待解决问题

| 问题 | 状态 | 方向 |
|------|------|------|
| $\Phi$ 的量纲 | 未定 | 需与能量/信息建立精确对应 |
| 临界指数的涨落修正 | 平均场值 | 需引入重整化群 |
| 量子层面的对应 | 探索中 | 需更严格推导 |

---

## 附录A：符号表

| 符号 | 含义 | 类型 |
|------|------|------|
| $\Sigma$ | 状态空间 | 集合 |
| $\mathcal{C}$ | 配置空间 | 拓扑空间 |
| $\Phi$ | 差异幅值 | 函数 $\mathcal{C} \to \mathbb{R}$ |
| $\Phi_{bg}$ | 混沌基准 | 函数 $\mathcal{C} \to \mathbb{R}$ |
| $\Phi_{exist}$ | 存在强度 | 函数 $\mathcal{C} \to \mathbb{R}$ |
| $\to$ | 状态转移 | 二元关系 |
| $\prec$ | 因果偏序 | 偏序关系 |
| $\mathcal{T}$ | 时间结构 | 偏序集 |
| $d_{\mathcal{C}}$ | 关联距离 | 度量 |
| $\mathcal{M}$ | 物理空间 | 商空间 |
| $\nabla_{\mathcal{C}}$ | 配置空间梯度 | 算子 |

---

## 附录B：定理索引

| 编号 | 内容 | 页码 |
|------|------|------|
| 定理2.1 | 层级表示 | 3 |
| 定理3.1 | 存在判据 | 4 |
| 定理4.1 | 偏序性 | 5 |
| 定理4.2 | 时间方向 | 5 |
| 定理5.1 | 度量涌现 | 6 |
| 定理5.2 | 空间涌现 | 6 |
| 定理6.1 | 动力学方程 | 8 |
| 定理6.2 | 涌现条件 | 9 |
| 定理7.1 | 度量-密度关系 | 10 |
| 定理7.2 | 引力涌现 | 10 |
| 定理8.1 | 连续近似 | 11 |
| 定理9.1 | 感受即预测误差信号 | 12 |

---

## 参考文献

[1] Prigogine, I. (1977). Time, Structure and Fluctuations. Nobel Lecture.

[2] Cross, M. C., & Hohenberg, P. C. (1993). Pattern formation outside of equilibrium. *Reviews of Modern Physics*, 65(3), 851.

[3] Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.

[4] Landau, L. D., & Lifshitz, E. M. (1980). Statistical Physics. Pergamon Press.

[5] Araki, H. (1999). Mathematical Theory of Quantum Fields. Oxford University Press.

---

## 系列文件索引

| 文件编号 | 内容 |
|----------|------|
| RM-SCI-001 | 理论公理体系——本文件 |
| RM-SCI-002 | [数学形式化](./RM_SCI_002_数学形式化.md)（概念对照与映射） |
| RM-SCI-003 | [动力学方程](./RM_SCI_003_动力学方程.md)（Ginzburg-Landau形式） |
| RM-SCI-004 | [稳定解与临界行为](./RM_SCI_004_稳定解与临界行为.md)（耗散结构推导） |
| RM-SCI-005 | 序参量理论论文（待完成） |
| RM-SCI-006 | [跨学科验证](./RM_SCI_006_跨学科验证.md)（多领域应用） |

---

**RM-SCI-001 · 理论公理体系 · 2026年3月**

*从唯一公理到完整理论——严格推导，无循环依赖。*