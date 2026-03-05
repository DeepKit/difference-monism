# 论文草稿：验收即事件（Acceptance as Operation）
**目标期刊**：*Journal of Responsible Technology* (Elsevier)
**语言**：中文（主线；英文并行）
**状态**：Draft v0.3 (CN) — updated 2026-02-01
**说明**：本文件为中文版主线；英文并行稿为 `草稿_验收即事件_EN_v0.3.md`（以术语对齐为目标同步迭代）。

> 写作约束：**不要**在正文中出现任何内部体系/项目名（也不要把内部方法当作“体系/学派”）；本文必须作为一篇**独立**的治理提案自洽。

---

## 工作标题
**“验收”不是判断：用可审计的验收事件把责任操作化**

## 摘要
在 AI 与自动化系统中，治理失效往往源于一种“心理主义陷阱”：把“验收/接受”理解为个体的心理认可（“我觉得没问题”），而不是一种公开、可追溯、可审计的制度操作（“在此时间点，由此授权角色，依据这些明确标准，对该产出物（artifact）做出了验收决定”）。当生产节奏加速、实现频繁再生成、作者身份与意图难以稳定归属时，责任无法再可靠地锚定在“谁写了代码/谁审了代码”。

本文主张将验收重新定义为**验收事件（acceptance event）**：一种离散、可记录的操作性交易，用于绑定（i）被验收的产出物（artifact），（ii）明确的约束集/验收标准（constraint set），（iii）证据包摘要（evidence bundle digest），以及（iv）具备授权的验收主体（authorized agent），形成带时间戳的可查询记录。其核心是对“产出物–约束–证据”的三元绑定（artifact–constraint–evidence binding）进行制度性签署，从而形成责任锚点。在该定义之上，本文提出一种治理机制：**制度固着（institutional fixation）**——要求每一次验收必须引用一个已注册的约束集（“无引用不验收”），从而避免隐性标准导致的责任扩散与事后争辩。我们以“AI 生成代码的验收”为例展示该机制如何把责任从“作者身份”转移到“验收签署”，并给出组织实践与政策层面的可落地建议。

**关键词**：责任技术；治理；可追溯性；可审计性；验收事件；责任锚定

---

## 1. 引言：为什么“信任”不足以成为责任锚
“信任”是重要的社会概念，但它不是好的工程控制原语。
当 AI 辅助系统造成事故时，“我们是否信任它？”这类问题无法支持治理追责，因为它不提供：
- 当时使用了哪些标准（criteria）？
- 谁具备授权（authority）？
- 当时有哪些证据（evidence）？
- 被验收的产出物到底是哪一个版本（exact artifact）？

在高速度社会技术系统中，治理缺口正在扩大：
- 生成速度远快于人类逐行审阅能力；
- 实现可被频繁再生成，作者身份与意图难以稳定归属；
- 责任扩散成为结构性结果（“大家都碰过，所以没人负责”）。

**核心主张**：要让责任可追溯，必须把验收从“心理判断”转为**可审计的事件**。

### 贡献
本文贡献包括：
1. 给出“验收事件”的最小可操作定义（产出物 + 约束集 + 证据包摘要 + 授权主体 + 时间戳记录）。
2. 提出“制度固着”：规定验收必须引用已注册约束集（无引用不验收）。
3. 通过 AI 生成代码的示例说明责任如何从作者身份转移到验收签署。
4. 给出组织实践与监管政策层面的最小建议。

**责任技术定位锚（Responsible Technology framing）**：在责任技术（responsible technology）的语境中，核心问题并非系统是否“被信任”，而是当系统造成后果时，是否存在可查询、可审计的责任锚点。本文关注的不是如何让系统更“智能”，而是如何让责任在高速自动化条件下仍然可被操作性地定位与追溯；因此，“验收事件”不是 DevOps 小技巧，而是一种治理原语（Kroll et al., 2017; Diakopoulos, 2016; Raji et al., 2020）。

**去同质化声明（避免“只是 sign-off / approval / release gate”的误判）**：本文的创新不在于“多一道审批”，而在于将责任锚定权从实现过程（review / authorship）与合规叙事（compliance）转移到一次可查询、可审计的验收操作本身。验收事件的关键，是对“产出物–约束–证据”（artifact–constraint–evidence）的三元绑定进行制度性签署，从而把责任从叙事判断变为可查询记录。

**边界而非垄断**：验收事件不是单点责任归因，而是一个让责任可拆分、可审计的接口；它划定的是**责任边界**，不是**责任垄断点**。

**核心论点（Thesis）**：将“验收”视为一种**责任绑定操作**而非心理判断，是在高速自动化系统中维持可追责治理的必要条件。

