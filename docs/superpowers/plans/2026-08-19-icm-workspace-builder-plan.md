# ICM Master Workspace Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the ICM (Interpretable Context Methodology) Master Workspace Builder in `./icm-generated`, complete with a 5-stage generator pipeline, 5 pre-built archetypes, mechanical Python automation tools (`create_workspace.py`, `validate_workspace.py`, `list_workspaces.py`), and a dedicated `uv` environment on Windows PowerShell.

**Architecture:** The root project acts as the Master Factory adhering to the 5-Layer Context Hierarchy (Layer 0 identity, Layer 1 routing, Layer 2 stage contracts, Layer 3 reference rules/archetypes, Layer 4 outputs). Local mechanical scripts powered by Python and `uv` handle rapid scaffolding and strict compliance auditing for child workspaces generated in `./workspaces/[workspace-name]`.

**Tech Stack:** Python 3.12+, `uv` (virtual environment & package management), `pytest`, PowerShell (Windows), Markdown / JSON schemas.

**Spec:** [`docs/superpowers/specs/2026-08-19-icm-workspace-builder-design.md`](file:///d:/AI%20Projects/icm-generated/docs/superpowers/specs/2026-08-19-icm-workspace-builder-design.md)

## Global Constraints
- Operating System: Windows. All scripts and terminal commands must run in PowerShell.
- Package Manager / Runtime: Always use `uv` (`uv venv`, `uv run pytest`, `uv run python`) for Python; use `bun` and `bunx` if JavaScript tools are needed. Never use npm/npx/yarn/pnpm.
- Strict ICM Compliance: All workspaces must have Layer 0 (`AGENT.md`), Layer 1 (`CONTEXT.md`), numbered stages (`01_*`), Layer 2 stage contracts (`CONTEXT.md` with `## Inputs`, `## Process`, `## Outputs`), and separation of `references/` (Layer 3) from `output/` (Layer 4).

---

### Task 1: Initialize UV Virtual Environment & Project Configuration

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`

**Interfaces:**
- Produces: Dedicated `.venv` managed by `uv`, containing `pytest` for testing.

- [ ] **Step 1: Create pyproject.toml configuration**

```toml
[project]
name = "icm-generated"
version = "0.1.0"
description = "Interpretable Context Methodology (ICM) Master Workspace Builder"
readme = "SOUL.md"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.0.0",
]
```

- [ ] **Step 2: Create .gitignore**

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
workspaces/*
!workspaces/.gitkeep
```

- [ ] **Step 3: Initialize uv virtual environment and install dev dependencies**

Run: `uv venv; uv pip install pytest` in PowerShell.

- [ ] **Step 4: Verify environment**

Run: `uv run pytest --version` in PowerShell.
Expected: Output shows pytest version.

---

### Task 2: Implement Core Validation Script & Tests (`scripts/validate_workspace.py`)

**Files:**
- Create: `scripts/validate_workspace.py`
- Create: `tests/test_validate_workspace.py`

**Interfaces:**
- Consumes: Workspace path or directory structure on disk.
- Produces: `validate_workspace(workspace_path: Path) -> tuple[bool, list[str]]`, CLI exit code `0` on valid ICM, `1` on failure.

- [ ] **Step 1: Write the failing test for workspace validation**

```python
# tests/test_validate_workspace.py
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.validate_workspace import validate_workspace

def test_validate_nonexistent_workspace(tmp_path):
    valid, errors = validate_workspace(tmp_path / "nonexistent")
    assert not valid
    assert any("does not exist" in e for e in errors)

def test_validate_empty_workspace(tmp_path):
    valid, errors = validate_workspace(tmp_path)
    assert not valid
    assert any("AGENT.md" in e for e in errors)
    assert any("CONTEXT.md" in e for e in errors)
    assert any("stages" in e for e in errors)

def test_validate_compliant_workspace(tmp_path):
    # Setup valid structure
    (tmp_path / "AGENT.md").write_text("# Identity\nLayer 0", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing\nLayer 1", encoding="utf-8")
    (tmp_path / "_config").mkdir()
    (tmp_path / "_config" / "rules.md").write_text("# Rules", encoding="utf-8")
    
    stage = tmp_path / "stages" / "01_test_stage"
    stage.mkdir(parents=True)
    (stage / "references").mkdir()
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text(
        "# Stage Contract\n## Inputs\n- Layer 3: references/\n## Process\nDo test.\n## Outputs\n- result.md -> output/",
        encoding="utf-8"
    )
    
    valid, errors = validate_workspace(tmp_path)
    assert valid, f"Validation errors: {errors}"
    assert len(errors) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_validate_workspace.py -v`
Expected: FAIL (module `scripts.validate_workspace` does not exist).

- [ ] **Step 3: Implement `scripts/validate_workspace.py`**

