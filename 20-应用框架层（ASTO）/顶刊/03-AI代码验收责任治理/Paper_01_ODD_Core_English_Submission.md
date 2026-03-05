# The ODD Series Paper I: Foundations of Artifact Legitimacy in AI-Native Software Engineering
<!-- ODD-ZENODO-DOI:18207648 BEGIN -->
> **统一确权引用 / Canonical Reference (Zenodo DOI)**
> 中文（推荐引用）：Yi Fu. 《输出驱动开发：AI辅助软件工程的范式转变》. Zenodo, 2026. DOI: 10.5281/zenodo.18207648. (https://doi.org/10.5281/zenodo.18207648)
> English (recommended citation): Yi Fu. *Output-Driven Development: A Paradigm Shift in AI-Assisted Software Engineering*. Zenodo, 2026. DOI: 10.5281/zenodo.18207648. (https://doi.org/10.5281/zenodo.18207648)
> Record: https://zenodo.org/records/18207648

```bibtex
@misc{odd_zenodo_18207648,
  author    = {Yi Fu},
  title     = {Output-Driven Development: A Paradigm Shift in AI-Assisted Software Engineering},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18207648},
  url       = {https://doi.org/10.5281/zenodo.18207648}
}
```
<!-- ODD-ZENODO-DOI:18207648 END -->

> **Author**: Yi Fu . (ODDFounder, fuyi.it@live.cn)
> **Date**: 2026-01-12
> **Version**: v7.1 (English Edition)

---

## Abstract

Large Language Models (LLMs) are making code generation abundant and inexpensive. This shifts the bottleneck of software engineering from producing code to governing outcomes: AI can generate changes faster than humans can review them. When review bandwidth collapses, traditional responsibility anchors—authorship and code review—no longer scale.

We introduce Output-Driven Development (ODD), a control paradigm for AI-native software engineering. ODD treats the *artifact* (a verifiable output with use-value) as the unit of governance, and treats *contracts* as legitimacy boundaries that anchor acceptance decisions. Unlike approaches that optimize prompts or simply add more tests, ODD explicitly reallocates responsibility from authorship to arbitration: humans approve contracts and accept or reject artifacts; the system generates evidence (tests, adversarial probes, and mutation testing) and seals accepted artifacts with an auditable record.

We present operational definitions, a minimal vignette, and practical implications for teams adopting AI-assisted development. Empirical validation with production data is planned as future work.

### Key takeaways (for practitioners)
- AI-native scaling requires shifting control from reviewing code to accepting artifacts under explicit contracts.
- Contracts are not prompts; they are legitimacy boundaries that make acceptance auditable.
- Replace "trust the author/reviewer" with "trust the evidence + explicit arbitration" (tests, adversarial probes, mutation testing).
- Sealing is an auditable acceptance record, similar in spirit to supply-chain provenance/attestation (e.g., in-toto and SLSA) but applied to AI-generated artifacts [12, 13, 15].
- ODD complements Agile/TDD; it is an orthogonal governance layer, not a replacement.

**Keywords**: Output-Driven Development, AI-Native Software Engineering, Software Governance, Artifact Legitimacy, Contract, Mutation Testing, Provenance, Accountability

---

# 1. Introduction

## 1.1 Background: The Broken Control Surface

Recent advances in large language models (LLMs) have fundamentally altered how software is produced [6, 7].
Code generation systems such as Copilot, ChatGPT, and Claude are no longer auxiliary tools; they increasingly act as *primary producers* of executable artifacts.

However, while generation capability has advanced rapidly, **the control structures of software engineering have not evolved accordingly**.

Traditional software engineering methodologies—including Agile, DevOps, Test-Driven Development (TDD), and Model-Driven Engineering (MDE)—implicitly assume that:

* source code is authored by humans,
* reasoning about behavior is mediated through code inspection,
* responsibility can be traced through authorship and commit history.

These assumptions no longer reliably hold in AI-assisted production.

As a result, modern software systems increasingly exhibit a paradoxical condition:

> **Code is abundant, yet responsibility is diffuse.
> Automation is powerful, yet control is fragile.**

Recent developer surveys suggest AI-assisted coding has reached critical mass, but verification and accountable acceptance have not kept up. For example, Stack Overflow’s 2024 Developer Survey reports broad use (or planned use) of AI tools alongside a persistent trust gap in AI output [17]. Sonar’s 2026 developer survey highlights what it calls a “verification gap” between low trust and inconsistent verification practices [18]. These signals suggest that the limiting factor is shifting from generation speed to verification and responsible acceptance.

## 1.2 The Core Problem: Loss of Responsibility Anchors

The central challenge introduced by AI-assisted software generation is **not correctness alone**, but the erosion of *responsibility anchors*.

In conventional workflows, responsibility is implicitly attached to:

* the human author of the code,
* the review process,
* or the ownership of a module.

In AI-assisted workflows, however:

* code may be generated, revised, and regenerated multiple times,
* generation paths are opaque and non-deterministic,
* multiple agents (human and AI) may contribute asynchronously.

Under such conditions, **the question "Who is responsible?" becomes structurally ill-defined**.

Existing responses largely attempt to restore control by:

* improving prompt engineering [8],
* adding more tests,
* constraining models or sandboxing execution.

While useful, these approaches operate *within* the code-centric paradigm and therefore fail to address the deeper structural shift.

ODD is not a new prompt recipe, a new testing technique, or a repackaging of Design by Contract (DbC) [2], TDD [3], CI quality gates, or software supply chain signing [12, 13, 15]. It is a change in the **control surface**: the primary object of governance becomes the artifact and its acceptance boundary, and responsibility is anchored in explicit arbitration decisions rather than in authorship or continuous review [11].

## 1.3 Why Code-Centric Control No Longer Suffices

Code-centric methodologies assume that:

* understanding code implies understanding system behavior,
* reviewing code implies validating intent,
* maintaining code implies preserving correctness over time.

In AI-assisted development, these assumptions degrade for three reasons:

1. **Human unreadability**
   Generated code may be syntactically valid and functionally correct, yet cognitively opaque.

2. **Ephemeral implementations**
   Code becomes disposable: regeneration is often cheaper than maintenance.

3. **Decoupling of intent and implementation**
   The entity expressing intent (human) is no longer the entity producing implementation (AI).

Consequently, code can no longer serve as the primary locus of control, verification, or responsibility.

## 1.4 Reframing the Question: From "How Is Code Written?" to "What Is Produced?"

This work argues that the appropriate response is not to further optimize code generation, but to **reframe the unit of software engineering itself**.

Instead of asking:

* *How should code be written?*
* *How can AI generate better code?*

We propose to ask:

* *What outputs are acceptable?*
* *How can those outputs be verified, audited, and owned?*
* *Where does responsibility reside when implementations are transient?*

This shift motivates a paradigm in which **the produced output artifact, rather than the code or generation process, becomes the primary object of control**.

> **Definition**: An *Artifact* in ODD is a verifiable output produced during software development that satisfies specific human needs and has use-value. Artifacts are the true goal of software development—not code itself.

## 1.5 Output-Driven Development (ODD): A Paradigm Shift

To address the above challenges, we introduce **Output-Driven Development (ODD)**, an artifact-centric methodology for AI-assisted software engineering.

ODD is founded on three core principles:

1. **Outputs as first-class entities**
   Artifacts are explicitly specified, validated, and audited.

2. **Contracts before generation**
   Acceptable output spaces are defined prior to any AI execution.

3. **Responsibility through arbitration**
   Humans are positioned as contract reviewers and final arbiters, not routine implementers.

Rather than attempting to eliminate human involvement, ODD **concentrates human attention on irreducible decision points**, while delegating routine generation and validation to AI systems.

### Figure 1. ODD control surface (artifact legitimacy)

```
Human intent
   |
   v
Contract (legitimacy boundary)  <--- human arbitration (approve/clarify)
   |
   v
Artifact candidate (AI-generated output)
   |
   v
Verification policy (tests + adversarial probes + mutation testing)
   |
   v
Evidence package (reports + hashes + provenance metadata)
   |
   v
Arbitration decision: ACCEPT -> SEAL  /  REJECT -> REWORK
```

## 1.6 Contributions

This paper makes the following contributions:

1. **Control-surface reframing**
   We define ODD as a shift in software governance: from code/process as the primary control unit to **artifact legitimacy** as the unit of acceptance.

2. **Responsibility anchoring via arbitration**
   We make explicit the responsibility shift from authorship and routine code review to **contract approval and artifact acceptance** at well-defined decision points [11].

3. **Operational definitions**
   We provide testable, operational definitions of *artifact*, *legitimacy*, *evidence package*, and *sealing*, and relate sealing to provenance/attestation concepts in software supply chain security [12, 13, 15].

4. **A minimal workflow + vignette**
   We outline a lightweight, magazine-style workflow and a concrete vignette showing how ODD can ship a high-risk change without line-by-line code review.

5. **Implications and research agenda**
   We summarize implications for practitioners and open research directions for contracts, verification economics, and governance under AI-assisted production.

## 1.7 Scope and Limitations

This paper focuses on **foundational definitions and conceptual structure**.

We do not claim:

* empirical superiority across all domains,
* immediate applicability to exploratory or creative programming,
* replacement of existing engineering practices.

Instead, this work provides a **structural lens** for reasoning about responsibility, control, and legitimacy in AI-assisted software production.

Empirical evaluation and system-level validation are addressed in subsequent papers in the ODD series.

> *This work does not aim to maximize automation or replace human intelligence. Instead, it introduces structural constraints to ensure that responsibility, auditability, and human arbitration remain intact and scalable under AI-assisted production.*

**Disclaimer**: This paper establishes a conceptual framework and testable hypotheses. Empirical validation using production data from our reference implementation (Progee) is planned as immediate future work. *This work is released as a preprint and has not undergone peer review.*

## 1.8 Paper Organization

The remainder of this paper is organized as follows:

* Section 2 formally defines Output-Driven Development and its core axioms.
* Section 3 contrasts ODD with existing software engineering paradigms.
* Section 4 discusses implications for verification, responsibility, and governance.
* Section 5 outlines limitations and directions for future work.

---

# 2. Core Concepts

## 2.1 Artifact Legitimacy as the Unit of Control

In ODD, the unit of engineering control is not source code or development process steps, but the **produced artifact**—a verifiable output that satisfies a human need and has direct use-value.

An artifact is *legitimate* when it is accepted under an explicit contract and backed by verifiable evidence (e.g., tests, mutation analysis, and auditable acceptance records). In other words: ODD optimizes for **defensibility of outcomes**, not readability of implementations.

**Key properties**:
- **Verifiable**: correctness can be checked against explicit criteria.
- **Need-fulfilling**: it corresponds to an explicit human need (not an internal engineering activity).
- **Use-value**: it can be used to produce real utility.

> Intuition: mature industries do not require customers to observe the entire production process; they rely on rigorous quality control and traceable acceptance.

**Operational definition (used in this paper).** We treat an artifact as a versioned deliverable that is always referenced by:
- a contract ID (what is acceptable),
- a verification policy (how it is checked),
- and an evidence package (what was observed when it was checked).

An artifact is **legitimate at time T** if it (1) passes the verification policy for its contract version, and (2) has a sealed evidence package that binds contract, code, tests, and environment via hashes.

**Formal definition (artifact legitimacy).** Let $A$ be an artifact, $c$ a contract version, $V$ a verification policy, and $s$ a seal record. $A$ is legitimate at time $t$ iff:

$$\text{Legitimate}(A, t) \iff \exists c,s: \text{Complies}(A, c) \land \text{Verified}(A, V) \land \text{Sealed}(A, s, t)$$

This definition makes the time dimension explicit: legitimacy is not a static property of code; it is a property of an accepted artifact bound to a specific contract and evidence at a specific time.

## 2.2 Contracts as Legitimacy Boundaries

A contract in ODD is a precise, machine-checkable specification of acceptable outputs, boundaries, and failure modes. It serves two functions:

1. **Constraint definition**: it bounds the acceptable output space before any generation happens.
2. **Responsibility anchoring**: acceptance is an explicit, auditable decision at a well-defined boundary.

ODD does **not** assume the contract is a complete system model; it is a control instrument that makes acceptance legible and scalable.

## 2.3 Verification and Sealing (High Level)

ODD treats verification as a layered pipeline that targets the artifact rather than the transient implementation:

1. Contract compliance checks (tests/spec checks)
2. Robustness checks (boundary/adversarial probing)
3. Test adequacy checks (mutation testing)
4. Sealing (recording evidence and freezing the accepted artifact)

The goal is not to claim “the generator is trustworthy,” but to produce an artifact whose acceptance is defensible given explicit criteria and recorded evidence.

**Sealing (operational).** A seal is an immutable record that (a) identifies the artifact version, (b) records the contract version and verification results, and (c) binds them together with cryptographic hashes/signatures. This is similar in spirit to software supply chain provenance and signing frameworks (e.g., in-toto [12], SLSA [13], Sigstore [15]), but used here as a governance primitive for AI-generated artifacts.

**Making Sealed(A,s,t) concrete: a seal record sketch.** A practical seal record should be append-only and independently verifiable. At minimum it should bind: (1) the artifact digest, (2) the contract digest, (3) the verification policy digest, (4) the evidence bundle digest, (5) the execution environment digest, and (6) the human arbiter identity and signature bundle.

```json
{
  "seal_id": "seal:2026-01-28T02:15:09Z:pay-001",
  "timestamp_utc": "2026-01-28T02:15:09Z",
  "arbiter": {
    "id": "user:yi-fu",
    "role": "human_arbiter"
  },
  "artifact": {
    "name": "payment-charge-endpoint",
    "version": "1.0.7",
    "digest": "sha256:..."
  },
  "contract": {
    "contract_id": "PAYMENTS-GATEWAY-V1",
    "digest": "sha256:..."
  },
  "verification": {
    "policy_digest": "sha256:...",
    "results_digest": "sha256:...",
    "evidence_bundle_digest": "sha256:..."
  },
  "environment_digest": "sha256:...",
  "provenance_ref": "in-toto:...",
  "signature": {
    "scheme": "sigstore/cosign",
    "bundle_digest": "sha256:..."
  }
}
```

In ODD, this record is what makes an acceptance decision auditable: an auditor can later re-run verification under the declared policy/environment, compare digests, and confirm the arbiter signature and inclusion in an append-only log (e.g., via transparency logs) [12, 13, 15].

## 2.4 A Minimal Vignette: Shipping a Payment Integration Without Code Review

Consider a team integrating a payment gateway. AI can generate the integration in minutes, but human review bandwidth is scarce and the risk of silent regressions is high. In ODD, the team does not ask humans to read every line; it asks humans to approve what “acceptable” means and to accept artifacts only with evidence.

**Step 1 — Contract (legitimacy boundary).** Before generation, the team approves a contract that makes failure modes explicit:

```yaml
contract_id: PAYMENTS-GATEWAY-V1
artifact: payment-charge-endpoint
inputs:
  idempotency_key: required
invariants:
  - never_double_charge
timeouts:
  upstream_timeout_ms: 1000
retries:
  max_attempts: 2
errors:
  - name: timeout
    rule: "no charge may be committed"
  - name: duplicate_idempotency_key
    rule: "return existing transaction id"
audit:
  required_log_fields: [request_id, idempotency_key, provider_txn_id]
```

**Step 2 — Generation + verification (evidence).** An AI agent produces implementation and tests. The system then executes the verification policy (unit/integration tests, adversarial probes for edge cases, and mutation testing to check test adequacy).

**Step 3 — Sealing (acceptance record).** If verification passes, the artifact is accepted and sealed with an evidence package, e.g.:

```json
{
  "artifact_id": "payment-charge-endpoint",
  "contract_id": "PAYMENTS-GATEWAY-V1",
  "decision": "accept",
  "evidence": {
    "tests": "pass",
    "adversarial_suite": "pass",
    "mutation_testing": "pass"
  },
  "hashes": {
    "contract": "sha256:...",
    "code": "sha256:...",
    "tests": "sha256:..."
  }
}
```

Humans intervene only when the contract is ambiguous, verification fails, or risk policy requires explicit sign-off—not as a routine code-reading bottleneck.

**Failure and escalation examples (when verification fails).**
- If mutation testing reveals the test suite is inadequate, reject the artifact, strengthen tests (or the verification policy), and re-run.
- If the contract is ambiguous, escalate to arbitration, clarify requirements, and version the contract before acceptance.
- If adversarial probes expose boundary violations, treat as a contract violation and reject/rework.

---

# 3. Output-Driven Development in Context (Condensed)

ODD is best understood as an axis of control that is **orthogonal** to code-centric methodologies. It can coexist with existing practices while changing what is treated as the primary object of governance:

- **Agile/DevOps**: ODD does not change iteration cadence; it changes what is audited and accepted.
- **TDD**: tests remain valuable, but become one layer of evidence rather than the sole specification of intent.
- **MDE**: contracts are not comprehensive models; they are legitimacy boundaries over outputs.
- **Prompt engineering**: prompts may improve generation, but responsibility requires artifact-level evidence.
- **HITL**: humans move from continuous process supervision to decision-point arbitration.

## 3.1 ODD vs. Design by Contract (DbC)

Design by Contract (DbC) [2] introduced contracts as a way to specify and check module behavior via preconditions, postconditions, and invariants. ODD differs in scope and control surface:

- **Target of governance**: DbC assumes human-authored modular components; ODD assumes AI-generated, frequently regenerated implementations where authorship is diffuse.
- **Primary question**: DbC asks “is this implementation correct w.r.t. pre/post conditions?” ODD asks “is this artifact acceptable under an explicit acceptance boundary, with recorded evidence, at time $t$?”.
- **Time and responsibility**: DbC checks conditions at runtime; ODD includes **sealing**—a time-indexed acceptance attestation that freezes a specific artifact+contract+evidence tuple and anchors responsibility in the arbitration decision.
- **Separation vs. embedding**: DbC often embeds contracts into code; ODD treats contracts and verification policy as first-class, versioned governance artifacts that may live outside the implementation.

In short, DbC is a specification/verification technique; ODD is a governance paradigm that reallocates responsibility from authorship to arbitration under auditability constraints.

### Table 1. ODD vs Agile/TDD/DevOps/CI (control surface)

| Dimension | Agile/DevOps/TDD/CI (code-centric default) | ODD (artifact-centric governance) |
|---|---|---|
| Primary control unit | Code changes + process steps | Artifact legitimacy (artifact + contract + evidence + seal) |
| Responsibility anchor | Authorship + review + ownership | Arbitration decision at acceptance boundary |
| Specification form | User stories, tests, policies | Acceptance contracts + verification policies |
| Quality gate | Code review + CI checks | Evidence package + sealing (auditable acceptance record) |
| Scaling lever | Add people / review bandwidth | Add compute / automate verification + concentrate human decisions |

ODD aligns with empirical observations that modern code review is constrained by human understanding bandwidth and provides benefits beyond defect finding [11]. ODD also borrows from software supply chain provenance/attestation work—recording what was built and tested, and tying it cryptographically to acceptance—while shifting the motivation from consumer security to organizational responsibility at scale [12, 13, 15]. The broader context of LLM-based automation in software engineering is surveyed in [14].

For extended diagrams and detailed comparison tables (removed for magazine length), see `Paper_01_ODD_Core_English_Submission_Supplement.md`.

---

# 4. Implications of an Artifact-Centric Control Model

## 4.1 Responsibility Reallocation in AI-Assisted Production

In traditional software engineering, responsibility is implicitly anchored in authorship.
Code is written, reviewed, and maintained by identifiable individuals or teams, enabling post hoc attribution.

In AI-assisted development, this linkage weakens substantially:

* generation paths are non-deterministic,
* code authorship is diluted across multiple agents,
* implementations are frequently regenerated.

Under such conditions, responsibility can no longer be reliably inferred from process participation.

ODD addresses this issue by **reallocating responsibility from authorship to arbitration**.

> Responsibility in ODD is not derived from who wrote the code,
> but from who accepted the artifact under a specified contract.

This shift preserves accountability without requiring transparency into AI internals.

## 4.2 Contracts as Responsibility Anchors

In ODD, contracts serve a dual function:

1. **Constraint definition**
   They define the acceptable space of outputs.

2. **Responsibility anchoring**
   They establish explicit decision points at which acceptance or rejection occurs.

By requiring human confirmation at contract boundaries—rather than continuous supervision—ODD makes responsibility:

* explicit,
* auditable,
* and scalable.

Importantly, contracts in ODD are not assumed to be complete system descriptions.
They are **control instruments**, not ontological models.

## 4.3 Verification Beyond Correctness

Verification in conventional workflows is largely concerned with correctness relative to implementation.

ODD broadens the notion of verification to include:

* **contract compliance**,
* **robustness under perturbation**,
* **adversarial resistance**.

This motivates a layered verification structure in which:

* unit and integration tests assess functional behavior,
* mutation testing evaluates test adequacy,
* adversarial testing probes boundary conditions and misuse scenarios.

Crucially, verification targets the *artifact*, not the implementation.

> An implementation may vary;
> an accepted artifact must remain defensible.

## 4.4 Progressive Trust and Conditional Human Intervention

A central design principle of ODD is **progressive trust**.

Rather than applying uniform scrutiny to all tasks, ODD dynamically adjusts verification rigor based on:

* estimated complexity,
* safety sensitivity,
* external dependencies.

Human intervention is triggered only when:

* contracts are ambiguous,
* adversarial agents disagree,
* or high-risk conditions are detected.

This approach preserves human authority while preventing cognitive overload.

> Human attention is treated as a scarce governance resource.

## 4.5 Governance Without Full Transparency

A common objection to AI-assisted systems is the lack of model transparency.

ODD deliberately avoids assuming:

* interpretable models,
* explainable generation paths,
* or deterministic outputs.

Instead, it adopts a governance strategy based on **observable outcomes** and **documented acceptance decisions**.

This makes ODD compatible with:

* proprietary models,
* evolving AI architectures,
* and heterogeneous toolchains.

Governance is achieved not by introspection, but by **controlled acceptance**.

## 4.6 Risk, Failure, and Explicit Non-Goals

ODD does not eliminate risk.
It makes risk *legible*.

Failures in ODD manifest as:

* contract violations,
* failed verification stages,
* or unresolved arbitration.

These failure modes are explicit and auditable.

Equally important are ODD's non-goals:

* It does not aim to automate ethical judgment.
* It does not guarantee optimal implementations.
* It does not replace domain expertise.

ODD provides structure, not omniscience.

## 4.7 Implications for AI-Native Organizations

As AI systems become primary producers rather than assistants, organizations face a structural challenge:

> How can legitimacy be maintained when production is automated?

ODD suggests an answer:

* legitimacy derives from controlled acceptance,
* authority is exercised through arbitration,
* and responsibility is preserved through explicit contracts.

These implications extend beyond software engineering into organizational design and governance, which are explored further in subsequent work.

### Practical adoption checklist (first iteration)
- Pick 1–2 high-value artifact types (e.g., one API endpoint type + one batch job type) and define what “acceptance” means for each.
- Create contract templates that force boundary conditions (timeouts, idempotency, error codes, invariants) to be explicit.
- Define a verification policy per risk level (what tests must run, what adversarial probes are required, what mutation threshold is acceptable).
- Treat “sealing” as an append-only acceptance record (artifact version, contract version, evidence hashes); require a new seal for any change.
- Make exceptions explicit: when humans override automation, record who decided, why, and what evidence was missing.

## 4.8 Transition to Limitations and Future Work

The implications discussed above suggest both strengths and inherent limitations.

The following section examines:

* scenarios where ODD is unsuitable,
* potential failure modes,
* and directions for empirical validation.

---

# 5. Limitations and Future Work

## 5.1 Scope Limitations

ODD, as presented in this paper, is a conceptual framework rather than a fully validated engineering methodology. Several limitations constrain its current applicability:

**Domain constraints.** ODD is most naturally suited to domains where:
- outputs are objectively verifiable,
- contracts can be precisely specified,
- and mutation testing is computationally feasible.

Domains involving subjective judgment (e.g., UI aesthetics), emergent behavior (e.g., complex simulations), or real-time physical interaction (e.g., robotics) may require significant adaptation.

**Subjective acceptability.** In domains where “correctness” is partly subjective (e.g., UX feel, brand tone, fairness trade-offs, policy interpretation), ODD can still help by (1) making evaluation rubrics explicit (checklists, golden examples, rater guidelines), (2) recording arbitration decisions and their rationale as auditable governance artifacts, and (3) preventing silent drift by requiring re-sealing when criteria change. However, ODD cannot fully automate subjective judgment; it mainly provides guardrails and traceable accountability around human evaluation.

**Contract expressiveness.** Not all requirements are easily contractifiable. Tacit knowledge, contextual nuance, and evolving user expectations resist formalization. ODD does not claim to eliminate this gap—it aims to make the gap explicit and manageable.

**Verification costs.** Mutation testing, while mathematically grounded, is computationally expensive. Current implementations may not scale to very large codebases without optimization strategies such as incremental mutation, sampling, or parallelization.

## 5.2 Methodological Limitations

**Lack of empirical validation.** This paper presents ODD as a theoretical framework. Rigorous empirical studies—controlled experiments, longitudinal case studies, and industry deployments—are necessary to validate its claimed benefits.

**Organizational adoption.** ODD implies significant changes to development workflows, team structures, and skill requirements. The sociotechnical challenges of adoption are not addressed in this paper.

**Tool maturity.** While ODD is tool-agnostic in principle, practical adoption depends on mature tooling for contract authoring, mutation testing, and artifact sealing. Current tool ecosystems are fragmented.

## 5.3 Explicit Non-Goals

To prevent misinterpretation, we state what ODD does *not* aim to achieve:

- **Fully autonomous development.** ODD requires human judgment for contract definition, acceptance decisions, and exception handling. It is not a path to unsupervised AI coding.

- **Elimination of all bugs.** ODD reduces certain classes of defects (those detectable by mutation testing) but does not guarantee bug-free software.

- **Replacement of domain expertise.** Contracts encode domain knowledge; they do not generate it. Domain experts remain essential.

- **Universal applicability.** ODD is designed for AI-assisted development contexts. It may offer limited value in environments where AI code generation is not used.

## 5.4 Future Work

The ODD framework opens several research directions:

**Empirical validation.** Controlled studies comparing ODD-based workflows against traditional and AI-assisted baselines, measuring productivity, defect rates, and developer experience.

**Contract languages.** Development of domain-specific contract languages that balance expressiveness with verifiability, potentially leveraging formal methods or lightweight specification techniques.

**Scalable verification.** Research into mutation testing optimization, including machine learning-guided mutant selection, incremental analysis, and cloud-native parallelization.

**Organizational models.** Investigation of team structures, skill transitions, and governance frameworks suited to ODD adoption.

**Integration with formal methods.** Exploration of how ODD contracts can interface with formal verification, model checking, or proof assistants for high-assurance domains.

## 5.5 Threats to Validity

- **Construct validity**: Mutation score and test outcomes are proxies for acceptability; contracts may omit latent requirements.
- **Internal validity**: Tooling variance and nondeterminism in generation/adversarial probing can introduce noise in evidence.
- **External validity**: Results may not generalize to domains with subjective outputs or hard-to-contractify requirements.
- **Practical validity**: Verification costs may limit adoption without optimization and organizational support.

## 5.6 The ODD Paper Series

This paper (Paper I) establishes the core paradigm. Subsequent papers in the series address complementary concerns:

- **Paper II — Human Delegation Proof**: How trust transfers progressively from human review to verifiable mechanisms while preserving human-legible accountability.

- **Paper III — Contract Execution**: Why contract precision determines artifact correctness; methods for measuring and improving contract clarity.

- **Paper IV — Legitimacy Evolution**: How to govern re-legitimation and lifecycle management under changing requirements.

- **Paper S1 — Context Engineering**: A practical context-engineering stack (layering, token budgets, evidence-first memory) for scalable ODD implementation.

Together, these papers aim to make ODD not merely a conceptual proposal, but a complete, implementable, and auditable methodology for AI-native software production.

---

# 6. Conclusion

This paper has proposed **Output-Driven Development (ODD)**, a software development paradigm designed for the AI era.

## 6.1 Summary of Contributions

1. **Reframed the control problem.** We argued that AI-assisted development breaks the traditional control surface of software engineering, where human code review served as the final quality gate. ODD addresses this by shifting control from process supervision to artifact acceptance.

2. **Introduced artifact-centric governance.** ODD centers on *artifacts*—verifiable outputs that satisfy human needs—rather than code. This reorientation aligns development goals with user value and enables systematic verification.

3. **Established contracts as responsibility anchors.** In ODD, contracts define what constitutes acceptable output, creating explicit decision points for human acceptance. Responsibility derives from arbitration, not authorship.

4. **Proposed verification beyond code review.** ODD replaces human code review with layered verification (contract compliance, mutation testing, adversarial probing), enabling scalable quality assurance without cognitive bottlenecks.

5. **Articulated governance without transparency.** ODD demonstrates that effective governance of AI-assisted systems does not require model interpretability—it requires controlled acceptance and auditable decisions.

## 6.2 The Core Insight

The central insight of ODD is simple but consequential:

> In AI-assisted development, humans should define *what* is acceptable, not supervise *how* it is produced.

This shift preserves human authority while accommodating AI's generative capacity. It transforms the developer's role from code author to artifact architect—from someone who writes implementations to someone who specifies outcomes.

## 6.3 Implications

If ODD's premises are correct, several implications follow:

- **For practitioners**: The skills that matter shift from coding proficiency to contract specification, verification design, and acceptance judgment.

- **For organizations**: Development workflows must be restructured around artifact pipelines rather than code commits.

- **For researchers**: New research agendas emerge around contract languages, scalable mutation testing, and human-AI collaboration patterns.

- **For the field**: Software engineering may be entering a paradigm transition comparable to the shift from assembly to high-level languages—a transition in which the unit of human concern moves up the abstraction stack.

## 6.4 Subsequent Work in the ODD Series

While this paper introduces Output-Driven Development (ODD) as an artifact-centric paradigm grounded in artifact legitimacy rather than code correctness, it does not yet address several critical questions:

1. **Contract acquisition**: How can contracts be acquired with low human effort and without requiring formal-methods expertise?
2. **Enforcement mechanisms**: How can such contracts be enforced through systematic validation during AI-dominant production?
3. **Legitimacy evolution**: How do legitimacy standards evolve over time as contexts change?
4. **Context engineering**: How can context be assembled under token budgets with hard boundaries and traceability guarantees?

These questions are addressed in subsequent papers in the ODD series:

- **Paper II** (*Human Delegation Proof*) studies contract acquisition and human role minimization through clarity assessment and structured context injection.
- **Paper III** (*Contract Precision*) investigates contract precision as a control variable and proposes adversarial enforcement mechanisms with empirical evidence.
- **Paper IV** (*Legitimacy Evolution*) examines the evolution of legitimacy standards across temporal and organizational settings.
- **Paper S1** (*Context Engineering*) provides supporting infrastructure for auditable, cost-effective context assembly.

## 6.5 Closing Remarks

ODD is not a finished methodology. It is a proposal, a direction, a bet on how software development might evolve as AI capabilities advance. Its validity will be determined not by theoretical argument alone, but by empirical evidence, practical adoption, and the judgment of the engineering community.

What we offer here is a framework for thinking about a problem that will only grow more pressing: How do humans maintain meaningful control over software systems when they no longer write—or even fully understand—the code?

ODD suggests an answer: by defining what we want, verifying what we get, and accepting responsibility for the difference.

---

# References

[1] T. S. Kuhn, *The Structure of Scientific Revolutions*. Chicago, IL, USA: University of Chicago Press, 1962.

[2] B. Meyer, "Applying Design by Contract," *Computer*, vol. 25, no. 10, pp. 40–51, 1992.

[3] K. Beck, *Test-Driven Development: By Example*. Addison-Wesley, 2002.

[4] Y. Jia and M. Harman, "An analysis and survey of the development of mutation testing," *IEEE Trans. Software Eng.*, vol. 37, no. 5, pp. 649–678, 2011.

[5] R. A. DeMillo, R. J. Lipton, and F. G. Sayward, "Hints on test data selection: Help for the practicing programmer," *Computer*, vol. 11, no. 4, pp. 34–41, 1978.

[6] S. Bubeck et al., "Sparks of artificial general intelligence: Early experiments with GPT-4," *arXiv preprint arXiv:2303.12712*, 2023.

[7] M. Chen et al., "Evaluating large language models trained on code," *arXiv preprint arXiv:2107.03374*, 2021.

[8] J. Austin et al., "Program synthesis with large language models," *arXiv preprint arXiv:2108.07732*, 2021.

[9] S. Amershi et al., "Software engineering for machine learning: A case study," in *Proc. ICSE-SEIP*, 2019, pp. 291–300.

[10] M. Fowler, *UML Distilled: A Brief Guide to the Standard Object Modeling Language*, 3rd ed. Addison-Wesley, 2004.

[11] A. Bacchelli and C. Bird, "Expectations, outcomes, and challenges of modern code review," in *Proc. ICSE*, 2013, pp. 712–721, doi: 10.1109/ICSE.2013.6606617.

[12] S. Torres-Arias et al., "in-toto: Providing farm-to-table guarantees for bits and bytes," in *Proc. USENIX Security*, 2019, pp. 1393–1410.

[13] OpenSSF, "Supply-chain Levels for Software Artifacts (SLSA)," Version 1.0, 2023. [Online]. Available: https://slsa.dev

[14] A. Fan et al., "Large language models for software engineering: Survey and open problems," *arXiv preprint arXiv:2310.03533*, 2023.

[15] Z. Newman, J. S. Meyers, and S. Torres-Arias, "Sigstore: Software signing for everybody," in *Proc. CCS*, 2022, pp. 2353–2367, doi: 10.1145/3548606.3560596.

[16] Y. Fu, "ODD output-driven development - a novel methodology for AI-assisted (v1.0)," Zenodo, 2026, doi: 10.5281/zenodo.18207648. [Online]. Available: https://doi.org/10.5281/zenodo.18207648

[17] Stack Overflow, "Developer Survey 2024," 2024. [Online]. Available: https://survey.stackoverflow.co/2024/

[18] Sonar, "Sonar Data Reveals Critical 'Verification Gap' in AI Coding," Press release, 2026. [Online]. Available: https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/

---

# Appendix A: Supplementary Material

Extended diagrams and detailed comparison tables removed for magazine length are collected in:
- `Paper_01_ODD_Core_English_Submission_Supplement.md`

The detailed technical content—including the 698 artifact classification system, contract templates, mutation testing configurations, sealing record structures, and implementation architecture—is available in the companion whitepaper:

> **Output-Driven Development: Complete Technical Reference**
> Available at: Zenodo DOI 10.5281/zenodo.18207648 (https://doi.org/10.5281/zenodo.18207648) [16]

This supplementary material provides:
- Complete artifact taxonomy with examples
- Contract specification language reference
- Mutation testing configuration guides
- Multi-agent architecture details
- Case studies and worked examples

---

*End of Academic Paper*

---
---
---