---

## 2. 从心理认可到验收事件
### 2.1 定义
我们将**验收事件（acceptance event）**定义为一种离散操作，用以生成可审计记录：

- **产出物（artifact, $A$）**：被验收的对象（例如构建产物、部署包、规则集、模型、配置集），以不可变摘要（digest/hash）识别。
- **约束集（constraint set, $C$）**：验收标准与边界（测试、扫描、关键不变量、运行边界、风险门槛等），必须明确、可引用、可版本化。
- **证据包摘要（evidence bundle digest, $\\mathcal{E}$）**：验收时引用的证据材料集合的摘要/承诺（例如测试报告、扫描报告、对抗探测等的汇总摘要）。
- **授权主体（authorized agent, $S$）**：在组织治理结构中被授权做出验收决策的角色/主体。
- **事件记录（event record, $E$）**：把 $A$、$C$、$\\mathcal{E}$ 与 $S$ 绑定到时间 $t$ 的记录。

> 术语说明：在软件工程流水线语境中，artifact 也常被译作“工件/构建工件”。本文为跨领域一致性，统一使用“产出物”。

一种最小抽象形式为：

$$E = \\text{Sign}_S(A, C, \\mathcal{E}, t)$$

其中 $\\mathcal{E}$ 表示证据包摘要（evidence bundle digest），是对测试、扫描、探测等验证材料的密码学承诺（cryptographic commitment）；它使“事件记录”与“证据材料”在逻辑上可绑定、在实现上可解耦。

这里的 Sign 表示制度性签署操作，而非特定的密码学签名实现；其核心是责任可追溯性（accountability traceability），而非密码学意义上的不可否认性（non-repudiation）。

之所以使用“事件”而非“状态”，是为了强调验收的时间绑定与签署点：即使后续需要撤销/替换，也应通过新的验收事件完成，从而责任可锚定到具体时间点与具体签署行为。

该定义的关键不是形式化本身，而是把“责任”变成**可查询记录**：事后审计可直接查询“引用了哪个约束集”“验收了哪个产出物版本”“对应证据包摘要”“谁签署”。

### 2.2 最小记录结构（与实现无关）
为了做到技术栈无关但又可落地，验收事件至少应绑定：
- 产出物标识（name + version + digest）
- 约束集标识（constraints_id + version + digest）
- 证据包标识（evidence bundle digest；例如测试报告/扫描报告/对抗探测等的汇总）
- 授权主体身份（role + identity reference）
- 时间戳 + 决策结果（accept/reject/exception）

以上要素共同构成对“产出物–约束–证据”的三元绑定（artifact–constraint–evidence binding）以及责任锚点，使验收从“感觉上可接受”变为“结构上可审计”。

**图 1（概念示意）**：产出物–约束–证据三元绑定 → 验收事件 → 责任锚点（见 `submission/figure1_mermaid.txt`）。

示例记录（示意）：

```json
{
  "acceptance_event_id": "acc:2026-01-31T00:00:00Z:artifact:payments-api:1.0.7",
  "timestamp_utc": "2026-01-31T00:00:00Z",
  "agent": {
    "role": "release_arbiter",
    "id": "user:team-lead-001"
  },
  "artifact": {
    "name": "payments-api",
    "version": "1.0.7",
    "digest": "sha256:..."
  },
  "constraints": {
    "constraints_id": "PAYMENTS-ACCEPTANCE-V1",
    "version": "1.2",
    "digest": "sha256:..."
  },
  "evidence": {
    "bundle_digest": "sha256:...",
    "summary": {
      "tests": "pass",
      "security_scan": "pass",
      "mutation_testing": "pass"
    }
  },
  "decision": "accept",
  "signature": {
    "scheme": "institutional",
    "bundle_digest": "sha256:..."
  }
}
```

### 2.3 验收事件“是什么/不是什么”
- 它不是伦理讨论的替代品；它是把决策**留痕可审计**的机制。
- 它不是可解释性（explainability）；它不要求看懂 AI 内部机理，只要求验收可追溯。
- 它不是一般性的决策记录（decision logging）：验收事件要求绑定可执行约束集与证据包摘要，从而使“是否被接受”成为可被外部重放与审计的操作，而不仅是组织内部的叙事记录（Singh et al., 2018）。决策日志记录“发生了什么决定”；验收事件记录“谁在什么标准下对哪个产出物承担了责任”（并绑定证据摘要以支撑审计重放）。
- 它不是“更多文书工作”；它是治理原语——没有它，责任很难稳定追踪。

