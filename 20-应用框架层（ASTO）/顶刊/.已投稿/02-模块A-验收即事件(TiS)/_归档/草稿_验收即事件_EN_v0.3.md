# Manuscript draft: Acceptance as an Event (Acceptance as Operation)
**Target journal**: *Journal of Responsible Technology* (Elsevier)
**Language**: English (Academic)
**Status**: Draft v0.3 (EN) — updated 2026-02-01
**Note**: Parallel English draft aligned with `草稿_验收即事件_CN_v0.3.md`.

> Writing constraint: **do not** mention any internal project/system name. Treat this as a standalone governance proposal.

---

## Working title
**Acceptance Is Not a Judgment: Operationalizing Accountability with Auditable Acceptance Events**

## Abstract
Governance failures in AI-assisted and automated systems often stem from a **judgmental fallacy**: treating acceptance as a private mental state (“it seems fine”) rather than a public, auditable operation (“it was accepted under these explicit criteria by this authorized role at this time”). In high-velocity socio-technical systems—where generation is fast, implementations are frequently regenerated, and authorship is diffuse—responsibility cannot reliably be anchored in who wrote or reviewed code.

This paper argues that acceptance should be redefined as an **acceptance event**: a discrete, recordable transaction that institutionally binds (i) an artifact, (ii) a versioned constraint set, and (iii) an evidence bundle digest, to (iv) an authorized sign-off at time *t*. The core novelty is not “approval” itself, but treating acceptance as the **primary responsibility-binding operation** via an explicit artifact–constraint–evidence binding. Building on this definition, we propose **institutional fixation** (“no acceptance without citation”), requiring every acceptance decision to cite a registered constraint set to prevent criteria drift and post-hoc denial.

We illustrate the approach with an AI-generated code vignette and derive practical and policy recommendations for responsible acceptance logging in organizations and regulators.

**Keywords**: Responsible Technology; Governance; Accountability; Acceptance event; Auditability; Traceability

---

## 1. Introduction: why “trust” cannot anchor responsibility
“Trust” is an important social concept, but it is a weak engineering control primitive.
When an AI-assisted system causes harm, questions like “did we trust it?” are not operationally actionable: they do not identify *which criteria were applied*, *who had authority*, *what evidence existed at the time*, or *what exactly was accepted*.

Meanwhile, modern production creates a governance gap:
- systems can generate changes faster than humans can read and review them;
- implementations can be frequently regenerated, making authorship and intent difficult to attribute;
- responsibility diffuses (“everyone touched it, therefore no one owns it”).

**Responsible technology framing.** In responsible technology, the key question is not whether a system is “trusted,” but whether consequences can be traced to an auditable responsibility anchor. The goal is not to make systems more “intelligent,” but to make responsibility operationally locatable under automation (Kroll et al., 2017; Diakopoulos, 2016; Raji et al., 2020).

**De-homogenization statement (avoid “this is just sign-off / release gate”).** The novelty is not adding another approval step. It is re-centering accountability on an auditable acceptance operation: shifting responsibility-binding power away from process derivatives (authorship/review) and compliance narratives, and into an explicit artifact–constraint–evidence binding recorded at acceptance time.

**Boundary, not monopoly.** Acceptance events do not impose single-point blame. They define a responsibility boundary and a decomposable, auditable interface: *a responsibility boundary, not a responsibility monopoly*.

**Thesis.** Treating acceptance as a **responsibility-binding operation** (rather than a psychological judgment) is a necessary condition for accountable governance in high-velocity automated systems.

### Contributions
This paper makes four contributions:
1. **Definition**: acceptance events as a minimal auditable unit binding artifact + constraint set + evidence digest + authorized agent at time *t*.
2. **Mechanism**: institutional fixation (no acceptance without citing a registered constraint set).
3. **Vignette**: AI-generated code acceptance illustrating how responsibility shifts from authorship to sign-off.
4. **Recommendations**: organizational and regulatory guidance for responsible acceptance logging.

---

## 2. From mental approval to an acceptance event
### 2.1 Definition
We define an **acceptance event** as a discrete operation that creates an auditable record:

