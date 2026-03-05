# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## 1. Project Overview
This repository (`D:\_Progs\01Center\ASTO\小说故事`) hosts the **ASTO Eight Books (ASTO 八部曲)**, a monumental science fiction and philosophical novel series.
The series constructs a grand universe spanning hundreds of years, exploring the dynamic equilibrium between "System" (Algorithm/Rationality) and "Human" (Existence/Pain).

### Core Structure: 0-7-0 Cycle
The series follows a recursive "0-7-0" structure, mapping to the **ASTO Dynamics Mechanism**:
- **0**: Chaos/Origin (e.g., 《验收之前》)
- **1-6**: Evolution Stages (Creation, Order, Golden Age, Cost, Collapse, Eternity)
- **7**: Resilience/Return (e.g., 《逻辑裂缝》)
- **0**: Reset (Cycle begins again)

## 2. Directory & Architecture
The repository is structured by "Book", with each book having its own dedicated folder.

### Folder Structure
- **Root**: Contains the central series bible (`readme.md`), promotion strategies, and global concept docs.
- **Book Folders** (e.g., `《作品》`, `《凛冬之宪》`, `《逻辑裂缝3.0》`):
  - **Manuscript Files**: Individual chapters in Markdown format (e.g., `第01章_xxx.md`).
  - **Outlines**: `创作指南.md`, `大纲.md` (Crucial for understanding plot/character arcs).
  - **Scripts**: Python (`.py`) or PowerShell (`.ps1`) scripts for text processing/merging.
  - **Archives**: `归档`, `Old_Versions` folder for version control.

### Key Configuration Files
- `readme.md`: **The Series Bible**. Contains the master timeline, character alignment table (generations of Shen family), and the "5 States / 6 Stages / 7 Orders" theoretical mapping. **Always consult this first.**
- `小说推广策略.md`: Promotion and publication strategy.
- `痛苦私有性.md`: Core ethical setting regarding pain and ownership.

## 3. Development & Writing Workflows

### Text Processing & Merging
The repository uses scripts to merge scattered chapter files into a single manuscript.

**Common Scripts:**
- `realism_merge.py` (Found in `《逻辑裂缝3.0》`):
  - **Usage**: Merges chapters into a "Realism Cleaned" version.
  - **Logic**: Sorts by Chinese numerals, truncates meta-analysis sections, normalizes headings, and applies safe text replacements (e.g., changing names).
- `merge_book_v2.ps1` (Found in `《凛冬之宪》/2.0`):
  - **Usage**: PowerShell script to join markdown files.
  - **Logic**: Filters for chapter files and appends "Artifact" files (files ending in `-产出物.md`) to the end of chapters.

**How to Run:**
```bash
# Example: Merging Logic Rift 3.0
cd "《逻辑裂缝3.0》"
python realism_merge.py

# Example: Merging Constitution of Winter
cd "《凛冬之宪》/2.0"
pwsh merge_book_v2.ps1
```

### Writing Conventions
- **Format**: Markdown.
- **Chapter Naming**: `第[XX]章_[Title].md` (e.g., `第01章_冰风暴否决案.md`).
- **Headings**: 
  - H1 (`#`): Book Title
  - H2 (`##`): Volume/Part
  - H3 (`###`): Chapter Title
- **Meta-Data**: Often included at the top of chapter files or in `tasks.md` within book folders.

## 4. Literary & Theoretical Guidelines (The "Rules")

### The ASTO Philosophy
Do not treat this merely as a story; it is a **simulation of a philosophical system**.
- **5 States**: Being (自在) → Consensus (共识) → Coding (编码) → Materialization (物化) → Orientation (定向).
- **The "Residue" (剩馀物)**: The core conflict. Systems inevitably produce residue (pain, outcasts, bugs) that cannot be optimized.
- **Pain Sovereignty**: Pain is a private asset and the ultimate proof of existence (Dimension 0).

### Tone & Style
- **Rational & Restrained**: Avoid emotional outbursts. The horror comes from the "reasonableness" of the system.
- **Structure over Plot**: Focus on how structures (laws, algorithms, economics) shape human choices.
- **"The Crossing" Style**:
  - Solid (Solid State): 1958-1980s
  - Plasma (Fire): 1990s-2008
  - Liquid (Water): 2008-2019
  - Crystal (Ice): 2020s-Present
- **"Logic Rift" Style**: Highly realistic, "cracks" in the everyday logic of Chengdu.

### Cross-Book Consistency
- **Character Inheritance**: Refer to the "Character Alignment Table" in `readme.md`.
  - e.g., Shen Jibai (Book 1) -> Shen Zhixing (Book 2/3/4).
- **Symbol Flow**: Watch for recurring symbols:
  - **The Coin**: 2024 vending machine coin -> Movie prop -> Key -> Hard currency -> Physical blade.
  - **The Click (Click sound)**: Fan noise -> Gear bite -> Bone fracture -> Cosmic background noise.
  - **Red Oil**: Hotpot -> Blood -> Nebula.

## 5. Common Tasks for Agents
1.  **Contextual Analysis**: When asked about a specific book, always read its `创作指南.md` or `大纲.md` first.
2.  **Consistency Check**: When suggesting plot points, verify against the `readme.md` timeline to avoid anachronisms or character conflicts.
3.  **Refactoring**: If asked to "merge" or "clean" a book, look for existing `.py` or `.ps1` scripts in that book's directory and use/adapt them rather than writing new ones from scratch.
4.  **Formatting**: Ensure all generated text adheres to the specific "Texture" (Solid/Liquid/Crystal) defined for that era/book.
