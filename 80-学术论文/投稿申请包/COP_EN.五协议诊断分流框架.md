# A Five-Protocol Diagnostic Triage Framework for Complex Real-World Decisions

> **Author**: Yi Fu (付毅, ODDFounder, fuyi.it@live.cn)
> **ORCID**: 0009-0008-1251-2632

---

## Abstract

When AI systems are deployed in high-stakes domains — healthcare, autonomous driving, organizational governance — they face a problem that pure accuracy metrics cannot capture: knowing when NOT to decide. This paper introduces the Cognitive Operations Protocol (COP), a five-protocol diagnostic pipeline that transforms raw real-world signals into triage states (RESOLVE, MIXED, FREEZE, UNKNOWN, REFER) with explicit confidence levels. The key innovation is the FREEZE state: treating "not deciding" as a legitimate, structured output rather than a system failure. The paper presents the pipeline architecture (Input Sampling → State Encoding → Diagnostic Judgment → Referral & Limited Intervention → Feedback Calibration) and demonstrates it with an end-to-end walkthrough example.

---

## 1. The Problem: When Should an AI System Say "I Don't Know"?

Most AI evaluation focuses on accuracy — how often the system is right. But in high-impact domains, the more dangerous error is not being wrong but being confidently wrong in situations where the system should have recognized its own ignorance.

In medical diagnosis, a system that says "I'm 92% confident this is Condition X" is useful. A system that says "I'm 92% confident" when it has never seen a case like this before is dangerous. The difference is not accuracy — it is **knowing the boundary of one's knowledge**.

COP addresses this by making "I don't know" a first-class output of the system, with structured escalation paths.

---

## 2. The Five-Protocol Pipeline

COP is not a classifier. It is a diagnostic pipeline in which each protocol transforms the previous protocol's output into a more computationally tractable form.

### Protocol 1: Input Sampling (P1)

Raw real-world signals — natural language descriptions, questionnaire responses, behavioral logs, indicator panels — are transformed into structured sampling frames. The key discipline: **no judgment at this stage**. Sampling only collects; it does not interpret.

Every sampling frame must declare its bias: what signals is this frame most likely missing?

### Protocol 2: State Encoding (P2)

Sampling frames are mapped into COP's encoding space. Before COP's core encoding begins, the protocol inherits structural precoding from ASTO (Attribute-Set Transition Ontology): state type, stage, sequence position, boundary status, and exception flags.

Core encoding produces two separate vectors:
- **Clarity vector**: signal completeness, signal consistency, category concentration
- **Structural risk vector**: responsibility diffusion, power asymmetry, irreversibility potential

These two vectors are deliberately NOT combined into a single score — a situation can be "clear but dangerous" or "confusing but low-risk," and conflating them is the root cause of many AI safety failures.

### Protocol 3: Diagnostic Judgment (P3)

Based on the encoded vectors, the system outputs one of five triage states:

| State | Meaning | Default Action |
|-------|---------|---------------|
| RESOLVE | Clear, consistent, low structural risk | Proceed with automated processing |
| MIXED | Contradictory signals or unclear categorization | Limited proceed with flagged areas |
| FREEZE | High structural risk or red-line violation | Stop automation, escalate to human review |
| UNKNOWN | Insufficient signal completeness | Request supplementary information |
| REFER | Beyond COP's scope | Route to TAT, ODD, or human review |

The judgment matrix prioritizes safety: edge cases default to FREEZE. Low-confidence outputs (below 0.6) never receive RESOLVE.

### Protocol 4: Referral and Limited Intervention (P4)

Based on the triage state, P4 generates next-step actions and referral routing. COP can recommend; COP cannot execute. The hard boundary: COP may suggest FREEZE and route to TAT for responsibility adjudication, but COP may not itself authorize high-risk mandatory actions, issue final behavioral lockdowns, or define consent/appeal/compensation structures.

### Protocol 5: Feedback Learning Calibration (P5)

Diagnostic outcomes are compared against real-world results. Three misclassification types are tracked:
- **False Safe**: judged as RESOLVE/MIXED but should have been FREEZE
- **Over Freeze**: judged as FREEZE but human review found it should have proceeded
- **Wrong Type**: correct triage direction but incorrect classification label

Calibration is parameter-level, not axiom-level. FREEZE as a structural safety mechanism cannot be "optimized away" by any learning result.

---

## 3. Relationship to Upstream Theory

COP inherits structural encoding from ASTO (five states, six stages, boundary status) and provides diagnostic triage that feeds into TAT (responsibility thresholds), ODD (engineering gates), and RT6 (engagement methodology). COP does not rewrite upstream theory; it compresses structural diagnosis into computationally tractable triage states.

---

## 4. Limitations

The five protocols are a conceptual framework. Calibration parameters and judgment thresholds are domain-specific and require empirical tuning. The single walkthrough example is illustrative, not systematic validation.

---

## References

- Amodei, D. et al. (2016). "Concrete Problems in AI Safety." arXiv:1606.06565.
- Hendrycks, D. et al. (2021). "Unsolved Problems in ML Safety." arXiv:2109.13916.
- Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*. Little, Brown Spark.
