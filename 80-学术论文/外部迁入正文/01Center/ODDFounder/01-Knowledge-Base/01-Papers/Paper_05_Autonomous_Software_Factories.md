# Paper V: Autonomous Software Factories
## Risk-Graded Architecture and Adversarial Protocols for AI-Native Engineering

**Abstract**

The rapid evolution of Large Language Models (LLMs) has shifted the bottleneck of software engineering from code generation to quality governance. While AI can produce code at scale, traditional verification methods—reliant on human review and static tests—fail to match this velocity, leading to a "Trust Gap." This paper introduces a reference architecture for **Autonomous Software Factories (ASF)**, designed to bridge this gap through two core mechanisms: the **Contract Adversarial Protocol (CAP)** and **Risk-Graded Autonomy**. By shifting human responsibility from "in-the-loop" supervision to "on-the-loop" governance (Governance-by-Exception), and by employing adversarial multi-agent systems to ensure contract rigidity, we propose a scalable paradigm for AI-native software production. We demonstrate these concepts through **Progee**, a reference implementation that embodies the "Tent-Staff-Workshop" architectural pattern.

---

## 1. Introduction: The Industrialization of Intelligence

### 1.1 The Narrative of Evolution: A Developer's Confession

*The following account reflects the real-world experience of the author during the development of Progee, an AI-native IDE.*

It started with a sense of liberation. When GPT-4 first appeared, I felt like I had acquired a superpower. Features that used to take days were completed in minutes. I was the pilot; AI was my hyper-competent navigator.

But as the codebase grew from a prototype to a complex system of 50,000 lines, the honeymoon ended. I found myself drowning in a sea of generated code. Every time I asked the AI to refactor a module, it would rewrite it in a slightly different style, sometimes introducing subtle regressions. I spent my days (and nights) not writing code, but *reviewing* it—squinting at diffs, hunting for hallucinations, and patching logic errors.

I realized I had become a bottleneck. I was no longer a creator; I was a glorified spell-checker for a machine that could type faster than I could think.

The epiphany came late one night while debugging a complex state management module. I thought: *"Why am I obsessed with these lines of code? I don't care how the state is stored; I only care that when Event A happens, State B is updated, and the UI reflects C."*

I realized that to scale software production in the AI era, we must stop treating code as an **asset**. Code is a **liability**—it costs money to read, store, and debug. The only things that matter are the **Intent** (what I want) and the **Artifact** (the verified result).

This was the birth of **Output-Driven Development (ODD)**. It was not an invention of theory, but a survival strategy for the trenches.

### 1.2 The Core Conflict: Abundance vs. Scarcity

The fundamental contradiction of AI-assisted engineering is the mismatch between **abundant intelligence** and **scarce human attention**.

*   **Supply Side**: AI can generate infinite variations of implementation instantly.
*   **Demand Side**: Human cognitive bandwidth for review is linear and limited.

This creates a dual crisis:
1.  **For Developers**: "Review Fatigue" leads to rubber-stamping bad code, introducing subtle bugs that manifest only in production.
2.  **For Enterprises**: The promise of "AI Speed" is negated by the "Quality Bottleneck." Paradoxically, adding more AI coding assistants often *slows down* shipping because the team is paralyzed by the volume of unverified code.

Traditional software engineering methodologies—Agile, Code Review, CI/CD—are predicated on the assumption that code is expensive to write and therefore carefully crafted by humans. In this model, "Review" is a viable quality gate. In the AI era, this gate collapses. We need a new control surface—one that guarantees **Business Velocity** without sacrificing **Operational Risk**.

### 1.3 The ODD Proposition: The Intelligent Pharma Factory

Output-Driven Development (ODD) proposes a radical shift: **Control the Artifact, not the Code.**

Instead of supervising the *process* of coding (the "How"), humans should define the *boundary conditions* of the result (the "What"). This leads to the concept of the **Autonomous Software Factory**, which can be best understood through the metaphor of an **Intelligent Pharmaceutical Factory**:

