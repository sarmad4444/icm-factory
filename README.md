# 🏭 ICM Factory (v0.5.0)

**Purpose:** Provide software teams and autonomous AI agents with an LLM-agnostic, deterministic, filesystem-driven control plane for scaffolding, validating, and executing complex multi-stage and multi-agent projects without runtime code lock-in.

---

[![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)](pyproject.toml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Tooling](https://img.shields.io/badge/package%20manager-uv-green.svg)](https://github.com/astral-sh/uv)
[![Architecture](https://img.shields.io/badge/architecture-ICM%205--Layer-purple.svg)](resources/foundations/quality_standards.md)
[![Tests](https://img.shields.io/badge/tests-41%2F41%20passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Production-grade scaffolding engine, master control plane, and multi-agent workspace orchestrator built on Jake Van Clief's Interpretable Context Methodology (ICM).**

---

## 📑 Table of Contents

* [1. Executive Overview](#1-executive-overview)
* [2. What is Interpretable Context Methodology (ICM)?](#2-what-is-interpretable-context-methodology-icm)
* [3. Why ICM? (The Paradigm Shift)](#3-why-icm-the-paradigm-shift)
* [4. The Five Core Principles of ICM](#4-the-five-core-principles-of-icm)
* [5. The 5-Layer Context Hierarchy](#5-the-5-layer-context-hierarchy)
* [6. Workspace Topologies & Pluggable Add-Ons](#6-workspace-topologies--pluggable-add-ons)
* [7. Multi-Agent Chambers & Plain-Text Handoffs](#7-multi-agent-chambers--plain-text-handoffs)
* [8. Installation & Prerequisites](#8-installation--prerequisites)
* [9. Quick Start: Usage Guide](#9-quick-start-usage-guide)
  * [Mode A: Terminal CLI & Scripts](#mode-a-terminal-cli--scripts)
  * [Mode B: AI-Assisted (Claude Code, Antigravity, OpenCode, Cursor)](#mode-b-ai-assisted-execution-llm-native)
* [10. Master Tooling & Control Plane Reference](#10-master-tooling--control-plane-reference)
* [11. Repository Floor Plan](#11-repository-floor-plan)
* [12. Credits & Foundational References](#12-credits--foundational-references)
* [13. Testing & Verification](#13-testing--verification)

---

## 1. Executive Overview

Current AI agent frameworks (CrewAI, LangGraph, AutoGen) attempt to manage agent coordination, memory passing, and state through complex code wrappers and live runtime message brokers. While functional, they create massive engineering overhead, opaque execution states, and heavy vendor lock-in.

**ICM Factory** replaces framework-level code orchestration with **filesystem architecture**:
* **Stages are Folders:** Numbered directories (`01_spec/`, `02_tdd/`, `03_impl/`, `04_verify/`) isolate tasks into single-responsibility boundaries.
* **Contracts are Markdown:** Plain text files (`CONTEXT.md`, `AGENTS.md`) carry the explicit instructions, tool whitelists, and quality constraints.
* **Every Output is an Edit Surface:** Intermediate deliverables land on disk in `output/` so humans can inspect, edit, or steer work mid-run.
* **100% LLM-Agnostic:** Works seamlessly with Claude Code, Google Antigravity, OpenCode, Codex, Cursor, or pure Python scripts.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ICM Master Control Plane                        │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Scaffolding    │ 2. Validation     │ 3. Multi-Agent Chambers        │
│    Topologies 1-4 │    5-Tier Linter  │    Plain-Text Handoffs         │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ 4. Prompt Backlog │ 5. Agile Sprints  │ 6. JIT Skills Catalog          │
│    5-Part Schema  │    DoD & Goals    │    Dynamic Mounts              │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

---

## 2. What is Interpretable Context Methodology (ICM)?

**Interpretable Context Methodology (ICM)** was formulated by **Jake Van Clief** and **David McDermott** (Eduba / University of Edinburgh). 

ICM applies time-tested systems engineering traditions—**Unix Pipelines (1970s)**, **Modular Information Hiding (Parnas, 1972)**, **Make Dependency Graphs (Feldman, 1979)**, and **Multi-Pass Compilation (1980s)**—to the modern challenge of AI context management.

> [!NOTE]
> **The Core ICM Thesis:**
> If the prompts, inputs, and constraints for each stage of a workflow already exist as plain files in a structured folder hierarchy, you do **not** need a multi-agent runtime framework. You need **one agent reading the right file at the right moment**.

```
[Traditional Agent Frameworks]
  Prompt ──> [Python Orchestrator] ──> [Vector DB] ──> [Memory Queue] ──> [Agent A] ──> [Agent B]
             (Opaque Execution, High Complexity, Heavy Code Overhead)

[ICM Architecture]
  Directory:   stages/01_spec/ ──> stages/02_tdd/ ──> stages/03_impl/ ──> stages/04_verify/
  Contracts:   [CONTEXT.md]        [CONTEXT.md]       [CONTEXT.md]        [CONTEXT.md]
  Deliverable: output/spec.md  ──> output/tests.py ──> output/diff.md ──> output/report.md
               (100% Transparent, Inspectable on Disk, Zero Runtime Lock-in)
```

---

## 3. Why ICM? (The Paradigm Shift)

| Architectural Dimension | Traditional Agent Frameworks (CrewAI, LangGraph, AutoGen) | ICM Factory Architecture |
| :--- | :--- | :--- |
| **State Storage** | Ephemeral RAM, vector DBs, opaque state machines | **Plain Markdown files on disk** (Layer 4) |
| **LLM Portability** | Locked to specific Python/JS SDKs and API keys | **100% LLM-Agnostic** (Claude, Antigravity, OpenCode, Cursor) |
| **Context Window** | Stuffs massive chat history into context | **Layered Context Loading** (reads only active stage contracts) |
| **Human In The Loop** | Hard to intercept subagent thoughts mid-run | **Every output is an edit surface** (edit `output/` files directly) |
| **Multi-Agent Coordination** | Live async message queues and network sockets | **Plain-Text Handoff Contracts** (`docs/phases/*/handoffs/`) |
| **Debugging Failed Steps** | Sifting through thousands of log lines | **Open the stage folder and read the output markdown file** |

---

## 4. The Five Core Principles of ICM

* **Principle 1: One Stage, One Job:** Decompose complex tasks into linear, single-responsibility stages (`01_discovery`, `02_blueprint`, `03_scaffold`, `04_verify`).
* **Principle 2: Plain Text as Universal Interface:** Contracts, backlog initiatives, schemas, and outputs are written in standard Markdown and JSON.
* **Principle 3: Layered Context Loading:** AI models only read their active stage contract—preventing context bloating and hallucination.
* **Principle 4: Every Output is an Edit Surface:** Intermediate deliverables are saved to disk under `output/` so humans can review, refine, or redirect work.
* **Principle 5: Configure Factory, Not Product:** Define your operating rules, quality standards, and tool mounts once; individual runs only produce deliverables.

---

## 5. The 5-Layer Context Hierarchy

ICM workspaces use a strict 5-layer hierarchy to guarantee that AI models always have the exact context they need—no more, no less:

```
workspaces/[my-project]/
├── AGENTS.md                     # Layer 0: Master Identity & Operating Guide
├── CONTEXT.md                    # Layer 1: Master Intent Router & Task Dispatcher
├── stages/                       # Layer 2: Sequential Stage Contracts
│   ├── 01_spec/CONTEXT.md
│   └── 02_impl/CONTEXT.md
├── resources/                    # Layer 3: Static References & Quality Standards
│   └── quality_standards.md
└── stages/01_spec/output/        # Layer 4: Working Deliverables & Artifacts
```

| Layer | File / Location | Purpose & Responsibility |
| :--- | :--- | :--- |
| **Layer 0** | [`AGENTS.md`](file://./AGENTS.md) | **Identity & Rules:** Who the agent is, its mission, core constraints, and floor plan. |
| **Layer 1** | [`CONTEXT.md`](file://./CONTEXT.md) | **Task Router:** Master dispatch matrix mapping user intents to specific directories. |
| **Layer 2** | `stages/NN_*/CONTEXT.md` | **Stage Contracts:** Bounded task execution defining `## Inputs`, `## Process`, and `## Outputs`. |
| **Layer 3** | `resources/` or `skills/` | **Knowledge & Tools:** Static styling guidelines, quality standards, and dynamic skills. |
| **Layer 4** | `stages/*/output/` or `handoffs/` | **Working State:** Intermediate draft artifacts, final deliverables, and inter-agent requests. |

---

## 6. Workspace Topologies & Pluggable Add-Ons

### 4 Structural Topologies
1. **Topology 1 (Lean Single-Pipeline):** Pure linear assembly line (`stages/01_...` $\rightarrow$ `stages/04_...`). Best for focused scripts and utilities.
2. **Topology 2 (Managed Single-Pipeline):** Linear stages combined with `docs/STRATEGY.md`, sprint goals, and task backlogs. Best for agile apps and MVPs.
3. **Topology 3 (Multi-Workflow Pipeline):** Parallel domain pipelines (`workflows/backend/`, `workflows/frontend/`).
4. **Topology 4 (Enterprise Engine):** Complete system combining multi-domain workflows, strategic roadmaps, and full governance.

### 8 Pluggable Add-Ons (Utilities)
| Add-On Flag | Name | Capabilities Injected |
| :--- | :--- | :--- |
| `--with-pm` | **Agile Project Management** | Injects `docs/STRATEGY.md`, `docs/phases/`, `goals.md`, and `tasks.md`. |
| `--with-compiler` | **5-Part Prompt Compiler** | Injects `docs/backlog/` (`raw_ideas.md` $\rightarrow$ `shaped_initiatives.md`). |
| `--with-agents` | **Multi-Agent Specialist Chambers** | Injects `agents/` recursive sub-chambers, dispatcher matrix, and sprint `handoffs/`. |
| `--multi-workflow` | **Multi-Domain Orchestrator** | Organizes stages under `workflows/<domain>/stages/`. |
| `--with-skills` | **Curated Skills Bundle** | Injects JIT-loadable `skills/` (`workspace-architect`, `superpowers`, `graphify`). |
| `--with-skill-governance`, `--with-governance` | **Universal Skill Lifecycle Manager** | Dynamic installer, 4-dimension audit scoring, auto-sync manifest. |
| `--telemetry-style` | **Pluggable Response Telemetry** | Injects chosen telemetry style (`pill-bar`, `terminal-box`, `cockpit-hud`, etc.). |
| `--adopt <path>` | **Legacy Codebase Adapter** | Non-destructively wraps an existing repo into ICM without moving files. |

---

## 7. Multi-Agent Chambers & Plain-Text Handoffs

When `--with-agents` is enabled, agents communicate asynchronously through **Plain-Text Handoff Contracts** stored in `docs/phases/phase_NN/handoffs/`:

```
workspaces/my-app/
├── agents/
│   ├── CONTEXT.md                <── Master Dispatcher & Intent Matrix
│   └── lead_engineer/            <── Specialist Chamber (AGENT.md + skills whitelist)
└── docs/phases/phase_01_mvp/
    ├── tasks.md                  <── Sprint Task Board (@agent assignees)
    └── handoffs/                 <── Asynchronous Plain-Text Requests
        └── 2026-08-25_frontend_to_backend_auth_api.md
```

### Anatomy of a Handoff Contract
```markdown
# Inter-Agent Handoff: User Authentication API

**Purpose:** `@frontend` requests an authentication REST endpoint schema from `@backend`.

| Field | Value |
| :--- | :--- |
| **From Agent** | `@frontend` |
| **To Agent** | `@backend` |
| **Status** | `Pending` |

## Request Details
* **Objective:** Create `POST /api/v1/auth/login` returning JWT access tokens.
* **Input Files:** [`src/types/auth.ts`](file://./src/types/auth.ts)

## Acceptance Criteria
* **Target Output:** `src/routes/auth.py`
* **Verification:** `uv run pytest tests/test_auth.py`
```

---

## 8. Installation & Prerequisites

### Prerequisites
* **Python:** 3.11 or higher
* **Package Manager:** [`uv`](https://github.com/astral-sh/uv) (strongly recommended) or `pip`
* **Node.js / Bun:** Optional (for executing dynamic JavaScript/TypeScript tools)

### Quick Installation
```bash
# 1. Clone the ICM Factory repository
git clone https://github.com/your-org/icm-factory.git
cd icm-factory

# 2. Sync virtual environment and dependencies with uv
uv sync

# 3. Verify master workspace compliance
uv run python scripts/validate_workspace.py
```

---

## 9. Quick Start: Usage Guide

### Mode A: Terminal CLI & Scripts

#### 1. Interactive Socratic Wizard
Launch the step-by-step interactive CLI wizard to scaffold or adopt projects:
```bash
uv run python scripts/create_workspace.py --interactive
```

#### 2. Fast-Track Scaffolding One-Liners
```bash
# Example A: Managed Agile Workspace with PM and Skills
uv run python scripts/create_workspace.py \
  --name saas-backend \
  --topology 2 \
  --with-skills

# Example B: Multi-Agent Specialist Chamber Workspace
uv run python scripts/create_workspace.py \
  --name fullstack-platform \
  --topology 2 \
  --with-pm \
  --with-agents \
  --with-skills

# Example C: Adopt an Existing Legacy Repository Non-Destructively
uv run python scripts/create_workspace.py \
  --adopt /path/to/existing-django-app \
  --name modern-django \
  --topology 2
```

#### 3. Real-Time Workspace Dashboard
Monitor the health, stage progression, sprint status, and compliance of all child workspaces:
```bash
uv run python scripts/dashboard.py
```

---

### Mode B: AI-Assisted Execution (LLM-Native)

ICM Factory works out-of-the-box with **Google Antigravity**, **Claude Code**, **OpenCode**, **Cursor**, **Codex**, and any markdown-capable agent.

1. **Step 1 — Point the Agent:** Open your LLM terminal in the project root.
2. **Step 2 — Read Entry Contract:** The AI reads [`AGENTS.md`](file://./AGENTS.md) for its identity and [`CONTEXT.md`](file://./CONTEXT.md) for task routing.
3. **Step 3 — Execute by Intent:** Ask the AI natural-language commands:
   - *"Scaffold a new managed workspace called `order-service` with multi-agent chambers."*
   - *"Audit `workspaces/saas-backend/` against the 5-tier ICM quality standard."*
   - *"Initialize Phase 02 for our mobile app workspace."*
   - *"Add a community skill to `./skills/`."*

---

## 10. Master Tooling & Control Plane Reference

| Script / Tool | Command Line Execution | Primary Purpose |
| :--- | :--- | :--- |
| **Workspace Builder** | `uv run python scripts/create_workspace.py` | Scaffolds Topologies 1-4, injects add-ons, or adopts legacy codebases. |
| **5-Tier Validator** | `uv run python scripts/validate_workspace.py` | Lints structural integrity, dead links, contradictions, and high-signal voice. |
| **Phase Initializer** | `uv run python scripts/init_phase.py` | Provisions new agile sprint phases (`goals.md`, `tasks.md`, `handoffs/`). |
| **Skills Manager** | `uv run python scripts/manage_skills.py` | Lists, installs, and synchronizes dynamic JIT skills in `./skills/`. |
| **Terminal Dashboard** | `uv run python scripts/dashboard.py` | Rich interactive terminal monitor tracking workspace health and stage gates. |
| **Scenario Evaluator** | `uv run python scripts/evaluate_scenarios.py` | Automated end-to-end test suite testing 5 complex real-world workflows. |

---

## 11. Repository Floor Plan

```
icm-factory/
├── AGENTS.md                     # Layer 0: ICM Factory Master Identity & Operating Guide
├── CONTEXT.md                    # Layer 1: Master Intent Router & Task Dispatcher
├── CLAUDE.md                     # Universal Claude & LLM Entry Pointer
├── GEMINI.md                     # Google Antigravity Entry Pointer
├── pyproject.toml                # Project configuration, dependencies, and metadata (v0.5.0)
├── scripts/                      # Control plane automation and CLI tools
│   ├── create_workspace.py       # Workspace scaffolding & legacy code adoption engine
│   ├── validate_workspace.py     # 5-Tier governance and quality compliance linter
│   ├── dashboard.py              # Rich terminal workspace monitoring UI
│   ├── manage_skills.py          # Dynamic skill management and JIT discovery tool
│   ├── init_phase.py             # Sprint phase provisioning tool
│   └── evaluate_scenarios.py     # End-to-end scenario evaluation harness
├── resources/                    # Foundational specifications, quality rules, and templates
│   ├── foundations/              # Master methodology papers and quality standards
│   │   ├── methodology.md        # Jake Van Clief's foundational ICM research paper
│   │   └── quality_standards.md  # 5 principles, 5 layers, and high-signal invariants
│   ├── templates/                # Reusable *.template.md contracts for scaffolding
│   └── archetypes/               # Pre-built domain presets (agile software, RFCs, bug triage)
├── skills/                       # Curated JIT dynamic skills library
│   ├── superpowers/              # TDD, plan authoring, and review skills
│   ├── adhd/                     # High-signal formatting & executive focus protocol
│   ├── graphify/                 # Codebase knowledge graph generator & visualizer
│   └── workspace-architect/      # Socratic workspace blueprint designer
├── stages/                       # Meta-pipeline for building child ICM workspaces (01 to 05)
└── tests/                        # 100% automated pytest suite (41 tests)
```

---

## 12. Credits & Foundational References

ICM Factory is built on foundational context engineering research and community contributions:

* 📄 **Foundational Research Paper:**
  - **Author:** Jake Van Clief & David McDermott (Eduba / University of Edinburgh).
  - **Paper Repository:** [Interpretable-Context-Methodology-ICM- on GitHub](https://github.com/RinDig/Interpretable-Context-Methodology-ICM-)
  - **Local Copy:** [`resources/foundations/methodology.md`](file://./resources/foundations/methodology.md)
* 🏫 **Jake Van Clief's Skool Community:**
  - Connect with ICM practitioners and agent builders: [Interpreted Context Methodology on Skool](https://www.skool.com/interpreted-context-methodology)
* 🧠 **Anthropic Context Engineering Research:**
  - Deep-dive into modern context management: [The New Rules of Context Engineering for Claude Models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
* ⚡ **Superpowers Engineering Protocols:**
  - TDD, brainstorming, and execution skills: [`skills/superpowers/`](file://./skills/superpowers/)
* 🕸️ **Graphify Knowledge Graph System:**
  - Persistent codebase knowledge graph engine: [`skills/graphify/`](file://./skills/graphify/)

---

## 13. Testing & Verification

Run the full automated test suite anytime:
```bash
# Run all 41 unit and scenario tests
uv run pytest

# Run the 5-tier linter on the factory itself
uv run python scripts/validate_workspace.py
```

---

## 14. License

ICM Factory is open-source software licensed under the [MIT License](https://opensource.org/licenses/MIT).
