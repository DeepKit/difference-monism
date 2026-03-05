# ASTO 跨学科元语言：模拟顶级审稿意见（Major Revision）与回应策略
**目标期刊**：Applied Ontology  
**模拟审稿团**：N. Guarino, B. Smith, C. Welty, A. Gangemi, K. Janowicz  
**定位**：将 ASTO 定义为“解决跨学科知识割裂的内容工程元语言”，而非纯粹的形式系统。

---

## 总体评价（Executive Summary）
**推荐结论**：**Major Revision**（有条件重投）  
**共识意见**：本文提出的 ASTO（Attribute-Set Theory Ontology？）作为一个跨学科元语言，其核心动机（解决知识割裂）非常契合本刊宗旨。作者试图通过一组最小原语（属性集、切割、扰动、封板）来统一描述不同学科中的对象化与规范性问题，这是一个雄心勃勃且必要的尝试。然而，当前版本在以下三个方面存在关键缺陷，阻碍了其发表：
1.  **本体承诺（Ontological Commitment）不清晰**：ASTO 到底是一种实在论的描述语言，还是一种工具主义的规范语言？
2.  **形式语义与互操作性（Formal Semantics & Interoperability）脱节**：原语定义缺乏形式化约束，且未展示与现有标准（如 RDF/OWL, PROV, ODRL）的明确映射。
3.  **评估（Evaluation）薄弱**：虽然给出了 ODD 等案例，但缺乏系统的“能力问题（Competency Questions）”测试来证明其确实减少了跨学科割裂，而非仅仅造了一套新术语。

我们鼓励作者在进行重大修改后重投。

---

## 审稿人 1 (Nicola Guarino - Formal Ontology & Conceptual Analysis)
**[Critical] 1. 本体承诺的模糊性**  
作者声称 ASTO 是“元语言”，但其中的“属性集（Attribute-Set）”和“切割（Cut）”到底是世界本身的结构（Realism），还是认知主体的操作（Constructivism）？在文中，有时候“扰动”被描述为物理事件（能量耗散），有时候又被描述为认知状态（信息熵）。  
*   **审稿人建议**：必须明确区分“对象层（Object-level）”的属性和“元层（Meta-level）”的规范。请使用 DOLCE 或 BFO 的顶层分类来定位你的原语。例如，ODD 中的“Contract”是信息对象（Information Object），还是社会性承诺（Social Object）？
*   **回应策略**：
    *   **承认**：承认当前混合了描述性与规范性。
    *   **修正**：明确 ASTO 的双重性——它是一种**“操作性本体论”（Operational Ontology）**。它不关心“世界到底是什么”，而关心“在特定操作约束下，对象如何被构建”。
    *   **落地**：将 ASTO 原语映射到 BFO/DOLCE：例如，“Perturbation”映射为 `Process`，“Contract”映射为 `Generic Dependent Continuant`（规范）。

**[Major] 2. “同一性”的跨域问题**  
文中提到“通过封板（Sealing）确立同一性”。这在工程上讲得通（hash 相同即同一），但在哲学上，如果一个属性集变了一个非关键属性，它还是同一个对象吗？ASTO 如何处理“忒修斯之船”问题在跨学科语境下的不同标准？

---

## 审稿人 2 (Barry Smith - Realism & BFO)
**[Critical] 3. 避免“规范”与“描述”的范畴错误**  
我非常担心作者混淆了“是（Is）”和“应当（Ought）”。ASTO 试图用同一套语言描述“物理扰动”和“违反合同”。物理扰动是因果的，违反合同是规范的。如果不做区分，这套语言在逻辑上就是不一致的。
*   **审稿人建议**：引入模态算子（Modal Operators）或明确的 Deontic Logic（道义逻辑）层，将“Acceptance Criteria”与“Physical Properties”严格分开。
*   **回应策略**：
    *   **核心辩护**：ASTO 的创新点正是在于**打破二分**——在工程系统中，物理失效（bug）和规范失效（policy violation）在“阻断交付”这一功能上是等价的。
    *   **技术修正**：引入 `Constraints` 原语，作为连接 `Is` 与 `Ought` 的桥梁：物理约束（硬）vs 规范约束（软/可仲裁）。