### 2.4 明确区分：Acceptance ≠ Certification ≠ Review
为避免审稿人将本文误判为“DevOps best practice”或“合规/认证老话题”，我们在操作层面明确画线：

| 概念 | 关注点 | 谁负责/谁签 | 是否生成责任锚点 |
|---|---|---|---|
| Code Review（代码审查） | 实现质量（实现是否可靠/可维护） | 开发者 / 评审者（Bacchelli & Bird, 2013） | 否（难以稳定锚定后果责任） |
| Certification（认证/合规） | 合规符合性（是否满足外部规范/认证条款） | 第三方/机构（或组织合规职能） | 部分（弱：更偏“是否合规”，不一定绑定具体产出物与当时证据） |
| Acceptance Event（验收事件） | 是否在**此标准**下被**此授权主体**于**此时间点**接受 | 授权主体（组织定义的验收签署角色） | 是（将责任锚定到可查询记录） |

---

## 3. 制度固着：无引用不验收

### 3.0 术语界定（避免“fixation = 僵化”的误读）
“fixation/fixity”在某些语境中可能被理解为信念固化或制度粘性/路径依赖。本文使用 *institutional fixation* 仅指一种**验收操作要求**：在验收瞬间将“约束集的版本与摘要”显式绑定到验收事件上，使标准在该时刻可被锚定、可被审计、不可事后漂移；它不主张增加制度僵化或形式主义。
为避免误读，你也可以将“制度固着”理解为：**显式约束绑定要求（explicit constraint binding requirement）**，或更直接的 **约束引用要求（constraint referencing requirement）**。
从制度理论与 STS 的语言看，这相当于把“验收标准/责任锚点”从隐性实践转化为可引用的制度化对象，并将治理结构嵌入到技术流程中（DiMaggio & Powell, 1983; Scott, 2014; Akrich, 1992; Winner, 1980）。

很多治理失败并非来自恶意，而是来自**隐性约束**：人们用“看起来对”“差不多”“以前也这样”作为标准。
这种标准既不稳定，也不可审计，事故发生后只会导致叙事争辩。

本文提出**制度固着**规则：

> **每一次验收事件必须引用一个已注册的约束集（constraint set）。**

### 3.1 注册约束集
注册约束集可以很轻量（检查清单 + 必需证据 + 风险门槛），但必须：
- 明确（explicit）
- 可版本化（versioned）
- 可引用（referencable）
- 足以支撑审计查询（audit queries）

本文不规定约束集的价值充分性，仅要求其被显式注册并在验收时被引用；约束集本身的充分性问题，应通过组织治理或监管机制解决，而不应在验收时被隐性处理。

制度固着的目标不是保证“正确标准”，而是确保组织无法在事故后否认其当时所采用的标准（从而回避责任）。

### 3.2 为什么它有效
制度固着至少能压制三类常见失效模式：
1. **事后合理化**：事故后临时“补标准”。
2. **责任扩散**：人人都以为别人检查过。
3. **标准漂移**：组织在不留痕的情况下改变“可接受”的含义。

需要强调的是，制度固着并非要求更复杂的验收流程，而是将原本已经发生但未留痕的判断，转化为最小可查询记录。它减少的是事后争辩成本与责任漂移成本，而不必然增加事前决策成本。

### 3.3 反例：隐性约束陷阱
若团队以“看起来没问题”验收 AI 生成的变更，则事后根本不存在可审计对象：
- 没有约束集对象（C）
- 没有证据包绑定（evidence）
- 没有可追溯签署点（sign-off）

---

## 4. 小案例：AI 生成代码的验收
本节为示意性案例（vignette），用于解释机制如何工作。

### 4.1 场景
AI 工具为高影响服务（支付/医疗分诊/身份认证等）生成一段变更。变更能通过部分测试，但人类不可能逐行理解所有边界条件与涌现行为。

### 4.2 传统路径：以审查作为控制面
- 责任隐含绑定在作者身份与代码审查上。
- 在 AI 生成情境下，作者身份稀释、审查带宽崩溃。
- 结果往往在“橡皮图章式上线”与“无法上线的瘫痪”之间摇摆（Parasuraman & Riley, 1997）。

### 4.3 事件化路径：以验收签署作为控制面
组织先定义一个约束集，例如：
- 功能测试必过项
- 安全扫描门槛
- 不变量（如幂等/不重复扣款）
- 运行边界（超时、回滚策略、告警与观测字段）

例如，针对支付服务的 AI 生成代码，约束集 $C$ 可以具体包含：通过 OWASP Top 10 相关静态扫描且高危漏洞为 0；变异测试覆盖率 ≥ 80%；包含幂等性不变量检查（idempotency key validation）；回滚策略已配置并经演练/混沌验证。

