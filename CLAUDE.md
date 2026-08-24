# Interpretable Context Methodology (ICM) — Master Control Plane

**Purpose:** Developer cheatsheet for master control plane execution commands and test runners.

---

## 1. Quick Command Matrix

| Action | Command | Scope |
| :--- | :--- | :--- |
| **Run All Tests** | `uv run pytest` | Master test suite |
| **Validate Master Workspace** | `uv run python scripts/validate_workspace.py` | 4-Tier self-audit |
| **Scaffold Child Workspace** | `uv run python scripts/create_workspace.py --name [name] --topology [1-4]` | `./workspaces/[name]` |
| **Open Rich Dashboard** | `uv run python scripts/dashboard.py` | Live ecosystem TUI |
| **List Child Workspaces** | `uv run python scripts/list_workspaces.py` | Terminal table |
| **Sync Skills Manifest** | `uv run python scripts/manage_skills.py sync` | `skills/CONTEXT.md` |

---

## 2. Core Operating Contract

* **Identity & Rules:** See [`AGENT.md`](file://./AGENT.md) for master architecture, 4 topologies, and add-ons.
* **Intent Routing:** See [`CONTEXT.md`](file://./CONTEXT.md) for master task routing and archetype references.
