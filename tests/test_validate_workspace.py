# tests/test_validate_workspace.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
from scripts.validate_workspace import validate_workspace, detect_git_and_prompt_safety


def test_validate_nonexistent_workspace(tmp_path):
    valid, errors = validate_workspace(tmp_path / "nonexistent")
    assert not valid
    assert any("does not exist" in e for e in errors)


def test_validate_empty_workspace(tmp_path):
    valid, errors = validate_workspace(tmp_path)
    assert not valid
    assert any("Layer 0" in e or "AGENT.md" in e for e in errors)
    assert any("Layer 1" in e or "CONTEXT.md" in e for e in errors)


def test_validate_compliant_workspace(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity\nLayer 0", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing\nLayer 1", encoding="utf-8")
    (tmp_path / "resources").mkdir()
    (tmp_path / "resources" / "quality_standards.md").write_text("# Rules", encoding="utf-8")
    
    stage = tmp_path / "stages" / "01_test_stage"
    stage.mkdir(parents=True)
    (stage / "references").mkdir()
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text(
        "# Stage Contract\n## Inputs\n- Layer 3: references/\n## Process\nDo test.\n## Outputs\n- result.md -> output/",
        encoding="utf-8",
    )
    
    valid, errors = validate_workspace(tmp_path)
    assert valid, f"Validation errors: {errors}"
    assert len(errors) == 0


def test_validate_missing_sections_in_stage(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    stage = tmp_path / "stages" / "01_test_stage"
    stage.mkdir(parents=True)
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text("# Stage Contract\nOnly description", encoding="utf-8")
    
    valid, errors = validate_workspace(tmp_path)
    assert not valid
    assert any("missing '## Inputs'" in e for e in errors)
    assert any("missing '## Process'" in e for e in errors)
    assert any("missing '## Outputs'" in e for e in errors)


def test_validate_dead_context_broken_links(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity\nSee [`non_existent_file.md`](file://./non_existent_file.md)", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    stage = tmp_path / "stages" / "01_test"
    stage.mkdir(parents=True)
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text("# Stage\n## Inputs\nNone\n## Process\nRun\n## Outputs\nNone", encoding="utf-8")

    res = validate_workspace(tmp_path)
    # Warnings should capture dead link
    assert any("non_existent_file.md" in w for w in res.warnings)


def test_validate_rule_contradictions(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity\nUse `npm install package` here.", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    (tmp_path / "_config").mkdir()
    (tmp_path / "_config" / "rules.md").write_text("# Rules\nAlways use bun and bunx.", encoding="utf-8")
    stage = tmp_path / "stages" / "01_test"
    stage.mkdir(parents=True)
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text("# Stage\n## Inputs\nNone\n## Process\nRun\n## Outputs\nNone", encoding="utf-8")

    res = validate_workspace(tmp_path)
    assert any("npm" in e.lower() or "contradiction" in e.lower() or "package manager" in e.lower() for e in res.errors)


def test_validate_task_governance_and_skills(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    
    # Create phases with malformed task
    phase_dir = tmp_path / "docs" / "phases" / "phase_01_core"
    phase_dir.mkdir(parents=True)
    (phase_dir / "goals.md").write_text("# Goals", encoding="utf-8")
    (phase_dir / "tasks.md").write_text("# Task Board\nMissing proper task ID format", encoding="utf-8")

    # Create skills missing SKILL.md
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / "CONTEXT.md").write_text(
        "# Skills\n| `ghost_skill` | `skills/ghost_skill/SKILL.md` | \"ghost\" | `local` | `v1` |",
        encoding="utf-8",
    )
    
    stage = tmp_path / "stages" / "01_test"
    stage.mkdir(parents=True)
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text("# Stage\n## Inputs\nNone\n## Process\nRun\n## Outputs\nNone", encoding="utf-8")

    res = validate_workspace(tmp_path)
    assert not res.valid
    assert any("ghost_skill" in e for e in res.errors)


def test_validate_multi_workflow_topology(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    
    wf1 = tmp_path / "workflows" / "software_dev" / "stages" / "01_spec"
    wf1.mkdir(parents=True)
    (wf1 / "output").mkdir()
    (wf1 / "CONTEXT.md").write_text("# Stage\n## Inputs\nNone\n## Process\nRun\n## Outputs\nNone", encoding="utf-8")
    
    valid, errors = validate_workspace(tmp_path)
    assert valid, f"Multi-workflow validation failed: {errors}"


def test_auto_fix_missing_outputs(tmp_path):
    (tmp_path / "AGENT.md").write_text("# Identity", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Routing", encoding="utf-8")
    stage = tmp_path / "stages" / "01_test"
    stage.mkdir(parents=True)
    # output/ folder intentionally omitted
    (stage / "CONTEXT.md").write_text("# Stage\n## Inputs\nNone\n## Process\nRun\n## Outputs\nNone", encoding="utf-8")

    valid_before, errors_before = validate_workspace(tmp_path, fix=False)
    assert not valid_before
    assert any("missing Layer 4 'output/'" in e for e in errors_before)

    # Run auto-fix
    valid_after, errors_after = validate_workspace(tmp_path, fix=True, non_interactive=True)
    assert (stage / "output").is_dir()
    assert (stage / "output" / ".gitkeep").is_file()
    assert valid_after, f"Expected fix to repair output/ dir: {errors_after}"


def test_git_safety_advice(tmp_path):
    # Simulate git repo
    (tmp_path / ".git").mkdir()
    proceed, advice = detect_git_and_prompt_safety(tmp_path, non_interactive=True)
    assert proceed is True
    assert "Git Safety" in advice or "git worktree" in advice or "branch" in advice


def test_validate_high_signal_formatting(tmp_path):
    # Setup compliant workspace
    (tmp_path / "AGENT.md").write_text("# Identity\n\n**Purpose:** Bounded workspace for testing.\n", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("# Task Routing\n\n**Purpose:** Route tasks.\n\n| Action | Target |\n|---|---|\n| Run | `stages/` |\n", encoding="utf-8")
    stage = tmp_path / "stages" / "01_test"
    stage.mkdir(parents=True)
    (stage / "output").mkdir()
    (stage / "CONTEXT.md").write_text("# Stage 01\n\n**Purpose:** Execute test stage.\n\n## Inputs\n| Source | Desc |\n|---|---|\n| Ref | None |\n\n## Process\n1. Run\n\n## Outputs\n| File | Path |\n|---|---|\n| out | output/ |\n", encoding="utf-8")

    res = validate_workspace(tmp_path)
    assert res.valid
    assert len(res.errors) == 0

    # Test failure on forbidden meta-tag
    (tmp_path / "AGENT.md").write_text("# Identity\n\n> **BLUF:** Forbidden meta-tag.\n", encoding="utf-8")
    res_bad = validate_workspace(tmp_path)
    assert not res_bad.valid
    assert any("forbidden meta-tag" in e.lower() or "jargon" in e.lower() or "bluf" in e.lower() for e in res_bad.errors)