流水线产生证据包（测试报告、扫描报告、对抗探测摘要等）。
授权主体对“产出物 + 约束集版本 + 证据包摘要”做出签署，生成验收事件。

**结果**：事故发生时，追责从“谁写了”转为“谁在什么标准下验收了哪个版本”。

在实践中，验收事件并不能消除错误，但它决定了错误发生后组织能否停止在“谁觉得没问题”的层面争论。更重要的是，该机制不必然降低错误发生率，但能显著降低**错误后的治理不确定性**（标准漂移、叙事争辩与追责成本）。

### 4.4 历史类比（脚注式提醒）
类似的“验收缺口”在部分安全关键系统的历史事件中也曾以结构性方式出现[^hist]。本文不展开事实细节与责任归属争论，仅将其作为提醒：当验收标准未被显式引用、验收决策未形成可查询记录时，事故后往往只能回到叙事争辩，而难以形成可审计的追责路径。

[^hist]: 例如 Therac-25、Boeing 737 MAX（MCAS）等常被讨论的案例。本文不在此复盘事实细节，仅取其“验收缺口 → 叙事争辩”的结构类比。

---

## 5. 实践建议与政策建议
### 5.1 组织层面的最小落地（立即可行的基础方案）
本文主张的不是“每次变更都重验”，而是：只要存在“被接受”的决策，就必须留下可审计的验收事件。

1. **定义授权角色**：按风险等级规定谁可以签署验收。
2. **把约束集当作一等产出物**：必须版本化、可引用。
3. **验收必须绑定证据包**：无证据的验收一律无效。
4. **维护追加写入的验收日志**：作为治理账本（ledger）。
5. **用查询做审计**：定期抽样验收记录，验证证据完整性与可复现性。

### 5.2 监管/政策建议（高影响领域）
监管可要求组织维护最低限度的验收事件日志，至少包含：
- 产出物标识（digest）
- 约束集 ID/版本引用
- 证据包引用
- 签署角色与时间戳

考虑跨境数据流动、商业秘密与安全敏感信息，约束集的“注册/公开”可以采用**哈希承诺（hash commitment）**：对外仅公开可验证的摘要/承诺值，必要时在受控审计条件下披露完整内容，以兼顾可验证性与保密性。

该思路不规定具体技术实现，而是规范“验收操作”，因此能跨技术栈适配。

---

## 6. 讨论与局限

### 6.1 技术局限与实现风险
- **证据可信性**：验收日志的可信度取决于证据生成环境；建议在受控 CI/受信环境中生成证据包（Souppaya et al., 2022）。
- **成本与摩擦**：事件化验收会引入开销；目标是把开销从“持续人工审查”迁移到“结构化证据 + 集中签署”。
- **撤销、回滚与时间窗口**：高可用系统中的紧急回滚往往发生在原验收事件之后、新事件生成之前。本文主张的最小要求是：回滚/替换决策也应形成新的验收事件（或“回滚事件”）并绑定对应约束集/证据摘要；同时保留时间线，明确“间隙”期间采取的是何种风险控制与授权。在这一意义上，时间窗内的运行状态本身，也应被视为一种“被接受的风险配置”。

### 6.2 治理局限与伦理风险
- **非伦理万能解**：该机制不解决价值冲突本身，但能让冲突决策可追溯、可审计。
- **与溯源（provenance）与证明（attestation）的关系**：溯源回答“如何构建”（供供应链完整性验证）；证明/签名回答“谁对什么做过声明”。验收事件则回答“谁在何标准下接受了什么”，并通过“约束集显式引用 + 证据包摘要绑定”把治理决策变成可审计操作。它不替代 in-toto/SLSA/Sigstore，而是叠加一层**责任锚定**（Torres-Arias et al., 2019; OpenSSF, 2023; Newman et al., 2022）。
- **例外处理（exception handling）**：若授权主体在未满足既有约束集的情况下做出例外验收，制度固着不应沦为形式主义。一个可行做法是将例外本身事件化：例外验收必须引用更高阶、预先注册的约束集（如“危机响应协议V1/紧急变更流程V1”），并记录理由、有效期（TTL）与后续补救义务（例如必须在 N 小时内补齐证据并再封存一次标准验收事件）。
- **责任转移与道德风险**：把责任锚从“谁写了”转到“谁验收了”可能带来责任甩锅与道德风险（moral hazard）。本文不主张将验收者设为唯一责任承担者；相反，应将责任拆分为可审计的角色链条（约束集制定/批准、证据生成与保真、验收签署与例外审批），并通过抽样审计与事后复盘防止“仅做形式签署”的审计社会陷阱（Power, 1997; Young, 2011）。

