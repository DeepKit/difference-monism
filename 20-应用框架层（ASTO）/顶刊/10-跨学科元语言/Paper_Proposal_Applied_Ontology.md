# Paper Proposal: ASTO as a Middle-out Ontology for Cross-Disciplinary Governance
**Target Journal**: *Applied Ontology* (IOS Press)
**Type**: Research Article (Foundational & Application)

---

## Title
**Bridging the Epistemic Gap: ASTO as a Middle-out Operational Ontology for Governance in Socio-Technical Systems**
*(弥合认识论鸿沟：ASTO 作为社会-技术系统治理的中出式操作性本体)*

## Abstract (Applied Ontology Style)
Cross-disciplinary governance often fails due to the "epistemic gap": the lack of a shared, executable vocabulary to bridge domain-specific descriptions (e.g., medical diagnostics) and engineering implementations (e.g., algorithmic logic). Traditional top-down foundational ontologies (like BFO or DOLCE) provide metaphysical rigor but lack direct executability in engineering pipelines. Conversely, bottom-up schemas (like JSON Schema) offer executability but lack semantic coherence across domains.

This paper introduces the **Attribute-Set Theory Ontology (ASTO)**, a "middle-out" operational ontology designed to unify the description of **objecthood, boundaries, and acceptance** across heterogeneous domains. We define a minimal set of primitives—**Attribute-Set, Cut, Perturbation, Contract, and Seal**—and provide their formal semantics rooted in a non-representational, perturbation-based epistemology.

We demonstrate ASTO's utility through two isomorphic case studies: (1) governing AI-generated code via Output-Driven Development (ODD), and (2) analyzing systemic failure in cross-regional medical diagnostics. We show that ASTO enables the compilation of normative constraints (contracts) into executable acceptance functions, effectively bridging the "Is/Ought" gap in operational contexts. Finally, we map ASTO to existing standards (PROV-O, ODRL) and evaluate its expressivity using a set of competency questions regarding responsibility attribution and failure tracing.

**Keywords**: Middle-out Ontology, Socio-Technical Systems, Governance, Attribute-Set, Perturbation, Interoperability

---

## Key Contributions
1.  **A "Middle-out" Approach**: Proposing an ontology that sits between metaphysical foundational ontologies and engineering schemas, prioritizing *operational executability* over metaphysical realism.
2.  **Unified Primitives**: Defining 5 core primitives (Attribute-Set, Cut, Perturbation, Contract, Seal) that map isomorphic structures across engineering, biology, and social governance.
3.  **Formal Semantics of Acceptance**: Providing a computable definition of "Acceptance" as a function of Artifact and Contract, bridging descriptive facts and normative judgments.
4.  **Isomorphic Evaluation**: Demonstrating that the same ontological structure explains failure modes in both software engineering (AI code) and healthcare (medical imaging).

---

## Annotated Outline (8 Sections)

### 1. Introduction: The Epistemic Gap in Governance
*   **The Problem**: Why can't lawyers, engineers, and doctors talk to each other? The misalignment of "objects" (e.g., is a "diagnosis" a mental state or a database record?).
*   **Existing Gaps**: Top-down ontologies are too heavy; bottom-up schemas are too fragmented.
*   **The Solution**: ASTO as a "Pidgin" or "Meta-language" for operational governance.

### 2. Theoretical Foundations: From Realism to Operation
*   **Ontological Commitment**: Explicitly adopting an **Operationalist** stance. We do not define what things *are* in themselves, but how they are *individuated* through operations.
*   **The Perturbation Principle**: An entity exists (in the system) if and only if it resists perturbation.
*   **The Is/Ought Bridge**: In engineering systems, physical laws and social rules both function as *constraints* on the acceptance function.

### 3. The ASTO Core: Primitives and Semantics
*   **Attribute-Set ($A$)**: A collection of property-value pairs (snapshot of state).
*   **Cut ($C$)**: An operation that separates an entity from the background field.
*   **Perturbation ($P$)**: An external force that tests the stability of the Attribute-Set.
*   **Contract ($K$)**: A set of constraints (normative boundaries) defined on $A$.
*   **Seal ($S$)**: A cryptographic or institutional record of the decision: $Accept(A, K) \rightarrow S$.
*   **Formalism**: Presenting the `Acceptance Function` and `Sealing Logic` (using First-Order Logic or set-theoretic notation).

### 4. Alignment with Existing Standards
*   **Provenance**: Mapping ASTO `Sealing` to **PROV-O** `Entity` and `Activity` (W3C).
*   **Rights/Policies**: Mapping ASTO `Contract` to **ODRL** (Open Digital Rights Language).
*   **Validation**: Mapping ASTO `Verification` to **SHACL** (Shapes Constraint Language).
*   *Goal*: Show ASTO is compatible, not competitive.

### 5. Case Study I: Engineering (Output-Driven Development)
*   **Domain**: AI-Native Software Engineering.
*   **Mapping**:
    *   $A$: The compiled binary.
    *   $P$: Mutation testing (injecting faults).
    *   $K$: The YAML configuration of passing thresholds.
    *   $S$: The digital signature in the CI log.
*   **Result**: Resolving the "responsibility crisis" by making acceptance explicit.

### 6. Case Study II: Healthcare (Diagnostic Failure)
*   **Domain**: The failure of AI diagnostics when moved from US to Thailand (based on the *Running Failure* paper).
*   **Mapping**:
    *   $A$: The CT scan image (Attribute-Set).
    *   $P$: Changes in lighting, machine resolution (environmental perturbations).
    *   $K$: The hidden assumptions of the AI model (implicit contract).
    *   $S$: The doctor's final diagnosis.
*   **Result**: Identifying the "Operational Rupture" as a mismatch between the Contract ($K$) and the local Perturbation ($P$) environment.

### 7. Evaluation: Competency Questions (CQs)
*   **Method**: Testing ASTO against specific queries to prove utility.
*   **CQ1**: "Which contract clause caused this artifact to be rejected?" (Traceability)
*   **CQ2**: "Who signed the seal that authorized this artifact despite the perturbation?" (Responsibility)
*   **CQ3**: "Are these two artifacts 'the same' with respect to Contract X?" (Identity under constraints)

### 8. Conclusion and Future Work
*   **Summary**: ASTO successfully provides a unified grammar for cross-domain governance.
*   **Limitations**: Currently focused on "discrete" artifacts; continuous streams are future work.
*   **Call to Action**: Inviting the ontology community to help refine the formal semantics for wider adoption.

---

## Sample Text: Section 3.3 (The Contract Primitive)
> "In traditional ontologies, a 'norm' is often treated as a social object distinct from physical laws. In ASTO, however, we adopt a functionalist unification. A **Contract ($K$)** is defined as a decidable predicate function $K: \mathbb{A} \rightarrow \{0, 1\}$ over the space of possible Attribute-Sets $\mathbb{A}$. Whether the constraint arises from thermodynamic limits (e.g., 'temperature must be < 100°C') or regulatory compliance (e.g., 'data must be encrypted'), its role in the **Sealing** process is identical: it serves as a selection filter that distinguishes legitimate artifacts from illegitimate ones. This unification allows ASTO to model 'hybrid failures'—where a system fails partly due to physics and partly due to policy—within a single causal graph."
