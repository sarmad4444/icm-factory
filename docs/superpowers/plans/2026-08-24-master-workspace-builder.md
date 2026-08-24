# Master Workspace Builder & Governance Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement, refactor, and verify the entire Master Workspace Builder, 4-tier Governance Control Plane, Dynamic Skills system, Rich Terminal Dashboard, and End-to-End Evaluation runner in `icm-generated/seanettle`.

**Architecture:** A deterministic 3-tier "Folder as App" context engineering architecture with progressive disclosure. The control plane provides 4 topologies (Lean, Managed, Multi-Workflow, Enterprise), pluggable utilities (--with-pm, --with-compiler, --with-skills, --with-governance, --adopt), 4-tier validation (structure, dead context, rule contradictions, task/skills governance), Rich TUI dashboard, and an automated 5-scenario evaluation runner.

**Tech Stack:** Python 3.11+ (`uv`, `pytest`, `rich`), Bun (`bun`/`bunx`), Windows PowerShell, Markdown.

**Spec:** `docs/detailed_prompt.md`

## Global Constraints

- Tooling & Runtime: Python tools run exclusively via `uv run python` / `uv run pytest`. Package & skill management uses `bun` / `bunx`. Never use npm/npx/yarn/pnpm.
- Operating System: Windows PowerShell.
- Child Workspace Isolation: All generated or adopted child workspaces must reside in `./workspaces/[workspace-name]` and be 100% self-contained.
- Zero-Knowledge Usability: Child workspace files must NOT contain academic jargon; use friendly headings and `<!-- 💡 HOW THIS WORKS -->` comments.
- Mandatory Git Safety Protocol: In `validate_workspace.py --fix`, detect `.git` repository and prompt/advise branch or git worktree isolation before modifying files.
- Preserved Integrity: All existing tests must remain 100% passing.

---

### Task 1: Master Workspace Skills Directory & Skills Manifest (`skills/`)

**Files:**
- Create: `skills/CONTEXT.md`
- Create: `skills/adhd/SKILL.md`
- Create: `skills/graphify/SKILL.md`
- Create: `skills/caveman/SKILL.md`
- Create: `skills/superpowers/SKILL.md`
- Test: `tests/test_skills_catalog.py`

**Interfaces:**
- Consumes: `docs/detailed_prompt.md` section 3.6
- Produces: Master `./skills/` directory with `skills/CONTEXT.md` catalog mapping skill names, relative paths, triggers, source URLs, and pinned versions.

- [ ] **Step 1: Write the failing test for skills catalog**
Write `tests/test_skills_catalog.py` verifying that `skills/CONTEXT.md` exists and catalogs `adhd`, `graphify`, `caveman`, and `superpowers`, each having a corresponding `SKILL.md` with description and instructions.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_skills_catalog.py -v`
Expected: FAIL (missing `skills/` directory or `skills/CONTEXT.md`).

- [ ] **Step 3: Implement skills directory and manifest**
Create `skills/CONTEXT.md` and the 4 skill folders with canonical `SKILL.md` files:
- `skills/adhd/SKILL.md`
- `skills/graphify/SKILL.md`
- `skills/caveman/SKILL.md`
- `skills/superpowers/SKILL.md`

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_skills_catalog.py -v`
Expected: PASS.

---

### Task 2: Upgraded Templates and Archetypes (`_config/templates/`, `_config/archetypes/`)

**Files:**
- Create: `_config/templates/AGENT.md.tmpl`
- Create: `_config/templates/CONTEXT.md.tmpl`
- Create: `_config/templates/skills_CONTEXT.md.tmpl`
- Create: `_config/templates/STRATEGY.md.tmpl`
- Create: `_config/templates/goals.md.tmpl`
- Create: `_config/templates/tasks.md.tmpl`
- Create: `_config/templates/raw_ideas.md.tmpl`
- Create: `_config/templates/shaped_initiatives.md.tmpl`
- Create/Upgrade: `_config/archetypes/software_feature/` (4 stages: 01_spec, 02_tdd, 03_implementation, 04_verification)
- Create: `_config/archetypes/system_architecture_rfc/` (5 stages: 01_discovery, 02_tradeoffs, 03_diagrams, 04_migration, 05_rfc)
- Create: `_config/archetypes/systematic_bug_triage/` (4 stages: 01_reproduction, 02_root_cause, 03_regression_test, 04_fix_and_review)
- Create: `_config/archetypes/agile_software_engine/` (Topology 2/4 engine with `docs/STRATEGY.md`, `docs/phases/`, `docs/backlog/`, stages)
- Upgrade: `_config/archetypes/minimal_starter/` (2 stages: 01_draft, 02_refine)
- Test: `tests/test_archetypes.py`

