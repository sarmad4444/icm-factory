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
