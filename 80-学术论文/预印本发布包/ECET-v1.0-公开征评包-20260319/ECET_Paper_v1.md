# Evolutionary Constraint Existential Theory (ECET): A Cross-Domain Governance Framework for Accountability in Complex and AI-Driven Systems

**Author**: Yi Fu (付毅)
**Affiliation**: ODDFounder
**Contact**: fuyi.it@live.cn
**Date**: March 2026
**Version**: 1.0 Public Review Preprint
**License**: CC BY 4.0

---

> **Public note**: This manuscript is part of the ECET `v1.0 public review package`.
> It is suitable for preprint-style release and public review, but should not be described as a peer-reviewed final theory or as having completed large-scale empirical validation.

## Abstract

Contemporary governance frameworks face a structural problem: decision-making authority increasingly operates faster and at greater scale than accountability structures can track. This paper introduces Evolutionary Constraint Existential Theory (ECET), a cross-domain governance framework derived from three irreducible physical constraints — the energy constraint, the adaptive selection constraint, and the incompleteness constraint. From these axioms, ECET derives three governance principles (responsibility symmetry, anti-finalization, and AI attribution) and three operational boundary conditions (responsibility tracing boundary, audit adjudication closure, and scale-triggered hierarchical accountability). Unlike existing frameworks that identify accountability gaps without providing operationalizable solutions, ECET provides a unified conceptual language accessible to engineers, lawyers, policymakers, and organizational theorists. The framework is applied to AI agent safety architecture, demonstrating that output verification is structurally superior to process inspection as an alignment strategy. Ten testable hypotheses are derived, providing a scientific interface for empirical validation. ECET's contribution is not the discovery of new problems but an attempt to systematically, structurally, and operationally integrate existing insights into a cross-domain governance framework.

**Keywords**: accountability gap, shadow sovereignty, AI governance, responsibility symmetry, evolutionary constraints, output verification, cross-domain framework

---

## 1. Introduction

### 1.1 The Core Problem

A structural pattern recurs across modern complex systems: decision-making authority expands faster than accountability structures can track. We call this pattern **shadow sovereignty** — structures where decision authority exists, but the subject bearing consequences is diffuse or absent.

Shadow sovereignty is not a new phenomenon. The East India Company exercised sovereign-level decision authority over millions while responsibility remained legally ambiguous in London. Weberian bureaucratic chains systematically diluted accountability through delegation. Financial derivative structures in the 2000s separated risk-taking from risk-bearing so thoroughly that the 2008 collapse imposed costs on parties who had never authorized the decisions that caused it.

AI systems represent the latest and most extreme instantiation of this pattern, characterized by three amplifying factors:
- **Speed asymmetry**: decisions occur at millisecond timescales while accountability operates at year timescales
- **Scale**: a single model deployment affects millions of users simultaneously
- **Opacity**: the decision process is not interpretable, making causal attribution structurally difficult

### 1.2 Why Existing Frameworks Are Insufficient

The accountability gap has been identified by multiple research traditions. Subsidiarity principles in Catholic social philosophy and EU governance identify the problem of mismatched decision levels. Academic accountability gap research documents the phenomenon empirically. The EU AI Act and national AI regulations establish compliance requirements. Over 84 AI ethics declarations have been published since 2016.

These frameworks share a common limitation: they identify the problem without providing an operationalizable, cross-domain solution. The fragmentation is itself part of the problem:

- Engineers describe "alignment problems"
- Lawyers describe "agency liability"
- Politicians describe "accountability deficits"
- Philosophers describe "crises of subjectivity"

These are descriptions of the same structural phenomenon in domain-specific languages that cannot communicate with each other. Without a common language, principles cannot be operationalized.

### 1.3 ECET's Contribution

Evolutionary Constraint Existential Theory (ECET) does not claim to have discovered new problems. Its contribution is to offer a systematic, structural, and operational integration of existing insights into a cross-domain governance framework with the following properties:

1. **Derived from physical constraints**: governance principles follow from irreducible physical facts, not ethical preferences
2. **Operationalizable**: three boundary conditions translate principles into executable institutional and engineering requirements
3. **Cross-domain**: a common conceptual language accessible to engineers, lawyers, policymakers, and organizational theorists
4. **Falsifiable**: ten testable hypotheses provide a scientific interface for empirical validation

### 1.4 Paper Structure

Section 2 presents the three axioms and their derivation. Section 3 derives three governance principles from the axioms. Section 4 specifies three operational boundary conditions. Section 5 applies the framework to AI agent safety architecture. Section 6 presents ten testable hypotheses. Section 7 situates ECET within existing literature. Section 8 discusses limitations and future directions.

---

## 2. Three Axioms

ECET begins from a foundational question: what constraints are irreducible and jointly sufficient to characterize the evolutionary dynamics of any system — physical, cognitive, or social?

The answer is three constraints. Their necessity and sufficiency are argued as follows.

**Necessity**: each constraint is independently irreducible.
- Without the energy constraint, systems could operate on unlimited resources — this does not exist physically
- Without the adaptive selection constraint, systems need not adapt to their environment — this does not exist evolutionarily
- Without the incompleteness constraint, systems could completely describe their environment — this does not exist logically (Gödel, Turing)

**Sufficiency**: other candidate constraints reduce to these three.
- Time constraints → temporal dimension of the energy constraint
- Spatial constraints → spatial dimension of the energy constraint
- Information constraints → information-theoretic expression of the incompleteness constraint
- Social constraints → social-level expression of the adaptive selection constraint

