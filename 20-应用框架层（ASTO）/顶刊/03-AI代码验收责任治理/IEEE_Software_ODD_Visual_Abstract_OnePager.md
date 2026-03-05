# ODD / Artifact–Contract–Sealing 一页实施路线图（Visual Abstract Draft）
面向：IEEE Software（Practices / Thought Leadership）

---

## 核心主张（给实践者的一句话）
**我们可以在不逐行阅读 AI 生成代码的前提下上线——前提是把“批准”绑定到可验证的合同（Contract）与可审计的签章（Seal），而不是绑定到作者或 diff。**

---

## 问题（Why now?）
- **AI 让代码产出变得充裕**，但 **责任与验收变得弥散**：谁该为一次“看似通过 CI、但最终出事故”的变更负责？
- 传统 Code Review 以“阅读 diff”作为主要控制面，在 AI 生成与代理式提交场景下变成瓶颈。

---

## 方案（What is ODD?）
ODD（Output-Driven Development）把治理控制面从 *diff 阅读* 转移到 *输出验收*：
- **Artifact**：要上线的输出物（镜像/二进制/包/配置/迁移脚本等）
- **Contract**：验收标准（Acceptance Criteria），可被自动验证
- **Evidence**：验证证据包（测试、扫描、构建、环境、SBOM 等）
- **Seal**：对“该 Artifact 在该 Contract 下已通过验收”的**签名决策记录**（谁签、何时签、签了什么）

---

## 一图读懂（Control Surface）
```mermaid
flowchart LR
  A[AI/Dev changes] --> B[Build produces Artifact]
  B --> C[Run Verification]
  D[Contract
(acceptance criteria)] --> C
  C --> E[Evidence Package]
  E --> F[Decision: Pass / Exception]
  F -->|Pass| G[Seal (signed approval)]
  F -->|Exception| H[Human arbitration
(sign-off + rationale)]
  G --> I[Release gate allows deploy]
  H --> I
```

---

## 三步落地（Monday-morning adoption）
### Step 1 — 选一个“高价值输出物”（1 天内）
优先选择：
- 每周改动频率高、review 成本高
- 失败代价可控（适合试点）
- 验收能被契约化（测试/扫描/策略阈值可定义）

例：一个新 API endpoint / 一个微服务的容器镜像 / 关键配置包。

### Step 2 — 写一个“能跑起来”的 Contract（1–2 天）
Contract 不追求完美，追求可迭代：
- 功能：关键集成测试必须通过
- 安全：secrets scanning / SAST / 依赖漏洞阈值
- 质量：覆盖率/突变测试阈值（先低后高）

（写作提示：把“legitimacy/arbitration”等抽象术语落到“acceptance/sign-off/exception handling”。）

### Step 3 — 把 verify + seal 接入 CI（1–3 天）
最小可用工作流（示意）：
```text
odd verify --contract payments.yaml --artifact dist/payments-service
odd seal   --contract payments.yaml --artifact dist/payments-service --evidence evidence.json
odd attest --format slsa --out provenance.intoto.jsonl
```

---

## 角色与责任（Who does what?）
- **Contract Author（通常是 Tech Lead / Service Owner）**：定义验收边界；为“合同缺口”负责。
- **Seal Signer（Release Manager / Security Owner 之一）**：为“在该合同下批准上线”负责。
- **Arbitrator（当出现例外）**：在 dashboard/PR gate 上记录理由与补救措施（例：临时豁免 + 期限）。

---

## 失败场景（一定要写进正文的例子）
**When the contract was wrong**：
- mutation tests 通过，但上线后发现密钥泄露（或权限过大）。
- 追溯：Contract 未包含 secrets scanning / policy-as-code 检查。
- 处理：记录一次 arbitration；补齐 contract；生成新的 seal。

*要点：ODD 不承诺“不会出错”，它承诺“错误可追溯、可复盘、可迭代收敛”。*

---

## 与 SLSA / in-toto 的互操作（必须明确）
- **SLSA/in-toto provenance**：回答“这个 artifact 是怎么构建出来的”。
- **ODD seal**：回答“这个 artifact 在哪些验收标准下被谁批准上线”。
- ODD 的增量价值：把“验收决策（acceptance decision）”作为独立、可签名、可审计的层加入供应链记录。

---

## 成本现实（突变测试怎么不把 CI 打爆？）
推荐在正文给出三条策略：
1) **采样**：mutation sampling（先覆盖关键模块）
2) **增量**：只对受影响范围做 mutation（基于变更影响分析）
3) **并行**：CI fan-out + 结果汇总进 evidence

---

## 你应该在 paper 里显式回答的 3 个问题
1) 经理会问：**“我下周一怎么试点？”** → 用“三步落地 + 7 天试点脚本”回答。
2) 安全会问：**“这和 SLSA/in-toto 什么关系？”** → 用互操作映射回答。
3) 平台会问：**“mutation testing 太贵怎么扩展？”** → 用成本现实与策略回答。
