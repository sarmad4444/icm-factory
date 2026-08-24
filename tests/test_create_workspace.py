# tests/test_create_workspace.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.create_workspace import (
    scaffold_from_archetype,
    scaffold_custom_workspace,
    scaffold_workspace,
    adopt_existing_codebase,
)
from scripts.validate_workspace import validate_workspace


def test_scaffold_from_archetype(tmp_path):
    target = tmp_path / "my_content_workspace"
    success = scaffold_from_archetype("content_pipeline", target, "My Content Studio", "Pipeline for tech videos")
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Scaffolded workspace invalid: {errors}"
    assert (target / "AGENT.md").exists()
    assert (target / "CLAUDE.md").exists()
    assert (target / "CONTEXT.md").exists()
    assert (target / "stages" / "01_research" / "output").exists()


def test_scaffold_custom_workspace(tmp_path):
    target = tmp_path / "custom_etl"
    stages = [
        {"name": "extract", "title": "Data Extraction", "inputs": "- Raw files", "outputs": "- data.json -> output/"},
        {"name": "transform", "title": "Data Cleaning", "inputs": "- ../01_extract/output/data.json", "outputs": "- clean.json -> output/"},
        {"name": "load", "title": "Database Load", "inputs": "- ../02_transform/output/clean.json", "outputs": "- report.md -> output/"},
    ]
    success = scaffold_custom_workspace(
        name="custom_etl",
        target_dir=target,
        description="ETL Process Pipeline",
        stages=stages,
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Custom workspace invalid: {errors}"
    assert (target / "AGENT.md").exists()
    assert (target / "CLAUDE.md").exists()
    assert (target / "stages" / "01_extract" / "CONTEXT.md").exists()
    assert (target / "stages" / "02_transform" / "CONTEXT.md").exists()
    assert (target / "stages" / "03_load" / "CONTEXT.md").exists()


def test_scaffold_topology_1_lean(tmp_path):
    target = tmp_path / "lean_app"
    success = scaffold_workspace(
        name="lean_app",
        target_dir=target,
        topology="1",
        stages=["draft", "refine"],
        with_skills=True,
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Topology 1 invalid: {errors}"
    assert (target / "stages" / "01_draft").is_dir()
    assert (target / "skills" / "CONTEXT.md").is_file()
    assert not (target / "docs").exists()


def test_scaffold_topology_2_managed(tmp_path):
    target = tmp_path / "managed_app"
    success = scaffold_workspace(
        name="managed_app",
        target_dir=target,
        topology="2",
        stages=["spec", "tdd", "impl"],
        with_pm=True,
        with_compiler=True,
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Topology 2 invalid: {errors}"
    assert (target / "docs" / "STRATEGY.md").is_file()
    assert (target / "docs" / "phases" / "phase_01_mvp_core").is_dir()
    shaped_file = target / "docs" / "backlog" / "shaped_initiatives.md"
    assert shaped_file.is_file()
    shaped_content = shaped_file.read_text(encoding="utf-8")
    assert "### 1. Identity" in shaped_content
    assert "### 2. Task" in shaped_content
    assert "### 3. Context" in shaped_content
    assert "### 4. Constraints" in shaped_content
    assert "### 5. Output & Execution Lifecycle" in shaped_content
    assert (target / "stages" / "01_spec").is_dir()


def test_scaffold_topology_3_multi_workflow(tmp_path):
    target = tmp_path / "multi_wf_app"
    workflows = {
        "software_dev": ["spec", "impl"],
        "deployment": ["staging", "production"],
    }
    success = scaffold_workspace(
        name="multi_wf_app",
        target_dir=target,
        topology="3",
        workflows=workflows,
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Topology 3 invalid: {errors}"
    assert (target / "workflows" / "software_dev" / "stages" / "01_spec").is_dir()
    assert (target / "workflows" / "deployment" / "stages" / "02_production").is_dir()


def test_scaffold_topology_4_enterprise(tmp_path):
    target = tmp_path / "enterprise_platform"
    workflows = {
        "backend": ["api_spec", "api_impl"],
        "frontend": ["ui_spec", "ui_impl"],
    }
    success = scaffold_workspace(
        name="enterprise_platform",
        target_dir=target,
        topology="4",
        workflows=workflows,
        with_pm=True,
        with_compiler=True,
        with_skills=True,
        with_governance=True,
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Topology 4 invalid: {errors}"
    assert (target / "docs" / "STRATEGY.md").is_file()
    assert (target / "workflows" / "backend" / "stages" / "01_api_spec").is_dir()
    assert (target / "skills" / "CONTEXT.md").is_file()
    assert (target / "scripts" / "validate_workspace.py").is_file()


def test_adopt_existing_codebase(tmp_path):
    # Create dummy existing Python repository
    existing_repo = tmp_path / "existing_fastapi_app"
    existing_repo.mkdir()
    (existing_repo / "main.py").write_text("print('hello world')", encoding="utf-8")
    (existing_repo / "requirements.txt").write_text("fastapi\nuvicorn\n", encoding="utf-8")
    src_dir = existing_repo / "src"
    src_dir.mkdir()
    (src_dir / "auth.py").write_text("def auth(): pass", encoding="utf-8")

    # Adopt into child workspace
    adopted_target = tmp_path / "adopted_fastapi_app"
    success = adopt_existing_codebase(
        source_dir=existing_repo,
        target_dir=adopted_target,
        workspace_name="adopted_fastapi_app",
        description="FastAPI Service adopted into ICM",
        topology="managed",
    )
    assert success
    # Verify original files are preserved intact
    assert (adopted_target / "main.py").read_text(encoding="utf-8") == "print('hello world')"
    assert (adopted_target / "src" / "auth.py").read_text(encoding="utf-8") == "def auth(): pass"
    assert (adopted_target / "requirements.txt").read_text(encoding="utf-8") == "fastapi\nuvicorn\n"

    # Verify ICM control plane was created and is 100% compliant
    valid, errors = validate_workspace(adopted_target)
    assert valid, f"Adopted workspace failed validation: {errors}"
    assert (adopted_target / "AGENT.md").is_file()
    assert (adopted_target / "CONTEXT.md").is_file()
    assert (adopted_target / "docs" / "STRATEGY.md").is_file()
