# Vol01 卷结构详解：《代价的计算》(The Cost of Living)

**全卷概览**：集数 001-024 | 4小案 × 6集 = 24集 | 主题：生命定价与漏洞反杀

---

## Part A：卷级去重方案（如何不重复）

### 本卷的"反疲劳签名"
| 维度 | 签名 |
|---|---|
| **案型** | 漏洞案（系统自相矛盾的理赔规则） |
| **对手形态** | NPC (Brad + HR的官僚机器) |
| **标准升级** | v1.0：Red Lines + Human Check（基线） |
| **证据增量** | 104_C 首次出现（代码片段） |
| **结局类型** | 胜利（救下Lily但付出代价） |
| **呈现形式** | 传统叙述（Ethan第一人称） |
| **情感主线** | 道德损伤：每次赢都要背叛规则 |
| **地理线** | 理赔中心→医院财务→法务→街道 |

### 为什么这卷不会像其他卷重复
- **Vol02** 会是"责任链案"（谁负责？），对手是"链条"  
- **Vol03** 会是"资源稀缺案"，对手是"无脸算法"  
- 所以 **Vol01必须专注"漏洞反杀"** + "NPC对抗"，这样就不会预占其他卷的玩法

---

## Part B：4小案结构（每小案6集）

### 小案 1：The Pre-existing Condition（Ep001-006）
**主题**：Lily 的拒保信 → 发现第一个漏洞 → 系统开始反制

#### Ep001 — Docket（立案/痒点）🆓
- **场景**：Ethan在办公室收到Lily的求助电话
- **痒点**：拒保信理由是"pre-existing condition"，但Lily出生后才诊断
- **结尾**：Ethan意识到"这不是医学问题，是条款问题"
- **Sophie出场**：播客开头介绍"Kill Line"（保险定价的死亡界线）

**赤裸裸的客观事实给读者的第一击**：
- 拒保金额：$475,000 for a 7-year-old's CAR-T cell therapy
- Lily的预期寿命（算法估计）：3.4 years
- ROI calculation: -100%（算法认为不值得）

#### Ep002 — Evidence（取证）🆓
- **场景**：Ethan在数据库里查条款
- **Kay的第一次出现**：Ethan在搜索Section 104时，一个黑色背景的聊天窗口自动弹出
  - **消息**："K: Check Alabama state prison intake logs. October 2018. Same override code used in medical transfers."
  - **Ethan的反应**：打字"Who is this?"，窗口立即关闭
  - **验证**：Ethan查到Alabama监狱确实使用过104_C代码延迟医疗，2人死亡
  - **意义**：Ethan意识到104_C不是保险专有，而是跨系统的"安全阀"代码
- **证据**：Section 104 的两条互相矛盾的规则
  - Rule 104a：Pre-existing conditions 不赔
  - Rule 104b：出生6个月内诊断的遗传病 必须赔（纽约州法律要求）
- **数学**：Lily是第7个月诊断，理论上在"灰色地带"
- **邮件**：Brad 给Rachel的备忘录（泄露的）："Mark 104b claims as edge case, auto-deny for now."

#### Ep003 — Sophie + Emotion（呼吸集）🆓
- **Sophie 的恐惧**：Sophie 在播客录音时停下来，深呼吸。她说："I've been doing this for six years. I still can't say the number out loud." 她念出 $475,000——一个7岁女孩的命价。
- **Ethan 的"回家"人**：Ethan 下班后去医院看 Lily。Lily 画了一幅画给他——画里有一个穿西装的人在哭。Ethan 把画折好放进口袋。
- **道德损伤内化**：Ethan 回到家，发现自己无法打开冰箱（手抖）。他不说"我很痛苦"，而是盯着冰箱门把手看了三十秒。
- **病毒金句**：*"The algorithm doesn't hate Lily. It doesn't know Lily exists. That's worse."*
- **Knowledge Check**：Sophie 用30秒解释 "pre-existing condition" 的历史起源（Lao-A Tier 1 术语）

