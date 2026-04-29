# The ODD Series Paper II: Human Delegation Proof via Progressive Trust and Adversarial Validation
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
> **Date**: 2026-01-15
> **Version**: Draft v0.5 (Expanded)
> **Positioning**: ODD Paper Series · Paper II (Human Delegation Proof)

---

## Abstract

**Background**: As AI code generation speed surpasses human cognitive bandwidth, traditional "Code Review" has become the primary bottleneck in software engineering. Relying on human review as the final defense line inevitably leads to rubber-stamping or delivery blockages.

**Thesis**: This paper proposes **Human Delegation Proof**, arguing that under the Output-Driven Development (ODD) paradigm, humans can completely exit the high-frequency loop of "writing and reviewing code," shifting roles to rule-making and exception arbitration.

**Methodology**: We construct a **Progressive Trust Model** enabling "zero-trust" verification of AI artifacts via (1) Automated Contract Generation, (2) Structured Adversarial Validation, and (3) Evidence Sealing.

**Conclusion**: Human Delegation is not about eliminating humans, but upgrading human intelligence from "spell-checking" to "legislation and governance."

**Keywords**: ODD, Human Delegation, Code Review, Progressive Trust, Adversarial Validation, Governance

---

## 1. Introduction: The Death of Code Review

### 1.1 Moore's Law Hits Software Production

With improvements in LLM context windows and reasoning capabilities, the marginal cost of software production approaches zero. An Agent can generate a complete microservice module (including tests, docs, config) in minutes. This explosive growth in productivity invalidates many assumptions of traditional software engineering.

### 1.2 The Collapse of Human Review Bandwidth

Human code reading speed (approx. 200-500 lines/hour) is linear and fatigue-prone. When AI output speed is 100x human reading speed, only two outcomes are possible:

1. **Review Collapse**: Humans click 'Approve' after reading only the title. This "rubber stamp" review not only fails to ensure quality but gives the team a false sense of security.
2. **Delivery Blockage**: Code piles up in PR queues, creating massive inventory waste. Time waiting for review may exceed time spent coding.

### 1.3 The ODD Solution

ODD posits: **The process is untrusted, the result is verifiable.** We don't care who wrote the code (human or AI) or what it looks like; we only care if it satisfies the **Contract** and survives **Adversarial Validation**.

The core shift is: from "trusting the author" to "trusting the evidence."

### 1.4 Positioning Within the ODD Series

Building upon the definition of artifact legitimacy introduced in Output-Driven Development (Paper I), this paper focuses on how contracts can be acquired and finalized with minimal human effort via clarity assessment and structured context injection, enabling non-experts to participate without writing formal specifications.

> *This work does not aim to maximize automation or replace human intelligence. Instead, it introduces structural constraints to ensure that responsibility, auditability, and human arbitration remain intact and scalable under AI-assisted production.*

**Disclaimer**: This paper establishes a conceptual framework and testable hypotheses. Empirical validation using production data from our reference implementation (Progee) is planned as immediate future work. *This work is released as a preprint and has not undergone peer review.*

---

## 2. Progressive Trust Model

Trust is not a binary switch but a ladder. We define four trust stages; organizations can choose their starting point based on maturity and progress incrementally.

### 2.1 S0: Bootstrapping

- **Characteristics**: No historical data, imperfect contracts, team unfamiliar with ODD workflows.
- **Human Involvement**: 100%. Humans write core contracts and confirm every artifact.
- **Verification**: Basic compilation, unit testing.
- **Typical Scenario**: New project kickoff, new team adopting ODD.
- **Exit Criteria**: 50+ sealed artifacts accumulated, contract templates covering major artifact types.

### 2.2 S1: Assisted

- **Characteristics**: Sparse historical samples, templated contracts, team begins trusting system verification.
- **Human Involvement**: 50%. Humans no longer write code, only review contracts (Review Contract, not Code).
- **Verification**: Mutation Testing introduced to ensure test suite validity.
- **Typical Scenario**: Iterative development on mature modules.
- **Exit Criteria**: Mutation coverage > 80%, all contracts at Green clarity.

### 2.3 S2: Automated

