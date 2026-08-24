# tests/test_init_phase.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.init_phase import init_phase


def test_init_phase_creates_phase_structure(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(parents=True)
    strategy_file = docs_dir / "STRATEGY.md"
    strategy_file.write_text(
        "# Project Strategy\n\n**Active Phase:** `phase_01_init`\n\n- Active Phase Directory: `docs/phases/phase_01_init/`\n",
        encoding="utf-8",
    )
    
    phase_dir = init_phase(
        name="billing_engine",
        number=2,
        workspace_dir=tmp_path,
        goal="Implement Stripe and LemonSqueezy billing integrations",
    )
    
    assert phase_dir.is_dir()
    assert phase_dir.name == "phase_02_billing_engine"
    
    goals_file = phase_dir / "goals.md"
    assert goals_file.is_file()
    assert "Implement Stripe and LemonSqueezy" in goals_file.read_text(encoding="utf-8")
    
    tasks_file = phase_dir / "tasks.md"
    assert tasks_file.is_file()
    tasks_content = tasks_file.read_text(encoding="utf-8")
    assert "TASK-02-A01" in tasks_content
    
    # Check that STRATEGY.md was updated
    strategy_content = strategy_file.read_text(encoding="utf-8")
    assert "phase_02_billing_engine" in strategy_content


def test_init_phase_auto_increments_number(tmp_path):
    docs_dir = tmp_path / "docs"
    phases_dir = docs_dir / "phases"
    phases_dir.mkdir(parents=True)
    (phases_dir / "phase_01_mvp").mkdir()
    
    phase_dir = init_phase(
        name="user_auth",
        workspace_dir=tmp_path,
        goal="User authentication with OAuth",
    )
    
    assert phase_dir.name == "phase_02_user_auth"
