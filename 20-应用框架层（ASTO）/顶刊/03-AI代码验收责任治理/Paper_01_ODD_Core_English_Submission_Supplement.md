# Supplementary Material (Submission Appendix)

> This file collects extended figures, examples, and detailed comparisons that were removed from the magazine-style submission for brevity.

Source: Paper_01_ODD_Core_English_Submission_Full.md
---

# 2. Core Concepts

## 2.1 Artifacts: The True Goal of Software Development

### 2.1.1 What is an Artifact?

**Definition**: An Artifact is a verifiable output produced during software development that can satisfy specific human needs.

```
┌─────────────────────────────────────────────────────────────────┐
│                  Essential Definition of Artifact                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Artifact = Verifiable Output + Satisfies Specific Need + Has Use Value │
│                                                                  │
│  Three core properties of artifacts:                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Verifiability                                           │ │
│  │    • Correctness can be confirmed through testing          │ │
│  │    • Compliance can be checked against contracts           │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2. Need-fulfilling                                         │ │
│  │    • Corresponds to explicit human needs                   │ │
│  │    • Solves concrete business problems                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 3. Use-value                                               │ │
│  │    • Can be directly used by users                         │ │
│  │    • Produces actual utility                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 The Relationship Between Artifacts and Human Needs

**Philosophical insight**: Humans fundamentally need **results**, not processes.

**Analogy 1: The Intelligent Pharma Factory**

Imagine this scenario: You need a cure for a disease. You have funding.

```
┌─────────────────────────────────────────────────────────────────┐
│                The Essence of the Pharma Transaction             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Intent]  ─────────────────────────────────────→  [Drug]       │
│  (Treat X)      Do you care what happens in between?   (Artifact) │
│                                                                  │
│  The mixing process? The chemical reactions? The lab coats?     │
│                                                                  │
│  ──────────────────────────────────────────────────────────────  │
│  Answer: You don't care about the process. You care about SAFETY.│
│  You trust the drug not because you saw it being mixed,         │
│  but because it passed strict GMP Quality Control (QC).         │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│  Insight: Process is the manufacturer's problem;                │
│          Verified Artifact is the patient's need.               │
└─────────────────────────────────────────────────────────────────┘
```

**Analogy 2: The Official Stamp and Blank Paper**

You go to a government office. You hold a paper filled with text (an application).

What's your purpose? Not "queuing," not "talking to the clerk," not "watching them press down on the paper."

Your only purpose is: **To get a red official stamp on this paper.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Artifact State Transition                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  State A: Paper without stamp                                   │
│          Value = 0                                              │
│                    ↓                                             │
│          [Queue → Submit → Review → Stamp]                      │
│                    ↓                                             │
│  State B: Paper with stamp                                      │
│          Value = Permission/Rights                               │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│  Insight: Work is essentially artifact state transition.        │
│          All processes exist only to transform artifacts        │
│          from State A to State B.                               │
└─────────────────────────────────────────────────────────────────┘
```

**Software domain mapping**:

A client gives you $1 million for an e-commerce system. They don't care if you use Java or Go, microservices or monolith. They only care about:
- Can users place orders?
- Can payments succeed?
- Can shipping be tracked?

**These are artifacts—things that can be used and create value.**

### 1.3 Artifact Classification System

ODD categorizes software development artifacts into 698 types, each with clear definitions, templates, and acceptance criteria.