- **Artifact ($A$)**: the specific object being accepted (e.g., a build, model, rule set, configuration bundle), identified by immutable digests.
- **Constraint set ($C$)**: explicit acceptance criteria and boundaries (tests, scans, invariants, operating constraints), versioned and referenceable.
- **Evidence bundle digest ($\mathcal{E}$)**: a digest/commitment to the evidence bundle referenced at acceptance time (tests, scans, probes, etc.).
- **Authorized agent ($S$)**: the role/entity permitted to accept within an institution’s governance structure.
- **Event record ($E$)**: a time-indexed record binding $A$, $C$, $\mathcal{E}$, and $S$.

A minimal abstraction is:

$$E = \text{Sign}_S(A, C, \mathcal{E}, t)$$

Here, $\mathcal{E}$ is a cryptographic commitment to evidence materials; it binds “the record” to “the evidence” while remaining implementation-agnostic.

**Clarification.** “Sign” denotes an institutional sign-off operation, not a specific cryptographic signature scheme. The core requirement is accountability traceability, not cryptographic non-repudiation.

We use “event” rather than “state” to emphasize time-binding and the sign-off point: if later rollback/replacement is needed, it should be achieved via new events so responsibility remains anchored to concrete decisions at concrete times.

The point of formalization is to make responsibility **queryable**: auditors can ask *which constraint set was cited*, *which artifact version was accepted*, *which evidence digest was referenced*, and *who signed*.

### 2.2 Minimal record schema (implementation-agnostic)
An acceptance event should be technology-agnostic but operationally precise. A minimal record should bind:
- artifact identifier (name + version + digest)
- constraint set identifier (ID + version + digest)
- evidence bundle identifier (digest)
- authorized agent identity (role + identity reference)
- timestamp + decision outcome (accept/reject/exception)

Together, these elements create the explicit **artifact–constraint–evidence binding** and thereby a responsibility anchor.

**Figure 1 (conceptual overview).** Artifact–constraint–evidence binding → acceptance event → responsibility anchor (see `submission/figure1_mermaid.txt`).

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
- Acceptance events are **not** a replacement for ethical deliberation; they make decisions auditable.
- Acceptance events are **not** explainability; they do not require transparency into how an AI produced an output.
- Acceptance events are **not** generic decision logging: decision logs record “a decision happened”; acceptance events record **who accepted what under which constraints with which evidence**, enabling audit queries and replay (Singh et al., 2018).
- Acceptance events are **not** “more paperwork”. They are a governance primitive: without them, responsibility cannot be reliably traced.

### 2.4 Distinguishing acceptance from review and certification
To avoid being read as “DevOps best practice” or “compliance again,” we draw an operational boundary:

| Concept | Focus | Who is responsible / who signs | Does it anchor responsibility? |
|---|---|---|---|
| Code review | implementation quality (reliability/maintainability) | developers / reviewers (Bacchelli & Bird, 2013) | weak: consequences are hard to anchor to a stable record |
| Certification / compliance | conformance to external standards | third parties / compliance function | partial: may not bind to a specific artifact and evidence at time *t* |
| Acceptance event | accepted *under this constraint set* by *this authorized role* at *this time* | authorized acceptance role | yes: creates a queryable responsibility anchor |

---

## 3. Institutional fixation: no acceptance without citation
### 3.0 Term clarification (fixation ≠ rigidity)
In some contexts, “fixation” may suggest belief rigidity or institutional path dependence. Here, **institutional fixation** means a *procedural requirement at acceptance time*: the acceptance event must explicitly bind the **version and digest** of the cited constraint set so criteria cannot silently drift post hoc.

If “fixation” risks misunderstanding, the same idea can be read as an **explicit constraint binding requirement**, or a **constraint referencing requirement**.

Many governance failures are caused not by malice, but by **implicit constraints**: accepting artifacts because they “look reasonable” or “worked last time.” Such criteria are unstable and unauditable.

We propose a rule:

> **Every acceptance event must cite a registered constraint set.**

### 3.1 Registered constraint sets
A constraint set can be lightweight (a checklist + required evidence + risk thresholds), but it must be:
- explicit
- versioned
- referenceable
- stable enough to support audit queries

This paper does not evaluate whether the constraint set is “good enough”; that question belongs to governance/regulation. The point of fixation is not to guarantee correct standards, but to ensure an organization cannot deny *which* standards it actually used after an incident.

### 3.2 Why fixation works
Institutional fixation suppresses three common failure modes:
1. **Post-hoc rationalization**: inventing criteria after an incident.
2. **Responsibility diffusion**: “everyone assumed someone else checked it.”
3. **Criteria drift**: silently changing what “acceptable” means without leaving a trace.