**Interfaces:**
- Consumes: Templates and archetype definitions from spec sections 2, 3.3, 3.5, 3.7
- Produces: Standardized template files in `_config/templates/` and complete archetypes in `_config/archetypes/` conforming to ICM structure.

- [ ] **Step 1: Write failing tests for templates and archetypes**
Update `tests/test_archetypes.py` to verify:
- All required templates exist in `_config/templates/`.
- All required archetypes (`software_feature`, `system_architecture_rfc`, `systematic_bug_triage`, `agile_software_engine`, `minimal_starter`, `content_pipeline`, `course_deck`, `research_synthesis`) exist and are 100% ICM compliant.
- Templates contain `<!-- 💡 HOW THIS WORKS -->` and zero academic jargon.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_archetypes.py -v`
Expected: FAIL (missing new archetypes and templates).

- [ ] **Step 3: Implement templates and archetypes**
Write all template files in `_config/templates/` and construct the archetype directories with their respective `AGENT.md`, `CONTEXT.md`, `CLAUDE.md`, `GEMINI.md`, `_config/`, and `stages/NN_*/CONTEXT.md`.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_archetypes.py -v`
Expected: PASS.

---

### Task 3: Dynamic Skills CLI Management Tool (`scripts/manage_skills.py`)

**Files:**
- Create: `scripts/manage_skills.py`
- Test: `tests/test_manage_skills.py`

**Interfaces:**
- Consumes: `./skills/` directory structure and `skills/CONTEXT.md`
- Produces: CLI tool with functions:
  - `add_skill(name, url, commit, trigger, workspace_dir)`
  - `list_skills(workspace_dir) -> list[dict]`
  - `sync_skills_manifest(workspace_dir) -> bool`
  - `update_skill(name, workspace_dir) -> bool`
  - `remove_skill(name, workspace_dir) -> bool`

- [ ] **Step 1: Write failing tests for `scripts/manage_skills.py`**
Write `tests/test_manage_skills.py` testing `add_skill`, `list_skills`, `sync_skills_manifest`, `remove_skill`, and CLI argument parsing.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_manage_skills.py -v`
Expected: FAIL (module `scripts.manage_skills` not found).

- [ ] **Step 3: Implement `scripts/manage_skills.py`**
Implement dynamic skill addition, list rendering, synchronization with `skills/CONTEXT.md`, and version tracking.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_manage_skills.py -v`
Expected: PASS.

---

### Task 4: Objective Sprint Phase Initializer (`scripts/init_phase.py`)

**Files:**
- Create: `scripts/init_phase.py`
- Test: `tests/test_init_phase.py`

**Interfaces:**
- Consumes: `docs/STRATEGY.md` and `_config/templates/goals.md.tmpl`, `tasks.md.tmpl`
- Produces: Function `init_phase(name: str, number: int | None, workspace_dir: Path | str, goal: str | None) -> Path` and CLI interface.

- [ ] **Step 1: Write failing tests for `scripts/init_phase.py`**
Write `tests/test_init_phase.py` verifying:
- Creates `docs/phases/phase_NN_<name>/` directory with `goals.md` and `tasks.md`.
- Generates compliant `TASK-NN-A01` task format.
- Updates `docs/STRATEGY.md` with active phase pointer.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_init_phase.py -v`
Expected: FAIL (module `scripts.init_phase` not found).

- [ ] **Step 3: Implement `scripts/init_phase.py`**
Implement phase creation logic, template hydration, and `docs/STRATEGY.md` synchronization.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_init_phase.py -v`
Expected: PASS.

---

### Task 5: 4-Tier Health Check Engine, Rule Inspector & Auto-Fix (`scripts/validate_workspace.py`)

