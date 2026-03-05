# Bridging the Epistemic Gap

## ASTO as an Operational Middle-out Ontology for Governance in Socio-Technical Systems

**Author**: Yi Fu

---

## Abstract

Governance failures in socio-technical systems rarely result from insufficient domain knowledge. Instead, they emerge from **epistemic fragmentation**: heterogeneous disciplines employ incompatible criteria to determine when an artifact, decision, or outcome is acceptable. Engineering, medicine, and law validate objects through fundamentally different regimes, producing systems that are technically correct yet socially invalid, or normatively compliant yet operationally unsafe.

This paper introduces the **Attribute-Set Theory Ontology (ASTO)**, a **middle-out operational ontology** designed to formalize *acceptance events* in governance processes. ASTO does not aim to describe what exists in the world; rather, it models how artifacts are individuated, tested, legitimized, and institutionally fixed.

ASTO is built upon five primitives—**Attribute-Set, Cut, Perturbation, Contract, and Seal**—which together define a formal semantics of acceptance. By unifying descriptive states and normative constraints within a single operational structure, ASTO enables traceable responsibility attribution and cross-domain interoperability.

Two isomorphic case studies—AI-generated software governance and cross-regional medical diagnostics—demonstrate that seemingly unrelated failures share the same structural cause: rupture between perturbation and contractual legitimacy. Evaluation via competency questions shows that ASTO supports traceability, exception handling, and contract-relative identity.

ASTO contributes an applied ontology of governance operations, providing a formal bridge between philosophical theories of normativity and executable socio-technical systems.

**Keywords**: Operational Ontology; Governance; Acceptance; Normativity; Socio-Technical Systems

---

## 1. Introduction

Modern governance increasingly unfolds across heterogeneous expert domains. A single socio-technical artifact—such as an AI diagnostic system—simultaneously participates in engineering validation, clinical judgment, and legal accountability. Each domain employs distinct criteria of validity, which are rarely aligned.

As a result, failures frequently occur not because systems malfunction technically, but because acceptance criteria diverge across domains. Such failures expose an **epistemic gap**: the absence of a shared formal structure for determining when an artifact should be accepted, rejected, or overridden.

Existing ontological approaches offer limited solutions. Foundational ontologies provide metaphysical rigor but are poorly suited to transient, policy-driven artifacts. Data schemas provide executability but lack semantic grounding. What remains under-modeled is the governance operation itself.

This paper proposes ASTO as a **middle-out operational ontology**. Rather than modeling domain entities, ASTO formalizes the operations through which governance decisions are produced.

---

## 2. Ontological Position

ASTO adopts an **operational constructivist** commitment. It does not address the metaphysical nature of entities, but the conditions under which objects become governable.

Within ASTO, objecthood is not a natural given but an institutional achievement. Artifacts exist operationally insofar as they are:

1. individuated from a background,
2. tested against perturbations,
3. evaluated under explicit constraints,
4. and stabilized through authorized acceptance.

Reality enters governance not through correspondence to truth, but through **resistance to perturbation**. Normativity enters not as moral judgment, but as **decidable constraint**.

ASTO therefore provides an ontology of governance operations rather than of reality itself.

---

## 3. Core Primitives

### 3.1 Attribute-Set (A)

An Attribute-Set is a finite collection of property–value pairs representing a candidate artifact at a given time:

[
A = {(p_1,v_1),(p_2,v_2),\dots}
]

ASTO deliberately assigns no intrinsic typing; interpretation arises solely through contractual evaluation.

---

### 3.2 Cut (C)

A Cut is an operation of individuation:

[
C : \text{Field} \rightarrow A
]

In this context, 'Field' represents the unbounded data stream or phenomenological substrate prior to individuation (in a sense analogous to pre-individuated states discussed in process-oriented philosophies).

Different institutional contexts impose different cuts upon the same underlying reality, producing distinct governable objects.

---

### 3.3 Perturbation (P)

A Perturbation is an operator applied to test stability:

[
P(A) \rightarrow A'
]

An artifact is operationally meaningful only insofar as its structure persists within tolerated bounds under perturbation. In the medical case, perturbation refers to variations in environmental conditions (e.g., lighting, machine resolution) that test the robustness of the diagnostic inference.

---

### 3.4 Contract (K)

A Contract is a decidable legitimacy function:

[
K : \mathbb{A} \rightarrow {0,1}
]

Contracts encode all constraints—technical, institutional, and normative—under which acceptance is evaluated. ASTO enforces a strict separation between artifact and contract, enabling diagnosis of failure sources. In ASTO, a Contract is treated as an information artifact expressing institutional constraints, not as a moral or intentional entity.

---

### 3.5 Seal (S)

A Seal records an authorized acceptance event:

[
S = \text{Sign}(\text{Hash}(A),\text{Hash}(K),\text{Evidence})
]

The Seal anchors responsibility by binding artifact, contract, agent, and time. Ontologically, the Seal is modeled as an information artifact generated by an acceptance event, serving as a responsibility anchor.

---

## 4. Alignment with Existing Standards

ASTO is designed for interoperability and compiles into established semantic standards:

| ASTO          | Function    | Standard |
| ------------- | ----------- | -------- |
| Seal          | Provenance  | PROV-O   |
| Contract      | Normativity | ODRL     |
| Verification  | Constraints | SHACL    |
| Attribute-Set | Description | RDF      |

*Note on BFO compatibility*: While ASTO is an operational ontology, `Attribute-Set` loosely corresponds to BFO's `Continuant` (at a time slice), and `Perturbation` corresponds to `Process`.

*Note on ODRL*: ASTO's `Contract` maps to `odrl:Policy`, where acceptance criteria function as `odrl:Constraint`.

ASTO thus operates as a meta-ontology coordinating existing representations rather than replacing them.

---

## 5. Isomorphic Case Studies

### 5.1 AI-Generated Software

AI-generated code is evaluated through mutation testing. Perturbations intentionally alter code structure, while acceptance depends on contractual thresholds (e.g., mutation score). Failure arises when perturbation violates explicit constraints.

### 5.2 Cross-Regional Medical Diagnostics

Diagnostic AI systems trained under high-resource conditions fail in low-resource environments due to environmental perturbations not covered by implicit contracts. Acceptance is issued despite exceeding assumed bounds.

### Structural Insight

Both failures instantiate the same pattern: **perturbation exceeds contractual legitimacy**. ASTO renders this rupture explicit and traceable.

---

## 6. Evaluation via Competency Questions

* **Traceability**: Which constraint caused rejection?
  → Identify violated contract clause.

* **Responsibility**: Who authorized an exception?
  → Retrieve Seal with non-standard contract.

* **Operational Identity**: When are two artifacts the same?
  → When they satisfy the same contract under relevant perturbations.

Identity is thus contract-relative.

---

## 7. Conclusion

Socio-technical governance depends on structured acceptance. Failures arise when acceptance criteria remain implicit, fragmented, or untraceable.

ASTO provides a middle-out operational ontology that formalizes individuation, testing, legitimacy, and responsibility within a unified structure. By modeling governance operations rather than domain entities, ASTO bridges epistemic divides without imposing a unified metaphysics.

ASTO does not describe what exists.
In operational terms, it formalizes what is allowed to stand.

---

