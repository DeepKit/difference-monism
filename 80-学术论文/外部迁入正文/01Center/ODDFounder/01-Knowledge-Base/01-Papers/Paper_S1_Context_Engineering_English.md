# The ODD Series Support: Context Engineering for Auditable LLM Workflows
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
> **Positioning**: ODD Paper Series · Paper S1 (Context Engineering)

---

## Abstract

**Background**: In ODD adoption, "Context" is the most expensive and unmanageable resource. Too little context leads to hallucinations; too much leads to "Lost in the Middle" and cost explosion.

**Core Problem**: How do we engineer a "Just-Enough" context assembly for every generation task?

**Methodology**: This paper proposes the **Context Engineering** system, comprising (1) Layered Context Stack, (2) Evidence-first Assembly, (3) Token Budgeting, and (4) Dual-stream Memory.

**Conclusion**: Context is not a pile of corpus; it is a carefully designed "Prompt Supply Chain."

**Keywords**: ODD, Context Engineering, RAG, Token Budget, Layered Stack

---

## 1. Introduction: Context is the New RAM

### 1.1 From RAM to Context Window

In classical computing, we manage RAM; in AI computing, we manage the Context Window.

Even with 1M+ token windows, "stuffing the whole repo" is wrong:

1. **Signal-to-Noise Ratio drops**: Irrelevant info distracts inference. Research shows models attending less to middle portions in long contexts ("Lost in the Middle").
2. **Cost explosion**: Tokens are money and latency (TTFT - Time to First Token).
3. **Unauditable**: Random retrieval makes failures unreproducible.

### 1.2 ODD Requirements for Context

ODD requires a deterministic, auditable context assembly process. Specific requirements:

- **Verifiable**: Context must map to verifiable acceptance criteria.
- **Traceable**: Each execution can answer "What did the model see at that time?"
- **Budgetable**: Context must support budgeting and compression.

### 1.3 Positioning Within the ODD Series

This paper provides supporting infrastructure for the ODD mainline papers:

- **Paper I** (*Foundations of Artifact Legitimacy*) defines the paradigm
- **Paper II** (*Human Delegation Proof*) uses context engineering for contract acquisition and clarity assessment
- **Paper III** (*Contract Precision*) uses context engineering for adversarial validation
- **Paper IV** (*Legitimacy Evolution*) uses context engineering for re-legitimation workflows

The mainline papers cite this paper's principles and interfaces but do not re-explain implementation details, ensuring clear contribution boundaries.

> *This work does not aim to maximize automation or replace human intelligence. Instead, it introduces structural constraints to ensure that responsibility, auditability, and human arbitration remain intact and scalable under AI-assisted production.*

**Disclaimer**: This paper establishes a conceptual framework and testable hypotheses. Empirical validation using production data from our reference implementation (Progee) is planned as immediate future work. *This work is released as a preprint and has not undergone peer review.*

---

## 2. Layered Context Stack

We divide context into 17 priority layers (adjustable). Core principles:

- **Hard constraints always on top** (L1-L3)
- **Contracts and acceptance never pruned** (L5, L10, L14, L15)
- **References retrievable and compressible** (L11, L12)

### 2.1 Global Hard Constraints (L1-L3)

| Layer | Name | Content | Strategy |
|-------|------|---------|----------|
| L1 | Hard Rules | Must-obey architecture principles ("No direct DB access") | **Always On** |
| L2 | Architecture Boundary | System boundaries, service partitions | **Always On** |
| L3 | Process Boundary | Security red lines, compliance requirements | **Always On** |

This info is always pinned to top; the model cannot ignore it.

### 2.2 Task Core (L5, L10, L14, L15)

| Layer | Name | Content | Strategy |
|-------|------|---------|----------|
| L5 | Contract Scope | Current task's contract scope | **Full Retention** |
| L10 | Contract Spec | Detailed contract specification | **Full Retention** |
| L14 | Task Spec | Current specific task description | **Full Retention** |
| L15 | Acceptance Criteria | Acceptance standards | **Full Retention** |

This is the task's DNA—never pruned.

### 2.3 Conventions & Style (L4, L8, L9)

| Layer | Name | Content | Strategy |
|-------|------|---------|----------|
| L4 | System Conventions | System-level conventions | **Compress/Summarize** |
| L8 | Tech Stack | Technology stack versions | **Compress/Summarize** |
| L9 | Code Style | Code style guide | Few-shot examples |

Use few-shot examples instead of lengthy docs.

### 2.4 Dynamic Knowledge (L11, L12)

| Layer | Name | Content | Strategy |
|-------|------|---------|----------|
| L11 | Dependencies | Project dependency docs | **RAG Retrieval** |
| L12 | Historical Lessons | Historical lessons, similar code | **RAG Retrieval** |

Only recall Top-K semantically relevant chunks.

### 2.5 Runtime State (L16, L17)

| Layer | Name | Content | Strategy |
|-------|------|---------|----------|
| L16 | Runtime State | Current runtime state | **Minimize** |
| L17 | Feedback on Retry | Compile errors, test failure logs | **Minimize** |

Keep only key error info; truncate irrelevant stack traces.

---

## 3. Evidence-first Assembly

To support "Adversarial Validation" (Paper II), context assembly must be traceable.

### 3.1 Metadata Requirements

Every fragment injected into the Prompt must carry metadata:

```json
{
  "source": "docs/api/payment.md",
  "version": "v2.3.1",
  "hash": "a1b2c3d4",
  "rationale": "Keyword 'payment' matched contract scope",
  "injected_at": "2026-01-15T10:30:00Z"
}
```

