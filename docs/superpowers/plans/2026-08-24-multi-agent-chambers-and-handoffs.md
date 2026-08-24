# Implementation Plan: Multi-Agent Chambers & Plain-Text Handoff Contracts

**Purpose:** Actionable, step-by-step TDD implementation plan for adding `--with-agents`, agent templates, validator extensions, and automated tests to `icm-factory`.

---

## 1. Plan Overview

| Task | Module | Changes | Verification Command |
| :--- | :--- | :--- | :--- |
| **Task 1** | `resources/templates/` | Create `agents_CONTEXT.template.md`, `agent_AGENT.template.md`, `agent_handoff.template.md` | `uv run pytest tests/test_archetypes.py` |
| **Task 2** | `tests/test_archetypes.py` | Add new templates to `required_templates` | `uv run pytest tests/test_archetypes.py` |
| **Task 3** | `scripts/create_workspace.py` | Add `--with-agents` CLI flag, `inject_agents()` function, and template wiring | `uv run pytest tests/test_create_workspace.py` |
| **Task 4** | `tests/test_create_workspace.py` | Add `test_scaffold_with_agents` verifying `agents/` scaffolding and handoffs | `uv run pytest tests/test_create_workspace.py` |
| **Task 5** | `scripts/validate_workspace.py` | Enhance Tier 4 check to audit `agents/CONTEXT.md`, chamber `AGENT.md`, Purpose, guardrails, and skills | `uv run pytest tests/test_validate_workspace.py` |
| **Task 6** | `tests/test_validate_workspace.py` | Add `test_validate_agents_chambers` for compliance and violation detection | `uv run pytest tests/test_validate_workspace.py` |
| **Task 7** | `AGENT.md` & `quality_standards.md` | Update Add-Ons matrix and document multi-agent standard | `uv run python scripts/validate_workspace.py` |
| **Task 8** | Verification & Git | Run full pytest suite, ensure 100% pass, and commit | `git commit` |

---

## 2. Step-by-Step Task Breakdown

### Task 1: Create Universal Agent Templates in `resources/templates/`
- Create `resources/templates/agents_CONTEXT.template.md`.
- Create `resources/templates/agent_AGENT.template.md`.
- Create `resources/templates/agent_handoff.template.md`.

### Task 2: Update `tests/test_archetypes.py`
- Add `"agents_CONTEXT.template.md"`, `"agent_AGENT.template.md"`, `"agent_handoff.template.md"` to `required_templates`.
- Run `uv run pytest tests/test_archetypes.py`.

### Task 3: Update `scripts/create_workspace.py`
- Add `--with-agents` argument to `argparse` in `main()`.
- Update `scaffold_workspace(...)` to accept `with_agents: bool = False`.
- Implement `inject_agents(target: Path, workspace_name: str)`:
  - Create `target / "agents"`.
  - Hydrate `agents/CONTEXT.md` from `agents_CONTEXT.template.md`.
  - Create chamber `agents/lead_engineer/AGENT.md` from `agent_AGENT.template.md`.
  - If `(target / "docs" / "phases").is_dir()`, create `docs/phases/phase_01_mvp_core/handoffs/.gitkeep`.
- Update `AGENT.md` rendering to include `- \`agents/\`: Specialized agent chambers & routing.` if `with_agents`.
- Update `CONTEXT.md` rendering to include `| **Dispatch Agent Chamber** | Agent Dispatcher | Read \`agents/CONTEXT.md\` | Multi-agent task routing |` if `with_agents`.

### Task 4: Add Scaffolding Unit Test to `tests/test_create_workspace.py`
- Write `test_scaffold_with_agents(tmp_path)`:
  - Scaffolds a workspace with `with_agents=True`.
  - Asserts `(tmp_path / "agents" / "CONTEXT.md").is_file()`.
  - Asserts `(tmp_path / "agents" / "lead_engineer" / "AGENT.md").is_file()`.
  - Asserts `(tmp_path / "docs" / "phases" / "phase_01_mvp_core" / "handoffs").is_dir()`.
  - Runs `validate_workspace(tmp_path)` and asserts `valid is True`.

### Task 5: Enhance Tier 4 in `scripts/validate_workspace.py`
- Extend `check_task_governance_and_skills(path: Path)`:
  - Check `agents_dir = path / "agents"`.
  - If `agents_dir.is_dir()`:
    - Verify `agents_dir / "CONTEXT.md"` exists.
    - For each subfolder `chamber` in `agents_dir`:
      - Verify `chamber / "AGENT.md"` exists.
      - Verify top 10 lines contain `**Purpose:**` or `**Mission:**`.
      - Verify `* **Forbidden:**` negative guardrails are present.
      - Parse skills table in `AGENT.md` and check that any referenced skill in `skills/` exists.

### Task 6: Add Validation Unit Test to `tests/test_validate_workspace.py`
- Write `test_validate_agents_chambers(tmp_path)`:
  - Verifies valid chamber passes.
  - Verifies missing `AGENT.md` in chamber is caught.
  - Verifies missing `**Purpose:**` is warned.
  - Verifies missing `* **Forbidden:**` is caught.

### Task 7: Update Documentation
- Update `AGENT.md` Section 3 Add-Ons table to include `--with-agents`.
- Update `resources/foundations/quality_standards.md` to define Multi-Agent Chamber standards.

### Task 8: Full Verification & Git Commit
- Run `uv run pytest` (all tests passing).
- Run `uv run python scripts/validate_workspace.py` (100% compliant).
- Commit to git with message `feat(agents): add multi-agent chambers, handoff contracts, and --with-agents scaffolding`.
