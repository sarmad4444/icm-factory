# Architecture Spec: Multi-Agent Chambers & Plain-Text Handoff Contracts

**Purpose:** Defines the architecture, file layout, contract templates, CLI add-on (`--with-agents`), and validation rules for multi-agent chambers and inter-agent handoff protocols in `icm-factory`.

---

## 1. Executive Summary & Problem Statement

Current AI orchestration frameworks (e.g. CrewAI, AutoGen, LangGraph) enforce code-level agent definitions and runtime message brokers that introduce engineering overhead and vendor lock-in. Interpretable Context Methodology (ICM) replaces code-level coordination with filesystem boundaries.

This specification introduces **Multi-Agent Chambers** and **Plain-Text Handoff Contracts** to `icm-factory`:
1. **Multi-Agent Chambers (`agents/<role>/`):** Self-contained, recursive ICM sub-modules with an explicit Identity (`AGENT.md`), private execution pipeline, scoped skill mount whitelist, and negative guardrails.
2. **Master Agent Dispatcher (`agents/CONTEXT.md`):** A Layer 1 routing matrix that maps task categories and file glob patterns to specialized agent chambers.
3. **Plain-Text Inter-Agent Handoffs (`docs/phases/phase_NN/handoffs/`):** Asynchronous Markdown contracts for inter-agent work requests, schema handshakes, and reviews that provide a human-inspectable audit trail.
4. **CLI Add-On Flag (`--with-agents`):** An opt-in scaffolding flag in `scripts/create_workspace.py` that provisions the `agents/` layer and handoff directory.
5. **Tier 4 Validator Audit:** Automated checks in `scripts/validate_workspace.py` verifying agent chamber integrity, `**Purpose:**` headers, negative guardrails, and skill mount existence.

---

## 2. Directory Hierarchy & Contract Architecture

When a child workspace is scaffolded with `--with-agents` (or `--with-pm --with-agents`), the filesystem structure is:

```
workspaces/[workspace-name]/
├── AGENT.md                      # Layer 0: Workspace Identity & Multi-Agent Chamber Table
├── CONTEXT.md                    # Layer 1: Master Task Router linking to agents/CONTEXT.md
├── skills/                       # Layer 3: Workspace-wide Dynamic Skills
├── stages/                       # Layer 2: Sequential Macro Pipeline (Assembly Line)
├── docs/                         # Layer 3/4: Strategy, Phases, and Backlog
│   └── phases/phase_01_mvp_core/
│       ├── goals.md
│       ├── tasks.md              # Role-tagged sprint task board (@agent assignees)
│       └── handoffs/             # Layer 4: Inter-agent work requests & handshakes
│           └── .gitkeep
└── agents/                       # Layer 2/3: Multi-Agent Specialist Chambers
    ├── CONTEXT.md                # Master Agent Dispatcher & Task Routing Matrix
    └── lead_engineer/            # Starter Agent Chamber
        └── AGENT.md              # Agent Identity, Pipeline, Skill Whitelist, Guardrails
```

---

## 3. Template Specifications (`resources/templates/`)

