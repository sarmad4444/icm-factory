# tests/test_skills_catalog.py
from pathlib import Path
import re

ROOT_DIR = Path(__file__).parent.parent


def test_master_skills_directory_exists():
    skills_dir = ROOT_DIR / "skills"
    assert skills_dir.is_dir(), "Master skills/ directory must exist"
    
    context_file = skills_dir / "CONTEXT.md"
    assert context_file.is_file(), "skills/CONTEXT.md manifest must exist"
    
    content = context_file.read_text(encoding="utf-8")
    assert "## Available Skills" in content or "## Skills Catalog" in content
    
    # Check all 5 required master skills
    for skill_name in ["adhd", "graphify", "caveman", "superpowers", "workspace-architect"]:
        skill_path = skills_dir / skill_name / "SKILL.md"
        assert skill_path.is_file(), f"Skill '{skill_name}/SKILL.md' must exist"
        skill_text = skill_path.read_text(encoding="utf-8")
        assert len(skill_text) > 20, f"Skill '{skill_name}/SKILL.md' must have content"
        assert skill_name in content, f"Skill '{skill_name}' must be listed in skills/CONTEXT.md"
