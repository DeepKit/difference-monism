# IEEE Software 深度审阅报告（优化版）
面向：IEEE Software（Magazine，领先软件实践者）
建议结论：Major Revision（有条件接收）

---

## 0. 执行摘要（给编辑/作者的一页版）
**一句话评价：** 文章提出的 Artifact–Contract–Sealing（ACS）/ Output-Driven Development（ODD）把“AI生成代码的责任与验收”从 *code review* 转移到 *contract + evidence + sign-off*，非常契合 IEEE Software 对「思想领导力 + 可落地实践」的定位。

**当前最大风险：** 文章整体仍偏“研究论文/宣言”，而 IEEE Software 更看重“下周一就能用”的工作流、工具链、失败复盘与成本现实。

**本轮改稿三大目标（只抓大石头）：**
1. **压缩到 ≤5,000 words**：删/并/移，把“解释框架”变成“可用方法”。
2. **把 ODD 变成可执行流程**：给出 *CLI/CI* 路径、角色分工、迁移路线、失败场景。
3. **补齐互操作与成本**：SLSA/in-toto 映射、mutation testing 成本与扩展策略。

---

## 1. 期刊适配（Magazine Fit）——为什么现在读起来像 TSE/TSE 风格
### 1.1 读者预期（IEEE Software 典型“阅读方式”）
IEEE Software 读者通常：
- 先看 **摘要 + 图 1 + Checklist**
- 再快速扫 **工具/流程/角色**
- 最后才愿意读概念来源与相关工作

你当前稿件的阅读阻力：
- **Abstract 缺“可执行承诺”**（像研究论文摘要）
- **形式化/定义密度偏高**（LaTeX 公式在该刊极不友好）
- **缺工具链与迁移路径**（读者无法评估投入产出）

### 1.2 最小改动原则（不推倒重写的改造策略）
核心思路：
- **把“定义”移到边栏/框（Sidebar/Callout Box）**
- **把“流程”拉到正文主线**（图 + step-by-step + CLI）
- **把“可信度”用互操作/成本/失败案例来补**

---

## 2. 结构性建议：建议改稿后的目录（含字数预算）
> 目的：把 8,000+ 收敛到 5,000 左右，同时把“宣言感”替换为“实践指南感”。

**建议目录（可直接照抄）：**
1. **What problem are we solving?（~500）**
   - Hook：*“We can ship AI-generated code without reading every line—if approval attaches to contracts, not diffs.”*
2. **ODD in one picture（~400）**
   - 一张清晰流程图：Artifact → Evidence → Contract → Seal → Deploy gate
3. **Three primitives: Artifact / Contract / Seal（~900）**
   - 每个 primitive：一句定义 + 一段“工程含义” + 一个例子
   - 形式化定义放 Sidebar
4. **Workflow: how a team uses ODD（~1,000）**
   - CLI/CI 示例（哪怕伪命令）
   - 角色：谁写 contract，谁签 seal，谁仲裁
5. **Interoperability: mapping to SLSA / in-toto（~600）**
   - 明确：ODD 在 provenance 上“复用/兼容”，并新增“contract acceptance decision”的签名层
6. **Cost & scale reality（~600）**
   - mutation testing 成本估算 + 采样/增量/并行策略
7. **Adoption guide（Checklist + migration path）（~800）**
   - “Monday morning plan”：从一个 artifact type 开始
8. **Risks & mitigations（~200）**
   - 取代 Threats to Validity（用工程语言）

> 备注：相关工作与哲学性对比（Agile/DevOps/DbC 的长论述）尽量压缩成“对照表 + 150 字解释”。

---

## 3. 分章节点评（保留你原有框架，但更“可执行”）

### 3.1 Abstract & Introduction
**问题：** Abstract 现在更像 research manifesto，缺少对实践者的直接承诺。

**推荐改写模板（可直接替换摘要首句/末句）：**
- 开场：
  > We introduce Output-Driven Development (ODD), a practical governance workflow that lets teams ship AI-generated code without reading every line—by shifting approval from code review to verifiable contracts.
- 收尾：
  > Practitioners can adopt ODD in three steps: pick one artifact type, draft contracts as acceptance criteria, and seal passing artifacts in CI with an auditable sign-off record.

**术语密度控制：**
- 第一屏只出现：ODD、contract、seal（最多再加 evidence）
- “responsibility anchors / legitimacy / arbitration” 延后，并配 1 句通俗解释

### 3.2 Core Concepts（第2章）：形式化过剩
**风险：** LaTeX 公式会让 IEEE Software 读者直接跳过。

**建议：**
- 正文只保留操作性定义：
  - “contract = acceptance criteria”
  - “seal = signed decision that binds artifact + contract + evidence”
- 形式化表达：放 **Sidebar: Formal definition (optional)**

**必须补：失败案例（Failure Scenario）**
你当前 vignette 只有“成功路径”，缺少“失败后谁负责”。

**建议插入一个具体争议：**
- mutation tests 通过，但安全审计发现密钥泄露
- 追溯：contract 缺少“secrets scanning”条款 → contract 作者/签署者责任清晰化
- 产出：一个“改进后的 contract diff + 新的 seal”示例

**工具链空白（Magazine 的硬门槛）**
即使 Progee 未开源，也必须给“读者可想象的工作流”。

