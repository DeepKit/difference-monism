# **ASTO19. 附录：术语表与工程映射**

> **Version**: Γ.11 (The Dictionary)
> **Status**: Living Document
> **作者**: Fuyi (ODDFounder fuyi.it@live.cn)
> **Context**: 本文档是 属集变迁存在论(ASTO) 体系的工具书。它包含两个部分：
> 1.  **核心术语表 (Glossary)**：定义 ASTO 的专用词汇。
> 2.  **工程映射表 (Concept Mapping)**：将 ASTO 哲学映射到 ODD 软件工程实体。

---

## **第一部分：核心术语表 (Glossary)**

### **1. 本体论基础 (Ontology)**

| 术语 (CN) | Term (EN) | 定义 |
| :--- | :--- | :--- |
| **属集** | **Attribute-Set** | 存在的最小单元。不是实体，而是属性在特定时空下的暂时聚合。工程上指可序列化、可被函数调用的状态向量。 |
| **结构** | **Structure** | 维持属集不散的最小内耗构型。既是支撑，也是牢笼。 |
| **动变性** | **Motility** | 驱动系统演化的因果倾向。动变性不是人类独有，所有存在物都有动变性。根据因果机制复杂度分为四类：**本律式**（环境条件变化引发确定性反应，无主体、唯律而行）、**涌现式**（微观交互产生宏观模式）、**目标式**（预设目标驱动反馈调节）、**建模式**（修改自身认知模型）。详见 [ASTO06 § 动变性四分类](./ASTO06.公理.Proto.v8.0.md)。 |
| **场域** | **Field** | 所有属集及其相互作用的总和。 |

### **2. 形态学 (Morphology - 五态)**

| 术语 (CN) | Term (EN) | 定义 | 代码映射 |
| :--- | :--- | :--- | :--- |
| **自在态** | **In-itself** | 未被问责、未被解释的存在。 | Legacy Code, Firmware |
| **共识态** | **Consensus** | 正在涌现、尚未固化的理解。 | RFC, Specs |
| **编码态** | **Encoded** | 被形式化记录的规范蓝图。 | Source Code, Smart Contract |
| **物化态** | **Materialized** | 获得强制力、正在运行的系统。 | Running Pod, Binary |
| **定向态** | **Oriented** | 对自身进行反思与重构的时刻。 | Refactoring, Hotfix |

### **3. 动力学 (Dynamics - 六阶)**

| 术语 (CN) | Term (EN) | 定义 | 运维映射 |
| :--- | :--- | :--- | :--- |
| **混沌** | **Chaos** | 无结构的高熵状态。 | Incident, War Room |
| **秩序** | **Order** | 结构与环境匹配的稳态。 | Stable Release |
| **流变** | **Flux** | 环境变而结构未变，张力积累。 | Tech Debt, Latency |
| **脉冲** | **Pulse** | 局部压力突破阈值。 | Alert, Circuit Break |
| **崩解** | **Collapse** | 结构彻底失效。 | Downtime, Outage |
| **归元** | **Return** | 结构重组，跃迁至新稳态。 | Upgrade, Migration |

### **4. 治理与规范 (Governance)**

| 术语 (CN) | Term (EN) | 定义 |
| :--- | :--- | :--- |
| **EN** | **Executable Norm** | 可执行规范。机器可自动处理的逻辑。 |
| **NEN** | **Non-Executable Norm** | 不可执行规范。需人类价值判断的领域。 |
| **NCP** | **Normative Consensus Protocol** | 规范共识协议。不同平台间交换张力与规则的通信标准。 |
| **对话平台** | **Dialogue Platform** | 连接五态、将言语转化为结构的工程界面。 |

### 5. 介入相 (Intervention - 七序)

| 术语 (CN) | Term (EN) | 定义 | 动作 |
| :--- | :--- | :--- | :--- |
| **觉醒** | **Awakening** | 意识到"我不只是用户，我是编织者"。 | Awareness, Intent |
| **感知** | **Perceive** | 捕捉场域中的微弱信号，看见"自在态"。 | Monitoring, Sensing |
| **解析** | **Resolve** | 定位核心矛盾，诊断结构问题。 | Diagnosis, Analysis |
| **干预** | **Intervene** | 制定方案，进行场域层面的调制。 | Planning, RFC |
| **设计** | **Design** | 构建新结构，将意图转化为蓝图。 | Architecture, Design |
| **物化** | **Materialize** | 落地执行，注入算力运行。 | Coding, Deploy |
| **回溯** | **Retrospect** | 复盘效果，验证预期与结果的偏差。 | Review, Testing |
| **消解** | **Dissolve** | 结构完成使命，清理脚手架，回归自然。 | Deprecate, Cleanup |

---

## **第二部分：ASTO-ODD 工程映射表**

ASTO 认为：**软件工程是人类唯一能完全掌控“属性结构”上帝视角的领域。** ODD (Output-Driven Development) 是 ASTO 的数字实验室。