This is not a complete proof. It is a defensible minimal completeness argument. If a researcher can demonstrate a fourth irreducible foundational constraint, the ECET framework should be revised accordingly.

### 2.1 Axiom 1: The Energy Constraint

**Statement**: Any system must operate within the upper limit of available resources. Exceeding this limit causes system collapse.

**Philosophical foundation**: The first and second laws of thermodynamics. No physical system can create resources from nothing, nor maintain a low-entropy state indefinitely.

**Operational definition**: The energy constraint is directly measurable across system types:

| System Type | Measurable Indicators |
|-------------|----------------------|
| AI Agent | Compute budget, token limit, API call frequency, context window length |
| Biological system | Metabolic rate, ATP availability |
| Organizational system | Budget, personnel, time window |
| Social system | Fiscal revenue, natural resources, population scale |

**Governance derivation**: Decisions are not free. Every decision consumes resources and produces consequences. Critically, decisions do not merely consume resources — they irreversibly alter the state of the environment. Even "revocable" mechanisms only revoke future permissions; they cannot undo consequences that have already occurred. This strengthens the urgency of the **AI attribution principle**: AI decisions consume compute and produce consequences — both are physical facts. Physical facts require physical bearers. When the bearer disappears, the decision authority loses its legitimacy basis.

### 2.2 Axiom 2: The Adaptive Selection Constraint

**Statement**: Any system's behavior must produce positive adaptation in its environment, or be eliminated. Non-adaptive structures do not persist indefinitely.

**Philosophical foundation**: Darwinian natural selection. Adaptiveness is not a goal but a condition of persistence. Non-adaptive features are eliminated by environmental filtering mechanisms — without any subjective intent, this is a structural necessity.

**Operational definition**: The adaptive selection constraint requires the existence of a filtering mechanism independent of the behaving agent:

| System Type | Filtering Mechanism | Judgment Method |
|-------------|--------------------|-----------------| 
| AI Agent | ODD gate (PASS/FAIL/FREEZE three-value judgment) | Whether output passes independent validator's contract check |
| Biological system | Natural selection (survival/reproductive success) | Population frequency change |
| Organizational system | Market competition, institutional audit | Organizational survival/elimination |
| Social system | Institutional evolution, revolution, reform | Institutional survival/replacement |

**Critical criterion**: If a system's outputs take effect without passing through any filtering mechanism independent of the generation source, that system violates the adaptive selection constraint. The key phrase is "independent of the generation source" — self-generation and self-verification does not constitute filtering.

**Governance derivation**: Responsibility-misaligned structures are unstable and will eventually be eliminated. This directly derives the **responsibility symmetry principle**: binding decision authority to consequence-bearing is not a moral requirement but a condition of structural persistence. Responsibility-misaligned systems collapse under evolutionary pressure — not because they are "immoral" but because they are "unstable."

### 2.3 Axiom 3: The Incompleteness Constraint

**Statement**: No cognitive system can completely describe its environment. Incompleteness is not a defect but a condition of cognitive existence.

**Philosophical foundation**: Gödel's incompleteness theorems (any sufficiently strong formal system contains true propositions that cannot be proven within the system) and Turing's halting problem (no algorithm can determine whether all programs halt). These results jointly establish that completeness is logically unachievable.

**Operational definition**: The incompleteness constraint is measurable through a system's uncertainty-handling capacity:

| System Type | Measurable Indicators |
|-------------|----------------------|
| AI Agent | FREEZE trigger rate (frequency of "I don't know" responses), hallucination rate (should-have-frozen but didn't) |
| Biological system | Hesitation behavior frequency, exploration/exploitation ratio |
| Organizational system | Decision delay rate, "need more information" request frequency |
| Social system | Institutional revision frequency, policy pilot proportion |

**Critical criterion**: If a system provides deterministic answers to all inputs and never expresses uncertainty, that system is not correctly handling the incompleteness constraint. A healthy system must have a non-zero FREEZE rate. A FREEZE rate of zero means the system is pretending to be complete — this is more dangerous than acknowledging incompleteness.

**Governance derivation**: No institutional design can anticipate all future situations. This directly derives the **anti-finalization principle**: structures claiming "permanent validity" violate the basic logic of incompleteness. Incompleteness is not a defect of institutions but a condition of their existence.

### 2.4 Derivation Structure

```
Energy Constraint        Adaptive Selection        Incompleteness
(Resources finite)       (Non-adaptive eliminated) (Cognition incomplete)
        │                         │                        │
        │                         ├────────────────────────┤
        │                         ↓                        ↓
        └──────────→    Responsibility Symmetry    Anti-Finalization
                        (Decision authority to     (No permanently
                        consequence-bearers)        valid structure)
                                  │
                                  ↓
                           AI Attribution
                        (AI decision authority
                         requires human org bearer)
```

The three governance principles are not independent moral claims. They are structural conclusions derived from the three axioms.

### 2.5 Epistemic Status of the Axioms

ECET's three axioms are a **generative framework**, not a falsifiable scientific theory.

| Knowledge Type | Definition | Examples | ECET's Position |
|----------------|------------|----------|-----------------|
| Scientific theory | Falsifiable specific explanation | Relativity, natural selection | Derived hypothesis layer (Section 6) |
| Formal system | Strict derivation from axioms | Euclidean geometry | Partial |
| Generative framework | Provides conceptual tools, generates falsifiable derived theories | Darwinism, thermodynamics | **ECET itself** |

The axioms themselves are not directly falsifiable — this is the same epistemic status as Darwinism and the second law of thermodynamics. Falsifiability exists at the derived theory layer (Section 6, H1–H10).

**The three axioms do not share the same ontological status.** This requires honest acknowledgment:

- **Energy constraint**: Closest to physical necessity. All known physical systems are subject to energy conservation — the most universal physical law known. The extension from physical systems to cognitive and social systems is an analogy from concrete to abstract, but rests on the most solid foundation.
- **Adaptive selection constraint**: Stronger empirical character. Darwinian natural selection has robust empirical support in biological systems, but when extended to organizational and AI systems, the mechanism of "selection" shifts from blind environmental filtering to purposive design selection — this asymmetry must be acknowledged. In AI systems, the more accurate analogy is "contract enforcement" rather than "natural selection": ODD gate criteria are rules embedded by designers, not blind environmental pressure. The validity of the adaptive selection constraint in AI governance depends on the empirical claim that "responsibility-misaligned structures are genuinely unstable over sufficiently long time horizons" — not on logical necessity.
- **Incompleteness constraint**: Strongest analogical character. Gödel's incompleteness theorems strictly apply to formal systems — artificial systems with finite axiom sets and explicit inference rules. Extending this to "any cognitive system" involves a categorical leap: cognitive systems (human brains or AI models) are not formal systems. A more robust formulation is that the incompleteness constraint is an **empirical structural feature** of cognitive systems — humans and AI genuinely cannot possess complete information about the world. Gödel's theorems and Turing's halting problem provide the strongest available analogical support, but do not constitute a logical proof.

This difference in ontological status does not undermine the governance derivations from the three axioms, but requires readers to understand that the three axioms differ in argumentative strength, and the corresponding governance conclusions differ in certainty.

**Core-periphery structure of governance principles**: The three governance principles are not equally central to the theory. Responsibility symmetry is the core of the core — derived directly from the adaptive selection constraint; if falsified, the entire framework requires fundamental reconstruction. Anti-finalization is core — if falsified, governance conclusions require major revision. AI attribution is a peripheral corollary — it depends on the current premise that "AI cannot independently bear consequences"; if this premise changes, the specific form of the principle adjusts accordingly, without affecting the framework's core structure.

---

## 3. Three Governance Principles

### 3.1 Principle 1: Responsibility Symmetry

**Source**: Adaptive selection constraint

**Statement**: All decision authority must be held by the subject bearing consequences.

This is the minimum condition for structural stability, not a moral requirement. Responsibility-misaligned structures are unstable under evolutionary pressure and will be eliminated — not because they are wrong but because they are structurally fragile.

**For distributed consequences**: When consequences are distributed, decision authority must also be distributed and authorized, with each authorization layer being:
- Traceable (who authorized this decision?)
- Revocable (authorization can be withdrawn)
- Attributable (each layer has a clear responsible subject)

### 3.2 Principle 2: Anti-Finalization

**Source**: Incompleteness constraint

**Statement**: No irreplaceable final legitimate structure exists.

No institutional design can anticipate all future situations. Structures claiming "permanent validity" violate the basic logic of incompleteness. All governance structures must remain: questionable, revisable, replaceable.

This principle is not a claim that all structures are equally valid or that stability is undesirable. It is a claim that structures which cannot be revised will eventually fail to adapt to environmental change and be replaced — often catastrophically rather than gracefully.

### 3.3 Principle 3: AI Attribution

**Source**: Energy constraint + adaptive selection constraint

**Statement**: AI decision capacity is fundamentally an authorization granted by some human organization.

Decisions consume resources and produce consequences — both are physical facts. Physical facts require physical bearers.

- AI behavioral responsibility must be attributed to the authorizing subject
- If the authorizing organization disappears, there must be a succession structure
- If no one bears responsibility, that decision authority is in an illegitimate state

---

## 4. Three Operational Boundary Conditions

Principles are insufficient. ECET specifies three operational boundary conditions that make principles executable.

### 4.1 Responsibility Tracing Boundary (Subject Identification)

**Core tension**: Unlimited tracing chains → system paralysis; too short → responsibility disappears.

**Solution structure**:

**Dual-layer principal**: Responsible subjects are divided into two layers:
- Direct controller (entity executing the decision)
- Legal responsibility-bearing organization (organization that remains responsible for the direct controller's actions)

Both layers must exist simultaneously. When the direct controller disappears, the legal承接 organization cannot disappear with it.

**Responsibility tracing chain**: Each decision carries a complete authorization source record, auditable and traceable.

**Limited liability correction**:
- Responsibility chains must trace at minimum to the dual-layer principal
- Beyond N layers, institutional mechanisms or mandatory insurance backstops assume the residual burden
- N is dynamically adjusted based on system complexity and potential harm magnitude
- Core logic: responsibility must be traceable but need not exhaust the chain

**Theoretical connection**: The adaptive selection constraint explains why limited tracing is sufficient — responsibility-misaligned structures will be eliminated without requiring infinite tracing to generate this elimination pressure.

### 4.2 Audit Adjudication Closure (Execution Mechanism)

**Core tension**: No adjudicator (principles become empty) vs. adjudicator abuse (adjudication authority itself becomes shadow power).

**Solution structure**:

**Multi-layer audit**: No single adjudicator exists. Audit proceeds by level:
1. Self-audit at current layer
2. Superior-level audit
3. Institutional arbitration (third party independent of the authorization chain)

**Adjudication closure**: The final adjudicator must also bear corresponding responsibility.

> If the adjudicator bears no consequences, adjudication authority itself becomes shadow power.

**Transparent traceability**: Each layer's audit opinion and adjudication record is public; the audit process itself is verifiable.

**Conflict resolution rules**:
- Resolve at current layer first
- If unresolvable, escalate to superior
- If superior cannot resolve, enter institutional arbitration
- Arbitration results are public; adjudicators bear corresponding responsibility

### 4.3 Scale-Triggered Hierarchical Accountability (Scale Boundary)

**Core tension**: Responsibility symmetry is directly implementable in small systems, but in large-scale social systems "decision-maker = consequence-bearer" is physically impossible.

**Solution structure**:

**Scale thresholds**: Define scale boundaries using quantifiable indicators:

| Indicator | Small Scale (Single-layer) | Large Scale (Hierarchical) |
|-----------|---------------------------|---------------------------|
| Affected population | < threshold T₁ | ≥ threshold T₁ |
| Economic impact | < threshold T₂ | ≥ threshold T₂ |
| Consequence reversibility | Reversible | Irreversible or difficult to reverse |

T₁ and T₂ specific values are set by regulatory bodies based on domain characteristics. ECET provides the framework, not the specific values.

**Hierarchical trigger rules**:
- Small scale: single-layer responsibility, decision-maker directly bears consequences
- Exceeds threshold: at least two layers of responsibility tracing
- Each order-of-magnitude increase in impact scale adds one layer of responsibility tracing requirement

**Theoretical connection**: The incompleteness constraint explains why large-scale systems cannot rely solely on individual responsibility — no individual can completely anticipate all consequences of large-scale decisions.

---

## 5. Application: AI Agent Safety Architecture

### 5.1 The Core Paradigm Shift

Current AI alignment approaches — RLHF, Constitutional AI, prompt engineering, red-teaming — share a common structural assumption: make the model less likely to produce bad outputs by modifying the generation process.

ECET derives a different conclusion from the adaptive selection constraint:

> Alignment is not making the model "intrinsically good" — it is making "bad outputs" unable to pass through system gates.

The theoretical basis for this shift:
- **Filtering must be independent of generation** (adaptive selection constraint): self-verification does not constitute filtering
- **Deviation cannot be eliminated** (necessary consequence of the three axioms): attempting to eliminate all deviation simultaneously eliminates adaptive capacity
- **Incompleteness cannot be overcome** (incompleteness constraint): no training can make a model complete

Therefore, the design goal of safety architecture is not "a deviation-free model" but "a system with effective filtering."

### 5.2 Three-Layer Constraint System

AI agent constraints are organized in three layers corresponding to the three axioms:

**Specification Layer (Hard Constraints)**
- Corresponds to: energy constraint — physical boundaries cannot be exceeded
- Definition: non-negotiable physical/logical/safety boundaries; violation = FAIL, no exceptions
- Characteristics: deterministic, auditable, cannot be modified through learning
- Examples: cannot output certain categories of harmful content; transfer amounts cannot be negative; code must compile; operations cannot exceed authorized scope

**Mapping Layer (Soft Constraints)**
- Corresponds to: adaptive selection constraint — optimize adaptiveness within constraints
- Definition: negotiable preferences, style, efficiency tradeoffs; adjustable through learning
- Characteristics: probabilistic, adjustable, allows deviation
- Examples: tone should be polite; code style should be concise; responses should be brief

**Self-Referential Layer (Meta-Constraints)**
- Corresponds to: incompleteness constraint — the system must be able to reflect on its own limitations
- Definition: the agent's capacity to reflect on and revise its own constraints
- Characteristics: evolutionary, requires human participation
- Examples: agent discovers a specification layer rule is self-contradictory in the current context; agent identifies that a mapping layer preference has produced unexpected harmful consequences; agent identifies its knowledge boundary and actively FREEZEs

### 5.3 Execution Architecture: Seven-Step Cycle

Based on the closed-loop evolutionary dynamics of Section 2, the AI agent execution layer is implemented as a seven-step cycle:

```
1. Perceive      User input / environment state
      ↓
2. Parse         Intent recognition + risk classification
      ↓
3. Generate      Candidate output (deviation permitted)
      ↓
4. Verify        Independent gate check (three-value judgment)
      ↓
PASS ──────→ 5. Output    Result + audit log
FAIL ──────→ 6. Rollback  Record failure + regenerate
FREEZE ────→ 7. Resolve   Pause + request human escalation

5/6/7 → Feedback record → Learning layer → Evolutionary layer
```

**Critical design points**:
- Step 4's validator must be independent of Step 3's generation model
- FREEZE is not failure — it is the correct response to the incompleteness constraint
- All paths (PASS/FAIL/FREEZE) must produce audit records

### 5.4 Responsibility Symmetry: Minimum Engineering Implementation

Three mechanisms constitute the minimum engineering implementation of the responsibility symmetry principle:

**Emergency Kill Switch**
- Physical control layer held by humans, not routable through the agent's software stack
- Hardware power switch (bypasses software stack), network isolation switch (physical disconnect), storage read-only lock
- Constraint: the Kill Switch trigger path cannot pass through the agent's own software stack

**Authorization Signature Chain**
Each operation carries a complete authorization chain:
```
Operation Request = {
  Executor:        Agent-ID
  Authorizer:      Superior principal
  Authorization scope: Explicit decision boundary
  Authorization TTL:   Explicit time limit
  Authorization chain: Complete upstream authorization record
  Signature:       Cryptographically unforgeable signature
}
```
Constraint: if any layer of the authorization chain is missing or expired, the operation directly FAILs.

**Revocable Key Architecture**
```
Key hierarchy:
  Root Key (human-held, offline)
    └── Org Key (TTL = 1 year)
         └── Agent Key (TTL = 24 hours)
              └── Session Key (TTL = 1 hour)

Rules:
  • No permanent keys
  • Superior can revoke subordinate keys at any time (immediate effect)
  • Root Key must be stored offline
  • Revocation cascades: superior revocation automatically invalidates all subordinates
```

### 5.5 Comparison with Existing AI Safety Frameworks

| Framework | Core Mechanism | Limitation from ECET Perspective |
|-----------|---------------|----------------------------------|
| RLHF | Adjust probability distribution during training | Filtering not independent of generation; deviation eliminated rather than managed |
| Constitutional AI | Rules embedded in training | Rules fixed at training time, cannot dynamically update (violates anti-finalization) |
| Red-teaming | Post-hoc failure discovery | Execution-layer intervention after failure; not preventive architecture |
| EU AI Act | Regulatory compliance requirements | Provides boundaries, not architecture; no operationalizable implementation path |
| **ECET + ODD** | Independent verification + three-value gate + responsibility chain | Derived from axioms, has theoretical foundation; operationalizable; cross-domain |

---

## 6. Testable Hypotheses

ECET's three axioms are not directly falsifiable — this is the same epistemic status as Darwinism and the second law of thermodynamics. But a framework that generates no testable predictions is philosophy, not a scientific tool.

ECET resolves this through derived hypotheses: the axioms themselves are not falsifiable, but specific hypotheses derived from the axioms can be experimentally verified or falsified.

> If the majority of H1–H10 are falsified, the ECET framework requires revision. This is the scientific honesty of the theory.

Each hypothesis includes: source axiom, statement, verification direction, and explicit falsification conditions.

### H1: Deviation Budget Hypothesis
**Source**: Energy constraint + adaptive selection constraint
**Statement**: Under fixed resource constraints, systems with non-zero deviation budgets adapt faster to novel environments than zero-deviation systems.
**Falsification condition**: If zero-deviation systems systematically outperform deviation-budget systems in novel environment adaptation speed, H1 is falsified.

### H2: FREEZE Rate Hypothesis
**Source**: Incompleteness constraint
**Statement**: In complex tasks, FREEZE rate (frequency of acknowledging uncertainty) is positively correlated with output quality until FREEZE rate exceeds a threshold, after which it becomes negatively correlated.
**Operationalization**: FREEZE rate is preset by system parameters, independent of quality evaluation; output quality is judged by independent evaluators or ground truth, independent of FREEZE definition.
**Falsification condition**: If no inverted-U relationship exists between FREEZE rate and output quality, H2 is falsified.

### H3: Responsibility Symmetry Stability Hypothesis
**Source**: Adaptive selection constraint
**Statement**: Organizations with higher decision-consequence symmetry survive longer under equivalent external pressure.
**Falsification condition**: If no significant positive correlation exists between responsibility symmetry and organizational survival time, H3 is falsified.

### H4: Independent Verification Hypothesis
**Source**: Adaptive selection constraint
**Statement**: AI systems using independent validators (verification separated from generation) have lower error rates in safety-critical tasks than self-verifying systems.
**Operationalization**: Verification architecture type is preset by system design, independent of error rate measurement; error rate is judged by standard test sets or independent audit, independent of verification architecture definition.
**Falsification condition**: If no significant difference in error rates exists between independent verification and self-verification, H4 is falsified.

### H5: Closed-Loop Speed Hypothesis
**Source**: Adaptive selection constraint + incompleteness constraint
**Statement**: Feedback loop speed (time from action to cognitive update) is positively correlated with system performance in dynamic environments until loop speed exceeds system processing capacity, after which it becomes negatively correlated.
**Falsification condition**: If no inverted-U relationship exists between loop speed and system performance, H5 is falsified.

### H6: Scale Boundary Hypothesis
**Source**: Incompleteness constraint + energy constraint
**Statement**: When decision impact scale exceeds a threshold, single-layer responsibility structure stability significantly declines; introducing hierarchical responsibility structure restores stability.
**Falsification condition**: If no significant positive correlation exists between scale and hierarchical responsibility structure requirements, H6 is falsified.

### H7: Shadow Sovereignty Fragility Hypothesis
**Source**: Adaptive selection constraint
**Statement**: Shadow sovereignty structures (systems with high decision-consequence separation) have higher collapse probability under external shocks than responsibility-symmetric structures.
**Falsification condition**: If shadow sovereignty structures are not less stable than responsibility-symmetric structures under external shocks, H7 is falsified.

### H8: Incompleteness Acknowledgment Hypothesis
**Source**: Incompleteness constraint
**Statement**: Systems that explicitly acknowledge their limitations (annotating uncertainty in outputs) achieve higher long-term user trust than systems that do not acknowledge limitations.
**Falsification condition**: If no positive correlation exists between acknowledging limitations and long-term trust, H8 is falsified.

### H9: Evolutionary Layer Intervention Hypothesis
**Source**: Adaptive selection constraint + incompleteness constraint
**Statement**: AI systems with human participation in evolutionary layer decisions (rule modification) maintain higher value alignment stability over long-term operation than fully autonomous evolutionary systems.
**Falsification condition**: If no significant positive correlation exists between human evolutionary layer participation and value alignment stability, H9 is falsified.

### H10: Anti-Finalization Hypothesis
**Source**: Incompleteness constraint + adaptive selection constraint
**Statement**: Institutional designs claiming "permanent validity" (containing no revision mechanisms) adapt more slowly after environmental change than institutional designs with explicit revision mechanisms.
**Falsification condition**: If institutions with revision mechanisms do not outperform fixed institutions in adaptation speed, H10 is falsified.

**Hypothesis priority**: H3, H4, H7 directly support the responsibility symmetry principle and are the most critical. If these three are falsified, ECET's governance conclusions require fundamental revision.

---

## 7. Related Work

### 7.1 Intellectual Precursor to "Shadow Sovereignty"

Nordstrom (2000), in "Shadows and Sovereigns" (*Theory, Culture & Society*), examined how transnational illicit networks exercise "social sovereignty" outside formal state and legal channels. ECET's "shadow sovereignty" concept shares terminological overlap with Nordstrom's framework but operates at a different analytical level. Nordstrom's "shadows" refer to concrete networks — illicit economies, smuggling, underground trade. ECET's "shadow sovereignty" refers to a structural state: the separation of decision authority from consequence-bearing. Nordstrom's analysis points toward specific illegal actors; ECET's shadow sovereignty can emerge in entirely legal organizations without any subjective intent — the East India Company, financial derivative markets, and AI deployments are all legally operating shadow sovereignty structures. ECET's contribution relative to Nordstrom is the shift from "describing the phenomenon" to "diagnosing the structure" and providing operational paths for closing the accountability gap.

### 7.2 Accountability Gap Research

**Accountability Gap Research**

Matthias (2004) first systematically articulated the "responsibility gap" concept: learning automata can produce behaviors that even their designers cannot anticipate, creating structural gaps in traditional accountability frameworks. Bovens (2007), Mulgan (2014), and subsequent researchers further documented and analyzed this phenomenon. ECET builds on this empirical foundation but provides what accountability gap research lacks: a theoretical derivation of why accountability gaps are structurally unstable (from the adaptive selection constraint), and operational boundary conditions for closing them.

### 7.3 Subsidiarity Principle

The subsidiarity principle in Catholic social philosophy and EU governance holds that decisions should be made at the lowest competent level. This partially overlaps with ECET's scale boundary condition. The key difference: subsidiarity is a normative principle without a theoretical derivation of why it holds. ECET derives the equivalent principle from the incompleteness constraint and energy constraint, providing a structural rather than normative justification.

### 7.4 AI Alignment Research

Current AI alignment approaches — RLHF (Christiano et al., 2017), Constitutional AI (Bai et al., 2022), scalable oversight (Amodei et al., 2016) — focus primarily on modifying the generation process to reduce the probability of harmful outputs. Recent engineering work has moved toward generation-verification separation: Chain-of-Verification (CoVe; Dhuliawala et al., 2023) proposes architectures where one model generates candidate outputs and an independent model verifies them. This engineering practice aligns closely with ECET's independent verification principle. ECET's contribution is to elevate this engineering practice to an axiomatic requirement: the adaptive selection constraint structurally requires that filtering be independent of generation — not merely as an efficiency optimization, but as a condition of system persistence. Additionally, ECET's reframing of FREEZE mechanisms as correct responses to the incompleteness constraint (rather than failures to be minimized) has no corresponding theoretical foundation in existing alignment research.

### 7.5 Free Energy Principle and Thermodynamic AI Frameworks

The Free Energy Principle (Friston, 2010) is the closest existing framework to ECET's thermodynamic derivation approach. It proposes that biological systems minimize "surprise" through active inference, grounded in variational inference and information theory, borrowing the concept of "free energy" from thermodynamics. However, the Free Energy Principle is primarily descriptive — it explains how cognitive systems work — and is applied to individual cognitive agents rather than social governance structures. ECET's use of thermodynamic constraints is normative: it derives governance principles from energy constraints, not a model of cognitive function.

A related framework, sometimes called the "Second Law of Intelligence," attempts to reframe AI alignment as a problem of "controlling ethical entropy" — providing a quantitative basis for ethical maintenance in AI systems. This framework focuses on individual AI system ethics, without extending to social governance structures or responsibility attribution. ECET's scope is broader: it derives governance principles applicable across physical, cognitive, organizational, and social systems from the same foundational constraints.

Recent control-theoretic AI safety research (e.g., arXiv:2506.23703) treats AI systems as controllable systems and applies classical control theory safety analysis, emphasizing data control, feedback mechanisms, and system boundaries. This has conceptual resonance with ECET's closed-loop evolutionary dynamics. The key distinction: control-theoretic frameworks focus on engineering safety of individual systems; ECET focuses on deriving governance principles for the social structures within which AI systems operate. The two frameworks are complementary rather than competing.

### 7.6 Complex Adaptive Systems

The Santa Fe school's work on complex adaptive systems (Holland, 1992; Kauffman, 1993) provides the systems-theoretic background for ECET's framework. ECET extends this tradition by deriving governance implications from the structural properties of complex adaptive systems, rather than treating governance as external to system dynamics.

### 7.7 Institutional Economics

North (1990) and subsequent institutional economists have analyzed how institutional structures shape incentives and outcomes. ECET's responsibility symmetry principle and operational boundary conditions can be read as a contribution to institutional design theory, providing a structural derivation of why certain institutional configurations are more stable than others.

### 7.7 Evolutionary Governance Theory

Evolutionary Governance Theory (EGT; Beunen et al., 2015; Van Assche et al., 2014) explicitly treats governance as an evolutionary process, emphasizing path dependence, selection pressures, and institutional evolution. ECET shares EGT's evolutionary perspective but differs in its starting point: EGT is descriptive — analyzing how governance institutions evolve historically; ECET is normative — deriving from evolutionary constraints how governance should be designed. EGT asks "how does governance evolve?"; ECET asks "what governance structures can persist under evolutionary pressure?" The two frameworks are complementary: EGT provides historical case evidence; ECET provides structural predictions that EGT cases can test.

### 7.8 Distinction from TGC v2

Kim's (2023) Trust Governance Compact v2 framework also employs the term "responsibility symmetry," defined as "the structural inseparability of power and responsibility," with a focus on the objects of trust in democratic governance. ECET's responsibility symmetry principle reaches similar conclusions but from a fundamentally different foundation: TGC v2 is grounded in social ontology and democratic trust theory; ECET is grounded in the adaptive selection constraint — responsibility-misaligned structures are unstable under evolutionary pressure and will be eliminated. This is not a moral requirement but a condition of structural persistence. The distinction: TGC v2 asks "how should democratic governance distribute responsibility?"; ECET asks "what responsibility structures can survive under evolutionary pressure?" The convergence of conclusions from different foundations strengthens the case for responsibility symmetry as a robust governance principle.

### 7.9 ECET as Meta-Framework

Taken together, the comparisons above suggest ECET's most accurate positioning: ECET is a **meta-framework** for AI governance, not a replacement framework. ECET does not claim to replace RLHF, Constitutional AI, the EU AI Act, subsidiarity principles, or TGC v2 — these frameworks have practical value in their respective domains. ECET's role is to provide theoretical foundations and meta-principles: why certain governance structures are more stable than others (adaptive selection constraint), why any governance structure must remain revisable (incompleteness constraint), why decision authority must have a physical bearer (energy constraint).

Existing frameworks can be reinterpreted, evaluated, and improved under ECET's meta-principles rather than being negated. RLHF, within the ECET framework, can be understood as an optimization tool for the mapping layer. The EU AI Act can be understood as a legal implementation of the specification layer. Subsidiarity can be understood as a normative expression of scale-triggered hierarchical accountability. ECET provides conceptual tools and value direction; domain experts develop specific solutions on this foundation. This is the correct use of a meta-framework.

---

## 8. Limitations and Future Directions

### 8.1 Limitations

**Axiom completeness**: The argument that three axioms are necessary and sufficient is defensible but not proven. A fourth irreducible constraint may exist.

**Operationalization gaps**: The three boundary conditions provide structural guidance but not specific parameter values (e.g., the specific thresholds T₁ and T₂ for scale-triggered hierarchical accountability). Domain-specific calibration is required.

**Empirical validation**: H1–H10 are derived hypotheses, not yet empirically validated at scale. Preliminary simulation evidence supports H1, H2, and H4 (see companion simulation report), but large-scale empirical validation remains future work.

**Self-reference**: ECET itself is subject to the incompleteness constraint — it cannot claim to be a complete description of incompleteness. This is acknowledged and handled through pragmatic truncation: ECET aims to be useful at a sufficient level of abstraction, not to achieve infinite regress.

This truncation has an explicit anchor point: C11's requirement that "physical control must remain in human hands" is ECET's pragmatic foundation — the point beyond which logical regression cannot practically proceed. If all structures are questionable and replaceable (anti-finalization principle), then the questioning mechanism itself can be questioned — producing infinite regress. ECET's response is to acknowledge that this regress cannot be perfectly resolved logically, while choosing a temporary, workable anchor point in practice. "Human physical control cannot be bypassed" is that anchor. This is not a betrayal of the anti-finalization principle but a rational truncation under the incompleteness constraint — acknowledging that we must begin somewhere, and that this starting point is itself subject to future revision.

**AI attribution principle scope boundary**: The current formulation of the AI attribution principle rests on an explicit real-world premise: AI systems do not possess independent legal personhood and cannot independently bear consequences. This is not a hidden assumption but a scope boundary that must be stated explicitly. If this premise changes in the future — for example, if some jurisdictions grant AI systems limited legal personhood, or if AI systems acquire the capacity to independently hold assets — the specific form of the AI attribution principle requires corresponding revision. This is not a theoretical defect but the anti-finalization principle applied to itself: ECET's own governance principles must remain revisable. The current version of the AI attribution principle is the optimal structure under the condition that "AI cannot independently bear consequences" — when the condition changes, the structure adjusts accordingly.

### 8.2 Three Open Challenges

Beyond the above structural limitations, three substantive challenges require explicit acknowledgment as open research problems.

**A clarification on the "shadow sovereignty structures are short-term stable" objection**

A common objection is that shadow sovereignty structures are often highly stable in practice due to their short-term efficiency — monopoly platforms, bureaucratic systems, and financial derivative markets all persisted for extended periods without "automatically collapsing" due to structural instability. This appears to contradict the adaptive selection constraint's predictions.

ECET's response is that this objection conflates "collapse" with "who bears the cost of collapse." Shadow sovereignty structures do collapse — the East India Company was ultimately dissolved, the 2008 financial derivative market did collapse — but the costs were borne externally: by taxpayers, colonial populations, and third parties who never authorized the decisions that caused the collapse. This is precisely the definition of shadow sovereignty: the separation of decision authority from consequence-bearing.

The correct formulation of the adaptive selection constraint is therefore not "shadow sovereignty structures will automatically collapse" but rather "shadow sovereignty structures externalize their collapse costs — the instability is transferred to parties who cannot refuse to bear it, not eliminated." The structure appears stable because it successfully transfers its instability to external parties. This transfer capacity is finite: when external absorption capacity is exhausted (social trust collapses, regulatory intervention occurs, systemic crisis materializes), the structure's internal instability manifests as crisis.

This mechanism explains why shadow sovereignty structures tend to collapse suddenly and catastrophically rather than gradually — instability accumulates through the externalization process until the threshold of external absorption capacity is breached.

**Challenge 1: The Validator Regress Problem**

ECET's independent verification architecture depends on validators that are themselves cognitive systems subject to the incompleteness constraint. A simple validator will suppress valuable complex outputs; a complex validator (e.g., a second large model) introduces its own deviation. This creates a potential regress: who validates the validator?

ECET's partial response is the layer distinction from B07: the evolutionary layer (rule modification) requires human participation, while the execution layer can operate autonomously. FREEZE escalation routes edge cases to human judgment. However, in high-frequency millisecond-scale decision environments, the compute cost and latency of human escalation remain an unresolved engineering challenge. This is an open problem, not a solved one.

**Challenge 2: The Safety-Speed Tradeoff in Adversarial Environments**

ECET's evolutionary layer requires human authorization for rule modification. In adversarial contexts — cyberwarfare, high-frequency financial trading, competitive AI deployment — an opponent system that permits autonomous rule modification may outperform an ECET-compliant system in short-term Darwinian competition. The "safe but slow vs. dangerous but fast" tradeoff is real.

ECET's structural response is that short-term speed advantages do not offset long-term structural fragility — shadow sovereignty structures are unstable over longer time horizons (H7). But this is currently a theoretical claim, not an empirically validated conclusion. The time horizon over which structural stability advantages materialize is unknown. This is precisely what H7 needs to establish empirically.

**Challenge 3: Regulatory Arbitrage in the International System**

ECET's governance principles operate at the level of structural stability arguments. They do not resolve the international coordination problem: if jurisdiction A strictly implements responsibility symmetry with high compliance costs, while jurisdiction B permits shadow sovereignty structures, jurisdiction B's AI industry may achieve short-term global market dominance through regulatory arbitrage.

ECET's scope boundary is explicit here: ECET is a governance framework, not an international treaty. It provides the structural argument for why responsibility-symmetric systems are more stable over time, but it does not resolve the collective action problem of international coordination. This is a limitation of scope, not a theoretical failure — but it must be acknowledged rather than elided.

### 8.3 Future Directions

**Empirical validation of H3, H7**: Most critical for ECET's governance conclusions; most amenable to testing using existing organizational survival and financial crisis data.

**Validator architecture research**: Developing lightweight, domain-specific validators that minimize the regress problem — formal contract languages for medical, legal, and financial AI applications where behavioral contracts can be precisely specified.

**Scale threshold calibration**: Empirical calibration of T₁ and T₂ thresholds across domains and risk profiles.

**Time-horizon analysis for Challenge 2**: Modeling the conditions under which structural stability advantages materialize faster than adversarial speed advantages — the key empirical question for the safety-speed tradeoff.

**Integration with existing legal frameworks**: Mapping ECET's three boundary conditions onto corporate law, administrative law, and tort law to identify gaps and integration points.

---

## 9. Conclusion

ECET provides a cross-domain governance framework derived from three irreducible physical constraints. Its core contribution is not the identification of new problems — accountability gaps, shadow sovereignty, and AI governance challenges have been identified by multiple research traditions. Its contribution is a systematic, structural, and operationalizable integration of these insights into a framework with the following properties:

1. Governance principles derived from physical constraints, not ethical preferences
2. Three operational boundary conditions that translate principles into executable requirements
3. A common conceptual language accessible across engineering, law, policy, and organizational theory
4. Ten testable hypotheses providing a scientific interface for empirical validation

The framework's most direct practical implication is for AI safety architecture: output verification by independent validators is structurally superior to process inspection as an alignment strategy, because the adaptive selection constraint requires that filtering mechanisms be independent of generation sources. This is achievable with current technology and does not require novel training techniques — it requires architectural discipline.

> ECET's value lies not in the novelty of its ideas but in offering a systematic, structural, and operational integration of existing insights into a cross-domain governance framework.

---

## References

Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). Concrete problems in AI safety. *arXiv preprint arXiv:1606.06565*.

Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., ... & Kaplan, J. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback. *arXiv preprint arXiv:2204.05862*.

Bovens, M. (2007). Analysing and assessing accountability: A conceptual framework. *European Law Journal*, 13(4), 447–468.

Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *Advances in Neural Information Processing Systems*, 30.

Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J. (2023). Chain-of-verification reduces hallucination in large language models. *arXiv preprint arXiv:2309.11495*.

Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.

Kim, Y. (2023). Trust Governance Compact v2: Responsibility symmetry in democratic AI governance. *Working paper*.

Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik*, 38(1), 173–198.

Holland, J. H. (1992). *Adaptation in Natural and Artificial Systems*. MIT Press.

Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.

Matthias, A. (2004). The responsibility gap: Ascribing responsibility for the actions of learning automata. *Ethics and Information Technology*, 6(3), 175–183.

Nordstrom, C. (2000). Shadows and sovereigns. *Theory, Culture & Society*, 17(4), 35–54.

Mulgan, R. (2014). *Making Open Government Work*. Palgrave Macmillan.

North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.

Van Assche, K., Beunen, R., & Duineveld, M. (2014). *Evolutionary Governance Theory: An Introduction*. Springer.

Polanyi, M. (1966). *The Tacit Dimension*. Doubleday.

Turing, A. M. (1936). On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, 2(42), 230–265.

---

*Correspondence: fuyi.it@live.cn*
*Current public release form: ECET v1.0 public review package (A/B/C document set)*
*Simulation appendix status: proof-of-concept level support only; not completed large-scale empirical validation*


---

## Framework Note

This manuscript belongs to the ECET framework package. For the ASTO to ECET derivation chain, framework positioning, and core terminology definitions, see:

**[ECET.A00 Theoretical Foundation](./ECET.A00_理论基础.md)**