*   **The Pharmacologist (Human)**: Designs the "Molecule Formula" (Contract) and sets the "QC Standards" (Acceptance Criteria). They do not mix the chemicals themselves.
*   **The Synthesizer (AI)**: A high-speed reactor that attempts to synthesize the compound (Code) according to the formula. It operates in a black box.
*   **The QC Line (System)**: An automated, ruthless verification pipeline. Every batch is tested for purity (Lint/Compile), toxicity (Security), and efficacy (Tests). Only batches that pass 100% of checks are released.
*   **The Approved Drug (Sealed Artifact)**: The final, trusted output. It is safe to use not because we trust the synthesizer, but because we trust the QC process (GMP).

In this paper, we formalize the architecture of such a factory. We move beyond the high-level philosophy of Paper I to the concrete mechanisms that make autonomy safe: **Adversarial Protocols** for contract generation and **Risk-Graded Loops** for execution.

---

## 2. Reference Architecture: The Tent, The Staff, The Workshop

To operationalize ODD, we propose a three-layer reference architecture inspired by military command structures. This separation of concerns ensures that decision-making, governance, and execution are decoupled and scalable.

### 2.1 High-Level View

#### Layer 1: The Tent (The Decision Layer)
*   **Role**: Intent Definition & Strategy.
*   **Metaphor**: The command tent where generals and strategists debate the plan before battle.
*   **Components**:
    *   **The Commander (Human/Agent)**: Owns the high-level intent and value judgment. The Commander is responsible for the "Why" and the ultimate "Yes/No" on high-risk decisions.
    *   **The 5-Role Consensus Model**: A multi-agent debate chamber designed to simulate a diverse engineering team. It ensures that the intent is vetted from all angles before it even reaches the contract stage.
        *   **Pangu (Architect)**: Focuses on system structure, scalability, and technical debt.
        *   **Ling'er (Product Manager)**: Focuses on user value, experience, and business goals.
        *   **Luban (Builder)**: Focuses on feasibility and implementation details.
        *   **Li Bing (QA)**: Focuses on testability, edge cases, and quality assurance.
        *   **Xian'er (Security)**: Focuses on threat modeling, vulnerabilities, and compliance.
*   **Output**: A finalized, unambiguous **Intent Narrative** (specifically, the 4D Narrative Model) that serves as the input for the Staff layer.

#### Layer 2: The Staff (The Governance Layer)
*   **Role**: Management, Risk Assessment & Dispatch.
*   **Metaphor**: The headquarters staff that translates strategy into specific orders and logistics.
*   **Components**:
    *   **Contract Manager**: Maintains the lifecycle of contracts (Draft -> Validated -> Active -> Sealed). It ensures that every active contract is versioned and traceable.
    *   **Risk Assessor**: Automatically assigns a risk level (L1-L4) to each task based on impact analysis (e.g., database writes, auth changes) and historical data. This determines the rigorousness of the verification loop.
    *   **Dispatcher**: Routes tasks to appropriate workshops. It manages the queue, prioritizes critical tasks, and handles resource allocation (e.g., assigning more GPU budget to L4 tasks).
*   **Output**: Formalized **Contracts** (JSON schemas with input/output/behavior definitions) and **Work Orders**.

#### Layer 3: The Workshop (The Execution Layer)
*   **Role**: Implementation & Verification.
*   **Metaphor**: The factory floor where goods are produced. It is an isolated, ephemeral environment.
*   **Components**:
    *   **Builder Agents**: LLM-based agents tasked with generating code and artifacts that satisfy the contract.
    *   **Breaker Agents**: Adversarial agents whose sole purpose is to "break" the builder's output by generating edge-case inputs, fuzzing attacks, and regression tests.
    *   **Adversarial Evaluator**: The referee of the workshop. It runs the Builder's code against the Breaker's tests. If the code fails, it triggers a **Rework Loop**. If it passes, it triggers **Mutation Testing** to ensure the tests themselves are valid.