---

## 审稿人 3 (Chris Welty - Conceptual Modeling & Evaluation)
**[Major] 4. 评估标准的缺失**  
作者声称 ASTO 解决了“知识割裂”。这目前只是一个断言。我需要看到证据。你怎么证明用 ASTO 描述“前列腺癌诊断”和“软件代码交付”，比用两套分别的语言描述更有效？
*   **审稿人建议**：设计一组 **Competency Questions (CQs)**。例如：“在 ASTO 中，能否查询‘哪个规范导致了这次验收失败’，无论该规范来自医学指南还是代码风格？”如果能，请展示 SPARQL 查询或逻辑推理路径。
*   **回应策略**：
    *   **新增章节**：在“Evaluation”部分，列出 3-5 个具体的 CQs。
    *   **实证演示**：用 ODD 的真实数据（Evidence Package）作为输入，展示 ASTO 如何统一查询“责任归属”。

---

## 审稿人 4 (Aldo Gangemi - Ontology Design Patterns)
**[Moderate] 5. 与现有模式的复用**  
ASTO 定义了“Artifact”、“Agent”、“Process”。为什么不复用 PROV-O（W3C Provenance Ontology）？重新发明轮子是本体工程的大忌。
*   **审稿人建议**：请提供一个 mapping table（映射表），说明 ASTO 原语与 PROV-O、ODRL（Rights Expression Language）的关系。如果 ASTO 只是 PROV-O 的一个 profile，请直说。
*   **回应策略**：
    *   **区分**：ASTO 不仅仅是 Provenance（过去发生了什么），它包含 Contract（未来应当发生什么）。PROV-O 缺乏这种“前瞻性规范”能力。
    *   **兼容**：承诺 ASTO 可编译为 PROV-O + ODRL 的组合。

---

## 审稿人 5 (Krzysztof Janowicz - Semantic Web & Interoperability)
**[Major] 6. 形式语义的可计算性**  
ASTO 看上去很灵活，但它的计算复杂度是多少？如果你允许任意的“属性集切割”，这在逻辑上可能是不可判定的（Undecidable）。
*   **审稿人建议**：定义 ASTO 的一个 **Decidable Fragment**（可判定子集）。例如，限制 Contract 的表达力为 SHACL 或 OWL 2 RL。
*   **回应策略**：
    *   **工程妥协**：明确 ASTO 在工程落地时（如 ODD），采用的是有限的、基于规则的验证（如 JSON Schema / Rego），而非全阶逻辑推理。这保证了 $O(n)$ 的验证效率。

---

## 作者（你）的行动计划（Action Plan）

基于以上意见，下一版论文（Revision 1）的**核心重构策略**：

1.  **明确本体定位（针对 Guarino & Smith）**：
    *   在 Intro 明确：ASTO 是一种 **"Middle-out Ontology"** —— 它不自上而下规定世界结构，而是自下而上提取跨域操作的公共模式（Pattern）。
    *   承认 ASTO 在“操作层”统一了物理与规范（因为在控制回路中它们都是“约束”）。

2.  **增强互操作性（针对 Gangemi）**：
    *   增加一节 **"Alignment with Standards"**。
    *   画一张图：ASTO = PROV-O (Traceability) + ODRL (Normativity) + SHACL (Validation)。

3.  **强化评估（针对 Welty）**：
    *   引入 **"Case Study: The Isomorphism of Failure"**。
    *   对比案例 A：AI 代码生成的封板失败（ODD）。
    *   对比案例 B：医疗诊断中的误诊（基于《运行何以失效》中的案例）。
    *   证明：用 ASTO 可以画出**完全同构**的“扰动-切割-失效”流程图。

4.  **形式化“最小核”（针对 Janowicz）**：
    *   不要试图形式化整个世界。只形式化 **"Acceptance Function"**：$f(Artifact, Contract) \rightarrow \{Pass, Fail\}$.
