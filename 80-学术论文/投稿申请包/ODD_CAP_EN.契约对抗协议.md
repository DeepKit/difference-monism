# CAP: The Contract Adversarial Protocol — Making AI Specifications Bulletproof

> **Author**: Yi Fu (付毅, ODDFounder, fuyi.it@live.cn)
> **ORCID**: 0009-0008-1251-2632

---

## Abstract

The fundamental challenge in AI-assisted software engineering is not generating code — it is specifying what "correct" means with sufficient precision that incorrect outputs cannot pass verification. Traditional requirements suffer from ambiguity that AI systems exploit unintentionally: a contract saying "implement user search" produces a function that works for exact matches but returns all 100,000 records on empty input. This paper introduces the Contract Adversarial Protocol (CAP), a three-role adversarial framework (Challenger, Attacker, Arbiter) that systematically discovers and closes specification loopholes before code generation begins. CAP transforms contracts from "probably good enough" to "hard to exploit without explicitly violating the contract."

---

## 1. The Specification Gap

When humans write code, they fill specification gaps with common sense. When AI writes code, specification gaps become execution gaps — the AI faithfully implements what was said, not what was meant.

Traditional responses — "write better prompts," "use more examples" — address the symptom (AI produced the wrong thing) rather than the cause (the specification did not define "wrong" with sufficient precision).

CAP addresses the cause: **before code is written, the contract itself is attacked to find where it can be satisfied without being correct.**

---

## 2. The Three-Role Architecture

CAP deploys three distinct roles in adversarial dialogue:

### Challenger
**Goal**: Find ambiguity. "What does 'user search' mean? Search which fields? Exact or fuzzy match? Case-sensitive? What happens on empty input?"

The Challenger does not need to be malicious — ambiguity is not malice, it is underspecification. The Challenger identifies where the contract says things a reasonable person would interpret consistently, but a literal executor would not.

### Attacker
**Goal**: Find exploitable loopholes. Given the clarified contract, construct a minimal implementation that satisfies every acceptance criterion while being useless or harmful.

Example: For a contract specifying "search for 'alice' returns alice" and "search for nonexistent returns empty," the Attacker writes: `if keyword == 'alice' return [alice] else return []`. This passes all tests but is obviously wrong.

The Attacker's output is typically executable code — a concrete demonstration that the contract, as written, permits garbage.

### Arbiter
**Goal**: Adjudicate. Is the Attacker's exploit a genuine gap in the contract (requiring contract revision), or a deliberately absurd interpretation that no reasonable implementation would produce (requiring no revision)?

The Arbiter prevents the adversarial process from degenerating into infinite escalation by distinguishing genuine specification weaknesses from bad-faith readings.

---

## 3. The CAP Cycle

```
Human writes contract draft
    ↓
Challenger identifies ambiguity → Human clarifies
    ↓
Attacker attempts to exploit → Human patches
    ↓
Arbiter adjudicates remaining disputes → Human confirms
    ↓
Contract reaches "bulletproof for current attack surface" status
    ↓ (optional, for high-risk systems)
Repeat with domain-specific attack vectors
```

A contract typically requires 2-4 rounds before reaching adequate defense. The adversarial history (`pk_history`) is preserved as evidence: it documents what attacks were attempted and how the contract was hardened in response.

---

## 4. Five Advanced Attack Dimensions

Beyond basic ambiguity detection, CAP supports five advanced adversarial dimensions:

### 4.1 Code-Level Probing
Attackers must produce executable exploit code, not merely describe risks. This forces specificity: "the contract might be vulnerable to boundary attacks" becomes "here is the exact input that causes the contract to accept an invalid output."

### 4.2 Domain-Specific Black Swan Injection
The Challenger is injected with domain models. For an e-commerce contract, the Challenger asks: "What happens with 100 simultaneous zero-value coupon redemptions? Negative quantity orders? Cross-border tax edge cases?"

### 4.3 Multimodal Adversarial
For UI or visual specifications, the Attacker generates the ugliest-possible-but-technically-compliant mockup. The human's immediate reaction — "that's hideous" — translates into constraints that text-based specification would miss.

### 4.4 Collusion Detection
When Proposer and Attacker are the same model (or same model family), they may inadvertently "go easy" on each other. CAP requires heterogeneous judge pools — at least two independent model families cross-verifying adversarial results.

### 4.5 Attention Budget 2.0
CAP attacks can generate many human-review-required outputs. Attention Budget 2.0 scores attack novelty against historical patterns. Attacks that are >95% similar to past attacks are auto-resolved. Only genuinely novel attack vectors consume human attention budget.

---

## 5. When to Apply CAP

| Scenario | CAP Intensity |
|----------|--------------|
| One-off scripts, personal tools | Self-checklist only |
| Team projects, reusable modules | Clarity assessment + 1 round of adversarial |
| Core business logic, security-critical | Full CAP cycle (3-5 rounds) |
| Safety-critical (medical, aviation, financial) | Mandatory CAP + human final confirmation |

---

## 6. Relationship to the ODD Methodology

CAP is a component of Output-Driven Development (ODD), an artifact-centric engineering methodology for AI-assisted software development. ODD's core loop is Contract → Execute → Verify → Seal. CAP operates at the Contract stage: before execution begins, CAP ensures the contract is sufficiently defended against both honest misinterpretation and malicious exploitation.

CAP inherits its structural foundation from the upstream theoretical chain: DM provides the ontological basis (specification is a structural boundary condition), ASTO provides the structural grammar (what state is the contract in?), ECET provides governance constraints (what are the energy limits on adversarial rounds?), and TAT provides the responsibility framework (who signs the final contract and bears the consequences of residual ambiguity).

---

## 7. Limitations

CAP does not guarantee that a contract is perfect — it guarantees that the contract has survived a specific set of adversarial attacks. If the Attacker fails to discover a genuine loophole, the contract remains vulnerable despite passing CAP. CAP protects against known attack patterns; genuinely novel attack vectors may require CAP protocol updates.

---

## References

- Christian, B. (2020). *The Alignment Problem*. W. W. Norton & Company.
- Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). "Explaining and Harnessing Adversarial Examples." ICLR 2015.
- Miller, G. A. (1956). "The Magical Number Seven, Plus or Minus Two." *Psychological Review*, 63(2), 81-97.
- Perez, E. et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations." arXiv:2212.09251.
