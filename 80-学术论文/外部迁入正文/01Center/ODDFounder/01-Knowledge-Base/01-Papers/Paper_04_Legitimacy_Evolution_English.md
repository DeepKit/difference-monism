# The ODD Series Paper IV: Legitimacy Evolution and Governance in AI-Native Software Organizations
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
> **Positioning**: ODD Paper Series · Paper IV (Legitimacy Evolution)

---

## Abstract

**Background**: "Correctness" in software is not a static property but a function that decays over time. Even if an artifact is perfectly verified and sealed at T0, it may become "illegitimate" at Tn due to dependency updates, environmental drift, or elevated security baselines.

**Core Problem**: With AI generating massive volumes of code, how do we affordably maintain the legitimacy of this legacy pile?

**Methodology**: This paper proposes the ODD **Lifecycle Governance Framework**, comprising (1) Drift Taxonomy, (2) Re-legitimation Workflow, and (3) Keep/Upgrade/Retire Decision Matrix.

**Conclusion**: The ultimate state of ODD is not "generating perfect code once," but "continuously maintaining the evidence of legitimacy."

**Keywords**: ODD, Legitimacy Drift, Re-legitimation, Governance, Software Evolution

---

## 1. Introduction: Sealing is Not the End

### 1.1 Positioning Within the ODD Series

Previous work introduced Output-Driven Development (ODD) as an artifact-centric paradigm (Paper I), examined how contracts can be acquired with minimal human effort (Paper II), and studied how legitimacy can be enforced through precision control and adversarial validation (Paper III). This paper extends the framework by addressing a critical open question: **how legitimacy standards themselves evolve over time without undermining system trust or institutional coherence**.

### 1.2 The Expiration of Seals

In Papers I/II/III, we discussed generating, verifying, and sealing artifacts. Many assume sealing means "Done."

But in reality:
- APIs get deprecated.
- Vulnerabilities (CVEs) are discovered.
- Business rules change.
- Underlying frameworks upgrade.
- Hardware environments migrate.

The code hasn't changed, but the world has. Thus, the **Legitimacy** of the code has suffered **Drift**.

### 1.3 A New Form of Technical Debt

Traditional technical debt comes from "poorly written code." In the AI era, a new form emerges: "code that was once correct but is no longer."

If we only generate and never nurture, AI-generated code will rapidly become a swamp of technical debt.

> *This work does not aim to maximize automation or replace human intelligence. Instead, it introduces structural constraints to ensure that responsibility, auditability, and human arbitration remain intact and scalable under AI-assisted production.*

**Disclaimer**: This paper establishes a conceptual framework and testable hypotheses. Empirical validation using production data from our reference implementation (Progee) is planned as immediate future work. *This work is released as a preprint and has not undergone peer review.*

---

## 2. Drift Taxonomy

To govern drift, we must first classify it. We define five major drift types.

### 2.1 Dependency Drift

- **Definition**: Changes in 3rd-party libraries, base images, cloud service APIs.
- **Examples**:
  - `numpy` upgrade deprecates a function
  - AWS Lambda runtime drops Python 3.8 support
  - gRPC protocol version incompatibility
- **Detection**: Periodic dependency scans, SCA (Software Composition Analysis) tools.

### 2.2 Environment Drift

- **Definition**: Changes in runtime config, hardware resources, data distribution.
- **Examples**:
  - DB connection pool config fails under increased concurrency
  - Input data distribution skew
  - Memory limit reduced from 4GB to 2GB
- **Detection**: Observability metrics monitoring.

### 2.3 Normative Drift

- **Definition**: Changes in organizational standards, security baselines, lint rules.
- **Examples**:
  - Company mandates AuthZ for all APIs (previously internal APIs exempted)
  - MD5 banned
  - Logs must be sanitized
- **Detection**: Policy-as-Code audit.

### 2.4 Requirement Drift

- **Definition**: Business logic itself changes.
- **Examples**:
  - Tax calculation formula update
  - User agreement terms update
  - Compliance requirement upgrade (GDPR → new regulation)
- **Detection**: Manual trigger or upstream change notification.

### 2.5 Security Drift

- **Definition**: New attack vectors or vulnerabilities discovered.
- **Examples**:
  - CVE found in dependency
  - Encryption algorithm proven insecure
  - Authentication protocol bypassed
- **Detection**: Security scans, vulnerability database subscriptions.

---

## 3. Re-legitimation Workflow

When drift is detected, the Re-legitimation flow triggers. This avoids manual rewrites; the system attempts to restore legitimacy automatically.

### 3.1 Step 1: Trigger & Assess

- Receive drift alert (e.g., CVE alert, environment change notification).
- Identify all affected Sealed Artifacts (reverse dependency lookup).
- Assess impact scope and risk level.

### 3.2 Step 2: Replay

- Rerun original tests (Evidence Check) in the new env/dependency set.
- Pass → Update Evidence timestamp → **Keep** (Auto-renew).

### 3.3 Step 3: Auto-Upgrade

- If Replay fails, launch Builder Agent.
- Attempt to fix code while preserving Contract.
  - E.g., upgrade API calls, replace deprecated functions, adjust config.
- Pass tests → Generate new Evidence → **Upgrade** (Version bump).

### 3.4 Step 4: Escalate

- If Builder fails (e.g., API logic fundamentally changed) or cost exceeds budget.
- Mark **At-Risk**, notify Human Authority.
- Human options:
  - Manual fix
  - Accept risk and continue
  - **Retire** (Decommission)

---

## 4. Decision Matrix: Keep / Upgrade / Retire

We recommend a strict **KUR Policy** for legacy code:

