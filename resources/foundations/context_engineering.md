# ICM Framework & Context Engineering Foundations

**Purpose:** Master architectural foundations, Anthropic context engineering guidelines, and Jake Van Clief video masterclasses.

---

## 1. Foundational Theory & Manifesto

* **[`methodology.md`](file://./methodology.md):** The original Interpretable Context Methodology (ICM) manifesto defining the 5-Layer Context Hierarchy, the "Factory vs. Product" separation, and the filesystem as the AI agent architecture.

---

## 2. Modern Context Engineering Principles (Anthropic)

| Old Mental Model | Modern Frontier Principle | Application in ICM Workspaces |
| :--- | :--- | :--- |
| **Rigid Constraint Walls** | **Principles & Architectural Judgment** | Provide clear domain principles; avoid defensive micromanagement |
| **Bulky Few-Shot Examples** | **Expressive Interfaces & Schemas** | Define structured stage contracts (`Inputs`, `Process`, `Outputs`) |
| **Upfront Context Dump** | **Progressive Disclosure & Dynamic Skills** | Keep root `AGENTS.md` lean; load context on-demand through folders |
| **Duplicated Instructions** | **Colocated Tool Definitions** | Keep tool documentation directly inside scripts and skills |
| **Static Prompt Boilerplate** | **Rich References & Dynamic Rubrics** | Reference ADRs and quality rubrics during verification passes |

---

## 3. Jake Van Clief Masterclass Video Series

| Video | Title & Link | Core Architectural Takeaway |
| :--- | :--- | :--- |
| **Video 1** | [*The AI Folder & Agentic Workflow System*](https://www.youtube.com/watch?v=KPVaUuBkPz8) | Deterministic directory contracts replace brittle orchestration frameworks |
| **Video 2** | [*Stop Building AI Agents. Use This Folder System*](https://www.youtube.com/watch?v=MkN-ss2Nl10) | The 3-Tier "Folder as App" floor plan (Floor Plan -> Rooms -> Tools) |
| **Video 3** | [*You're Automating The Wrong Layer*](https://www.youtube.com/watch?v=956DPSPX4wg) | The canonical 5-Part Prompt Architecture (Identity, Task, Context, Constraints, Output) |

---

## 4. Harmonized Architecture: 5 Layers Across 3 Tiers

The academic 5-Layer Context Hierarchy from [`methodology.md`](file://./methodology.md) maps 1-to-1 onto the 3-Tier "Folder as App" floor plan from Video 2:

| Layer | Tier | Component | Responsibility |
| :--- | :--- | :--- | :--- |
| **Layer 0** | **Tier 1 (Entrance)** | **Operating Contract** (`AGENTS.md`) | Ring-0 agent identity, authority, constraints, and telemetry |
| **Layer 1** | **Tier 1 (Blueprint)** | **Floor Plan & Map** (`CONTEXT.md` + `graphify-out/`) | Master intent routing and live architectural knowledge graph |
| **Layer 2** | **Tier 2 (The Rooms)** | **Execution Engines** (`stages/` or `workflows/`) | Sequential transformation stages and domain execution hubs |
| **Layer 3** | **Tier 3 (The Tools)** | **Tools & Memory** (`skills/`, `resources/`, `docs/`) | Dynamic skills, foundational standards, and project brain |
| **Layer 4** | **Tier 3 (The Output)** | **Deliverables** (`workspaces/` or `output/`) | Finished deliverables, sprint artifacts, and child workspaces |

