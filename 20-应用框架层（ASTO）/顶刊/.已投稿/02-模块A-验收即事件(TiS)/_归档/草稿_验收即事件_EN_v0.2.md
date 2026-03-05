# 论文草稿：验收即事件 (Acceptance as Operation)
**目标期刊**：*Journal of Responsible Technology* (Elsevier)
**语言**：English (Academic)
**状态**：Draft v0.2 (EN snapshot) — updated 2026-01-31
**Note**: This English file is a snapshot. Canonical conceptual baseline: `草稿_验收即事件_CN_v0.4.md`. Up-to-date English draft: `草稿_验收即事件_EN_v0.4.md`.

> Writing constraint: **do not** mention any internal project/system name. Treat this as a standalone governance proposal.

---

## Working title
**Acceptance Is Not a Judgment: Operationalizing Accountability with Auditable Acceptance Events**
*(验收不是判断：用“可审计的验收事件”将责任操作化)*

## Abstract
Governance failures in AI and automated systems often stem from a **judgmental fallacy**: treating acceptance as a private mental state (“it seems fine”) rather than a public, auditable operation (“it was accepted under these explicit criteria by this authorized role at this time”). In high-velocity socio-technical systems—where generation is fast, implementations are frequently regenerated, and authorship is diffuse—responsibility cannot reliably be anchored in who wrote or reviewed code.

This paper argues that acceptance should be redefined as an **acceptance event**: a discrete, recordable transaction that binds (i) an artifact, (ii) an explicit constraint set (acceptance criteria), and (iii) an authorized agent, into a time-indexed record. Building on this definition, we propose **institutional fixation**, a governance mechanism that requires every acceptance decision to cite a registered constraint set (“no acceptance without citation”). We illustrate the approach with an AI-generated code vignette and derive practical and policy recommendations for responsible acceptance logging in organizations and regulators.

**Keywords**: Responsible Technology, Governance, Accountability, Acceptance Event, Auditability, Traceability

---

## 1. Introduction: why “trust” cannot anchor responsibility
“Trust” is an important social concept, but it is a weak engineering control primitive.
When an AI-assisted system causes harm, questions like “did we trust it?” or “were we comfortable with it?” are not operationally actionable: they do not identify *which criteria were applied*, *who had authority*, *what evidence existed at the time*, or *what exactly was accepted*.

Meanwhile, the pace and structure of modern production creates a governance gap:
- AI systems can generate changes faster than humans can read and review them.
- Implementations can be frequently regenerated, making authorship and intent difficult to attribute.
- Responsibility tends to diffuse (“everyone touched it, therefore no one owns it”).

**Core claim.** To make responsibility traceable, acceptance must be treated as an **auditable event** rather than a psychological judgment.

### Contributions
This paper makes four contributions:
1. **Definition**: We define an *acceptance event* as a minimal, auditable unit that binds artifact + constraint set + authorized agent at time *t*.
2. **Mechanism**: We propose **institutional fixation**, requiring acceptance to cite a registered constraint set (no silent/implicit acceptance).
3. **Vignette**: We provide a concrete AI-generated code vignette illustrating how responsibility moves from authorship to sign-off.
4. **Recommendations**: We derive practical and policy recommendations for acceptance logging and auditability in responsible technology.

---

## 2. From mental approval to an acceptance event
### 2.1 Definition
We define an **acceptance event** as a discrete operation that creates an auditable record:

- **Artifact ($A$)**: the specific object being accepted (e.g., a build, model, rule set, deployment bundle), identified by immutable digests.
- **Constraint set ($C$)**: the explicit acceptance criteria and boundaries (tests, safety checks, invariants, operating constraints).
- **Authorized agent ($S$)**: the role/entity permitted to accept within an institution’s governance structure.
- **Event record ($E$)**: a time-indexed record binding $A$, $C$, and $S$.

A minimal abstraction is:

$$E = \text{Sign}_S(A, C, t)$$

This turns “responsibility” from a vague moral notion into a **queryable record**: later auditors can ask *which constraint set was cited*, *what artifact version was accepted*, and *who signed*.

### 2.2 Minimal record schema (implementation-agnostic)
An acceptance event should be technology-agnostic but operationally precise.
A minimal record should bind:
- artifact identifier (name + version + digest)
- constraint set identifier (ID + version + digest)
- evidence bundle identifier (digest; where evidence includes test reports, scans, probes)
- authorized agent identity (role + identity reference)
- timestamp + decision outcome

Example record (illustrative):

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