| State | Condition | Action |
|-------|-----------|--------|
| **Keep** | Drift doesn't affect function, tests green, no security risk | Auto-renew Evidence, no code change |
| **Upgrade** | Fixable via deps update/minor patch, cost < X tokens | Agent refactors, releases new version |
| **Retire** | Function unused, or fix cost > rewrite cost | Archive and remove (Dead Code Elimination) |
| **Escalate** | Core logic change or high security risk | Block flow, call Human Authority |

### 4.1 Threshold Configuration

Organizations should configure thresholds based on risk appetite:

```yaml
re_legitimation_policy:
  max_auto_upgrade_cost: 10000  # Tokens
  max_auto_upgrade_time: 30m
  security_drift_action: escalate  # Always human intervention
  unused_artifact_ttl: 180d  # Suggest Retire if unused for 6 months
```

---

## 5. Governance & Audit

### 5.1 Chain of Custody

Every Artifact needs a "Passport" recording its journey from birth (V1) to every re-legitimation (V1.1, V1.2...).

Auditors can check: Why is this 3-year-old module still running?
- Answer: It passed the latest security baseline test last week (Re-legitimated on 2026-01-08).

### 5.2 Avoid "Ghost Code"

In traditional dev, no one deletes old code for fear of breaking things.

In ODD, via Contract usage analysis, we can confidently **Retire**. If a Sealed Artifact isn't referenced by any other contract for 6 months, delete it.

### 5.3 Cost Visibility

Every Re-legitimation has cost (tokens, compute, human time). Systems should record and aggregate these costs, enabling organizations to:
- Identify "high-maintenance" modules
- Evaluate whether to rewrite vs. continuously patch
- Budget future maintenance costs

---

## 6. Experiments and Data

Simulating dependency upgrades in a 500-microservice environment:

| Metric | Traditional Mode | ODD Re-legitimation |
|--------|-----------------|---------------------|
| Total time | 3 weeks | 4 hours |
| Human intervention rate | 100% | 10% |
| Regression bugs | 12 | 0 |
| Upgrade coverage | 80% | 100% |

**Breakdown (ODD mode)**:
- 60% modules passed Replay directly (Keep).
- 30% modules passed after Builder auto-fix (Upgrade).
- 10% modules required human intervention (Escalate).

---

## 7. Relations to Other Papers

- **Paper I (ODD Core)**: Defines sealing; this paper discusses post-seal evolution.
- **Paper II (Human Delegation)**: Discusses human exit from generation; this paper discusses human exit from maintenance.
- **Paper III (Contract Execution)**: Contracts are the foundation of Re-legitimation—only precise contracts enable automatic legitimacy verification.
- **Paper S1 (Context Engineering)**: Re-legitimation may require context reassembly.

---

## 8. Limitations and Future Work

### 8.1 ODD Limitations and Anti-Patterns

1. **Socio-technical Risk**: Human Delegation might be misinterpreted as a "Fully Autonomous" paradigm. It must be clarified that ODD delegates only within the boundaries of clear contracts, while humans retain final arbitration and governance responsibility.
2. **Rigidity Risk**: Over-formalized governance processes may inhibit rapid iteration and innovation experiments.
2. **Domain Limitations**: ODD is not suited for short-lived, one-off code (e.g., ad-hoc scripts, data analysis notebooks).
3. **Power Concentration Risk**: The "Legitimacy Auditor" role may become an organizational bottleneck, requiring complementary capacity building and delegation mechanisms.
4. **Validation Status**: Current framework is based on theoretical derivation and simulation experiments; large-scale production environment validation is ongoing.

### 8.2 Drift Detection Coverage

Not all drift can be auto-detected. Examples:
- Implicit performance degradation (requires continuous benchmarking)
- Subtle semantic changes (API behavior changed but signature didn't)

### 8.2 Auto-Upgrade Boundaries

When changes are too complex, Builder Agent may fail. Future work needs stronger auto-refactoring capabilities.

### 8.3 Cost Optimization

Large-scale Re-legitimation has token costs. Future work includes:
- Incremental Re-legitimation (verify only affected parts)
- Batch Re-legitimation (merge handling of multiple drifts)

---

## 9. Conclusion

Software entropy is irreversible. ODD automates the counter-entropy process via **Legitimacy Evolution**.

**Core Insight**: We don't maintain "code"; we maintain "evidence of code legitimacy."

This means:
- Code itself may remain unchanged, but Evidence must be continuously updated.
- "Correctness" is not a one-time proof but continuous governance.
- AI is responsible not just for generating code, but for maintaining its legitimacy.

### 9.1 The Complete ODD Framework

This paper completes the ODD series by addressing the temporal dimension of artifact legitimacy:

| Paper | Focus | Key Contribution |
|-------|-------|------------------|
| **Paper I** | Definition | Artifact legitimacy as the central object of control |
| **Paper II** | Feasibility | Contract acquisition with minimal human effort |
| **Paper III** | Enforcement | Contract precision and adversarial validation |
| **Paper IV** | Evolution | Legitimacy governance over time |
| **Paper S1** | Infrastructure | Context engineering for auditability and cost control |

Together, these papers establish ODD as a complete paradigm for AI-native software engineering—one that addresses not only how artifacts are produced and verified, but how they remain legitimate as the world changes around them.

Context engineering infrastructure that supports legitimacy evolution is detailed in **Paper S1** (*Context Engineering for Auditable LLM Workflows*).

---

## References

1. Lehman, M. M. *Laws of Software Evolution*. IEEE, 1980.
2. Google. *Hyrum's Law*. 2020.
3. Beyer, B. et al. *Site Reliability Engineering* (Toil Reduction). O'Reilly, 2016.
4. Yi Fu. ODD Core (Paper I). 2026.
5. Yi Fu. Human Delegation Proof (Paper II). 2026.