```
┌─────────────────────────────────────────────────────────────────┐
│            698 Artifact Types Classification (Excerpt)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  01. Functional Artifacts (~300 types)                          │
│      01.01 API Endpoints    01.02 Business Services             │
│      01.03 Data Processors  01.04 User Interfaces               │
│      01.05 Background Tasks 01.06 Integration Adapters          │
│                                                                  │
│  02. Verification Artifacts (~150 types)                        │
│      02.01 Unit Tests       02.02 Integration Tests             │
│      02.03 E2E Tests        02.04 Performance Tests             │
│      02.05 Security Tests   02.06 Mutation Test Configs         │
│                                                                  │
│  03. Configuration Artifacts (~100 types)                       │
│      03.01 App Config       03.02 Environment Config            │
│      03.03 Build Config     03.04 Deployment Config             │
│      03.05 Monitoring Config 03.06 Security Config              │
│                                                                  │
│  04. Documentation Artifacts (~80 types)                        │
│      04.01 API Docs         04.02 Architecture Docs             │
│      04.03 User Manuals     04.04 Operations Manuals            │
│      04.05 Changelogs       04.06 Decision Records              │
│                                                                  │
│  05. Contract Artifacts (~68 types)                             │
│      05.01 Feature Contracts 05.02 API Contracts                │
│      05.03 Data Contracts   05.04 Performance Contracts         │
│      05.05 Security Contracts 05.06 Integration Contracts       │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│  Why 698 types?                                                 │
│  • Finer classification = More accurate AI understanding        │
│  • Each type has dedicated templates, reducing AI "creativity"  │
│  • AI understands these categories; humans define once          │
│  • Enables automated acceptance and quality metrics             │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Why Generate Artifacts, Not Code?

### 2.1 The True Status of Code

Traditional thinking holds that programmers' work is "writing code," and code is the programmer's "creation." But this is a **historical misunderstanding**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    The True Status of Code                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Traditional view:                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Requirements → Code → Value                               │ │
│  │                  ↑                                         │ │
│  │              (Core product)                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ODD perspective:                                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Requirements → Contract → Code → Tests → Artifact → Value │ │
│  │                             ↑              ↑               │ │
│  │                      (Intermediate)    (Core product)      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│                                                                  │
│  Analogy: Pharma Factory                                        │
│  • Drug = Artifact (what patients want)                         │
│  • Synthesizer = Code (production tools)                        │
│  • Chemical waste = Code byproducts (unavoidable outputs)       │
│                                                                  │
│  When you take a drug, you don't ask about the reactor model.   │
│  When clients buy software, they shouldn't care how "elegant"   │
│  your code is.                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Three Illusions of Traditional Programming Thinking

```
┌─────────────────────────────────────────────────────────────────┐
│          Three Illusions of Traditional Programming              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Illusion 1: Writing code itself is value                       │
│  ─────────────────────────────────────────────────────────────  │
│  → Truth: Code is just a means to an end                        │
│  → Analogy: You obsess over knife sharpening,                   │
│            but the customer just wants the dish                 │
│                                                                  │
│  Illusion 2: Code is an asset                                   │
│  ─────────────────────────────────────────────────────────────  │
│  → Truth: Code is a liability (more = harder to maintain,       │
│           harder to understand, more bugs)                      │
│  → Analogy: More factory machines = higher maintenance costs    │
│                                                                  │
│  Illusion 3: Code quality = Software quality                    │
│  ─────────────────────────────────────────────────────────────  │
│  → Truth: Artifact correctness = Software quality               │
│  → Analogy: Whether a drug is safe doesn't depend on            │
│            how shiny the reactor is                             │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│                                                                  │
│  Common programmer "self-indulgences":                          │
│  • Knife skills (code style)  → Patient just wants the cure     │
│  • Plating (architecture)     → Patient only cares about safety │
│  • Cookware (framework)       → Patient just wants to be healed │
│                                                                  │
│  These matter to professional chemists, but for patients,       │
│  they're secondary to GMP compliance.                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Why ODD Focuses on Artifacts

```
┌─────────────────────────────────────────────────────────────────┐
│                Why ODD Focuses on Artifacts                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Reason 1: Artifacts are verifiable                             │
│  ─────────────────────────────────────────────────────────────  │
│  • Whether code is "elegant" is subjective                      │
│  • Whether artifacts are "correct" is objective fact            │
│  • We can test artifacts; we can't test "code aesthetics"       │
│                                                                  │
│  Reason 2: Artifacts correspond to human needs                  │
│  ─────────────────────────────────────────────────────────────  │
│  • Code corresponds to "implementation approach"                │
│  • Artifacts correspond to "user stories"                       │
│  • Clients accept artifacts, not lines of code                  │
│                                                                  │
│  Reason 3: Artifacts can be sealed and protected                │
│  ─────────────────────────────────────────────────────────────  │
│  • Code can be accidentally modified or overwritten             │
│  • Once accepted, artifacts can be sealed                       │
│  • Sealed artifacts are stable "building blocks"                │
│                                                                  │
│  Reason 4: AI excels at generating code, but acceptance         │
│           requires humans                                        │
│  ─────────────────────────────────────────────────────────────  │
│  • AI can rapidly generate vast amounts of code                 │
│  • But AI can't judge "is this what the user wanted?"           │
│  • Artifact definition and acceptance is human work             │
│  • ODD: Humans focus on "define what"; AI focuses on "how"      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Paradigm Shift: From "Generating Code" to "Generating Artifacts"

```
┌─────────────────────────────────────────────────────────────────┐
│     Paradigm Shift: From "Code" to "Artifacts"                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Traditional AI-assisted development (e.g., GitHub Copilot):    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Human writes → AI completes → Human reviews → Human tests │ │
│  │       ↑             ↑              ↑                       │ │
│  │   (Human-led)   (AI assists)  (Bottleneck!)               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Problem: AI generates 100x faster than humans,                 │
│          but review speed remains human speed                   │
│  Result: Faster AI = Busier humans = Bigger bottleneck          │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  ODD approach:                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Human defines contract → AI generates → System verifies → Auto-seal │
│  │       ↑                                    ↑               │ │
│  │   (Human-led)                      (No human bottleneck)   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Key shifts:                                                    │
│  • Humans no longer review code—they define contracts           │
│  • System verifies via mutation testing, not human eyes         │
│  • Artifacts are central; code is just means to produce them    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# 3. Output-Driven Development in Context

