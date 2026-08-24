# ICM Master Control Plane & Workspace Wizard Architecture Specification

**Date:** 2026-08-24  
**Status:** Implemented & Verified (100% Passing Tests)  
**Root Workspace:** `icm-generated/seanettle`  
**Philosophy Reference:** [`resources/foundations/methodology.md`](file://./resources/foundations/methodology.md)  
**Implementation Plan:** [`docs/superpowers/plans/2026-08-24-master-workspace-builder.md`](file://./docs/superpowers/plans/2026-08-24-master-workspace-builder.md)

---

## 1. Executive Summary & Core Mission

This specification defines the complete architecture for the **Master Workspace Builder, Governance Control Plane, and Terminal Dashboard Engine** within the Interpretable Context Methodology (ICM) ecosystem.

The system serves as the foundational factory and management hub for creating, adopting, configuring, and governing deterministic, self-contained child developer workspaces in `./workspaces/[workspace-name]`. It combines:
1. **Jake Van Clief's "Folder as App" Philosophy**: The filesystem *is* the application UI, memory, and orchestration layer.
2. **Anthropic's Modern Context Engineering Principles**: Progressive disclosure, lightweight Layer 0 identity, expressive interfaces, on-demand community skills discovery, and rich rubrics.
3. **Agile Markdown-Driven Project Management**: Goal-oriented objective sprints, task tracking with subagent tags and commit hashes, and 5-part prompt compilation.
4. **Deep 4-Tier Governance**: Automated structural auditing, dead context detection, cross-layer rule contradiction analysis, and interactive auto-fix with Git safety protocols.

---

## 2. The 3-Tier "Folder as App" Architecture (The Floor Plan)

Every ICM workspace follows a transparent 3-tier hierarchy:

```
[Layer 1: The Floor Plan]  Root AGENT.md + CONTEXT.md (Who you are & where things live)
         │
         ├──► [Layer 2: The Rooms]  Stage & Phase directories with local CONTEXT.md (What to do in this room)
         │
         └──► [Layer 3: The Tools & Brain]  ./skills/ & ./docs/ (On-demand skills, ADRs, sprints, and strategy)
```

---

## 3. Strict 6-Entity Vocabulary

| Entity | Scope | Exact Definition | Concrete Example |
|---|---|---|---|
| **Workspace** | Root | The entire repository/project container holding `AGENT.md`, `CONTEXT.md`, and its stages or workflows. | `workspaces/saas_billing_engine/` |
| **Phase** *(Objective Sprint)* | Project Management | An outcome-driven milestone/cycle defined by a specific technical or product goal and Definition of Done (not time-bound). | `docs/phases/phase_01_mvp_core/` |
| **Task** | Execution Unit | An atomic work item within a Phase (`TASK-[PHASE]-[CAT]-[ID]`), tracked with `- [ ]`/`- [x]`, assigned to an `@agent`, and tied to git commits/worktrees. | `TASK-01-A01: Setup Stripe Webhook Receiver` |
| **Workflow** *(Pipeline)* | Domain Engine | A domain-specific execution engine (e.g. software development, deployment release, content marketing). | `workflows/software_dev/` |
| **Stage** | Pipeline Step | A numbered, sequential transformation pass (`stages/01_*`, `stages/02_*`) within a workflow or root workspace. | `stages/03_tdd/` or `workflows/software_dev/stages/03_tdd/` |
| **Step** | Micro-Action | A granular micro-instruction inside a Stage's `## Process` contract or task checklist. | `Step 2: Run pytest to verify token expiry` |

---

## 4. The 4 Modular Workspace Topologies

The generator supports 4 canonical topologies based on project scope:

1. **Topology 1: Lean Single-Pipeline** *(Simple Utilities & Generators)*
   - Root `stages/01_*`, `stages/02_*` directly at root + `./skills/`.
2. **Topology 2: Managed Single-Pipeline** *(Agile Software Services)*
   - Root `docs/` (`STRATEGY.md`, architecture ADRs, sprint phases) + `./skills/` + root `stages/01_*`.
3. **Topology 3: Multi-Workflow Pipeline** *(Multi-Domain Automation without PM)*
   - Root `workflows/software_dev/` + `workflows/deployment/` + `./skills/`.
4. **Topology 4: Enterprise Multi-Workflow & PM Engine** *(Full System)*
   - Root `docs/` + `workflows/backend_dev/` + `workflows/deployment/` + `./skills/`.

---

## 5. The 6 Pluggable Utilities (Add-Ons)

1. **`--with-pm` (Advanced Project Management)**: Injects `docs/phases/`, `tasks.md`, `goals.md`, and `STRATEGY.md`.
2. **`--with-compiler` (5-Part Prompt Compiler)**: Injects `docs/backlog/` (`raw_ideas.md` $\rightarrow$ `shaped_initiatives.md`).
3. **`--multi-workflow` (Multi-Pipeline Orchestrator)**: Injects `workflows/<domain>/stages/` structure.
4. **`--with-skills` (Pre-Curated Community Skills Bundle)**: Injects master `./skills/` + `skills/CONTEXT.md` (`superpowers`, `graphify`, `adhd`, `caveman`).
5. **`--with-governance` (Self-Contained Validator)**: Injects local `scripts/validate_workspace.py` inside the child workspace.
6. **`--adopt <path>` (Existing Codebase Adapter)**: Non-destructively wraps an existing repo in ICM without moving application source files.

---

## 6. The Unified `docs/` Project Brain

Managed workspaces centralize strategic context, architecture decisions, and task execution inside `docs/`:

```
docs/
├── STRATEGY.md                <-- Live state, active phase pointer & task rules
├── architecture/              <-- System Overview & ADRs
│   ├── system_overview.md
│   └── adrs/                  <-- Architecture Decision Records (001_*.md)
├── backlog/                   <-- Ideation & 5-Part Prompt Compilation
│   ├── raw_ideas.md           <-- Low-friction capture for unshaped thoughts
│   └── shaped_initiatives.md  <-- Compiled 5-part prompt contracts
└── phases/                    <-- Objective Sprints (Goal-driven)
    ├── phase_01_mvp_core/
    │   ├── goals.md           <-- Phase goals & Definition of Done
    │   └── tasks.md           <-- Task board (TASK-01-A01, @agent, git commits)
    └── phase_02_billing_infra/
```

---

## 7. Dynamic Community Skills Subsystem (`./skills/`)

Skills are **open-source community skills** installed dynamically from upstream registries via `bunx skills add <url-or-name>`:
- **Workspace-Scoped Hosting**: Installed directly into `./skills/[skill-name]/`.
- **Manifest Catalog (`skills/CONTEXT.md`)**: Records skill paths, JIT trigger phrases, upstream source URLs, and pinned commit hashes.
- **Just-In-Time (JIT) Activation**: The root prompt stays ultra-light. When a prompt or stage contract mentions a trigger phrase (e.g. *"Use adhd skill..."*), the AI loads `skills/<name>/SKILL.md` on-demand.
- **Upstream Updates**: `bunx skills update` or `manage_skills.py update` pulls updates without modifying custom workspace rules.

---

## 8. Jake Van Clief 5-Part Prompt Compiler

Raw thoughts are compiled into the canonical 5-part prompt contract:
1. **Identity**: Role and persona definition.
2. **Task**: Clear action verb + bounded scope + acceptance criteria.
3. **Context**: Stack, environment, and file references.
4. **Constraints**: Anti-patterns, quality rules, and limitations.
5. **Output Format**: Exact file paths and verifiable test commands.

---

## 9. 4-Tier Deep Governance & Interactive Auto-Fix

The validator (`scripts/validate_workspace.py`) enforces:
1. **Tier 1 (Structural Integrity)**: Verifies complete Layer 0–4 hierarchy and 2-digit sequential stage numbering (`01_`, `02_`).
2. **Tier 2 (Dead Context & Orphaned Files)**: Flags unlinked files and broken markdown references.
3. **Tier 3 (Contract & Rule Contradiction Inspector)**: Audits cross-layer semantic consistency across `AGENT.md`, `CONTEXT.md`, and `docs/`.
4. **Tier 4 (Task & Skills Governance)**: Validates task naming conventions (`TASK-[PHASE]-[CAT]-[ID]`), status markers (`- [x]`), subagent tags, and skills catalog synchronization.
5. **Interactive Auto-Fix (`--fix`) with Git Safety**: Displays proposed diffs and prompts the user to create an isolated branch or git worktree before applying modifications.

---

## 10. CLI Developer Tooling & Verification Suite

- `scripts/create_workspace.py`: Scaffolding across all 4 topologies, `--adopt`, and Socratic wizard.
- `scripts/validate_workspace.py`: 4-tier health check engine with auto-fix and Git safety advice.
- `scripts/dashboard.py`: Rich terminal UI dashboard for all child workspaces.
- `scripts/manage_skills.py`: Dynamic skills manager (add, list, sync, update, remove).
- `scripts/init_phase.py`: Sprint phase initializer.
- `scripts/evaluate_scenarios.py`: Automated 5-scenario evaluation runner.
- `tests/`: 38 unit and integration tests (100% passing).
