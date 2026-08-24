# tests/test_dashboard.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.dashboard import get_workspaces_summary, render_dashboard
from scripts.list_workspaces import get_workspaces_data
from scripts.create_workspace import scaffold_workspace


def test_get_workspaces_summary(tmp_path):
    ws_dir = tmp_path / "workspaces"
    ws_dir.mkdir()
    
    # Create sample child workspaces
    ws1 = ws_dir / "app_one"
    scaffold_workspace("app_one", ws1, topology="1", stages=["draft", "verify"], with_skills=True)

    ws2 = ws_dir / "app_two"
    scaffold_workspace("app_two", ws2, topology="2", stages=["spec", "impl"], with_pm=True)

    summaries = get_workspaces_summary(ws_dir)
    assert len(summaries) == 2
    
    s1 = next(s for s in summaries if s["name"] == "app_one")
    assert s1["topology"] == "Topology 1 (Lean)"
    assert s1["skills_count"] >= 1
    assert s1["valid"] is True

    s2 = next(s for s in summaries if s["name"] == "app_two")
    assert s2["topology"] == "Topology 2 (Managed)"
    assert s2["active_phase"] == "phase_01_mvp_core"
    assert s2["valid"] is True


def test_render_dashboard_once(tmp_path):
    ws_dir = tmp_path / "workspaces"
    ws_dir.mkdir()
    ws1 = ws_dir / "app_demo"
    scaffold_workspace("app_demo", ws1, topology="1", stages=["draft"])

    # render_dashboard with once=True must not block and return True
    success = render_dashboard(workspaces_dir=ws_dir, once=True)
    assert success is True


def test_list_workspaces_data(tmp_path):
    ws_dir = tmp_path / "workspaces"
    ws_dir.mkdir()
    ws1 = ws_dir / "child_test"
    scaffold_workspace("child_test", ws1, topology="1", stages=["init"])

    data = get_workspaces_data(ws_dir)
    assert len(data) == 1
    assert data[0]["name"] == "child_test"
    assert data[0]["valid"] is True