- **Characteristics**: High contract precision (Green), abundant historical evidence, mature adversarial validation.
- **Human Involvement**: 10% (Sampling). System automatically generates, tests, and seals.
- **Verification**: Adversarial Validation (Builder vs Breaker), multi-role competition.
- **Typical Scenario**: Routine iterations on stable business logic.
- **Exit Criteria**: 100 consecutive auto-seals without rollback.

### 2.4 S3: Exception-only

- **Characteristics**: System full autonomy, humans handle edge cases only.
- **Human Involvement**: <1%. Only intervene on alarms, metric drifts, or major architectural changes.
- **Verification**: Continuous monitoring, Re-legitimation.
- **Typical Scenario**: Highly mature platform systems.

---

## 3. Mechanism I: Automated Contract Generation

### 3.1 Learning from History

Writing contracts has a cost. Human Delegation requires automating contract generation. Utilizing the structure defined in **Paper III**, we retrieve similar tasks from the Sealed Artifacts library:

- **I/O Constraints**: Reuse schemas from similar interfaces.
- **Boundaries**: Reuse edge cases extracted from historical incidents.
- **Performance**: Reuse baselines from similar modules.

### 3.2 Adversarial Contract Refinement

Before Builder Agent generates code, Spec Agent drafts an initial contract. Breaker Agent attacks this contract (e.g., pointing out ambiguities). After 2-3 rounds of Agent negotiation, a "bulletproof" contract is formed, then confirmed by humans (in S0/S1 stages).

### 3.3 Contract Template Library

We recommend maintaining an organization-level contract template library, categorized by artifact type:
- HTTP API contract template
- Data pipeline contract template
- CLI tool contract template
- Configuration change contract template

Each template contains required fields, recommended fields, and common negative case checklists.

---

## 4. Mechanism II: Structured Distrust (Adversarial Validation)

The essence of human review is "finding faults." In ODD, we agentify this role.

### 4.1 Roles

- **Builder**: Make it work. Its goal is to generate implementations that satisfy the contract.
- **Breaker**: Make it fail. It attacks artifacts via Fuzzing, distribution shifts, fault injection.
- **Auditor**: Check the trace. Ensures all steps are logged and Evidence is complete.

### 4.2 Verification Flow

1. Builder submits code + tests.
2. System runs tests -> Pass.
3. Breaker launches attacks (e.g., mutated inputs, boundary probing).
4. If code crashes or behaves abnormally -> Reject, require Builder fix.
5. If code is robust -> Mutate the code itself (Mutation Testing).
6. If tests do not fail -> Test coverage insufficient -> Reject, require Builder to add tests.
7. All pass -> Generate Evidence.

### 4.3 Adversarial Intensity Levels

Different risk levels warrant different adversarial intensity:

| Risk Level | Adversarial Methods | Time Budget |
|------------|---------------------|-------------|
| Low | Basic mutation testing | < 1 min |
| Medium | Mutation + Fuzzing | < 10 min |
| High | Full adversarial + human sampling | < 1 hour |
| Critical | Full adversarial + mandatory human approval | Unlimited |

---

## 5. Mechanism III: Evidence Sealing

### 5.1 What is Evidence?

Evidence is a cryptographically signed package containing:

- Source snapshot hash
- Contract text and version
- Test execution reports (timestamps, environment fingerprints)
- Mutation score
- Adversarial validation logs
- Dependency manifest with version locks

### 5.2 Sealing

Seal = Artifact + Evidence + Signature.

Sealing means: **Because of this evidence, we choose to trust this version and accept the risk.**

In a production incident, the audit asks "Where did the Evidence fail?"—was the contract missing a boundary, or was adversarial intensity too low? This attribution approach clarifies improvement directions.

### 5.3 Evidence Lifecycle

Evidence is not permanently valid. As dependencies upgrade and environments change, original Evidence may no longer prove artifact legitimacy. This leads to the "re-legitimation" topic discussed in Paper IV.

---

## 6. Governance

### 6.1 Who is Responsible?

After human exit, liability shifts:

- **Micro-liability** (NPE in line 50): System bears it (rollback, fix, log).
- **Macro-liability** (Frequent incidents): **Rule-makers (Humans)** bear it. It implies humans set Gates too low or approved unsafe downgrades.

### 6.2 Policy as Code

Governance rules must be code:

