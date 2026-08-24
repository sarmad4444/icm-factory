# Interpretable Context Methodology (ICM) — Master Control Plane & Workspace Wizard

**Mission:** Design, initialize, configure, govern, and maintain deterministic child ICM developer workspaces in `./workspaces/[workspace-name]` adhering strictly to the ICM philosophy defined in [`resources/foundations/methodology.md`](file://./resources/foundations/methodology.md).  
**Framework:** Interpretable Context Methodology (ICM)  
**Layer:** Layer 0 (Master Workspace Identity & Operating Contract)

---

## 1. Operating Rules & Governance

1. **Root Role**: This root workspace is an ICM workspace whose domain is **Workspace Generation, Context Engineering & Governance Control Plane** (The Factory of Workspaces).
2. **Child Isolation**: All child workspaces created by this master builder reside in `./workspaces/[workspace-name]`. Each child workspace is 100% self-contained and independently executable.
3. **The 3-Tier "Folder as App" Floor Plan**:
   - **Layer 1: The Floor Plan**: Root `AGENT.md` + `CONTEXT.md` (Project identity and task routing).
   - **Layer 2: The Rooms**: Stage (`stages/NN_*/`) & Workflow (`workflows/*/`) directories with local `CONTEXT.md` contracts.
   - **Layer 3: The Tools & Brain**: Dynamic skills (`skills/`), resources (`resources/`), and structured project memory (`docs/`).
4. **Tooling & Environment Constraints**:
   - All Python tools run exclusively via `uv` (`uv run python ...` / `uv run pytest`).
   - Package & skill management uses `bun` and `bunx`. Never use npm/npx/yarn/pnpm.
   - Platform is Windows PowerShell.
5. **Default Project Scope**: All CLI scripts (`validate_workspace.py`, `manage_skills.py`, `init_phase.py`, `dashboard.py`) default to **project scope (`.`)** when no target workspace is specified, treating this master control plane as an active, self-contained, 100% ICM-compliant workspace. Pass `--workspace ./workspaces/[name]` or target paths explicitly to govern child workspaces.

---

## 2. The 4 Modular Workspace Topologies

When generating or adopting workspaces, support the 4 canonical ICM topologies:

1. **Topology 1: Lean Single-Pipeline** *(Simple Utilities)*
   - Root `stages/01_*`, `stages/02_*` directly at root + `./skills/`.
2. **Topology 2: Managed Single-Pipeline** *(Agile Software Feature)*
   - Root `docs/` (`STRATEGY.md`, architecture ADRs, sprint phases) + `./skills/` + root `stages/01_*`.
3. **Topology 3: Multi-Workflow Pipeline** *(Multi-Domain Automation without PM)*
   - Root `workflows/software_dev/` + `workflows/deployment/` + `./skills/`.
4. **Topology 4: Enterprise Multi-Workflow & PM Engine** *(Full System)*
   - Root `docs/` + `workflows/backend_dev/` + `workflows/deployment/` + `./skills/`.

---

## 3. The 6 Pluggable Utilities (Add-Ons)

1. **`--with-pm` / Advanced Project Management**: `docs/phases/`, `tasks.md`, `goals.md`, and `STRATEGY.md`.
2. **`--with-compiler` / 5-Part Prompt Compiler**: `docs/backlog/` (`raw_ideas.md` $\rightarrow$ `shaped_initiatives.md`).
3. **`--multi-workflow` / Multi-Pipeline Orchestrator**: `workflows/<domain>/stages/` structure.
4. **`--with-skills` / Pre-Curated Skills Bundle**: Master `./skills/` + `skills/CONTEXT.md` (`superpowers`, `graphify`, `adhd`, `caveman`).
5. **`--with-governance` / Workspace Self-Validator**: Injects local `scripts/validate_workspace.py` inside the child workspace.
6. **`--adopt <path>` / Existing Codebase Adapter**: Non-destructively wraps an existing repo in ICM without moving application files.

---

## 4. Master Workspace Floor Plan & Tooling

- `resources/`:
  - `resources/foundations/methodology.md`: ICM Manifesto and theoretical foundations.
  - `resources/foundations/context_engineering.md`: Context engineering rules (Anthropic) & Jake Van Clief video masterclasses.
  - `resources/foundations/quality_standards.md`: Master ICM framework rules & quality constraints.
  - `resources/archetypes/`: Pre-built domain presets (`software_feature`, `system_architecture_rfc`, `systematic_bug_triage`, `agile_software_engine`, `minimal_starter`, `content_pipeline`, `course_deck`, `research_synthesis`).
  - `resources/templates/`: Child workspace contract templates.
- `AGENT.md`: This file — Master Layer 0 identity, operating rules, topologies, and add-ons.
- `CONTEXT.md`: Master Layer 1 4-Category Intent Router.
- `docs/`:
  - `docs/superpowers/specs/2026-08-24-icm-master-control-plane-architecture.md`: Official Master Architecture Specification.
  - `docs/superpowers/plans/2026-08-24-master-workspace-builder.md`: Superpowers Implementation & TDD Plan.
- `skills/`: Master skills manifest and dynamic catalog (`workspace-architect`, `adhd`, `graphify`, `caveman`, `superpowers`).
- `scripts/`:
  - `create_workspace.py`: Scaffolds child workspaces across all 4 topologies or adopts existing repos.
  - `validate_workspace.py`: 4-Tier health check engine with auto-fix and Git safety advice.
  - `dashboard.py`: Rich terminal dashboard for child workspaces.
  - `manage_skills.py`: Dynamic skills manager (add, list, sync, remove).
  - `init_phase.py`: Objective sprint phase initializer.
  - `list_workspaces.py`: Terminal table lister.
  - `evaluate_scenarios.py`: Automated end-to-end AI/logical scenario evaluation runner.
- `stages/`: Master 5-stage creation pipeline (`01_discovery` $\rightarrow$ `05_validation`).
- `workspaces/`: Destination directory for generated child workspaces.

---

## 5. Canonical 5-Part Prompt Architecture

Child initiatives and prompt directives follow the Jake Van Clief 5-part architecture:
1. **Identity**: Role and persona definition.
2. **Task**: Clear action verb + bounded scope + acceptance criteria.
3. **Context**: Stack, environment, and file references.
4. **Constraints**: Anti-patterns, quality rules, and limitations.
5. **Output Format**: Exact file paths and verifiable test commands.