**建议最少提供：**
```text
odd contract init payments
odd verify --contract payments.yaml --artifact dist/payments-service
odd seal   --contract payments.yaml --artifact dist/payments-service --evidence evidence.json
odd attest --format slsa --out provenance.intoto.jsonl
```
（命令可为示意，但要把输入/输出讲清楚：artifact/evidence/seal/provenance 各是什么文件。）

### 3.3 Context（第3章）：区分度做对了，但缺迁移路线
**建议新增小节：Migration Path（强烈推荐）**
- Small：新 API endpoint
- Medium：一个微服务
- Large：遗留系统（先封装 contract 边界）

并给出“何时适合/不适合”：
- 适合：变更频繁、review 成本高、验收可契约化的模块
- 不适合：验收标准高度主观且短期难形式化的模块

### 3.4 Implications（第4章）：把 4.7 Checklist 升级成 Practitioner's Guide
**建议把 checklist 改成 7 天试点脚本：**
- Day 1：Inventory（选 1–2 artifact types）
- Day 2：Draft contract（用模板）
- Day 3：Wire into CI（产生 evidence package）
- Day 4：Set policy thresholds（mutation/coverage/security）
- Day 5：Run pilot + log arbitrations
- Day 6：Review failures + tighten contract
- Day 7：Decide expand/rollback

**前置卖点：Governance Without Full Transparency**
这段建议上移到 Introduction：
- 让读者立刻理解：ODD 不要求读懂每行 diff，也不要求模型可解释性本体论胜利；它只要求“验收与责任可追溯”。

### 3.5 Limitations（第5章）：改成 Risks & Mitigations
把 Threats to Validity 改写为工程语言，例如：
- False sense of security → “Seals can be over-trusted”
- Contract drift → “Contracts rot when systems evolve”
- Evidence spoofing → “Evidence must be generated in trusted CI”

---

## 4. 关键性内容缺口（Critical Gaps）

### 4.1 SLSA / in-toto 互操作（P0）
**风险：** 只引用不映射，会被认为“重复造轮子”或“概念不落地”。

**建议最小补丁段落（可直接粘贴进 2.3/Interoperability）：**
- ODD sealing 与 SLSA provenance 的关系：
  - provenance：描述“如何构建出来”
  - ODD seal：描述“是否通过验收 + 谁签字”

### 4.2 Mutation testing 成本现实（P0）
必须给：
- 粗略的时间/资源量级（哪怕区间）
- 三条可扩展策略：
  1) 采样（mutation sampling）
  2) 增量（只测受影响模块）
  3) 并行（CI fan-out）

### 4.3 人类角色具体化（P1）
建议明确：
- 仲裁者是谁：Tech Lead / Security Owner / Release Manager
- 仲裁在哪里发生：PR 评论？Dashboard？Release gate？
- 仲裁成本：一次 contract sign-off 的时间级别（分钟/小时）

---

## 5. 语言与风格：从“学术名词化”到“工程可读”
### 5.1 高频替换（建议全文一键统一）
- legitimacy → acceptance (criteria)
- arbitration → sign-off / exception handling
- responsibility anchors → who signs what
- artifact-centric governance → govern outputs, not diffs

### 5.2 句法规则
- 尽量主动语态：ODD does…, Verification checks…, Teams adopt…
- 每段第一句先给结论，第二句再解释
- 每一节至少给一个“文件/命令/截图/例子”作为落点

---

## 6. 改稿优先级清单（可直接当 TODO）

### P0（不做大概率拒）
- 压缩到 ≤5,000 words（删 30–40%）
- 移除正文 LaTeX 公式（移 Sidebar/附录）
- 补 SLSA/in-toto 映射（清晰说明“复用 + 新增一层签名决策”）
- 加 Progee/ODD 的最小 CLI/CI 工作流示例

### P1（显著提升接受率）
- 重写 Abstract：加入 “3 steps adoption”
- 把 4.7 扩成完整 practitioner's guide（7 天试点脚本/路线图）
- 增加失败案例：When the contract was wrong
- 角色具体化：谁写/谁签/谁仲裁/成本多少

### P2（锦上添花）
- 一张专业流程图替换 ASCII
- “Industry voices” 边栏（1–2 句来自采用者/团队反馈）
- 粗略成本收益：CPU vs human review time

---

## 7. 投稿策略建议（Cover Letter 可用话术）
- 指明栏目：Practices / Thought Leadership
- 明确文章定位：治理框架 + adoption guidance（不是实证论文）
- 如果有 companion work：说明“本篇给实践者可落地框架，后续篇章给实证细节/长期数据”（注意别显得在本篇“挖坑不填”，而是“分篇交付”）

---

## 8. 预测审稿人问题（你需要在正文里主动回答）
1. “How do I sell this to my manager on Monday?” → 用 adoption guide 回答
2. “How does sealing map to SLSA provenance?” → 用 interoperability 回答
3. “Mutation testing is too expensive—how does it scale?” → 用 cost & scale 回答

---

## 9. 下一步行动（写作层面最划算的 2 件事）
1. 先做 **一页 Visual Abstract（流程图 + 3-step adoption）**，再反推正文删改。
2. 准备 **一个工具链截图/伪 UI**（PR gate 或 dashboard），替换 ASCII 流程图，并把“仲裁发生在哪儿”具体化。
