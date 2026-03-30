---
title: "ASTO.U01. Figure Index: Panoramic Visual Index"
date: "2026-03-20"
version: "Γ.2"
author: "Yi Fu (付毅, ODDFounder, fuyi.it@live.cn)"
status: "Generated Reference Index"
layer: "ASTO"
abstract: "A collection of all core diagrams in the ASTO system as a panoramic visual index."
---

# **ASTO.U01. Figure Index: Panoramic Visual Index**

> **Version**: Γ.2 (Index Synced)
> **Status**: Generated Reference Index
> **Context**: This document collects all core diagrams in the Attribute-Set Transition Ontology (ASTO) system as a panoramic visual index.

---

## **Fig 01: Entry Path and Triple Filters**
*   **Source**: `ASTO.P02.Prologue` / `ASTO.P04.Manifesto`
*   **Description**: Describes the cognitive calibration process from "Reading Now" to "Entering the Field".

```mermaid
graph TD
    R["Reading Now"] --> A{"Core Judgment"}
    A --"Seeking Fixed Answer"--> X["Please Leave"]
    A --"Seeking Descriptive Language"--> Y["Accept Three Premises"]
    
    Y --> P1["I. Perspective is Blind Spot"]
    Y --> P2["II. Norm is Touch"]
    Y --> P3["III. Tool is Colonization"]
    
    P1 & P2 & P3 --> CORE["Attribute-Set Transition Ontology"]
    
    CORE --> S1["Statement 1: Existence is Attribute-Set"]
    CORE --> S2["Statement 2: Structure is Skeleton"]
    CORE --> S3["Statement 3: Transition is Destiny"]
    
    S1 --> D1["Freezing of Attribute Probability Cloud"]
    S2 --> D2["Duality of Support and Cage"]
    S3 --> D3["Thermodynamics of Alienation and Phase Change"]
    
    D1 & D2 & D3 --> LOOP["Existence-Structure-Transition Loop"]
    LOOP -.-> CORE
    
    classDef entry fill:#fffde7,stroke:#f57f17
    classDef warning fill:#ffebee,stroke:#c62828
    classDef premise fill:#e3f2fd,stroke:#1565c0
    classDef core fill:#e8f5e9,stroke:#2e7d32
    classDef statement fill:#f3e5f5,stroke:#4a148c
    classDef detail fill:#fff3e0,stroke:#ef6c00
    class R entry; class X warning; class P1,P2,P3 premise
    class CORE core; class S1,S2,S3 statement; class D1,D2,D3 detail
```

---

## **Fig 02: ASTO Core Dynamics Loop**
*   **Source**: `ASTO.P04.Manifesto`
*   **Description**: Shows how a system births order from chaos, alienates due to environmental transition, and finally moves towards collapse or transition.

```mermaid
graph TD
    Chaos[Chaos] --Attribute Random Collision--> Order(Order / Birth of Structure)
    Order --Env Transition causes Discomfort--> Alienation{Alienation}
    
    Alienation --Structure Suppression--> Cage[Fossilization/Cage]
    Alienation --Motility Intervention--> Transition[Transition]
    
    Cage --> Collapse[Collapse]
    Transition --> Order
    Collapse --> Chaos
    
    style Alienation fill:#fffde7,stroke:#f57f17,stroke-width:2px
    style Transition fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Cage fill:#ffebee,stroke:#c62828
```

---

## **Fig 03: System Thermodynamics Logic Flow**
*   **Source**: `ASTO.P05.Axioms`
*   **Description**: Shows how the six axioms connect the lifecycle of a system.

```mermaid
graph TD
    %% Core Flow
    Chaos[Rule 0: Env Full of Noise] -->|Against| Arch[Rule 1: Architecture is Low-Entropy Island]
    Arch -->|Layered Governance| Layer[Rule 2: Attribute Layering & Dependency]
    Layer -->|Path Guiding| Path[Rule 3: Path of Least Resistance]
    
    %% Motility Intervention
    Motility[Rule 4: Motility/Control Plane] -->|Construct Field| Path
    
    %% System Destiny
    Path -->|Form| System[Current Stable System]
    System -->|Endogenous Conflict/Env Change| Debt[Rule 5: Attribute-Set Mode Self-Reference/Tech Debt]
    Debt -->|Refactor or Die| Transition{Rule 6: Transition or Collapse}
    
    Transition -- Transition --> Arch
    Transition -- Collapse --> Chaos
    
    classDef chaos fill:#ffebee,stroke:#c62828
    classDef arch fill:#e8f5e9,stroke:#2e7d32
    classDef agent fill:#e3f2fd,stroke:#1565c0
    classDef debt fill:#fff3e0,stroke:#ef6c00
    
    class Chaos,Debt chaos
    class Arch,Layer,Path,System arch
    class Motility agent
```

---

## **Fig 04: SDLC State Machine (Five States Flow)**
*   **Source**: `ASTO.P06.Values` (or P05 depending on version, cited as ASTO06.Ontology in original)
*   **Description**: Shows the transition path of code between five forms.

```mermaid
graph TD
    Code[Code State<br/>Code] -->|Compile/Deploy| Infra[Materialized State<br/>Infra]
    Infra -->|Entropy| Legacy[In-itself State<br/>Legacy]
    Legacy -->|Incident| RFC[Consensus State<br/>RFC]
    RFC -->|Refactor| Conscious[Oriented State<br/>Refactoring]
    Conscious -->|Commit| Code
    
    classDef state fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    class Code,Infra,Legacy,RFC,Conscious state
```