**Files:**
- Modify: `scripts/validate_workspace.py`
- Test: `tests/test_validate_workspace.py`

**Interfaces:**
- Consumes: Target workspace path, `--fix`, `--non-interactive` / `--yes`
- Produces: `validate_workspace(workspace_path, fix=False, non_interactive=False) -> tuple[bool, list[str], list[str]]`
- Functions:
  - `check_structural_integrity(path)`
  - `check_dead_context_and_orphans(path)`
  - `check_cross_layer_rule_contradictions(path)`
  - `check_task_governance_and_skills(path)`
  - `detect_git_and_prompt_safety(path, non_interactive)`
  - `auto_fix_workspace(path)`

- [ ] **Step 1: Write failing tests for 4-tier validation**
Expand `tests/test_validate_workspace.py` to cover:
- Structural checks for all 4 topologies (lean, managed, multi-workflow, enterprise).
- Dead context detection (broken links in markdown files, missing output directory references).
- Rule contradiction detection (conflicting package managers like `npm` vs `bun`, conflicting tool rules).
- Task governance and skills health (validating `TASK-NN-XXX` format, `@agent` assignment, `skills/CONTEXT.md` sync).
- Git safety prompt handling on `--fix`.
- Auto-fix repair actions (missing `output/` folders, missing `.gitkeep`, missing Layer 0 pointer files).

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_validate_workspace.py -v`
Expected: FAIL on new checks.

- [ ] **Step 3: Implement 4-tier validation engine and auto-fix**
Implement Tier 1 (Structure), Tier 2 (Dead Context), Tier 3 (Rule Contradictions), Tier 4 (Task & Skills Governance), Git Safety protocol, and `--fix` in `scripts/validate_workspace.py`.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_validate_workspace.py -v`
Expected: PASS.

---

### Task 6: Master Workspace Generator Engine & Codebase Adoption (`scripts/create_workspace.py`)

**Files:**
- Modify: `scripts/create_workspace.py`
- Test: `tests/test_create_workspace.py`

**Interfaces:**
- Consumes: CLI options:
  - `--name <name>`
  - `--topology {1,2,3,4,lean,managed,multi-workflow,enterprise}`
  - `--archetype <name>`
  - `--stages <s1,s2,...>`
  - `--workflows <w1:s1,s2;w2:s3,s4>`
  - `--adopt <source_path>`
  - `--with-pm`
  - `--with-compiler`
  - `--with-skills`
  - `--with-governance`
  - `--interactive`
- Produces: Fully scaffolded, 100% compliant child workspace in `./workspaces/<name>/`.

- [ ] **Step 1: Write failing tests for all 4 topologies, add-ons, and `--adopt`**
Expand `tests/test_create_workspace.py` to test:
- Topology 1 (Lean Single-Pipeline).
- Topology 2 (Managed Single-Pipeline with `docs/`).
- Topology 3 (Multi-Workflow with `workflows/`).
- Topology 4 (Enterprise Multi-Workflow & PM Engine).
- Add-ons: `--with-pm`, `--with-compiler`, `--with-skills`, `--with-governance`.
- Codebase adoption: `--adopt <existing_project>` verifies existing project files are preserved intact, and ICM control plane is injected cleanly.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_create_workspace.py -v`
Expected: FAIL on new topology and adoption tests.

- [ ] **Step 3: Implement comprehensive workspace creation & adoption**
Update `scripts/create_workspace.py` to implement:
- Topology generator functions (`scaffold_topology_1`, `scaffold_topology_2`, `scaffold_topology_3`, `scaffold_topology_4`).
- Add-on injectors (`inject_pm`, `inject_compiler`, `inject_skills`, `inject_governance`).
- Non-destructive codebase adapter (`adopt_existing_codebase`).
- Enhanced Socratic interactive wizard.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_create_workspace.py -v`
Expected: PASS.

---

### Task 7: Rich Terminal Dashboard & Enhanced Workspace Lister (`scripts/dashboard.py`, `scripts/list_workspaces.py`)

**Files:**
- Create: `scripts/dashboard.py`
- Modify: `scripts/list_workspaces.py`
- Test: `tests/test_dashboard.py`