*   **Output**: Verified **Sealed Artifacts** (Artifact + Evidence + Signature). The "Seal" is a cryptographic proof that the artifact passed the specific verification pipeline defined by its risk level.

### 2.2 The Flow of Legitimacy

In this architecture, legitimacy flows downwards, while evidence flows upwards.

1.  **Intent** originates in The Tent.
2.  It is formalized into a **Contract** by The Staff.
3.  The Contract is executed in The Workshop to produce an **Artifact**.
4.  The Workshop returns a **Seal** (cryptographic proof of verification).
5.  The Staff archives the Seal, and The Tent marks the intent as satisfied.

This closed loop allows the human to remain at the "Intent" level, dipping into the lower layers only when the system flags an exception (e.g., a risk level too high for autonomy).

---

## 3. Mechanism I: Contract Adversarial Protocol (CAP)

A critical failure mode in AI development is "Garbage In, Garbage Out." If the human intent is ambiguous, the AI will happily generate code that is *technically* correct but *functionally* useless or dangerous.

To solve this, we introduce the **Contract Adversarial Protocol (CAP)**.

### 3.1 The "Garbage In" Problem

Ambiguity is the enemy of automation. A request like "Make the login secure" is interpreted differently by every model.
*   Model A might add a password complexity check.
*   Model B might implement 2FA.
*   Model C might simply hash the password (but use a weak algorithm).

Without a rigid spec, the "correctness" of the implementation is a matter of luck.

### 3.2 The Protocol: Debate to Consensus

CAP formalizes the contract generation process as a **multi-turn game** designed to maximize contract robustness before a single line of code is written.

1.  **Drafting Phase**:
    *   The **Proposer** (playing the Builder role) generates a Draft Contract (V1) based on the human intent.
    *   *Prompt Strategy*: "Optimize for feasibility and clarity."

2.  **Attack Phase**:
    *   The **Challenger** (playing the Breaker/Security role) analyzes V1 for weaknesses.
    *   It generates an **Attack Report** covering:
        *   **Ambiguity**: "What is the timeout duration? Can the username be emojis?"
        *   **Logic Gaps**: "If the token expires during a transaction, what happens to the database state?"
        *   **Malicious Compliance**: "I can satisfy this contract by returning a hardcoded 'Success' without checking the DB."
        *   **Security Risks**: "No rate limiting specified on the login endpoint."

3.  **Refinement Phase**:
    *   The Proposer receives the Attack Report and must produce V2.
    *   It must either **fix the ambiguity** (e.g., adding `timeout: 5000ms`) or **justify the design**.

*(Note: The Challenger's attack strategies are initialized from a static "Threat Library" and "Historical Incident Database" to ensure it doesn't invent unrealistic attacks.)*

4.  **Arbitration Phase**:
    *   The **Arbiter** evaluates the convergence. If the Challenger finds no new major vulnerabilities, the contract is marked as **Validated**. If high-risk issues persist after 3 rounds, it escalates to the Human Commander.

### 3.3 The 4D Narrative Bridge

To fuel this protocol, we define a standard input format called the **4D Narrative Model**, which captures the intent in four dimensions to minimize initial hallucination:

1.  **User Story (The Value)**: The "Happy Path" value proposition. (*"As a user, I want to log in so that I can access my dashboard."*)
2.  **Happy Path (The Expected)**: The detailed sequence of events when everything goes right. (*"User enters valid creds -> System validates hash -> System issues JWT -> User redirected."*)
3.  **Edge Cases (The Robustness)**: The known unknowns and environmental failures. (*"Network timeout, Database locked, Invalid UTF-8 input, Clock skew."*)
4.  **Threat Scenarios (The Defense)**: The adversarial perspective. (*"An attacker tries to brute-force; An attacker replays an old token; SQL injection attempt."*)