### 3.3 Failure mode example: implicit constraint trap
If a team accepts an AI-generated change because “it looks correct,” there is no constraint object to audit, no evidence digest to query, and no stable sign-off point. When incidents occur, investigations collapse into narrative debates rather than evidence-based accountability.

---

## 4. Vignette: accepting AI-generated code under explicit constraints
This vignette is illustrative.

### 4.1 Scenario
An AI tool generates a code change for a high-impact service (e.g., payments, healthcare triage, identity verification). The change is syntactically correct and passes a subset of tests. A human cannot realistically read every line and understand emergent edge cases.

### 4.2 Traditional approach (review-as-control)
- Responsibility is implicitly attached to authorship and code review.
- With AI-generated code, authorship is diluted and review bandwidth collapses.
- The outcome is unsafe shipping (rubber-stamping) or paralysis.

### 4.3 Acceptance-event approach (sign-off-as-control)
Instead, the organization defines a constraint set, for example:
- required functional tests
- security scan threshold
- invariants (no double-charge, idempotency)
- operational boundaries (timeouts, rollback plan)

A more concrete constraint set for a payments service might include: OWASP Top-10-relevant static analysis with 0 critical findings; mutation testing score ≥ 80%; explicit idempotency-key invariant checks; and a rollback strategy configured and validated via drills/chaos testing.

The pipeline produces an evidence bundle (test reports, scans, probes). An authorized agent signs the acceptance event that binds:
- the exact artifact digest
- the exact constraint set version
- the evidence bundle digest

**Result.** If the system later fails, accountability queries become concrete:
- Which constraint set was used?
- Was it adequate?
- Who signed the exception or acceptance?
- What evidence existed at acceptance time?

This shifts responsibility from “who wrote the code” to “who accepted this artifact under these criteria.” The mechanism does not necessarily reduce error frequency, but it substantially reduces **post-incident governance uncertainty** (criteria drift, narrative disputes, and accountability costs).

### 4.4 Historical analogy (footnote-only)
Similar “acceptance gaps” have appeared in discussions of safety-critical incidents[^hist]. This paper does not revisit factual disputes; we use these as a structural reminder that absent explicit criteria citation and queryable sign-off records, incidents revert to narrative argument.

[^hist]: Commonly discussed examples include Therac-25 and Boeing 737 MAX (MCAS). We do not analyze details here; we only reference the structure “acceptance gap → narrative dispute.”

---

## 5. Practical and policy recommendations
### 5.1 Organizational recommendations (minimum viable implementation)
The proposal is not “re-validate everything for every change.” It is: **whenever an artifact is accepted, an acceptance event must be produced.**

1. **Define authorization roles**: specify who can sign acceptance for each risk class.
2. **Make constraints versioned**: treat acceptance criteria as a first-class, versioned artifact.
3. **Require evidence bundles**: acceptance without evidence is invalid.
4. **Maintain an append-only acceptance log**: treat it as a governance ledger.
5. **Audit by query**: periodically sample accepted artifacts and verify evidence integrity and reproducibility.

### 5.2 Policy recommendations (for regulators and high-impact domains)
Regulators can require minimal acceptance-event logs containing:
- artifact identifiers (digests)
- referenced constraint set IDs and versions
- evidence bundle references
- signer roles and timestamps

To handle cross-border data, trade secrets, and sensitive security information, constraint-set registration/disclosure can adopt **hash commitments**: publish only verifiable digests externally, and disclose full details only under controlled audit conditions.

This approach is compatible with diverse technical stacks because it governs *acceptance operations*, not implementation details.

---

## 6. Discussion and limitations
### 6.1 Technical limitations and implementation risks
- **Evidence integrity**: acceptance logs are only as trustworthy as evidence generation. Evidence should be produced in controlled environments (e.g., trusted CI) to reduce spoofing (Souppaya et al., 2022).
- **Cost and friction**: acceptance events add overhead. The goal is to move overhead from continuous human review to structured evidence + concentrated sign-off.
- **Revocation, rollback, and time windows**: emergency rollbacks may occur between an original acceptance event and a new acceptance/rollback event. The minimum requirement is that rollback/replacement decisions should also be eventized and bound to constraints/evidence, preserving a timeline and clarifying what risk controls and authorization applied during the “gap”. In this sense, the system’s runtime state during the window is itself an **accepted risk configuration**.