---

## **Fig 05: Semantic Loss**
*   **Source**: `ASTO.E03.Web3`
*   **Description**: Shows how human intent loses NEN attributes during compilation.

```mermaid
graph LR
    Intent[Human Intent - NEN: No Unjust Enrichment] -->|Compiler<br/>Semantic Loss| Code[EVM Execution - EN: balance -= amount]
    
    subgraph Gap [Normative Media Mismatch]
        Intent -.->|Lack Constraint| Code
    end
    
    style Intent fill:#e1f5fe
    style Code fill:#ffebee
```

---

## **Fig 06: Five-State Layered Governance Architecture**
*   **Source**: `ASTO.E03.Web3` / `ASTO.E04.AI`
*   **Description**: Shows how NEN layer, EN layer, and App layer collaborate.

```mermaid
graph TD
    subgraph NEN [NEN Layer / Conscious Phase]
        Parliament[Human Parliament / DAO]
        Const[Constitution / Invariants]
    end
    
    subgraph EN [EN Layer / Existence Phase]
        Verifier[Runtime Verifier / RLEN Core]
        Contract[Smart Contract / Model]
    end
    
    subgraph App [App Layer / Consensus Phase]
        User[User Interaction]
        Feedback[Real-time Feedback]
    end
    
    Parliament -->|Enact| Const
    Const -->|Inject| Verifier
    Verifier -->|Intercept Unconstitutional| Contract
    Contract -->|Serve| User
    User -->|Feedback| Feedback
    Feedback -.->|Correction Signal| Parliament
    
    style NEN fill:#e3f2fd
    style EN fill:#e8f5e9
    style App fill:#fff3e0
```

---

## **Fig 07: Historical Coordinate System**
*   **Source**: `ASTO.P02.Prologue (Appendix)` / `ASTO.P12.Trace`
*   **Description**: Shows ASTO's inheritance and fusion of Eastern and Western thoughts.

```mermaid
graph TD
    subgraph Pre-Modern
        A[Eastern Wisdom<br/>Holism/Intuition] 
    end
    
    subgraph Modern
        B[Western Philosophy<br/>Hegel/Marx<br/>Speculation/Revolution]
        C[Modern Science<br/>Darwin/Systems Theory<br/>Positivism/Structure]
    end
    
    subgraph Digital Age
        D[ASTO Attribute-Set Transition Ontology]
    end
    
    A -->|Holism/Homeostasis| D
    B -->|Dialectics/Praxis| D
    C -->|Evolution/System/Information| D
    
    D --> E[Thinking Ground of Intelligent Age<br/>Philosophy+Science+Engineering]
    
    style D fill:#e1f5fe,stroke:#01579b,stroke-width:2px
```

---

## **Fig 08: Dialogue Platform Three-Layer Architecture**
*   **Source**: `ASTO.P10.Democracy`
*   **Description**: Shows how to transform speech into structural transition.

```mermaid
graph TD
    Input[Natural Language Input] --> Layer1[Structured Expression Layer - Proposal Template]
    Layer1 --> Layer2[Conflict Manifestation Layer - Diff View]
    Layer2 --> Layer3[Transition Trigger Layer - CI/CD Pipeline]
    Layer3 --> Output[System State Update]
    
    style Layer1 fill:#e1f5fe
    style Layer2 fill:#fff9c4
    style Layer3 fill:#ffccbc
```

---

## **Fig 09: Normative Executability Gradient (NEG)**
*   **Source**: `ASTO.E02.Automation`
*   **Description**: Shows automation grading from L1 to L4.

```mermaid
graph TD
    L1[L1: Deterministic Automation - Green Light] -->|Handle 90%| Done[Done]
    L1 -->|Exception/Threshold| L2[L2: Adaptive Automation - Green Light]
    L2 -->|Low Confidence| L3[L3: Human-Machine Synergy - Yellow Light]
    L3 -->|Involves Ethics/Ultimate Values| L4[L4: Manual Only - Red Light]
    
    style L1 fill:#c8e6c9
    style L2 fill:#dcedc8
    style L3 fill:#fff9c4
    style L4 fill:#ffcdd2
```

---

## **Fig 10: ASTO Civilization Panorama**
*   **Source**: `ASTO.P04.Manifesto`
*   **Description**: Shows the symbiotic civilization landscape ASTO pursues: "Antifragile, Non-Zero-Sum, Motility Maximization".

```mermaid
graph TB
    subgraph Civilization [ASTO Civilization Meta-Definition]
        direction TB
        
        Goal((Antifragile Ecology))
        
        subgraph Pillars [Three Pillars]
            P1[Structure as Support]
            P2[Tech as Extension]
            P3[Transition as Evolution]
        end
        
        subgraph Actors [Sources of Motility]
            Human(Carbon-based Individual)
            AI(Silicon-based Partner)
        end
        
        Goal --- P1 & P2 & P3
        P1 & P2 & P3 --> Actors
        
        Actors -- Create/Perturb --> Network{Non-Zero-Sum Symbiotic Network}
        Network -- Feedback/Nourish --> Goal
    end
    
    style Goal fill:#fff9c4,stroke:#fbc02d,stroke-width:4px
    style Human fill:#e1f5fe
    style AI fill:#e8f5e9
    style Network fill:#f3e5f5,stroke:#8e24aa
```

---

**(End of Figure Index)**