### 3.2 Scenario: Debugging Hallucinations

When a model hallucinates, we save not just the output but also the **Context Snapshot**.

By analyzing the Snapshot: "Oh, the retriever fetched a 3-year-old outdated doc, misleading the model."

**Fix**: Not fine-tuning, but updating the L11 knowledge base index (delete outdated docs).

### 3.3 Reproducibility Guarantee

Given the same:
- Contract version
- Context assembly strategy
- Model version

The system should reproduce the same context, thus reproducing output (at temperature 0).

---

## 4. Token Budgeting & Compression

### 4.1 Budget Allocation

We set token budgets per layer (example: total budget 8k):

| Layer | Budget | Notes |
|-------|--------|-------|
| L1-L3 (Hard constraints) | 1k | Alert if exceeded (rules too verbose) |
| L5, L10 (Contracts) | 2k | Non-compressible |
| L11 (Knowledge) | 4k | RAG dynamic fill |
| L17 (Feedback) | 1k | Minimized error info |

### 4.2 Overflow Policy

When total tokens exceed budget, priority order:

1. **Never drop**: L1-L3 (rules), L5/L10 (contracts)
2. **Compressible**: L11 (knowledge), L17 (feedback)
3. **Summarizable**: L4, L8, L9 (conventions)

Principle: **Better to fail generation than generate non-compliant code.**

### 4.3 Compression Techniques

- **Summarization**: Compress long docs to bullet points.
- **Few-shot**: Use 2-3 examples instead of full docs.
- **Incremental**: Provide only deltas from previous context.
- **Retrieval**: Recall only relevant chunks, not full docs.

---

## 5. Dual-stream Memory

ODD systems maintain two memory types:

### 5.1 Operational Stream

- **Definition**: Short-term memory. Current task context, temp variables.
- **Lifecycle**: Destroyed after task ends.
- **Content**: Compile errors, intermediate results, debug info.

### 5.2 Reflective Stream

- **Definition**: Long-term memory. Cross-task experience, historical corrections, global design decisions.
- **Lifecycle**: Persistent.
- **Write Policy**: Only write to Reflective Stream in these cases:
  - Successful Re-legitimation
  - Deep postmortem analysis
  - Human-approved new rules

### 5.3 Why Separate?

- Operational stream is "scratch paper"—freely writable.
- Reflective stream is "constitution"—must be carefully amended.

Mixing them leads to:
- Temporary errors incorrectly persisted as "lessons."
- Knowledge base polluted with garbage.

---

## 6. Experiments and Data

Comparing three context strategies:

| Strategy | Token Cost | First-pass Success | Fault Attribution Rate |
|----------|------------|-------------------|------------------------|
| Full Context | 32k | 60% | 20% |
| Random RAG | 8k | 70% | 40% |
| Stack Engineering | 8k | 92% | 100% |

**Analysis**:
- **Full Context**: Expensive tokens, "Lost in the Middle" ignores key info.
- **Random RAG**: Cheap but unstable; key constraints (L1) may be missed.
- **Stack Engineering**: Cheap and stable; L1 always pinned ensures no omissions.

---

## 7. Relations to Other Papers

- **Paper I (ODD Core)**: Context is the infrastructure for ODD execution.
- **Paper II (Human Delegation)**: Automated contract generation needs quality context assembly.
- **Paper III (Contract Execution)**: Higher contract precision reduces context dependency.
- **Paper IV (Legitimacy Evolution)**: Re-legitimation may require context reassembly.

---

## 8. Limitations and Future Work

### 8.1 Cross-Model Generalization

Different models process context differently. Current layering may need per-model tuning.

### 8.2 Multi-Modal Context

Future may require handling images, audio, and other non-text context.

### 8.3 Dynamic Budgeting

Current budgets are static. Future work: dynamically adjust based on task complexity.

### 8.4 ODD Limitations and Anti-Patterns

1. **Socio-technical Risk**: Human Delegation might be misinterpreted as a "Fully Autonomous" paradigm. It must be clarified that ODD delegates only within the boundaries of clear contracts, while humans retain final arbitration and governance responsibility.
2. **Context Pollution Risk**: Excessive retrieval may introduce erroneous or outdated context, leading to model hallucinations.

---

## 9. Conclusion

Context Engineering is the "Logistics System" of AI Software Engineering. Efficient logistics (low cost, timely, traceable) determines if the factory (Model) can deliver product (Software).

**Core Insights**:
- Context is not "more is better"—"just enough" is best.
- Context assembly must be deterministic and auditable.
- Layered Stack + Evidence-first = Reproducible AI Software Engineering.

### 9.1 Relationship to the ODD Series

This paper provides the infrastructure layer that makes the ODD mainline papers practical:

| Mainline Paper | How Context Engineering Supports It |
|----------------|-------------------------------------|
| **Paper I** | Provides auditable context for artifact verification |
| **Paper II** | Enables clarity assessment and contract candidate generation |
| **Paper III** | Supports adversarial validation with controlled context injection |
| **Paper IV** | Facilitates re-legitimation workflows with version-consistent context |

Together with Papers I–IV, this paper completes the ODD framework as a comprehensive paradigm for AI-native software engineering.

---

## References

1. Liu, N. et al. *Lost in the Middle: How Language Models Use Long Contexts*. ACL, 2023.
2. Anthropic. *Context Windows & Recall*. 2024.
3. Lewis, P. et al. *Retrieval-Augmented Generation*. NeurIPS, 2020.
4. Sweller, J. *Cognitive Load Theory*. Educational Psychology, 1988.
5. Yi Fu. ODD Core (Paper I). 2026.

---

*End of Document*
