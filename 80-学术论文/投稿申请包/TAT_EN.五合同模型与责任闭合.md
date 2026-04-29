# The Five-Contract Model and the Responsibility Closure Spectrum: A Governance Framework for High-Impact AI Systems

---

## Abstract

As AI systems increasingly make or influence high-impact decisions, the question "who is responsible?" becomes structurally ill-defined. Traditional accountability frameworks assume human authorship and traceable decision chains — assumptions that no longer hold when decisions emerge from multi-agent, non-deterministic, and opaque generation paths. This paper introduces the Accountability Threshold theory (TAT), which provides two core innovations: (1) a **five-contract model** (Subject, Interface, Evidence, Freeze, Compensation) that operationalizes responsibility assignment for AI-augmented systems, and (2) a **responsibility closure spectrum** (High Closure, Medium Closure, Controlled Ambiguity) that replaces binary "responsible/not responsible" judgments with graded structural requirements. Two end-to-end case studies — an autonomous vehicle accident and an AI medical advisory error — demonstrate the framework's applicability.

---

## 1. Introduction: The Erosion of Responsibility Anchors

In conventional software engineering, responsibility is implicitly attached to the human author, the review process, or module ownership. In AI-assisted workflows, code may be generated, revised, and regenerated multiple times; generation paths are opaque; and multiple agents contribute asynchronously. The question "Who is responsible?" becomes structurally unanswerable under inherited frameworks.

Existing responses — improved prompt engineering, more tests, model constraints — operate within the code-centric paradigm and fail to address the deeper structural shift: **the responsibility anchor itself has eroded**.

---

## 2. The Five-Contract Model

TAT proposes that any high-impact AI deployment must satisfy five contracts before responsibility can be considered structurally addressed:

### Contract 1: Subject Contract
**Who is the ultimate bearer of consequences?**

The subject contract requires specifying who cannot disappear through subcontracting, shell entities, or role drift. If every party in the chain can point to someone else, no subject exists.

### Contract 2: Interface Contract
**Which high-impact actions must pass through a responsibility interface?**

Certain actions — those with irreversible or high-magnitude consequences — must be channeled through defined interfaces. Bypass channels must be structurally impossible, not merely discouraged.

### Contract 3: Evidence Contract
**What records must be preserved and externally reviewable?**

Evidence must be structured, timestamped, tamper-evident, and independently verifiable. Four evidence types are defined: test reports, review records, decision narratives, and override records.

### Contract 4: Freeze Contract
**Who has the authority to pause, degrade, withdraw, freeze, or recall?**

A freeze authority must exist independently of the deployment authority. The same entity that benefits from deployment cannot be the sole arbiter of whether deployment continues.

### Contract 5: Compensation Contract
**After an incident, who pays, who compensates, and through what path?**

Compensation must have a predefined path. The cost of harm must not rest solely on the harmed party by default.

---

## 3. The Responsibility Closure Spectrum

TAT replaces binary "responsible/not responsible" judgments with a graded spectrum:

### High Closure
For high-irreversibility harm, high public risk, and large-scale externality scenarios. Requires: clearly identified subject, functioning interface, complete evidence chain, independent freeze authority, predefined compensation path, and external reviewability.

### Medium Closure
For general organizational governance and moderate-risk decisions. Allows limited division of labor and staged referral, but the audit trail and escalation path must not be severed.

### Controlled Ambiguity
For innovation exploration, rapid crisis response, or high-uncertainty early-stage experimentation. Allows local responsibilities to remain temporarily fuzzy, but requires minimum guardrails:
1. **Audit trail**: who made what judgment, when, with what escalation
2. **Trigger threshold**: what conditions move from ambiguity to closure (not retroactively written)
3. **Escalation and review interface**: ambiguity may not be a permanent shield
4. **Compensation and exit interface**: costs may not remain only at vulnerable nodes

---

## 4. Responsibility Escape Patterns

TAT identifies four common patterns through which responsibility evades structural closure:

1. **Strategic ambiguity**: using vague language to avoid specifying accountable parties
2. **Outsourcing chain severance**: cutting consequence-bearing links through subcontracting
3. **Collective decision erasure**: dissolving individual approval authority into "group decisions"
4. **High-risk experimentation bypass**: conducting irreversible trials while bypassing freeze and appeal interfaces

---

## 5. Case Study 1: Autonomous Vehicle Accident

A Level 3 autonomous vehicle fails to detect a pedestrian, causing severe injury. TAT analysis reveals: (a) the manufacturer is the primary subject, but the AI software supplier shares secondary responsibility because internal test reports showed known blind spots for partially occluded pedestrians; (b) the interface contract failed — pre-incident near-miss reports were not escalated; (c) the freeze contract was not triggered until after the accident, despite three prior near-miss events. The framework specifies: immediate OTA downgrade to L2, evidence sealing of pre-incident sensor logs and test reports, manufacturer compensation to victim with contractual recovery from supplier, and regulatory reform requiring blind-spot disclosure.

---

## 6. Case Study 2: AI Medical Advisory Error

An AI diagnostic support system fails to flag a known drug allergy because the allergy record was stored in a legacy system excluded from the AI's data migration. The doctor, relying on the AI's "no warning" output, prescribes the contraindicated drug. TAT analysis reveals the interface contract failure is the core issue: the AI system did not declare its data source scope — the doctor could not know what the system didn't know. The structural fix is not "train doctors not to trust AI" but requiring AI medical systems to explicitly declare their data source boundaries and known gaps. Primary responsibility falls on the hospital (system deployer and data manager), not the individual doctor.

---

## 7. Relationship to Upstream Theory

This framework sits within a larger theoretical architecture in which it inherits structural grammar from a prior ontological foundation and governance boundary analysis, and provides the responsibility threshold layer that downstream engineering methods compile into contracts, gates, and evidence sealing. The present paper is self-contained; readers need not consult the larger framework to evaluate its claims.

---

## 8. Limitations

TAT is a conceptual framework, not an empirically validated theory. The two case studies are post-hoc analyses, not prospective predictions. Systematic testing across multiple domains and incident types is required before TAT can claim empirical support.

---

## References

- Floridi, L. et al. (2018). "AI4People—An Ethical Framework for a Good AI Society." *Minds and Machines*, 28(4), 689-707.
- Mittelstadt, B. D. et al. (2016). "The Ethics of Algorithms." *Big Data & Society*, 3(2).
- Nissenbaum, H. (1996). "Accountability in a Computerized Society." *Science and Engineering Ethics*, 2(1), 25-42.
- Selbst, A. D. et al. (2019). "Fairness and Abstraction in Sociotechnical Systems." *FAccT 2019*.