### 3.1 `resources/templates/agents_CONTEXT.template.md`
```markdown
<!-- 💡 HOW THIS WORKS -->
<!-- This is the Master Agent Task Router for multi-agent task dispatching. -->

# Agent Directory & Task Routing Matrix

**Purpose:** Master Layer 1 routing matrix that maps task categories, intent triggers, and file glob patterns to specialized agent chambers.

---

## 1. Active Agent Roster & Dispatch Matrix

| Task Category / Trigger | File Pattern Glob | Assigned Agent | Agent Chamber Location |
| :--- | :--- | :--- | :--- |
| **Architecture & Systems Design** | `docs/architecture/**`, `adrs/**` | `@architect` | [`agents/architect/AGENT.md`](file://./agents/architect/AGENT.md) |
| **Core Engineering & Implementation** | `src/**`, `lib/**` | `@lead_engineer` | [`agents/lead_engineer/AGENT.md`](file://./agents/lead_engineer/AGENT.md) |
| **Quality & Verification** | `tests/**`, `pytest.ini` | `@qa_engineer` | [`agents/qa_engineer/AGENT.md`](file://./agents/qa_engineer/AGENT.md) |

---

## 2. Inter-Agent Handoff Directory

All cross-agent requests, schema handshakes, and reviews are written to the active sprint phase handoff folder (e.g., [`docs/phases/phase_01_mvp_core/handoffs/`](file://./docs/phases/phase_01_mvp_core/handoffs/)) using the standard handoff contract.
```

### 3.2 `resources/templates/agent_AGENT.template.md`
```markdown
<!-- 💡 HOW THIS WORKS -->
<!-- This file defines a specialized Agent Chamber persona, execution pipeline, and guardrails. -->

# Agent Identity: {AGENT_TITLE} (`@{AGENT_HANDLE}`)

**Purpose:** {AGENT_MISSION}

---

## 1. Allowed Skills & Tools (Mounted Envelope)

| Skill / Tool | Mount Location | Trigger Condition |
| :--- | :--- | :--- |
| `{SKILL_1_NAME}` | `{SKILL_1_PATH}` | {SKILL_1_TRIGGER} |
| `{SKILL_2_NAME}` | `{SKILL_2_PATH}` | {SKILL_2_TRIGGER} |

---

## 2. Private Execution Pipeline

1. **Context Ingestion:** Read input artifacts from `## Inputs` or assigned sprint task in `docs/phases/*/tasks.md`.
2. **Deterministic Processing:** Execute domain specialization tasks adhering strictly to project standards.
3. **Verification & Testing:** Run designated test and lint commands (`{SAMPLE_VERIFY_COMMAND}`).
4. **Deliverable Handshake:** Write verified outputs to designated `output/` path or log handoff deliverable.

---

## 3. Operating Constraints & Negative Guardrails

* **Scope Invariant:** {POSITIVE_CONSTRAINT_1}
* **Quality Invariant:** {POSITIVE_CONSTRAINT_2}
* **Forbidden:** {FORBIDDEN_ACTION_1}
* **Forbidden:** {FORBIDDEN_ACTION_2}
```

### 3.3 `resources/templates/agent_handoff.template.md`
```markdown
<!-- 💡 HOW THIS WORKS -->
<!-- Use this template for plain-text inter-agent requests, schema handshakes, or review requests. -->

# Inter-Agent Handoff: {HANDOFF_TITLE}

**Purpose:** Asynchronous, plain-text work request and context transfer from `@{FROM_AGENT}` to `@{TO_AGENT}`.

---

## 1. Handoff Metadata

| Field | Value |
| :--- | :--- |
| **From Agent** | `@{FROM_AGENT}` |
| **To Agent** | `@{TO_AGENT}` |
| **Status** | `Pending` |
| **Created Date** | {DATE} |

---

## 2. Request Details & Context Inputs

* **Objective:** {HANDOFF_OBJECTIVE}
* **Required Input Files:**
  - [`{INPUT_FILE_1}`](file://./{INPUT_FILE_1})

---

## 3. Expected Deliverable & Acceptance Criteria

* **Target Output File:** `{TARGET_OUTPUT_PATH}`
* **Verification Criteria:** {VERIFICATION_CRITERIA}
```

---

## 4. CLI Add-On Flag: `--with-agents`

In `scripts/create_workspace.py`:
* Argument: `--with-agents` (boolean flag, default `False`).
* Function `inject_agents(target: Path, workspace_name: str)`:
  - Creates `target / "agents"`.
  - Hydrates `agents/CONTEXT.md` from `agents_CONTEXT.template.md`.
  - Creates starter chamber `agents/lead_engineer/AGENT.md` from `agent_AGENT.template.md`.
  - If `docs/phases/` exists, creates `docs/phases/phase_01_mvp_core/handoffs/.gitkeep`.
* Updates rendered `AGENT.md` and `CONTEXT.md` to reference the `agents/` layer.

---

## 5. Validator Governance (Tier 4 Extension)

In `scripts/validate_workspace.py`:
* If `agents/` directory exists:
  - Verify `agents/CONTEXT.md` exists and contains a valid Markdown table with routing entries.
  - For every subfolder in `agents/`:
    - Verify `AGENT.md` exists.
    - Verify top 10 lines contain `**Purpose:**` or `**Mission:**`.
    - Verify `* **Forbidden:**` negative guardrails are present.
    - Parse `## Allowed Skills` table and verify that any skill listed in `skills/` exists on disk (or warning if missing).

---

## 6. Verification Criteria

1. `tests/test_archetypes.py`: All 11 templates (`*.template.md`) exist and pass zero-jargon checks.
2. `tests/test_create_workspace.py`: Scaffolding with `--with-agents` creates `agents/CONTEXT.md`, `agents/lead_engineer/AGENT.md`, and references in `AGENT.md` / `CONTEXT.md`.
3. `tests/test_validate_workspace.py`: `validate_workspace` successfully audits compliant `agents/` chambers and catches missing `AGENT.md`, missing Purpose, and broken skill mounts.
4. Full pytest suite passes 100% (40+ tests).