```
allow_automerge if:
  mutation_score > 95% AND
  coverage > 98% AND
  critical_path_touched == false AND
  security_scan == pass
```

This makes governance itself versioned, rollbackable, and auditable.

### 6.3 Exception Management

In some cases, bypassing automated flows is necessary (e.g., emergency fixes). ODD does not prohibit exceptions but requires:
- Exceptions must be explicitly declared
- Exceptions must have human signatures
- Exceptions must have time limits (e.g., Evidence must be completed within 24 hours)

---

## 7. Case Study

### Scenario: Payment Gateway Integration

- **S0 Stage**: Engineer writes contract & tests manually. AI implements. Human reviews every line. Duration: 2 weeks.
- **S1 Stage**: Human reviews only contract (idempotency, timeouts). AI generates implementation & tests. System runs mutation tests. Duration: 3 days.
- **S2 Stage**: System retrieves historical payment module contracts. Spec Agent drafts contract. Breaker Agent injects "network jitter" and "duplicate callback" scenarios. Builder Agent fixes until pass. Auto-sealed. Duration: 4 hours.

**Result**: S2 reduced delivery time by 90% vs S0, and edge case coverage improved by 40% due to Breaker.

---

## 8. Relations to Other Papers

- **Paper I (ODD Core)**: Defines artifact-centric, contract, mutation-testing trust, and sealing—the theoretical foundation of this paper.
- **Paper III (Contract Execution)**: Deep-dives into contract precision, detailing the "contract generation" mechanism.
- **Paper IV (Legitimacy Evolution)**: Discusses post-seal legitimacy evolution, continuing the "Evidence lifecycle" topic.
- **Paper S1 (Context Engineering)**: Discusses how to assemble context for Agents, the infrastructure for "automated contract generation."

---

## 9. Limitations and Future Work

### 9.1 Open-World Problems

For completely open-ended tasks without enumerable acceptance criteria (e.g., "write an interesting blog post"), Human Delegation has limited applicability. Such tasks may require humans in the loop.

### 9.2 Adversarial Validation Cost

Breaker Agent and mutation testing have computational costs. For high-frequency, low-risk tasks, trade-offs between verification depth and speed are needed.

### 9.3 Organizational Culture Fit

Human Delegation requires cultural alignment. If teams distrust automation, they may stall at S1/S2 stages.

---

## 10. Conclusion

Human Delegation Proof demonstrates that under ODD, **code can be trusted without human eyes on it**. This liberates human cognitive bandwidth for higher-dimensional system design and value definition.

The core insight is: **Trust comes not from "who wrote it" but from "how strong the evidence is."**

### 10.1 Subsequent Work

While the mechanisms described here make ODD feasible by reducing the human burden of contract authoring and code review, they do not quantify how contract precision interventions and adversarial enforcement affect defect escape rates. This enforcement question is the subject of **Paper III** (*Contract Precision as a Control Variable for AI Code Generation Quality*).

The evolution of legitimacy standards over time—how sealed artifacts remain valid as contexts change—is addressed in **Paper IV** (*Legitimacy Evolution and Governance*).

Context engineering infrastructure that supports the mechanisms in this paper is detailed in **Paper S1** (*Context Engineering for Auditable LLM Workflows*).

---

## References

1. Yi Fu. ODD Core (Paper I). 2026.
2. Google. *Software Engineering at Google* (Test Flakiness & Code Review). O'Reilly, 2020.
3. OpenAI. *GPT-4 Technical Report*. 2023.
4. Zeller, A. et al. *The Fuzzing Book*. 2019.
5. Meyer, B. *Design by Contract*. IEEE Computer, 1992.
6. Jia, Y. & Harman, M. *An Analysis and Survey of the Development of Mutation Testing*. IEEE TSE, 2011.

---

## Appendix: Disclaimer and Risks

### Limitations and Anti-Patterns

1. **Socio-technical Risk**: Human Delegation might be misinterpreted as a "Fully Autonomous" paradigm. It must be clarified that ODD delegates only within the boundaries of clear contracts, while humans retain final arbitration and governance responsibility.
2. **Rigidity Risk**: Over-reliance on automated verification may inhibit "untestable" innovations.
3. **Knowledge Decay**: Prolonged detachment from code implementation may degrade human engineers' intuition for the underlying system.

---

*End of Document*