### 6.2 Governance limitations and ethical risks
- **Not a full ethics solution**: acceptance events do not resolve value conflicts; they make decisions auditable when conflicts exist.
- **Relation to provenance and attestation**: provenance answers “how it was built”; attestation answers “who made a claim.” Acceptance events answer “who accepted what under which constraints,” adding a responsibility-binding governance layer on top of in-toto/SLSA/Sigstore (Torres-Arias et al., 2019; OpenSSF, 2023; Newman et al., 2022).
- **Exception handling**: if an authorized agent accepts without satisfying the current constraint set, the exception should be eventized: it must cite a higher-level, pre-registered constraint set (e.g., incident response protocol), record justification, include a TTL, and impose remediation obligations (e.g., evidence completion within N hours followed by a standard acceptance event).
- **Responsibility shifting and moral hazard**: moving responsibility anchors from “who wrote” to “who accepted” may enable blame shifting. Acceptance events should not make the acceptor the sole liable party; instead, responsibility should be decomposed into auditable role chains (constraint definition/approval, evidence generation integrity, sign-off, exception approval), and audited to prevent ritualistic verification (Power, 1997; Young, 2011).

---

## 7. Conclusion
The central challenge of responsible technology is not adding more principles, but making responsibility **land in systems**.

This paper does not propose new ethical principles. It provides an operational structure that makes existing responsibility principles executable and auditable: redefining acceptance as an auditable event, and enforcing institutional fixation (no acceptance without citation), so responsibility remains queryable even when production is accelerated by AI and authorship is diffuse.

---

## 8. References (candidates; to be formatted per JRT)
1. Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. In *Proceedings of the 35th International Conference on Software Engineering (ICSE 2013)*, 712–721. DOI: 10.1109/ICSE.2013.6606617.
2. Diakopoulos, N. (2016). Accountability in algorithmic decision making. *Communications of the ACM*, 59(2), 56–62. DOI: 10.1145/2844110.
3. Kroll, J. A., Huey, J., Barocas, S., Felten, E. W., Reidenberg, J. R., Robinson, D. G., & Yu, H. (2017). Accountable algorithms. *University of Pennsylvania Law Review*, 165(3), 633–705.
4. Parasuraman, R., & Riley, V. (1997). Humans and automation: use, misuse, disuse, abuse. *Human Factors*, 39(2), 230–253. DOI: 10.1518/001872097778543886.
5. Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020). Closing the AI accountability gap: defining an end-to-end framework for internal algorithmic auditing. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT* 2020)*. arXiv:2001.00973.
6. Singh, J., Cobbe, J., & Norval, C. (2018). Decision provenance: harnessing data flow for accountable systems. arXiv:1804.05741.
7. Souppaya, M., Scarfone, K., & Dodson, D. (2022). Secure software development framework (SSDF) version 1.1. *NIST Special Publication 800-218*. DOI: 10.6028/NIST.SP.800-218.
8. Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). in-toto: providing farm-to-table guarantees for bits and bytes. In *Proceedings of the 28th USENIX Security Symposium (USENIX Security 19)*, 1393–1410.
9. OpenSSF. (2023). Supply-chain Levels for Software Artifacts (SLSA) v1.0.
10. Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). Sigstore: software signing for everybody. In *Proceedings of the 2022 ACM Conference on Computer and Communications Security (CCS 2022)*.
11. DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: institutional isomorphism and collective rationality in organizational fields. *American Sociological Review*, 48(2), 147–160.
12. Scott, W. R. (2014). *Institutions and Organizations: Ideas, Interests, and Identities* (4th ed.). Sage.
13. Power, M. (1997). *The Audit Society: Rituals of Verification*. Oxford University Press.
14. Young, I. M. (2011). *Responsibility for Justice*. Oxford University Press.
15. Akrich, M. (1992). The de-scription of technical objects. In W. E. Bijker & J. Law (Eds.), *Shaping Technology/Building Society: Studies in Sociotechnical Change* (pp. 205–224). MIT Press.
16. Winner, L. (1980). Do artifacts have politics? *Daedalus*, 109(1), 121–136.

## Notes for the author (next iteration)
1. Add a simple figure: artifact/constraint/evidence → acceptance event → responsibility anchor.
2. Keep terminology consistent: acceptance event; institutional fixation (explicit constraint binding requirement); evidence bundle digest; artifact–constraint–evidence binding.
3. Submission materials templates are in `submission/`.