**Interfaces:**
- Consumes: `./workspaces/` directory contents, `validate_workspace`
- Produces:
  - `render_dashboard(workspaces_dir: Path, once: bool = False)`
  - CLI commands `python scripts/dashboard.py [--once]`
  - Enhanced `python scripts/list_workspaces.py`

- [ ] **Step 1: Write failing tests for dashboard and list_workspaces**
Write `tests/test_dashboard.py` to test dashboard table rendering with `--once` flag and inspect workspace properties.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_dashboard.py -v`
Expected: FAIL (module `scripts.dashboard` not found).

- [ ] **Step 3: Implement `scripts/dashboard.py` and upgrade `scripts/list_workspaces.py`**
Implement Rich table rendering with workspace topology, phase/stage progress, task count, skills, and validation health status.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_dashboard.py -v`
Expected: PASS.

---

### Task 8: Master Layer 0 & Layer 1 Contracts (`AGENT.md`, `CONTEXT.md`, `CLAUDE.md`, `GEMINI.md`)

**Files:**
- Modify: `AGENT.md`
- Modify: `CONTEXT.md`
- Modify: `CLAUDE.md`
- Modify: `GEMINI.md`
- Test: `tests/test_master_contracts.py`

**Interfaces:**
- Consumes: Specifications from `docs/detailed_prompt.md` sections 1, 2, 3
- Produces: Complete Layer 0 operating contract in `AGENT.md`, 4-category intent router in `CONTEXT.md`, and clean pointers in `CLAUDE.md` and `GEMINI.md`.

- [ ] **Step 1: Write failing tests for master contracts**
Write `tests/test_master_contracts.py` verifying:
- `AGENT.md` contains master Layer 0 identity, 4 topologies, 6 pluggable utilities, 5-part prompt architecture, and governance rules.
- `CONTEXT.md` contains 4-category intent router.
- `CLAUDE.md` and `GEMINI.md` point to `AGENT.md` and `CONTEXT.md`.
- `validate_workspace.py .` passes with 100% compliance on the master workspace itself.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_master_contracts.py -v`
Expected: FAIL.

- [ ] **Step 3: Update master contracts**
Update `AGENT.md`, `CONTEXT.md`, `CLAUDE.md`, and `GEMINI.md`.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_master_contracts.py -v`
Expected: PASS.

---

### Task 9: End-to-End AI & Logical Scenario Evaluation Runner (`scripts/evaluate_scenarios.py`)

**Files:**
- Create: `scripts/evaluate_scenarios.py`
- Test: `tests/test_scenarios.py`

**Interfaces:**
- Consumes: All CLI tools (`create_workspace`, `validate_workspace`, `manage_skills`, `init_phase`, `dashboard`)
- Produces: Automated runner executing the 5 canonical scenarios:
  1. Scenario 1: Lean Utility Creation (Topology 1)
  2. Scenario 2: Enterprise Multi-Workflow & PM Engine (Topology 4)
  3. Scenario 3: Existing Codebase Adoption (`--adopt`)
  4. Scenario 4: Deep Governance & Rule Conflict Detection
  5. Scenario 5: Skills Just-In-Time Discovery & Catalog Sync

- [ ] **Step 1: Write failing tests for evaluation runner**
Write `tests/test_scenarios.py` testing individual scenario execution functions.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_scenarios.py -v`
Expected: FAIL (module `scripts.evaluate_scenarios` not found).

- [ ] **Step 3: Implement `scripts/evaluate_scenarios.py`**
Implement the complete scenario runner with detailed output, Rich summary reporting, and error handling.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_scenarios.py -v`
Expected: PASS.

---

### Task 10: Full Master Suite Verification & Compliance Audit

**Files:**
- Verify: Full test suite and validation scripts.

- [ ] **Step 1: Run pytest across the entire workspace**
Run: `uv run pytest -v`
Expected: 100% PASS across all unit and integration tests.

- [ ] **Step 2: Run master workspace validator**
Run: `uv run python scripts/validate_workspace.py .`
Expected: PASS: 100% ICM Compliant.

- [ ] **Step 3: Run end-to-end evaluation runner**
Run: `uv run python scripts/evaluate_scenarios.py`
Expected: 100% PASS across all 5 scenarios.
