# High-Signal ICM Contracts & Superpowers Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize all ICM contracts across the master control plane, stage rooms, foundations, and archetypes into zero-jargon, high-signal Markdown, and integrate the Superpowers (Spec $\rightarrow$ Plan $\rightarrow$ Execution) workflow into `scripts/create_workspace.py` and the Prompt Compiler.

**Architecture:** Refactor Markdown contracts to use the Purpose + Constraints Matrix + Keyed Bullets standard. Update workspace generator templates and prompt compiler definitions to automatically wire `docs/superpowers/specs/` and `docs/superpowers/plans/` into generated child workspaces.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, PowerShell, Markdown.

**Spec:** [`docs/superpowers/specs/2026-08-24-high-signal-contracts-and-superpowers-integration.md`](file://./docs/superpowers/specs/2026-08-24-high-signal-contracts-and-superpowers-integration.md)

## Global Constraints

* **Zero Third-Party Jargon:** Never use explicit labels like `BLUF:`, `ADHD Protocol`, or external meta-tags.
* **100% Contract Integrity:** Preserve all existing commands, paths, parameters, topologies, and stage transitions verbatim.
* **Tooling Standard:** All scripts must run through `uv run python` on Windows PowerShell.
* **Test Coverage:** All existing pytest suites must pass without regression.

---

### Task 1: Standardize Master Control Plane Contracts (`AGENT.md`, `CONTEXT.md`, `CLAUDE.md`)

**Files:**
- Modify: `AGENT.md`
- Modify: `CONTEXT.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: Existing topology and add-on definitions in `AGENT.md`.
- Produces: Clean, high-signal master contracts with Purpose, constraints matrix, and routing table.

- [ ] **Step 1: Refactor `AGENT.md` to high-signal format**
Update `AGENT.md` with:
- Purpose beneath H1.
- Topologies & Add-ons comparison table.
- Bold keyword constraints (`* **Scope:**`, `* **Forbidden:**`, `* **Tooling:**`).

- [ ] **Step 2: Refactor `CONTEXT.md` to high-signal format**
Update `CONTEXT.md` with:
- Purpose beneath H1.
- 4-Category Intent Routing Matrix (Discovery, Mapping, Scaffolding, Factory Setup, Validation).

- [ ] **Step 3: Refactor `CLAUDE.md` to high-signal format**
Update `CLAUDE.md` with:
- Concise execution command table (`uv run pytest`, `uv run python scripts/...`).

- [ ] **Step 4: Verify Master Control Plane validation**
Run: `uv run python scripts/validate_workspace.py`
Expected: 100% PASS on Master Workspace validation.

- [ ] **Step 5: Commit**
```powershell
git add AGENT.md CONTEXT.md CLAUDE.md
git commit -m "docs: standardize master control plane contracts to high-signal format"
```

---

### Task 2: Standardize Stage Room Contracts (`stages/01_discovery` $\rightarrow$ `05_validation`)

**Files:**
- Modify: `stages/01_discovery/CONTEXT.md`
- Modify: `stages/02_stage_mapping/CONTEXT.md`
- Modify: `stages/03_scaffolding/CONTEXT.md`
- Modify: `stages/04_factory_setup/CONTEXT.md`
- Modify: `stages/05_validation/CONTEXT.md`

**Interfaces:**
- Consumes: Existing stage responsibilities and input/output contracts.
- Produces: Standardized stage room contracts with Purpose, Input/Output tables, and next actions.

- [ ] **Step 1: Refactor `stages/01_discovery/CONTEXT.md` and `stages/02_stage_mapping/CONTEXT.md`**
Apply Purpose + Rule matrix + Input/Output contract table.

- [ ] **Step 2: Refactor `stages/03_scaffolding/CONTEXT.md`, `stages/04_factory_setup/CONTEXT.md`, and `stages/05_validation/CONTEXT.md`**
Apply Purpose + Rule matrix + Verification gates table.

- [ ] **Step 3: Verify stage health check**
Run: `uv run python scripts/validate_workspace.py`
Expected: Stage health 100% compliant.

- [ ] **Step 4: Commit**
```powershell
git add stages/
git commit -m "docs: standardize all 5 stage room contracts to high-signal format"
```

---

### Task 3: Standardize Foundations & Quality Standards (`resources/foundations/`)

**Files:**
- Modify: `resources/foundations/methodology.md`
- Modify: `resources/foundations/context_engineering.md`
- Modify: `resources/foundations/quality_standards.md`

**Interfaces:**
- Consumes: Theoretical ICM manifesto, Jake Van Clief context rules, and quality thresholds.
- Produces: High-density foundational references with matrices and clear rule tables.

- [ ] **Step 1: Refactor `resources/foundations/methodology.md`**
Format ICM Laws and 3-Tier Floor Plan into structured tables.

- [ ] **Step 2: Refactor `resources/foundations/context_engineering.md`**
Format the Jake Van Clief 5-part prompt architecture and token heuristics into structured comparison matrices.

- [ ] **Step 3: Refactor `resources/foundations/quality_standards.md`**
Format test coverage gates, anti-patterns, and validation rules into clear tables.

- [ ] **Step 4: Commit**
```powershell
git add resources/foundations/
git commit -m "docs: standardize foundation documents to high-signal format"
```

---

### Task 4: Standardize Archetype Templates (`resources/archetypes/`)

**Files:**
- Modify: `resources/archetypes/*/*.md` across all 8 archetypes.

**Interfaces:**
- Consumes: Archetype presets.
- Produces: Ready-to-scaffold child contracts in high-signal format.

- [ ] **Step 1: Standardize software-oriented archetypes**
Update `software_feature`, `agile_software_engine`, `minimal_starter`, `system_architecture_rfc`.

- [ ] **Step 2: Standardize operational & content archetypes**
Update `systematic_bug_triage`, `content_pipeline`, `course_deck`, `research_synthesis`.

- [ ] **Step 3: Commit**
```powershell
git add resources/archetypes/
git commit -m "docs: standardize all 8 archetype domain templates to high-signal format"
```

---

### Task 5: Integrate Superpowers into Workspace Creator Engine (`scripts/create_workspace.py`)

**Files:**
- Modify: `scripts/create_workspace.py`
- Test: `tests/test_create_workspace.py`

**Interfaces:**
- Consumes: Scaffolding requests for Topologies 1-4.
- Produces: Child workspaces with pre-scaffolded `docs/superpowers/specs/`, `docs/superpowers/plans/`, and updated child `AGENT.md` contracts.

- [ ] **Step 1: Write test for Superpowers folder and contract generation**
Add test in `tests/test_create_workspace.py` checking that child workspaces receive `docs/superpowers/specs/`, `docs/superpowers/plans/`, and high-signal `AGENT.md`.

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_create_workspace.py -k test_superpowers_scaffolding -v`

- [ ] **Step 3: Update `scripts/create_workspace.py`**
Ensure scaffolding logic creates `docs/superpowers/{specs,plans}` and emits high-signal contracts.

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_create_workspace.py -v`
Expected: ALL PASS.

- [ ] **Step 5: Commit**
```powershell
git add scripts/create_workspace.py tests/test_create_workspace.py
git commit -m "feat: integrate superpowers lifecycle into workspace creation engine"
```

---

### Task 6: Integrate Superpowers into Prompt Compiler Templates (`resources/templates/compiler/`)

**Files:**
- Modify: `resources/templates/compiler/shaped_initiatives.md` (or relevant compiler template)
- Modify: `scripts/init_phase.py` (if applicable)

**Interfaces:**
- Consumes: Raw idea backlog.
- Produces: 5-Part initiatives targeting Spec $\rightarrow$ Plan $\rightarrow$ Subagent execution.

- [ ] **Step 1: Update compiler initiative template**
Structure initiatives to explicitly generate:
- Phase 1: `docs/superpowers/specs/YYYY-MM-DD-<initiative>-design.md`
- Phase 2: `docs/superpowers/plans/YYYY-MM-DD-<initiative>.md`
- Phase 3: TDD implementation via `superpowers:subagent-driven-development`.

- [ ] **Step 2: Commit**
```powershell
git add resources/templates/
git commit -m "feat: wire superpowers 3-phase execution into prompt compiler templates"
```

---

### Task 7: Full Regression Test & Validation Gate

**Files:**
- Verify: Full codebase

- [ ] **Step 1: Run all unit and integration tests**
Run: `uv run pytest tests/`
Expected: 100% tests passing.

- [ ] **Step 2: Run workspace self-validator**
Run: `uv run python scripts/validate_workspace.py`
Expected: 4-Tier validation 100% healthy.

- [ ] **Step 3: Final Git status check**
Run: `git status`
Expected: Clean working tree.