```python
"""
scripts/validate_workspace.py
Audits any target workspace for strict Interpretable Context Methodology (ICM) compliance.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

def validate_workspace(workspace_path: Path | str) -> tuple[bool, list[str]]:
    path = Path(workspace_path).resolve()
    errors: list[str] = []
    
    if not path.exists() or not path.is_dir():
        return False, [f"Directory does not exist: {path}"]
        
    # Check Layer 0: AGENT.md or CLAUDE.md or GEMINI.md
    has_l0 = (path / "AGENT.md").is_file() or (path / "CLAUDE.md").is_file() or (path / "GEMINI.md").is_file()
    if not has_l0:
        errors.append("Layer 0 missing: Workspace must contain AGENT.md (or CLAUDE.md / GEMINI.md)")
        
    # Check Layer 1: Root CONTEXT.md
    has_l1 = (path / "CONTEXT.md").is_file()
    if not has_l1:
        errors.append("Layer 1 missing: Workspace must contain root CONTEXT.md for task routing")
        
    # Check stages directory
    stages_dir = path / "stages"
    if not stages_dir.is_dir():
        errors.append("Stages directory missing: Workspace must contain a 'stages/' folder")
    else:
        stage_dirs = sorted([d for d in stages_dir.iterdir() if d.is_dir()])
        if not stage_dirs:
            errors.append("No stages found in 'stages/' folder")
        else:
            for idx, stage in enumerate(stage_dirs, start=1):
                # Check numbering format: 01_name, 02_name, etc.
                match = re.match(r"^(\d{2})_(.+)$", stage.name)
                if not match:
                    errors.append(f"Stage '{stage.name}' violates numbering pattern (must be NN_stagename e.g. 01_discovery)")
                else:
                    stage_num = int(match.group(1))
                    if stage_num != idx:
                        errors.append(f"Stage '{stage.name}' is out of sequence (expected {idx:02d}, got {stage_num:02d})")
                
                # Check Layer 2 contract: CONTEXT.md
                stage_context = stage / "CONTEXT.md"
                if not stage_context.is_file():
                    errors.append(f"Stage '{stage.name}' missing Layer 2 contract: CONTEXT.md")
                else:
                    content = stage_context.read_text(encoding="utf-8")
                    if "## Inputs" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Inputs' section")
                    if "## Process" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Process' section")
                    if "## Outputs" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Outputs' section")
                
                # Check Layer 4 output directory
                output_dir = stage / "output"
                if not output_dir.is_dir():
                    errors.append(f"Stage '{stage.name}' missing Layer 4 'output/' folder")
                    
    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description="Audit a workspace for ICM compliance.")
    parser.add_argument("path", nargs="?", default=".", help="Path to workspace directory (default: current dir)")
    args = parser.parse_args()
    
    target_path = Path(args.path).resolve()
    print(f"\n🔍 Auditing ICM Workspace: {target_path}\n" + "-" * 60)
    
    valid, errors = validate_workspace(target_path)
    if valid:
        print("✅ PASS: Workspace is 100% ICM Compliant!\n")
        sys.exit(0)
    else:
        print("❌ FAIL: Workspace has compliance violations:\n")
        for err in errors:
            print(f"  • {err}")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_validate_workspace.py -v`
Expected: PASS.

---

### Task 3: Build Reusable Templates & Archetypes

**Files:**
- Create: `shared/templates/child_agent_md.tmpl`
- Create: `shared/templates/child_context_l1.tmpl`
- Create: `shared/templates/child_stage_l2.tmpl`
- Create: `shared/templates/questionnaire.md`
- Create: `_config/icm_rules.md`
- Create: `_config/archetypes/content_pipeline/`
- Create: `_config/archetypes/research_synthesis/`
- Create: `_config/archetypes/course_deck/`
- Create: `_config/archetypes/software_feature/`
- Create: `_config/archetypes/minimal_starter/`
- Create: `tests/test_archetypes.py`

**Interfaces:**
- Produces: 5 validated ICM archetypes that can be copied or adapted by the scaffolding tool.

- [ ] **Step 1: Create shared markdown templates in `shared/templates/`**
- [ ] **Step 2: Create ICM master rules in `_config/icm_rules.md`**
- [ ] **Step 3: Create full archetype folders in `_config/archetypes/` with complete Layer 0, Layer 1, Layer 2 stage contracts, references, and output folders**
- [ ] **Step 4: Write automated tests in `tests/test_archetypes.py` verifying each archetype passes validation**

