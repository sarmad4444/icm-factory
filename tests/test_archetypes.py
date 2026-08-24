# tests/test_archetypes.py
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
from scripts.validate_workspace import validate_workspace


def test_required_templates_exist():
    templates_dir = ROOT_DIR / "resources" / "templates"
    assert templates_dir.is_dir(), "resources/templates directory must exist"
    
    required_templates = [
        "AGENT.template.md",
        "CONTEXT.template.md",
        "skills_CONTEXT.template.md",
        "STRATEGY.template.md",
        "goals.template.md",
        "tasks.template.md",
        "raw_ideas.template.md",
        "shaped_initiatives.template.md",
    ]
    
    for tmpl in required_templates:
        tmpl_file = templates_dir / tmpl
        assert tmpl_file.is_file(), f"Template '{tmpl}' must exist in resources/templates/"
        content = tmpl_file.read_text(encoding="utf-8")
        assert "<!-- 💡 HOW THIS WORKS -->" in content, f"Template '{tmpl}' must contain user-friendly guidance"
        # Zero-knowledge check: No academic jargon
        assert "Layer 0" not in content, f"Template '{tmpl}' should not contain academic jargon 'Layer 0'"
        assert "Epistemic compilation" not in content, f"Template '{tmpl}' should not contain academic jargon"


def test_all_required_archetypes_exist_and_are_valid():
    archetypes_dir = ROOT_DIR / "resources" / "archetypes"
    assert archetypes_dir.is_dir()
    
    required_archetypes = [
        "software_feature",
        "system_architecture_rfc",
        "systematic_bug_triage",
        "agile_software_engine",
        "minimal_starter",
        "content_pipeline",
        "course_deck",
        "research_synthesis",
    ]
    
    for arch_name in required_archetypes:
        arch_path = archetypes_dir / arch_name
        assert arch_path.is_dir(), f"Archetype '{arch_name}' must exist"
        valid, errors = validate_workspace(arch_path)
        assert valid, f"Archetype '{arch_name}' failed validation: {errors}"