### **1. 核心本体映射**

| ASTO 物理概念 | ODD 工程实体 | 映射逻辑 |
| :--- | :--- | :--- |
| **规范 (Norm)** | **契约 (Contract)** | 定义了什么是“合规的稳态”。不符合契约的代码无法被系统接受。 |
| **环境 (Environment)** | **需求与算力 (Context)** | 需求变更是环境压力。当旧代码无法支撑新需求时，Bug（张力）产生。 |
| **动变性对话平台** | **流水线 (Pipeline)** | CI/CD 是人工构建的通道，它加速了从“意图”到“产出物”的转化。 |
| **跃迁 (Transition)** | **版本升级 (Versioning)** | 当旧契约无法承载新需求，系统必须经历 Breaking Change。 |
| **稳态 (Homeostasis)** | **已封印产出物 (Artifact)** | 通过验证并被“封印”的 Docker 镜像，是能量最低点。 |

### **2. 规范类型的工程映射**

| 规范类型 | 含义 | ODD 对应实体 | 例子 |
| :--- | :--- | :--- | :--- |
| **EN (可执行)** | 可自动化判定 | **Automated Tests** | CI 脚本中的 `assert` 语句。 |
| **NEN (不可执行)** | 需人类判定 | **Code Review** | “代码风格应简洁”、“架构应高内聚”。 |

> **ODD 原则**：将 EN 全部交给 Pipeline 自动执行；将 NEN 明确标记并在 Review 环节由人工确认。

### **3. 动力学映射**

| ASTO 阶段 | ODD 阶段 | 现象描述 |
| :--- | :--- | :--- |
| **混沌** | **初始化** | 只有模糊想法，没有代码。 |
| **秩序** | **v1.0 发布** | 代码通过测试，稳定运行。 |
| **流变** | **技术负债** | 业务激增，架构老化，改动困难。 |
| **脉冲** | **报警** | 频繁 Bug，团队讨论重构。 |
| **跃迁** | **v2.0 重构** | 废弃旧契约，发布新架构。 |

### **4. 政治映射**

|| ASTO 政治概念 | ODD 技术实现 |
|| :--- | :--- |
|| **平台构建权** | **Pull Request (PR)**：任何人都可以提交代码，但必须通过 CI 验证。 |
|| **张力可视化** | **Issue Tracker**：Bug 是环境张力的可视化仪表盘。 |
|| **红绿灯协议** | **Gatekeeper**：CI 是绿灯；Review 是黄灯；架构委员会是红灯。 |
|| **反极权** | **Fork 机制**：如果核心团队堵塞了变革，社区可以 Fork 项目。 |

### **5. 工程实践机制 (Engineering Practices)**

|| 实践机制 | Term (EN) | ASTO 解释 | ODD 工程对应 |
|| :--- | :--- | :--- | :--- |
|| **对抗测试** | **Adversarial Testing** | 人为构造高张力“恶劣场域”，让系统在脉冲/崩解边缘暴露结构裂纹；用小脉冲替代大崩解，把隐性禁元与隐性基元提前显性化。 | Red Team、Fuzzing、Property-based Testing、Chaos Engineering、Mutation Testing |
|| **赛马机制** | **Horse Race Mechanism** | 并行建桥、证据化裁决、可回滚淘汰：把变迁从一次性豪赌改成可观测、可控的并行实验；以主目标 + 护栏指标 + 禁元红线共同裁决。 | Shadow Traffic、Canary、A/B Test、Bandit、Feature Flag、Metrics/Tracing |
|| **封板/解封** | **Seal/Unseal (Freeze/Unfreeze)** | 将胜者固化为“可上线稳态”，冻结其契约与关键行为边界；当需求/契约变化必须发生时，由人类主权发起“可回滚的小升级循环”（解封→赛马→对抗→再封板），防止偷渡变更或僵化。 | Release Freeze、Branch Protection、Artifact Versioning、Rollback Plan、Change Control |
|| **封板承诺包** | **Seal Bundle / Seal Bundle Manifest (SBM)** | 在网络/边缘/分布式场域下，封板对象是一份可签字的稳态承诺包：版本、契约、依赖窗口、发布路径、收敛目标、回滚方案、证据与审计；用于把封板变成可执行规范（CI 门禁可审计）。 | `release/seal-bundle.yaml`、CI Gatekeeper、Artifact Attestation/SBOM、Approval/Signature |

> 延伸：详见 **ASTO-Ext.09 工程实践指南：对抗测试与赛马机制**（`./Ext/ASTO-Ext.09.工程实践指南.v1.0.md`）。

---

## **结语**

**ODD 不是 ASTO 的“应用”，ODD 是 ASTO 的“全息碎片”。**

在软件工程这个微观宇宙中，我们能看到整个宇宙演化的缩影。
如果你能理解为什么代码需要重构，你就能理解为什么文明需要跃迁。

**(本文档是连接哲学与工程的罗塞塔石碑。)**