This narrative serves as the seed for the Proposer and the ammunition for the Challenger. By forcing the human (or the Tent agents) to articulate these 4 dimensions, we drastically reduce the search space for the contract generation.

---

## 4. Mechanism II: Risk-Graded Autonomous Loops

Not all code is equal. A UI color change does not require the same scrutiny as a payment gateway. Treating them the same leads to either **inefficiency** (over-testing) or **catastrophe** (under-testing).

We introduce a **Risk-Graded Governance Model (L1-L4)** that dynamically adjusts the verification rigor.

### 4.1 The L1-L4 Governance Model

#### L1: Low Risk (The "Fast Track")
*   **Scope**: Internal tools, UI cosmetic tweaks, static content, non-critical data.
*   **Process**: Generate -> Static Analysis (Lint) -> Seal.
*   **Human Role**: **Post-hoc Notification**. The human is informed *after* the artifact is sealed.
*   **Philosophy**: "Move fast, fix later. The cost of failure is negligible."

#### L2: Medium Risk (The "Standard Track")
*   **Scope**: Standard business logic, CRUD operations, non-financial data processing.
*   **Process**: Generate -> Unit Test -> Integration Test -> **Mutation Testing (Default Score > 80%, Configurable)** -> Seal.
*   **Human Role**: **Asynchronous Review**. The human can intervene, but the process does not block on their approval.
*   **Philosophy**: "Trust but verify via math. If the tests are robust (proven by mutation), the code is likely correct."

#### L3: High Risk (The "Robust Track")
*   **Scope**: Core algorithms, data integrity, external integrations, privacy-sensitive features.
*   **Process**: CAP (1 round) -> Generate -> **Adversarial Testing (Fuzzing/Attacks)** -> Seal.
*   **Human Role**: **Gatekeeper**. The human must approve the Contract before execution starts.
*   **Philosophy**: "Assume the code is broken until proven otherwise by active attack."

#### L4: Critical Risk (The "Governance Track")
*   **Scope**: Authentication, Payments, Cryptography, Destructive Operations (e.g., bulk delete).
*   **Process**: CAP (3 rounds) -> **Multi-Agent Consensus (Cross-Review)** -> **Human Arbitrator Approval** -> Seal.
*   **Human Role**: **Mandatory Sign-off**. The human must approve the Contract AND the final Evidence package.
*   **Philosophy**: "Zero Trust. Automated verification is necessary but not sufficient. Human judgment is the final firewall."

### 4.2 Dynamic Workflow Orchestration

The factory is not a static pipeline; it is a **State Machine** that adapts to risk. The Staff layer runs a **Risk Assessor** agent that evaluates every incoming intent against three dimensions to assign an Lx level:

1.  **Impact Analysis**: Does this task touch the database schema? Does it call external APIs? Does it modify auth middleware?
2.  **Code Complexity**: Estimated cyclomatic complexity and lines of code.
3.  **Historical Failure Rate**: Have similar tasks (e.g., "OAuth integration") failed in the past?

Based on this assessment, the Dispatcher routes the task to the appropriate pipeline. For example, a request to "Update the logo color" (L1) skips the expensive CAP and adversarial testing, while "Implement Stripe payments" (L4) triggers the full governance protocol. This ensures that the factory runs efficiently without compromising safety on critical paths.

---

## 5. Mechanism III: Evolutionary Legitimacy

An Autonomous Software Factory is not static; it learns.

### 5.1 Sealed Contract Library (SCL): The Factory Memory

An Autonomous Software Factory is not static; it learns. Every successfully sealed artifact is stored in the **Sealed Contract Library (SCL)**. This is not just a version control system; it is a semantic knowledge base of "Verified Intent-to-Implementation Mappings."