## 3.1 Why ODD Is Not an Incremental Improvement

At first glance, Output-Driven Development (ODD) may appear to be an incremental refinement of existing software engineering practices.
However, such an interpretation fundamentally misunderstands its intent.

ODD does not optimize *how* software is produced.
It redefines *what* constitutes the object of engineering control.

This section situates ODD relative to established paradigms and clarifies why ODD cannot be reduced to, or subsumed by, any of them.

## 3.2 ODD vs. Agile and DevOps

Agile and DevOps emphasize:

* rapid iteration,
* continuous feedback,
* close alignment between development and deployment.

These methodologies assume that:

* code changes are traceable to human decisions,
* system behavior evolves incrementally,
* responsibility can be inferred from process participation.

ODD differs in a fundamental way.

| Dimension            | Agile / DevOps        | ODD                     |
| -------------------- | --------------------- | ----------------------- |
| Primary control unit | Code & process        | Output artifact         |
| Change cost          | Managed incrementally | Often regenerated       |
| Responsibility       | Distributed by role   | Anchored by arbitration |
| Assumption           | Human-authored code   | AI-generated artifacts  |

ODD is compatible with Agile delivery pipelines, but **orthogonal to their control assumptions**.

## 3.3 ODD vs. Test-Driven Development (TDD)

Test-Driven Development enforces correctness by:

* writing tests before implementation,
* treating tests as executable specifications.

While TDD elevates tests, it remains fundamentally **code-centric**:

* tests validate implementations,
* test coverage approximates behavioral confidence,
* responsibility is mediated through test authorship.

In contrast, ODD:

* specifies *acceptable output spaces* via contracts,
* evaluates artifacts directly,
* uses tests, mutation analysis, and adversarial validation as supporting mechanisms—not as the primary specification.

| Aspect                 | TDD                     | ODD                        |
| ---------------------- | ----------------------- | -------------------------- |
| Specification form     | Tests                   | Contracts over artifacts   |
| Verification target    | Implementation behavior | Output validity            |
| Failure interpretation | Test fails              | Artifact violates contract |

Thus, ODD does not replace TDD, but **repositions it as a subordinate verification layer**.

## 3.4 ODD vs. Model-Driven Engineering (MDE)

Model-Driven Engineering promotes:

* abstract models as primary artifacts,
* code generation from models,
* consistency between model and implementation.

Despite superficial similarity, ODD diverges in two critical aspects:

1. **Epistemic status**
   MDE models are intended to *represent* system structure.
   ODD contracts define *acceptable outcomes* without claiming representational completeness.

2. **Responsibility locus**
   In MDE, correctness flows from model fidelity.
   In ODD, correctness flows from artifact validation and arbitration.

| Dimension           | MDE                   | ODD                |
| ------------------- | --------------------- | ------------------ |
| Primary abstraction | Structural model      | Output contract    |
| Failure mode        | Model-code divergence | Artifact violation |
| Human role          | Model author          | Contract arbiter   |

ODD explicitly avoids treating contracts as full system models.

## 3.5 ODD vs. Prompt Engineering and LLM-Oriented Practices

Recent AI-assisted workflows emphasize:

* prompt engineering,
* chain-of-thought control,
* fine-tuning or retrieval augmentation.

These approaches focus on **shaping generation behavior**.

ODD deliberately decouples itself from generation mechanisms:

> In ODD, the quality of an artifact must be defensible regardless of how it was generated.

This design choice has two consequences:

1. ODD remains model-agnostic.
2. Responsibility is not diluted by generation complexity.

Prompt engineering may improve outputs, but it cannot substitute for **artifact-level accountability**.

## 3.6 ODD vs. Human-in-the-Loop (HITL) Systems

Human-in-the-loop systems emphasize:

* frequent human intervention,
* oversight during generation,
* interactive correction.

ODD reframes this relationship.

| Dimension            | HITL          | ODD                      |
| -------------------- | ------------- | ------------------------ |
| Human involvement    | Continuous    | Conditional              |
| Intervention trigger | Process stage | Irreducible disagreement |
| Cognitive load       | High          | Concentrated             |

ODD is not "human-out-of-the-loop".
It is **human-at-the-decision-point**.

## 3.7 Summary: Orthogonality, Not Replacement

ODD does not seek to replace existing methodologies.
Instead, it introduces a **new axis of control** orthogonal to code-centric practices.

> Existing methods optimize production.
> ODD governs legitimacy.

This distinction explains why ODD becomes increasingly relevant as AI systems scale, implementations become transient, and responsibility must remain explicit.

## 3.8 Transition to Section 4

Having situated ODD relative to existing paradigms, the next section examines the **implications of an artifact-centric control model** for:

* verification strategies,
* responsibility allocation,
* and governance in AI-native software systems.

---

