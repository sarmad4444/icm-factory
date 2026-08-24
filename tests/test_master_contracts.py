# tests/test_master_contracts.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_workspace import validate_workspace


def test_master_agent_contract_spec_coverage():
    agent_file = ROOT_DIR / "AGENT.md"
    assert agent_file.is_file(), "Master AGENT.md must exist"
    content = agent_file.read_text(encoding="utf-8")

    # Verify 4 Topologies documented
    assert "Topology 1" in content or "Lean Single-Pipeline" in content
    assert "Topology 2" in content or "Managed Single-Pipeline" in content
    assert "Topology 3" in content or "Multi-Workflow" in content
    assert "Topology 4" in content or "Enterprise" in content

    # Verify 6 Pluggable Utilities documented
    assert "--with-pm" in content
    assert "--with-compiler" in content
    assert "--with-skills" in content
    assert "--with-governance" in content
    assert "--adopt" in content


def test_master_context_router_has_4_categories():
    context_file = ROOT_DIR / "CONTEXT.md"
    assert context_file.is_file(), "Master CONTEXT.md must exist"
    content = context_file.read_text(encoding="utf-8")

    # Verify 4 Intent Categories
    assert "Workspace Generation" in content or "Topology" in content
    assert "Project Management" in content or "Sprint" in content
    assert "Dynamic Skills" in content or "Skills" in content
    assert "Governance" in content or "Validation" in content


def test_master_workspace_itself_is_100_percent_compliant():
    valid, errors, warnings = validate_workspace(ROOT_DIR).full()
    assert valid, f"Master workspace failed validation: {errors}"
    assert len(errors) == 0