---

## 7. 结论
责任技术的关键挑战不在于提出更多原则，而在于让责任在系统中**落地**。
本文不主张提出新的伦理原则，而是提供一种让既有责任原则可被执行、可被审计的操作结构。
通过把验收定义为可审计事件，并实施制度固着（无引用不验收），组织可以在 AI 加速生产、作者身份稀释的条件下，仍然让责任保持可追溯与可查询。

---

## 8. 参考文献（候选，待按 JRT 格式统一）
1. Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. In *Proceedings of the 35th International Conference on Software Engineering (ICSE 2013)*, 712–721. DOI: 10.1109/ICSE.2013.6606617.
2. Diakopoulos, N. (2016). Accountability in algorithmic decision making. *Communications of the ACM*, 59(2), 56–62. DOI: 10.1145/2844110.
3. Kroll, J. A., Huey, J., Barocas, S., Felten, E. W., Reidenberg, J. R., Robinson, D. G., & Yu, H. (2017). Accountable algorithms. *University of Pennsylvania Law Review*, 165(3), 633–705. URL: https://www.jstor.org/stable/26600576
4. Parasuraman, R., & Riley, V. (1997). Humans and automation: use, misuse, disuse, abuse. *Human Factors*, 39(2), 230–253. DOI: 10.1518/001872097778543886.
5. Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020). Closing the AI accountability gap: defining an end-to-end framework for internal algorithmic auditing. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT\* 2020)*. arXiv:2001.00973. URL: https://arxiv.org/abs/2001.00973
6. Singh, J., Cobbe, J., & Norval, C. (2018). Decision provenance: harnessing data flow for accountable systems. arXiv:1804.05741. URL: https://arxiv.org/abs/1804.05741
7. Souppaya, M., Scarfone, K., & Dodson, D. (2022). Secure software development framework (SSDF) version 1.1: recommendations for mitigating the risk of software vulnerabilities. *NIST Special Publication 800-218*. DOI: 10.6028/NIST.SP.800-218.
8. Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). in-toto: providing farm-to-table guarantees for bits and bytes. In *Proceedings of the 28th USENIX Security Symposium (USENIX Security 19)*, 1393–1410. URL: https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias
9. OpenSSF. (2023). Supply-chain Levels for Software Artifacts (SLSA) v1.0. URL: https://slsa.dev/spec/v1.0/
10. Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). Sigstore: software signing for everybody. In *Proceedings of the 2022 ACM Conference on Computer and Communications Security (CCS 2022)*. DOI: 10.1145/3548606.3560596.
11. DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: institutional isomorphism and collective rationality in organizational fields. *American Sociological Review*, 48(2), 147–160. DOI: 10.2307/2095101. URL: https://www.jstor.org/stable/2095101
12. Scott, W. R. (2014). *Institutions and Organizations: Ideas, Interests, and Identities* (4th ed.). Sage. URL: https://us.sagepub.com/en-us/nam/institutions-and-organizations/book238776
13. Power, M. (1997). *The Audit Society: Rituals of Verification*. Oxford University Press.
14. Young, I. M. (2011). *Responsibility for Justice*. Oxford University Press.
15. Akrich, M. (1992). The de-scription of technical objects. In W. E. Bijker & J. Law (Eds.), *Shaping Technology/Building Society: Studies in Sociotechnical Change* (pp. 205–224). MIT Press. URL: https://mitpress.mit.edu/9780262521949/shaping-technology-building-society/
16. Winner, L. (1980). Do artifacts have politics? *Daedalus*, 109(1), 121–136. URL: https://www.jstor.org/stable/20024652

## 作者备注（下一步）
1. 本文主案例固定为“AI 生成代码上线”，优先把验收事件的最小结构写“硬”。
2. 历史事件（如 Therac-25、737 MAX）仅作结构类比：建议只在讨论段或脚注中一句提及，避免进入事实细节争论。
3. 参考文献候选已列在第 8 节（当前 16 条，覆盖 A/B/C + 治理理论/审计社会/责任伦理/STS）。下一步：将文中关键论断逐一补齐引用，并按 JRT 作者指南统一排版（投稿前需核对具体参考文献格式要求；此处先以“一致性优先”，录用后再按模板精排）。
4. 英文并行稿已创建：`草稿_验收即事件_EN_v0.3.md`。下一步：逐段对齐术语与结构（尤其 institutional fixation / explicit constraint binding requirement），并按期刊要求统一参考文献格式；保留 `草稿_验收即事件_EN_v0.2.md` 作为快照。