*   **Semantic Retrieval**: When a new task arrives (e.g., "Create a user table"), the Staff first queries the SCL: *"Have we solved a similar problem before?"*
*   **Template Injection**: If a high-confidence match is found, the system retrieves the **Contract Template** (proven to be robust) and the **Verification Strategy** (known to catch bugs), skipping the expensive CAP drafting phase.
*   **Zero-Shot to Few-Shot**: Over time, the factory shifts from zero-shot generation (guessing) to few-shot replication (copying success), drastically reducing the error rate.

### 5.2 Intelligent Horse Racing: Survival of the Fittest

When a task fails (e.g., Builder cannot satisfy Breaker), the system triggers **Intelligent Horse Racing**:

1.  **Parallel Execution**: It spawns multiple parallel Builders with different strategies (e.g., Model A vs. Model B, Chain-of-Thought vs. Tree-of-Thought, Python vs. Go).
2.  **The Race**: All builders attempt to satisfy the same Sealed Contract.
3.  **The Winner**: The first Builder to pass all verification gates wins.
4.  **Feedback Loop**: The winning strategy is tagged in the SCL. If "Model B + Tree-of-Thought" consistently wins on algorithmic tasks, the Dispatcher will prioritize this configuration for future L3 tasks.

This allows the factory to self-heal and evolve its internal heuristics without human intervention, turning failure into optimization data.

---

## 6. Case Study: The Progee Implementation

We have implemented this architecture in **Progee**, an AI-native IDE designed to be the first "Factory-in-a-Box" for full-stack development.

### 6.1 System Overview
Progee serves as the reference implementation for ASF. It integrates:
*   **The Tent**: A chat-based interface where the user (Commander) converses with the 5-Role Consensus Model.
*   **The Staff**: A background daemon that manages the PostgreSQL-based contract ledger.
*   **The Workshop**: A Dockerized execution environment where Builder and Breaker agents operate in isolation.

Unlike traditional IDEs (VS Code) which manage *files*, Progee manages *state*. Code is treated as a structured artifact stored in the database.

**Artifact Schema Example (JSON)**:
```json
{
  "artifact_id": "art_login_v1",
  "contract_id": "ctr_login_v3",
  "status": "sealed",
  "content": {
    "source_code": "def login(user, pass): ...",
    "tests": "def test_login(): ...",
    "dependencies": ["jwt", "bcrypt"]
  },
  "evidence": {
    "mutation_score": 0.92,
    "adversarial_report": "passed_12_vectors",
    "signed_by": "workshop_agent_07"
  }
}
```

### 6.2 A Day in the Life: Implementing "Secure Login" (L3 Task)

To demonstrate the architecture in action, let's walk through a real-world scenario: Implementing a secure login module using JWT.

