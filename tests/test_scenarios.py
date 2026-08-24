# tests/test_scenarios.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.evaluate_scenarios import (
    run_scenario_1_lean_utility,
    run_scenario_2_enterprise_engine,
    run_scenario_3_codebase_adoption,
    run_scenario_4_governance_conflicts,
    run_scenario_5_skills_sync,
    run_all_scenarios,
)


def test_scenario_1_lean_utility(tmp_path):
    success, msg = run_scenario_1_lean_utility(tmp_path / "s1")
    assert success, f"Scenario 1 failed: {msg}"


def test_scenario_2_enterprise_engine(tmp_path):
    success, msg = run_scenario_2_enterprise_engine(tmp_path / "s2")
    assert success, f"Scenario 2 failed: {msg}"


def test_scenario_3_codebase_adoption(tmp_path):
    success, msg = run_scenario_3_codebase_adoption(tmp_path / "s3")
    assert success, f"Scenario 3 failed: {msg}"


def test_scenario_4_governance_conflicts(tmp_path):
    success, msg = run_scenario_4_governance_conflicts(tmp_path / "s4")
    assert success, f"Scenario 4 failed: {msg}"


def test_scenario_5_skills_sync(tmp_path):
    success, msg = run_scenario_5_skills_sync(tmp_path / "s5")
    assert success, f"Scenario 5 failed: {msg}"