#### Ep004 — Options（逼近裁决 + 投票题）🆓
- **漏洞出现**：Ethan找到三条可能的反杀路线
  - **选项A**：直接上诉（走正式流程，快3-6个月）→ 救不了Lily
  - **选项B**：激活Section 104 override code（内部系统漏洞）→ 救Lily但触发监管告警
  - **选项C**：先救，后说（支付先行，事后争议）→ 模糊责任链
- **每个选项都有代价**：
  - A = 合法但Lily死了
  - B = 违反系统但救人，但会暴露 Brad 的违法
  - C = 模糊责任（Accountability Chain 会崩：谁该负责？）

**强制"不可裁决"**：没有完美解

**Audit Report 投票**：
> **[AUDIT REPORT: THIS IS NOT A POLL]**
>
> **OPTION A**: Appeal through proper channels. Cost: Lily's life (3-6 month wait). Risk: None — you followed the rules.
> **OPTION B**: Activate the override code. Cost: Your career, possibly your freedom. Risk: Red Lines — you become the weapon.
> **OPTION C**: Pay first, argue later. Cost: Accountability collapses. Risk: Human Check — no one is accountable.
>
> **What do you tell the operator to do?**
> *Vote closes in 24 hours. The next chapter executes your decision.*

#### Ep005 — Court（开庭/执行）⏩ Ream提前章节
- **Ethan执行选项B**：
  - 内心独白：为什么他选B（道德损伤的第一次）
  - 具体操作：如何激活 override（操作细节）
  - 系统反应：Brad 发现异常，开始追查
  - 结果：Lily被纳入治疗池
- **高潮**：Ethan 在系统里输入最后一个确认键时，屏幕弹出 "Authorization: OVERRIDE — IRREVERSIBLE"。他按了。

#### Ep006 — Aftermath（系统适应/升级）⏩ Ream提前章节
- **系统反制**：Brad 的电脑闪起警报。104_C override 被激活，但没人授权。Brad 启动内部调查。
- **规则升级**：Brad 给 IT 下令：所有 override code 需要双重授权。漏洞被堵了一半。
- **下一案痒点**：Ethan 发现系统日志里还有3次非授权激活记录——不是他做的。谁在用同样的漏洞？

**Sophie's Board 更新**（公开版部分打码）：