### 2.3 What acceptance events are (and are not)
- Acceptance events are **not** a replacement for ethical deliberation; they are a mechanism to make decisions *auditable*.
- Acceptance events are **not** the same as explainability; they do not require transparency into how an AI produced an output.
- Acceptance events are **not** “more paperwork”. They are a governance primitive: without them, responsibility cannot be reliably traced.

---

## 3. Institutional fixation: no acceptance without citation
Many governance failures are not caused by malicious intent, but by **implicit constraints**.
People accept artifacts because they “look reasonable,” “match expectations,” or “worked last time”—none of which are stable or auditable criteria.

We propose **institutional fixation**, a governance rule:

> **Every acceptance event must cite a registered constraint set.**

### 3.1 Registered constraint sets
A constraint set is a versioned, institutionally recognized specification of acceptance criteria.
It can be lightweight (a checklist + required evidence), but it must be:
- explicit
- versioned
- referencable (ID)
- stable enough to support audit queries

### 3.2 Why fixation works
Institutional fixation prevents three common failure modes:
1. **Post-hoc rationalization**: inventing criteria after an incident.
2. **Responsibility diffusion**: “everyone thought someone else checked it.”
3. **Criteria drift**: silently changing what “acceptable” means without versioning.

### 3.3 Failure mode example: implicit constraint trap
If a team accepts an AI-generated change because “it looks correct,” then *there is no constraint object to audit*.
When incidents occur, investigations collapse into narrative debates rather than evidence-based accountability.

---

## 4. Vignette: accepting AI-generated code under explicit constraints
This vignette is illustrative.

### 4.1 Scenario
An AI tool generates a code change for a high-impact service (e.g., payments, healthcare triage, identity verification). The change is syntactically correct and passes a subset of tests. A human cannot realistically read every line and understand emergent edge cases.

### 4.2 Traditional approach (review-as-control)
- Responsibility is implicitly attached to authorship and code review.
- With AI-generated code, authorship is diluted and review bandwidth collapses.
- The outcome is either unsafe shipping (rubber-stamping) or paralysis (no shipping).

### 4.3 Acceptance-event approach (sign-off-as-control)
Instead, the organization defines a constraint set, for example:
- required functional tests
- security scan threshold
- invariants (no double-charge, idempotency)
- operational boundaries (timeouts, rollback plan)

The pipeline produces an evidence bundle (test reports, scans, probes). An authorized agent signs the acceptance event that binds:
- the exact artifact digest
- the exact constraint set version
- the evidence bundle digest

**Result.** If the system later fails, accountability queries are concrete:
- Which constraint set was used?
- Was it adequate?
- Who signed the exception or acceptance?
- What evidence existed at acceptance time?

This shifts responsibility from “who wrote the code” to “who accepted this artifact under these criteria.”

---

## 5. Practical and policy recommendations
### 5.1 Organizational recommendations (Monday-morning implementable)
1. **Define authorization roles**: specify who can sign acceptance for each risk class.
2. **Make constraints versioned**: treat acceptance criteria as a first-class, versioned artifact.
3. **Require evidence bundles**: acceptance without evidence is invalid.
4. **Maintain an append-only acceptance log**: treat it as a governance ledger.
5. **Audit by query**: periodically sample accepted artifacts and verify evidence integrity.

### 5.2 Policy recommendations (for regulators and high-impact domains)
For systems with high social impact, regulators can require that organizations maintain acceptance-event logs containing:
- artifact identifiers (digests)
- referenced constraint set IDs and versions
- evidence bundle references
- signer roles and timestamps

This approach is compatible with diverse technical stacks because it governs *acceptance operations*, not implementation details.

---

## 6. Discussion and limitations
1. **Evidence integrity**: acceptance logs are only as trustworthy as evidence generation. Evidence should be produced in controlled environments (e.g., trusted CI) to reduce spoofing.
2. **Cost and friction**: acceptance events add overhead. The goal is to move overhead from continuous human review to structured evidence + concentrated sign-off.
3. **Not a full ethics solution**: acceptance events do not resolve value conflicts; they make decisions auditable when conflicts exist.
4. **Relation to provenance**: supply-chain provenance tells “how it was built”; acceptance events tell “who accepted it under what criteria.” These layers are complementary.

---

## 7. Conclusion
Responsible technology requires more than principles; it requires **operational accountability**.
By redefining acceptance as an auditable event and enforcing institutional fixation (no acceptance without citation), organizations can make responsibility traceable even when production is accelerated by AI and authorship is diffuse.

---

## Notes for the author (next iteration)
1. Pick **one** primary real-world incident as an optional parallel (keep it high-level, avoid factual over-claims).
2. Decide whether to keep the medical vignette as a second vignette or remove it to stay focused.
3. Add ~8–12 references (governance/accountability, audits, software supply-chain attestation, code review limits).