#### Phase 1: Intent Definition (The Tent)
*   **User**: "I need a login screen. It should be secure."
*   **Tent (Ling'er)**: "By 'secure', do you mean standard hashing + JWT, or do you need 2FA?"
*   **User**: "Standard JWT is fine for now."
*   **Tent (Xian'er)**: "Noted. I will add a requirement for rate limiting to prevent brute-force attacks."
*   **Output**: A **4D Narrative** defining the User Story ("Log in to access dashboard"), Happy Path ("Valid creds -> Token"), Edge Cases ("DB timeout"), and Threats ("Brute force").

#### Phase 2: Contract Negotiation (CAP)
*   **Proposer (Luban)**: Drafts Contract V1.
*   **Challenger (Li Bing)**: Attacks V1. *"Attack: The contract does not specify token expiration. I can generate a token that lasts forever."*
*   **Proposer**: Updates V1 -> V2. *"Fix: Added `token_expiry: 3600s` constraint."*
*   **Arbiter**: Approves V2. Contract moves to **Validated** state.

#### Phase 3: Risk Assessment & Dispatch (The Staff)
*   **Risk Assessor**: Analyzes V2. Keywords: `auth`, `password`, `security`.
*   **Verdict**: **L3 (High Risk)**.
*   **Dispatcher**: Allocates a high-performance Workshop and schedules **Adversarial Testing**.

#### Phase 4: Execution & Verification (The Workshop)
*   **Builder**: Generates the Python/Delphi implementation code.
*   **Breaker**: Generates a Fuzzing Suite based on the Threat Scenarios. It launches 10,000 requests to the login endpoint, testing for SQL injection and timing attacks.
*   **Adversarial Evaluator**:
    *   *Result*: Code passed functional tests but failed Rate Limiting (Breaker successfully flooded the endpoint).
    *   *Action*: Trigger **Rework Loop**. Builder is fed the failure logs and patches the code.
    *   *Retry*: Breaker attacks again. Rate limiting holds.
*   **Output**: Sealed Artifact.

#### Phase 5: Delivery
*   **User Notification**: *"Login module ready. Verified against 4 attack vectors (SQLi, XSS, Brute-force, Replay). Seal ID: `0x7f...a9`."*

### 6.3 Empirical Observations
In internal trials comparison against a standard "Copilot-style" workflow:
*   **Time-to-Start**: Increased by 40% (due to the Tent/CAP phase).
*   **Time-to-Fix**: Decreased by 80% (bugs caught in Workshop, not by human).
*   **First-Time Right**: The rate of artifacts passing acceptance without human intervention improved from 15% to 65%.
*   **Edge Case Coverage**: The CAP process identified an average of 3.5 missed edge cases per task that the human had originally overlooked.

---

## 7. Discussion: Open Challenges and Future Directions

While the ASF architecture provides a robust framework for AI-native engineering, several challenges remain.

### 7.1 The Convergence Problem: Can Adversaries Agree?
A core risk of CAP is infinite loops where the Challenger is too pedantic or the Builder is too stubborn.
*   **Mitigation**: We introduced a **"Grumpiness Decay"** parameter. In Round 1, the Challenger is strict. In Round 3, it relaxes minor stylistic constraints to focus only on critical logic errors.
*   **Deadlock Breaker**: If no consensus is reached after 3 rounds, the system flags the contract as **"Contested"** and escalates to the Human Commander for arbitration.

### 7.2 The Human Factor: Skill Shift
The shift to ODD requires a significant reskilling of the workforce.
*   **From Coding to Directing**: Developers must learn **"Prompt Architecture"** (how to structure intent) and **"Contract Auditing"** (how to verify specs).
*   **Loss of Muscle Memory**: Will developers lose the ability to debug low-level code if they never write it? This is a valid concern, similar to how pilots rely on autopilot. The solution may be **"Manual Mode Drills"** where humans periodically write code to stay sharp.

### 7.3 Invitation to Collaborate
We believe that the **Autonomous Software Factory** should not be a proprietary walled garden. We are open-sourcing the **Progee Protocol Specifications**, including:
*   The **4D Narrative Schema**.
*   The **CAP Interaction Rules**.
*   The **Sealed Artifact Data Format**.

We invite the community—researchers, tool builders, and enterprises—to collaborate on defining these standard interfaces. Together, we can build a software ecosystem that is not just faster, but fundamentally safer.

---

## 8. Conclusion

We are witnessing the industrialization of software engineering. The transition from "Hand-crafted Code" to "Factory-produced Artifacts" is as inevitable as the shift from cottage weaving to textile mills.

**Output-Driven Development (ODD)** provides the theoretical foundation for this shift, redefining software not as an asset to be maintained, but as an artifact to be verified. The **Autonomous Software Factory (ASF)** architecture translates this theory into practice, offering a blueprint for systems that can scale intelligence without scaling chaos.

By embracing **Adversarial Protocols** to purify intent and **Risk-Graded Autonomy** to balance speed with safety, we can build a future where AI is not just a copilot, but a trusted engine of creation.

The future of programming is not typing; it is directing. And the factory is open for business.