> **[SOPHIE'S BOARD: CASE UPDATE - VOL01 CASE 1]**
> *   **Current Target**: NewCare Insurance (Brad Kovac, Head of Claims)
> *   **Source Status**: Ethan Cole - ACTIVE (but exposed)
> *   **The Red String**: 
> *   Code `104_C` override was used. Where did Ethan learn it?
> *   System auto-denial rate on "edge cases" is 94% (vs 3% industry avg)
> *   **Threat Level**: MEDIUM (monitoring began)

> **[ADJUDICATION STACK: v1.0 - FIRST CASE]**
> *   **Red Lines**: [BORDERLINE]
> *   **Human Check**:
> *   **Replaceable?**: [OK - Ethan still acts as an individual, not a function]
> *   **Dialogue?**: [OPEN - Appeal process exists]
> *   **Exit?** (Refusal path): [NARROW - Override is one-way, can't undo]
> *   **Three Operational Questions**:
> *   **Sustainable?** [NO - Ethan can't keep hacking forever]
> *   **Survivable?** [YES - Lily lives, but company bleeds]
> *   **Exit Path?** [NO - He's now exposed, systems can track him]
> *   **Accountability Chain**: [FUZZY - Brad authorizes auto-deny, but the system executes]
> *   **Human Cost Index**: [0.85 → 0.80]

**Ream独占深度材料**（Tier 2+，永不上RR）：
- 完整的"未删减备忘录"：Brad的真实动机（不只是规则，是KPI）
- "反事实后果"：如果Ethan选了A或C会怎样
- **Sophie的历史研究笔记**：Triangle Shirtwaist Fire (1911) — 工厂主用成本计算决定了人命

---

### 小案 2：The Retroactive Audit（Ep007-012）
**主题**：系统回溯审计 → 漏洞被追踪 → 规则升级

#### Ep007 — Docket（立案/痒点）🆓
- **场景**：Ethan 收到一封系统自动邮件——Lily 的赔付被标记为"待回溯审计"
- **痒点**：新的审计算法正在扫描过去12个月所有"异常赔付"，Lily的案子排在第一个
- **发现**：审计不只针对Ethan——全部门有47个案子被标记

#### Ep008 — Evidence（取证）🆓
- **Kay的第二次出现**：Ethan收到一封匿名邮件
  - **主题**："Re: Case #4431 - The One They Don't Want You To See"
  - **内容**：Rachel和Brad的内部备忘录——Rachel建议"简化工作流程"，自动拒赔所有104b案件
  - **时间戳**：Lily案件前两周
  - **技术细节**：邮件经过7层代理路由，无法追踪
  - **Ethan的尝试**：回复"Who are you?"，收到退信"Recipient address not found"
  - **意义**：Ethan意识到K不只是观察者，K在系统内部
- **证据链**：审计算法的逻辑——所有"override"赔付自动触发回溯
- **数据**：47个案子，总额 $2.3M。其中34个是真正的"edge case"，13个是系统错误
- **Brad的困境**：如果全部追回，34个家庭失去治疗。如果不追回，Q3财报出问题
- **邮件**：CFO 给 Brad 的指示："Recover minimum 80% by end of quarter."

#### Ep009 — Sophie + Emotion（呼吸集）🆓
- **Sophie 的愤怒**：Sophie 在播客里第一次提高声音。她说："They're not auditing fraud. They're auditing mercy."
- **Ethan 的"回家"人**：Ethan 去看 Lily。Lily 在化疗后呕吐。Lily的妈妈问 Ethan："They can't take it back, can they?" Ethan 说不出话。
- **道德损伤内化**：Ethan 在停车场坐了40分钟才发动车。收音机在放广告——正好是 NewCare 的广告："We care about what matters."
- **病毒金句**：*"Mercy has a shelf life. The system just found the expiration date."*

#### Ep010 — Options（逼近裁决 + 投票题）🆓
- **选项A**：配合审计，让系统追回赔付（合法，但34个家庭失去治疗）
- **选项B**：攻击审计逻辑——找出算法的分类错误，证明34个案子不属于"override"类别（Malicious Compliance）
- **选项C**：泄露审计邮件给媒体，用公众压力逼公司放弃追回（核弹选项）

**Audit Report 投票**：
> **[AUDIT REPORT: THIS IS NOT A POLL]**
>
> **OPTION A**: Comply. Cost: 34 families lose treatment. Risk: None — you followed orders.
> **OPTION B**: Attack the algorithm's logic. Cost: You become a target. Risk: Red Lines — you’re now altering categories that decide who lives.
> **OPTION C**: Leak to press. Cost: Your career dies today. Risk: Human Check — 13 real errors get buried in the outrage.
>
> **What do you tell the operator to do?**

#### Ep011 — Court（开庭/执行）⏩ Ream提前章节
- **Ethan执行选项B**：Malicious Compliance——他不反对审计，而是用审计自己的标准证明34个案子的分类有误
- **具体操作**：逐一比对每个案子的 override 日志与州法律要求，证明它们不是"override"而是"mandatory compliance"
- **系统反应**：Brad 被迫承认审计算法有缺陷，但要求 IT 更新分类标准
- **结果**：34个案子保住了，但审计算法升级了——以后"mandatory compliance"也会被纳入审查

#### Ep012 — Aftermath（系统适应/升级）⏩ Ream提前章节
- **系统反制**：新的审计算法 v2.0 上线。它不再按"override"分类，而是按"cost anomaly"分类——任何超过预期成本150%的赔付都会被标记
- **Sophie's Board 更新**：

> **[ADJUDICATION STACK: v1.1 - RETROACTIVE]**
> *   **Red Lines**: [BORDERLINE - Reclassification is legal but manipulative]
> *   **Accountability Chain**: [FUZZY → FUZZY] (Brad can't pin Ethan, Ethan can't pin Brad)
> *   **Human Cost Index**: [0.80 → 0.75]

- **下一案痒点**：Ethan 注意到新算法有一个新字段："QALY Score"（质量调整寿命年）。每个患者现在都有一个"生命价值评分"。

**Ream独占深度材料**（Tier 2+，永不上RR）：
- Brad 的内部备忘录：为什么他选择升级算法而不是解雇 Ethan
- 反事实：如果选了C（泄露给媒体），NewCare 会发生什么
- 13个"真正错误"的案子里隐藏的模式

---

### 小案 3：The Waitlist Optimization（Ep013-018）
**主题**：QALY排队算法 → 生命被量化排序 → 零和博弈

#### Ep013 — Docket（立案/痒点）🆓
- **场景**：医院急诊部的白板上出现了新的排队系统——患者不再按到达顺序，而是按"QALY Score"排序
- **痒点**：一个72岁的退伍军人（Marcus）被排到最后——他的QALY Score是0.3，而一个25岁的程序员（Score 0.9）排在第一位
- **结尾**：Ethan 看到 Marcus 的病历备注："Low priority — resource allocation optimized."

#### Ep014 — Evidence（取证）🆓
- **Kay的第三次出现**：Ethan陷入困境，需要证明QALY公式歧视退伍军人
- **手机短信**：未知号码发来
  - **内容**："K: Check the VA appeals database. Public record. Search 'Torres v. VA 2019.' Same formula. Precedent already exists."
  - **Ethan的搜索**：找到三年前的案例，法官裁定QALY公式必须包含服役记录
  - **关键细节**：这个判例被刻意埋没，从未上诉，从未公开
  - **结果**：Ethan使用这个判例，Marcus得到治疗
  - **Ethan的回复**："Why are you helping me?"
  - **系统回复**：号码已断开连接
  - **意义**：Ethan保存这个号码，标签为"K. Ghost."，他不知道K是真实存在还是自己的幻觉
- **证据链**：QALY 计算公式——年龄×健康状态×预期产出÷治疗成本
- **数据**：Marcus 的"产出"被算法定义为零（退休=无经济产出）
- **系统设计者**：公式不是医生写的，是精算师写的。签名：Rachel Torres（Brad的下属）
- **邮件**：Rachel 给同事的 Slack 消息："Don't overthink it. It's just math."

#### Ep015 — Sophie + Emotion（呼吸集）🆓
- **Sophie 的无力感**：Sophie 采访 Marcus 的女儿。女儿说："Dad survived two tours in Fallujah. Now a spreadsheet says he's not worth saving." Sophie 关掉录音设备后，在车里哭了。
- **Ethan 的"回家"人**：Ethan 回到 Lily 的病房。Lily 在好转。但 Ethan 看到隔壁床空了——上周还有人住。护士说："Transferred. Optimization."
- **道德损伤内化**：Ethan 发现自己开始在心里计算每个患者的"价值"。他意识到自己正在变成系统的一部分。他在浴室镜子前说了一句话，然后立刻闭嘴。
- **病毒金句**：*"The moment you start counting, you've already decided who doesn't count."*

#### Ep016 — Options（逼近裁决 + 投票题）🆓
- **选项A**：为 Marcus 个案申诉（能救一个人，但不改变公式）
- **选项B**：修改 QALY 公式的权重参数——把"退休"从"零产出"改为"社会贡献"（Malicious Compliance：用系统的语言反驳系统）
- **选项C**：建立并行队列——急诊按到达顺序，非急诊按 QALY（妥协方案，但会被系统吞并）

**Audit Report 投票**：
> **[AUDIT REPORT: THIS IS NOT A POLL]**
>
> **OPTION A**: Save Marcus. Cost: Everyone else stays ranked. Risk: None — it's one exception.
> **OPTION B**: Redefine "value." Cost: Young patients drop in priority. Risk: Human Check — who decides what "contribution" means?
> **OPTION C**: Split the queue. Cost: Complexity doubles. Risk: Red Lines — the system will merge them back within 6 months.
>
> **What do you tell the operator to do?**

#### Ep017 — Court（开庭/执行）⏩ Ream提前章节
- **Ethan执行选项B**：他不删除QALY，而是在公式里加入"Community Impact Score"——让Marcus的军旅记录和社区志愿服务计入"产出"
- **具体操作**：找到Rachel的公式文档，提交"数据补充建议"（不改公式逻辑，只扩展数据源）
- **系统反应**：Rachel 同意（因为这不违反政策），但 Brad 注意到 Marcus 的排名突然上升
- **结果**：Marcus 得到治疗。但三个QALY Score在0.85-0.90之间的年轻患者被挤下去了

#### Ep018 — Aftermath（系统适应/升级）⏩ Ream提前章节
- **系统反制**：Rachel 提交报告：建议将所有"补充数据源"纳入统一权重模型。结果——"Community Impact Score"被稀释到几乎无效
- **零和博弈可视化**：Ethan 救了 Marcus，但每次修改参数都会挤掉别人。他第一次面对"你救了一个人，就间接害了另一个人"
- **Sophie's Board 更新**：

> **[ADJUDICATION STACK: v1.2 - ALLOCATION]**
> *   **Red Lines**: [PASS - No irreversible harm, but zero-sum exposure]
> *   **Human Check**: **Replaceable?** [BREACHED - Marcus was saved, but 3 others lost priority]
> *   **Human Cost Index**: [0.75 → 0.70]

- **下一案痒点**：Brad 宣布"季度成本优化"——所有争议案件将被批量和解（低价买断）

**Ream独占深度材料**（Tier 2+，永不上RR）：
- Rachel 的完整公式文档 + 设计理由
- 被挤下去的3个年轻患者后来怎么了
- 反事实：如果选了A或C，Marcus 和整个排队系统会如何演化

---

### 小案 4：The Settlement Cap（Ep019-024）
**主题**：批量和解 → 生命被定价买断 → Ethan 的终局选择

#### Ep019 — Docket（立案/痒点）🆓
- **场景**：公司会议室。Brad 宣布："All disputed claims from Q1-Q3 will be offered a settlement package."
- **痒点**：和解金额是算法自动计算的——基于“预期诉讼成本”而非“实际损失”。Lily 的案子：$38,000（她的治疗费是 $475,000）
- **发现**：和解协议第7页有一行小字："Acceptance waives all future claims related to this condition."

#### Ep020 — Evidence（取证）🆓
- **证据链**：和解协议模板是标准化的——所有 847 个争议案件用同一个模板
- **数据**：平均和解金额是实际损失的 26%。公司预计节省 $14.2M
- **Brad 的上级**：VP of Operations（Diana Chen）签署了批量和解方案。Brad 只是执行者。
- **邮件**：Diana 给 Board 的报告："Settlement program will improve Q4 margins by 3.2%. No material legal risk."

#### Ep021 — Sophie + Emotion（呼吸集）🆓
- **Sophie 面对自己的无力**：Sophie 拿到了和解协议的副本。她在播客里读了第7页的那行小字。然后沉默了15秒。她说："I can read you the number. But I can't make you feel what it means to sign away your daughter's future for thirty-eight thousand dollars."
- **Ethan 的"回家"人**：Ethan 去告诉 Lily 的妈妈。妈妈问："If I sign, does Lily keep her treatment?" Ethan 说："Yes. But if the cancer comes back, you're on your own." 妈妈看着 Lily 睡觉的脸，说："What choice do I have?"
- **道德损伤顶点**：Ethan 回到办公室，发现自己在计算——如果847个家庭都签了，公司省多少钱，Ethan 的部门奖金涨多少。他算出来了。然后他把计算器扔进了垃圾桶。
- **病毒金句**：*"She signed. Not because she agreed. Because the system made 'no' more expensive than 'yes.'"*

#### Ep022 — Options（逼近裁决 + 投票题）🆓
- **选项A**：帮助家庭们组团拒绝和解（集体行动，但耗时且结果不确定）
- **选项B**：泄露和解协议的内部底价给一个法律援助组织（自爆，但给家庭们谈判筹码）
- **选项C**：接受现实，帮 Lily 的妈妈签约，确保至少 Lily 这一次的治疗不断（投降）

**Audit Report 投票**：
> **[AUDIT REPORT: THIS IS NOT A POLL]**
>
> **OPTION A**: Organize resistance. Cost: 6-12 months. Risk: Families can't afford to wait.
> **OPTION B**: Leak the floor price. Cost: Your career, possibly criminal charges. Risk: Red Lines — you become the weapon.
> **OPTION C**: Sign and survive. Cost: 846 other families. Risk: Human Check — you chose one life over many.
>
> **What do you tell the operator to do?**

#### Ep023 — Court（开庭/执行）⏩ Ream提前章节
- **Ethan执行选项B**：他把和解协议的内部底价（公司的"最低可接受"数字）泄露给法律援助律师 James Ward
- **具体操作**：通过匿名邮件（但他知道 IT 能追查）。底价显示公司愿意接受每案最高 $38,000——远高于提议的 $12,000
- **系统反应**：James Ward 用底价数据代表 200 个家庭重新谈判。和解金额从 26% 提升到 71%
- **Brad 追查**：IT 锁定了泄露来源——Ethan 的工位。Brad 沉默了。他没有上报。
- **高潮**：Brad 把 Ethan 叫到办公室。Brad 说："You know I know." Ethan 说："Yes." Brad 说："I'm not going to report you. Because if I do, they'll find out what I told Rachel to do with 104b." 两个人互相持有对方的把柄。系统没有惩罚任何人——因为惩罚任何人都会让系统暴露。

#### Ep024 — Aftermath（系统适应/升级 + 全卷终局）⏩ Ream提前章节
- **系统反制**：Diana Chen 宣布新政策——以后所有和解协议将由外部律所起草，内部员工无权查看底价。信息隔离完成。
- **Ethan 的结局**：Ethan 被"提拔"到新的部门——"Claims Optimization"。Brad 说："You're good at finding holes. Now you'll be paid to close them." Ethan 意识到：系统没有惩罚他，系统收编了他。
- **Sophie 的终访**：Sophie 问 Ethan："Did you win?" Ethan 说："I don't know." Sophie 问："Would you do it again?" Ethan 说："That's not the right question. The right question is: did the system learn more from me than I learned from it?"

**Sophie's Board 更新**（全卷终版）：

> **[SOPHIE'S BOARD: VOL01 FINAL]**
> *   **Current Target**: NewCare Insurance
> *   **Source Status**: Ethan Cole - COMPROMISED (promoted into the system)
> *   **The Red String**: 
> *   Code `104_C` — origin still unknown
> *   Settlement floor prices — how many other companies use the same model?
> *   Brad and Ethan — mutual blackmail = system equilibrium
> *   **Threat Level**: HIGH (the system learned faster than we did)

> **[ADJUDICATION STACK: v1.3 - SETTLEMENT]**
> *   **Red Lines**: [FAIL - Information was weaponized]
> *   **Human Check**:
> *   **Replaceable?**: [BREACHED - Ethan is now part of the machine]
> *   **Dialogue?**: [CLOSED - Information silos erected]
> *   **Exit?**: [NONE - Ethan's only exit is complicity]
> *   **Three Operational Questions**:
> *   **Sustainable?** [NO]
> *   **Survivable?** [YES - but at what cost?]
> *   **Exit Path?** [NO - promoted = captured]
> *   **Accountability Chain**: [DENIED - mutual blackmail makes everyone untouchable]
> *   **Human Cost Index**: [0.70 → 0.60]
> *   *Vol01 Summary*: The machine learned our playbook. Ethan saved lives but fed the beast.

**Ream独占深度材料**（Tier 2+，永不上RR）：
- Diana Chen 的完整 Board 报告
- Brad 为什么不上报 Ethan（他自己的风险计算）
- 反事实：如果 Ethan 选了A或C，Vol02 的开局会完全不同
- Sophie的历史研究笔记：Victorian workhouse "less eligibility" principle — 系统怎样让“拒绝”比“接受”更贵

---

## Part C：卷级付费结构（双轨制：提前章节 + 独占深度材料）

### 免费（全部24集，Royal Road，延迟Ream 2-4周）交付
- **完整故事**：全部4案 × 6集 = 24集（包括Court和Aftermath）
- Audit Report 投票题（4次投票，与付费用户同步）
- Sophie's Board 状态版（关键原因打码）
- Sophie 的播客片段 + Knowledge Check
- 情感锚点场景（Lily、Marcus 等）

### Ream Tier1 $3 "The Clerk"（提前15章）
- 比免费读者早2-4周看到全部24集
- 每周多看1个完整小案的结局

### Ream Tier2 $5 "The Auditor"（提前20章 + 独占深度材料）
- **The Standard v1.0-v1.3**：红线 + 人性三测 + 行动三问 + 责任链（完整演化路径）
- **Reasoning Trace**：标准如何一步步导出裁决
- **Unredacted Files**（永不上RR）：
  - Brad 的真实备忘录
  - Rachel 的 QALY 公式文档
  - Diana Chen 的 Board 报告
  - 系统内部日志
- **Counterfactuals**：被否决方案的后果树

### Ream Tier3 $10 "The Architect"（提前25章 + 参与权）
- 所有上述内容
- **Sophie's History Files**：Triangle Fire + Victorian Workhouse的完整研究（与Ethan的案件平行对照）
- **Tribunal Seat**：月度读者案卷裁决
- **Standard Changelog**：v1.0 → v1.3 的完整推导过程
- NPC命名权

---

## Part D：情感线与地理线

### 情感线（不抒情，只记账）
- **Ep001**：Ethan听到Lily在电话里哭，他的手抖了
- **Ep003**：Sophie 念出 $475,000 时停顿。Ethan 打不开冰箱门。
- **Ep006**：Lily 被救了，但 Ethan 知道漏洞被堵了。下一个 Lily 怎么办？
- **Ep009**：Sophie 第一次在播客里提高声音。Ethan 在停车场坐了40分钟。
- **Ep012**：系统升级了，漏洞更难用。Ethan 意识到每次赢都让系统更聪明。
- **Ep015**：Ethan 发现自己在心里给人"算分"。他开始变成系统的一部分。
- **Ep018**：救了 Marcus，但挤掉了3个年轻人。零和博弈第一次可视化。
- **Ep021**：Sophie 的15秒沉默。Lily 的妈妈问"我有什么选择？"（道德损伤顶点）
- **Ep024**：Sophie 问"你赢了吗？"。Ethan 说"我不知道。"（全卷最强cliff）

### 地理线
- **小案1**（Ep001-006）：办公室 → 医院财务 → Lily 的病房 → Ethan 的厨房
- **小案2**（Ep007-012）：审计部门 → 停车场 → Brad 的办公室 → IT 机房
- **小案3**（Ep013-018）：急诊白板 → Rachel 的工位 → Marcus 的病房 → 浴室镜子
- **小案4**（Ep019-024）：会议室 → 法律援助办公室 → Brad 的办公室 → "Claims Optimization" 新工位

---

## Part E：Sophie Board 的"解锁层级"

### 公开版（Royal Road）
只给"状态"，不给"为什么"：
```
**Threat Level**: MEDIUM
**Accountability Chain**: FUZZY
```

### 付费版（Ream Tier2）
给"为什么"和具体受害者：
```
**Threat Level**: MEDIUM (because Brad is now adapting - he's learning our playbook)
**Accountability Chain**: FUZZY 
  - Brad authorizes auto-deny policy
  - System executes it
  - Executives don't know the rate is 94%
  - Regulators don't audit edge cases
  → No one is individually accountable, but collectively everyone is
```

---

## Part F：关键钩子点（用来吸读者持续付费）

### 强制"不可裁决"的瞬间（每案 Ep4 末）
- **Ep004 末**：Ethan违规了，但救了人。你支持他吗？（第1次投票上瘾）
- **Ep010 末**：系统在追回"仁慈"。你愿意用Malicious Compliance反击吗？（第2次）
- **Ep016 末**：救一个人就要挤掉另一个人。你怎么选？（第3次）
- **Ep022 末**：泄露底价能救847人，但你会坐牢。你做吗？（第4次，最强cliff）

### 提前章节吸引点（为什么要订阅Ream提前看）
- Ep005-006：Ethan 怎么执行的？Brad 的第一波反制是什么？（Ream用户提前2-4周看到）
- Ep011-012：审计算法怎么被攻破的？新算法 v2.0 有什么升级？
- Ep017-018：QALY 公式被怎么改的？被挤掉的人怎么了？
- Ep023-024：Brad 为什么不上报？Ethan 被"收编"意味着什么？
- **独占深度材料**：每案的Adjudication Stack + Unredacted Files + Counterfactuals（永不上RR）

---

## 执行指南

### 写作顺序
1. 先写每个小案的 **Ep1 Docket**（确立痒点）
2. 再写 **Ep2 Evidence**（找准数字/邮件/证据）
3. 然后写 **Ep3 Sophie+Emotion**（情感锚点 + 病毒金句）
4. 设计 **Ep4 Options**（三条路，每条都触线 + 投票题）
5. 写 **Ep5 Court**（执行 + 系统即时反应）
6. 最后写 **Ep6 Aftermath**（系统升级 + Sophie Board + 下一案钩子）

### 每个Ep的长度
- Docket：3000-4000 字（轻快，建立情绪）
- Evidence：4000-5000 字（密集信息，让读者看见河道）
- Sophie+Emotion：3500-4500 字（慢节奏，让读者呼吸，病毒金句必须在这里）
- Options：3500-4500 字（强制冲突，三个选项都要详细 + 投票题）
- Court：5000-6000 字（高潮，Ream提前章节）
- Aftermath：4000-5000 字（系统反制 + Sophie Board + 下一案埋线）

### 检查清单
- [ ] 每个小案是否在Docket有明确的"痒点"？
- [ ] 证据链是否能让读者理解"系统如何工作"？
- [ ] Sophie+Emotion 是否有：Sophie情感深度 + Emotional Anchor + 道德损伤内化 + 病毒金句？
- [ ] Options是否真的"不可裁决"（每个选择都有代价）？
- [ ] Court是否有具体操作细节和系统即时反应？
- [ ] Aftermath是否显示"系统适应/升级" + 下一案痒点？
- [ ] 情感线是否递进（而不是重复）？
- [ ] 地理线是否展示"制度地理"（而不只是风景）？
- [ ] Sophie Board是否在Ep6末尾露出"状态"但不露"原因"？
- [ ] Ream提前章节的节奏是否让付费用户始终领先2-4周？
- [ ] Ream独占深度材料（Adjudication Stack/Unredacted Files/Counterfactuals）是否每案都有？
