# ICM Factory — Master Control Plane & Workspace Builder

**Purpose:** Master control plane and workspace factory that designs, initializes, configures, governs, and validates deterministic child ICM developer workspaces in `./workspaces/[workspace-name]` adhering strictly to [`resources/foundations/methodology.md`](file://./resources/foundations/methodology.md).

---

## 1. Operating Rules & Governance

* **Root Role:** This root workspace is the master control plane (**Factory of Workspaces**) for context engineering and multi-topology generation.
* **Child Isolation:** All child workspaces reside in `./workspaces/[name]` and remain 100% self-contained and independently executable.
* **Tooling Standard:** Run Python tools via `uv run` and Node/skill utilities via `bun`/`bunx` on Windows PowerShell.
* **Default Scope:** All scripts (`validate_workspace.py`, `create_workspace.py`, `dashboard.py`, `manage_skills.py`) default to project scope (`.`) unless `--workspace ./workspaces/[name]` is specified.

### 3-Tier "Folder as App" Floor Plan
| Layer | Name | Files & Responsibilities |
| :--- | :--- | :--- |
| **Layer 1** | **The Floor Plan** | [`AGENT.md`](file://./AGENT.md) (Identity) + [`CONTEXT.md`](file://./CONTEXT.md) (Task Routing) |
| **Layer 2** | **The Rooms** | Stages (`stages/NN_*/`) & Workflows (`workflows/*/`) with local `CONTEXT.md` contracts |
| **Layer 3** | **Tools & Memory** | Dynamic skills (`skills/`), resources (`resources/`), and structured project memory (`docs/`) |

---

## 2. The 4 Modular Workspace Topologies

| Topology | Target Domain | Key Directory Structure |
| :--- | :--- | :--- |
| **Topology 1: Lean Single-Pipeline** | Simple Utilities & Scripts | Root `stages/01_*`, `stages/02_*` directly at root + `./skills/` |
| **Topology 2: Managed Single-Pipeline** | Agile Software Features | Root `docs/` (`STRATEGY.md`, ADRs, sprints) + `./skills/` + root `stages/` |
| **Topology 3: Multi-Workflow Pipeline** | Multi-Domain Automation | Root `workflows/software_dev/` + `workflows/deployment/` + `./skills/` |
| **Topology 4: Enterprise Engine** | Full System with PM | Root `docs/` + `workflows/backend_dev/` + `workflows/deployment/` + `./skills/` |

---

## 3. The 7 Pluggable Utilities (Add-Ons)

| Flag | Add-On Name | Injected Capabilities & Directory Structure |
| :--- | :--- | :--- |
| `--with-pm` | Advanced Project Management | `docs/phases/`, `tasks.md`, `goals.md`, and `STRATEGY.md` |
| `--with-compiler` | 5-Part Prompt Compiler | `docs/backlog/` (`raw_ideas.md` $\rightarrow$ `shaped_initiatives.md`) |
| `--with-agents` | Multi-Agent Specialist Chambers | `agents/` (recursive agent chambers) & `docs/phases/*/handoffs/` |
| `--multi-workflow` | Multi-Pipeline Orchestrator | `workflows/<domain>/stages/` structure |
| `--with-skills` | Pre-Curated Skills Bundle | Master `./skills/` + `skills/CONTEXT.md` (`workspace-architect`, `superpowers`, `graphify`) |
| `--with-governance` | Workspace Self-Validator | Injects local `scripts/validate_workspace.py` inside child workspace |
| `--adopt <path>` | Existing Codebase Adapter | Non-destructively wraps existing code in ICM without moving files |

---

## 4. Master Workspace Floor Plan & Tooling

| Directory / File | Type | Purpose |
| :--- | :--- | :--- |
| [`AGENT.md`](file://./AGENT.md) | Layer 0 Contract | Master control plane identity, operating rules, and topologies |
| [`CONTEXT.md`](file://./CONTEXT.md) | Layer 1 Router | Master 4-category intent router and stage dispatcher |
| [`CLAUDE.md`](file://./CLAUDE.md) | Command Runner | Quick execution cheatsheet for CLI commands |
| `resources/foundations/` | Layer 3 Reference | [`methodology.md`](file://./resources/foundations/methodology.md), [`context_engineering.md`](file://./resources/foundations/context_engineering.md), [`quality_standards.md`](file://./resources/foundations/quality_standards.md) |
| `resources/archetypes/` | Layer 3 Presets | 8 domain presets (`software_feature`, `agile_software_engine`, `minimal_starter`, etc.) |
| `resources/templates/` | Layer 3 Templates | Child workspace contract templates (`AGENT.template.md`, `CONTEXT.template.md`, etc.) |
| `scripts/` | Layer 3 Tooling | `create_workspace.py`, `validate_workspace.py`, `dashboard.py`, `manage_skills.py`, `init_phase.py` |
| `stages/` | Layer 2 Pipeline | Master 5-stage creation pipeline (`01_discovery` $\rightarrow$ `05_validation`) |
| `workspaces/` | Layer 4 Storage | Target directory for generated child workspaces |

---

## 5. Canonical 5-Part Prompt Architecture

Child initiatives and prompt directives follow the Jake Van Clief 5-part architecture:
* **Identity:** Role, expertise level, and bounded domain persona.
* **Task:** Action verb + bounded scope + verifiable acceptance criteria.
* **Context:** Tech stack, environment constraints, and file references.
* **Constraints:** Minimum 2 positive constraints + 2 negative guardrails (`* **Forbidden:** ...`).
* **Output Format:** Exact deliverable file paths + exact verification command (`uv run pytest ...`).

---

## 6. Agent Voice & Documentation Standard

All AI agents in this workspace must adhere to the high-signal, zero-jargon invariants defined in [`resources/foundations/quality_standards.md` (§4)](file://./resources/foundations/quality_standards.md#4-high-signal-documentation--agent-voice-invariants):
* **Core Policy:** Lead with top-level `**Purpose:**`, use structured Markdown tables, anchor constraints with bold keywords, and strictly eliminate conversational fluff and meta-labels.
* **Single Source of Truth:** See [`resources/foundations/quality_standards.md`](file://./resources/foundations/quality_standards.md) for detailed invariant definitions and audit rules.
