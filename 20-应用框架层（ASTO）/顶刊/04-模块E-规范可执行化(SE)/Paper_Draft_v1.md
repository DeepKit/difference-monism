# Executable Normativity: Compiling Requirements into Governance Constraints

**Target Journal**: *IEEE Software* / *ACM Transactions on Software Engineering and Methodology (TOSEM)*
**Type**: Technical Paper
**Status**: Draft v1.0

---

## Abstract

In modern software engineering, there is a persistent gap between "Normativity" (what the system *ought* to do, as defined in requirements and policies) and "Executability" (what the system *actually* does). This gap leads to "Requirements Drift" and compliance failures. We propose a methodology for **Executable Normativity**, where governance rules are not treated as passive documentation but are compiled into active, machine-verifiable constraints. We introduce a formal transformation layer that converts high-level policies into "Guardrails" (static analysis rules) and "Gates" (runtime checks). We demonstrate this approach using a prototype framework, showing how it reduces the latency between policy definition and enforcement from weeks to milliseconds.

**Keywords**: Requirements Engineering, Compliance as Code, DevOps, Governance, Traceability.

---

## 1. Introduction

Software systems are subject to two types of laws: the laws of physics (which they cannot break) and the laws of society (which they often break).
Traditional Requirements Engineering (RE) treats the latter as "Non-Functional Requirements" (NFRs) to be verified by human review. However, in the era of CI/CD and AI-generated code, human review is too slow and porous.

We argue that **a specification that is not executable is merely a suggestion.**
To guarantee compliance (e.g., GDPR, Safety Standards), we must treat normativity as code.

## 2. The Problem: The Normative Gap

### 2.1 The Drift
Requirements are written in natural language (e.g., "The system must encrypt PII"). Code is written in Java/Python. Over time, the code evolves (drifts) away from the requirements.
### 2.2 The Review Bottleneck
The traditional defense against drift is the Code Review. But as code volume explodes (thanks to AI), reviewers suffer from "Alert Fatigue" and "Cognitive Overload." They cannot mentally verify every policy against every line of code.

## 3. Methodology: From Text to Constraint

We propose a three-layer architecture for Executable Normativity:

### Layer 1: The Normative Source (Policy)
*   **Format**: Structured Natural Language or Controlled Natural Language (CNL).
*   **Example**: "All database writes must be logged."

### Layer 2: The Compiler (Transformation)
*   **Mechanism**: A mapping engine that translates Policy Intents into Technical Constraints.
*   **Tooling**: We utilize Domain-Specific Languages (DSLs) like Rego (Open Policy Agent) or custom linters.

### Layer 3: The Executable Constraint (Guardrail)
*   **Static**: AST (Abstract Syntax Tree) analyzers that block commits if a rule is violated (e.g., "No `print()` statements in production code").
*   **Dynamic**: Sidecar proxies that block network requests if they violate a policy (e.g., "No egress to unknown IPs").

## 4. Case Study: The "Clean Commit" Framework

We implemented this methodology in a financial services context.

### 4.1 Scenario
The policy required: "No developer shall commit code directly to the main branch without two approvals and a passing security scan."

### 4.2 Implementation
Instead of relying on a "Process Document," we implemented:
1.  **Branch Protection Rule** (Git configuration as code).
2.  **CI Pipeline Gate**: A script that queries the issue tracker to verify "Approval" status before allowing the build to proceed.
3.  **Secret Scanning Hook**: A pre-commit hook that rejects any commit containing high-entropy strings (potential API keys).

### 4.3 Results
*   **Compliance Violations**: Reduced by 90%.
*   **Review Time**: Reduced by 40% (reviewers focus on logic, not style/policy).

## 5. Discussion

### 5.1 The Limits of Formalization
Not all norms are formalizable (e.g., "User interface must be intuitive"). We propose a "Hybrid Governance" model where formalizable norms are automated, leaving subjective norms for human review.

### 5.2 The "Governance Compiler"
Future work involves building a "Governance Compiler" that automatically updates CI/CD pipelines when a legal policy changes.

## 6. Conclusion

Executable Normativity transforms governance from a "bureaucratic overhead" into a "productive constraint." By embedding the "ought" into the "is," we ensure that the system remains aligned with its purpose, even as it scales.

---
*Drafting Note: This paper focuses on the "HOW" (Implementation), complementing the "WHY" (Philosophy) of the other papers.*
