# ICM Factory — Master Task Router & Dispatcher

**Purpose:** Master Layer 1 task router that maps user intents to CLI automation tools, sprint managers, skills installers, governance auditors, and pipeline stages.

---

## 1. Intent Router (4 Core Categories)

### Category 1: Workspace Generation & Topologies
| Goal / Intent | Action / Tool | Command / Contract | Expected Output |
| :--- | :--- | :--- | :--- |
| **Scaffold Topology 1 (Lean)** | CLI Automation | `uv run python scripts/create_workspace.py --name [name] --topology 1` | `workspaces/[name]/` |
| **Scaffold Topology 2 (Managed)** | CLI Automation | `uv run python scripts/create_workspace.py --name [name] --topology 2 --with-pm` | `workspaces/[name]/` with `docs/` |
| **Scaffold Topology 3 (Multi-Workflow)** | CLI Automation | `uv run python scripts/create_workspace.py --name [name] --topology 3` | `workspaces/[name]/` with `workflows/` |
| **Scaffold Topology 4 (Enterprise)** | CLI Automation | `uv run python scripts/create_workspace.py --name [name] --topology 4` | `workspaces/[name]/` (Full engine) |
| **Adopt Existing Codebase** | CLI Adapter | `uv run python scripts/create_workspace.py --adopt [path] --name [name]` | Wrapped non-destructive workspace |
| **Fast-Track Archetype Preset** | CLI Fast-Track | `uv run python scripts/create_workspace.py --archetype [name]` | Pre-configured workspace |
| **Interactive Creation Wizard** | Socratic CLI Wizard | `uv run python scripts/create_workspace.py --interactive` | Step-by-step guided wizard |
| **Custom 5-Stage Master Flow** | Master Pipeline | [`stages/01_discovery/CONTEXT.md`](file://./stages/01_discovery/CONTEXT.md) | Domain brief & blueprint |

### Category 2: Project Management & Backlog Engine
| Goal / Intent | Action / Tool | Command / Contract | Expected Output |
| :--- | :--- | :--- | :--- |
| **Initialize New Sprint Phase** | Sprint Initializer | `uv run python scripts/init_phase.py [name] --goal "[goal]"` | `docs/phases/phase_NN_[name]/` |
| **View Active Strategy & Status** | Live Strategy Doc | Read [`resources/templates/STRATEGY.template.md`](file://./resources/templates/STRATEGY.template.md) | Live sprint & roadmap pointer |
| **Compile 5-Part Prompt Initiative** | Prompt Compiler | Read [`resources/templates/shaped_initiatives.template.md`](file://./resources/templates/shaped_initiatives.template.md) | Executable prompt contract in `docs/backlog/` |

### Category 3: Dynamic Skills & JIT Loading
| Goal / Intent | Action / Tool | Command / Contract | Expected Output |
| :--- | :--- | :--- | :--- |
| **List Installed Skills** | Skills Manager | `uv run python scripts/manage_skills.py list` | Terminal Table of Skills |
| **Add / Install New Skill** | Dynamic Installer | `uv run python scripts/manage_skills.py add [name] --url [url]` | `skills/[name]/SKILL.md` + catalog sync |
| **Synchronize Skills Manifest** | Manifest Sync | `uv run python scripts/manage_skills.py sync` | Updated [`skills/CONTEXT.md`](file://./skills/CONTEXT.md) |
| **Remove Installed Skill** | Skills Manager | `uv run python scripts/manage_skills.py remove [name]` | Cleansed skill directory & manifest |

### Category 4: Governance, Auditing & Terminal Dashboard
| Goal / Intent | Action / Tool | Command / Contract | Expected Output |
| :--- | :--- | :--- | :--- |
| **Audit Workspace Compliance** | 4-Tier Health Check | `uv run python scripts/validate_workspace.py [path]` | 4-Tier Compliance Audit Report |
| **Auto-Fix Structural Issues** | Interactive Repair | `uv run python scripts/validate_workspace.py [path] --fix` | Repaired folders + Git safety check |
| **Terminal Dashboard Overview** | Rich TUI Dashboard | `uv run python scripts/dashboard.py` (or `--once`) | Real-time ecosystem dashboard |
| **Quick Workspaces Table** | Table Lister | `uv run python scripts/list_workspaces.py` | Terminal Summary Table |
| **End-to-End Evaluation Runner** | Automated AI Suite | `uv run python scripts/evaluate_scenarios.py` | 5-Scenario Verification Report |

---

## 2. Archetype Catalog (Layer 3)

Located in [`resources/archetypes/`](file://./resources/archetypes/):
| Archetype | Pipeline Structure | Best For |
| :--- | :--- | :--- |
| `software_feature` | 4-stage: Spec $\rightarrow$ TDD $\rightarrow$ Implementation $\rightarrow$ Verification | Focused software components |
| `system_architecture_rfc` | 5-stage: Discovery $\rightarrow$ Tradeoffs $\rightarrow$ Diagrams $\rightarrow$ Migration $\rightarrow$ RFC | Architectural RFCs & System Design |
| `systematic_bug_triage` | 4-stage: Reproduction $\rightarrow$ Root-Cause $\rightarrow$ Regression Test $\rightarrow$ Fix | Deterministic bug fixing |
| `agile_software_engine` | Full Topology 2/4 engine with `docs/STRATEGY.md` and sprints | Full product lifecycle |
| `minimal_starter` | 2-stage: Discovery $\rightarrow$ Build | Quick prototyping & minimal tasks |
| `content_pipeline` | 3-stage: Research $\rightarrow$ Draft $\rightarrow$ Polish | Documentation & video production |
| `course_deck` | 5-stage: Outline $\rightarrow$ Modules $\rightarrow$ Exercises $\rightarrow$ Slides $\rightarrow$ Review | Educational course generation |
| `research_synthesis` | 4-stage: Ingest $\rightarrow$ Extract $\rightarrow$ Synthesize $\rightarrow$ Report | Document & literature analysis |