```python
# tests/test_archetypes.py
from pathlib import Path
from scripts.validate_workspace import validate_workspace

def test_all_archetypes_are_valid():
    archetypes_dir = Path(__file__).parent.parent / "_config" / "archetypes"
    assert archetypes_dir.is_dir()
    
    archetypes = [d for d in archetypes_dir.iterdir() if d.is_dir()]
    assert len(archetypes) >= 5, f"Found only {len(archetypes)} archetypes"
    
    for arch in archetypes:
        valid, errors = validate_workspace(arch)
        assert valid, f"Archetype '{arch.name}' failed validation: {errors}"
```

- [ ] **Step 5: Run tests and ensure all archetypes pass**

Run: `uv run pytest tests/test_archetypes.py -v`
Expected: PASS.

---

### Task 4: Implement Workspace Scaffolding & Listing Tools (`scripts/create_workspace.py`, `scripts/list_workspaces.py`)

**Files:**
- Create: `scripts/create_workspace.py`
- Create: `scripts/list_workspaces.py`
- Create: `tests/test_create_workspace.py`

**Interfaces:**
- Produces: `scaffold_workspace(...)` function and CLI commands `python scripts/create_workspace.py` and `python scripts/list_workspaces.py`.

- [ ] **Step 1: Write failing tests for workspace creation**

```python
# tests/test_create_workspace.py
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.create_workspace import scaffold_from_archetype, scaffold_custom_workspace
from scripts.validate_workspace import validate_workspace

def test_scaffold_from_archetype(tmp_path):
    target = tmp_path / "my_content_workspace"
    success = scaffold_from_archetype("content_pipeline", target, "My Content Studio")
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Scaffolded workspace invalid: {errors}"

def test_scaffold_custom_workspace(tmp_path):
    target = tmp_path / "custom_workflow"
    stages = ["extract", "transform", "load"]
    success = scaffold_custom_workspace(
        name="custom_workflow",
        target_dir=target,
        description="ETL Process",
        stages=stages
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Custom workspace invalid: {errors}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_create_workspace.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement `scripts/create_workspace.py` supporting both CLI arguments and interactive mode**
- [ ] **Step 4: Implement `scripts/list_workspaces.py`**
- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_create_workspace.py -v`
Expected: PASS.

---

### Task 5: Build Master Generator Stages & Root Routing (`stages/01_discovery` to `05_validation`)

**Files:**
- Create: `AGENT.md` (Master Builder Layer 0)
- Create: `GEMINI.md` (Master Builder Layer 0 link)
- Create: `CONTEXT.md` (Master Builder Layer 1 router)
- Create: `stages/01_discovery/` (`CONTEXT.md`, `references/heuristics.md`, `output/.gitkeep`)
- Create: `stages/02_stage_mapping/` (`CONTEXT.md`, `references/patterns.md`, `output/.gitkeep`)
- Create: `stages/03_scaffolding/` (`CONTEXT.md`, `references/standards.md`, `output/.gitkeep`)
- Create: `stages/04_factory_setup/` (`CONTEXT.md`, `references/guidelines.md`, `output/.gitkeep`)
- Create: `stages/05_validation/` (`CONTEXT.md`, `references/checklist.md`, `output/.gitkeep`)
- Create: `workspaces/.gitkeep`

**Interfaces:**
- Consumes: User requests for new workspaces or workspace modifications.
- Produces: Fully functional 5-stage Master Builder pipeline where the root project itself passes ICM validation.

- [ ] **Step 1: Create master root files `AGENT.md`, `GEMINI.md`, `CONTEXT.md`**
- [ ] **Step 2: Populate all 5 stages in `stages/01_discovery` through `stages/05_validation` with full Layer 2 contracts and Layer 3 reference guides**
- [ ] **Step 3: Create target `workspaces/` directory with `.gitkeep`**
- [ ] **Step 4: Validate the Master Builder root directory**

Run: `uv run python scripts/validate_workspace.py .`
Expected: PASS (Root master builder is 100% ICM compliant).

---

### Task 6: Full End-to-End Verification & Walkthrough

**Files:**
- Test generated workspaces in `workspaces/demo_video_project` and `workspaces/demo_custom_etl`
- Run full pytest test suite
- Verify clean state

- [ ] **Step 1: Run complete test suite across all modules**

Run: `uv run pytest -v`
Expected: All tests PASS.

- [ ] **Step 2: Generate sample archetype workspace and validate**

Run: `uv run python scripts/create_workspace.py --archetype content_pipeline --name demo_content_workspace --description "Weekly Tech Explainer"`
Run: `uv run python scripts/validate_workspace.py workspaces/demo_content_workspace`
Expected: PASS.

- [ ] **Step 3: Run workspace listing tool**

Run: `uv run python scripts/list_workspaces.py`
Expected: Displays table showing `demo_content_workspace` as Valid.

- [ ] **Step 4: Clean up demo workspaces to ensure repository is clean**
- [ ] **Step 5: Generate walkthrough documentation**
