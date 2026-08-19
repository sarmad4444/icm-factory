# tests/test_create_workspace.py
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.create_workspace import scaffold_from_archetype, scaffold_custom_workspace
from scripts.validate_workspace import validate_workspace

def test_scaffold_from_archetype(tmp_path):
    target = tmp_path / "my_content_workspace"
    success = scaffold_from_archetype("content_pipeline", target, "My Content Studio", "Pipeline for tech videos")
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Scaffolded workspace invalid: {errors}"
    assert (target / "AGENT.md").exists()
    assert (target / "CLAUDE.md").exists()
    assert (target / "GEMINI.md").exists()
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
        stages=stages
    )
    assert success
    valid, errors = validate_workspace(target)
    assert valid, f"Custom workspace invalid: {errors}"
    assert (target / "AGENT.md").exists()
    assert (target / "CLAUDE.md").exists()
    assert (target / "GEMINI.md").exists()
    assert (target / "stages" / "01_extract" / "CONTEXT.md").exists()
    assert (target / "stages" / "02_transform" / "CONTEXT.md").exists()
    assert (target / "stages" / "03_load" / "CONTEXT.md").exists()
