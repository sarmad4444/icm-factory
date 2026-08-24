# tests/test_manage_skills.py
"""
Practical, end-to-end integration tests for dynamic skills management in ICM workspaces.
Tests skill addition via GitHub URL, package name, metadata pinning, manifest synchronization, and removal.
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.manage_skills import (
    add_skill,
    list_skills,
    sync_skills_manifest,
    update_skill,
    remove_skill,
    parse_skill_md,
)
from scripts.validate_workspace import validate_workspace


def test_list_skills_on_master_workspace():
    """Verify that the master workspace has all 5 core skills properly registered in skills/CONTEXT.md."""
    skills = list_skills(ROOT_DIR)
    assert len(skills) >= 5
    names = [s["name"] for s in skills]
    assert "adhd" in names
    assert "graphify" in names
    assert "caveman" in names
    assert "superpowers" in names
    assert "workspace-architect" in names


def test_add_skill_via_github_repo_url(tmp_path):
    """
    Practical Test 1: Real-world addition of a community skill via GitHub Repository URL.
    Verifies that the skill is placed in project-scoped ./skills/<name>/, metadata is pinned,
    and skills/CONTEXT.md is dynamically updated.
    """
    ws_dir = tmp_path / "app_with_github_skill"
    ws_dir.mkdir(parents=True)
    (ws_dir / "AGENT.md").write_text("# Test App\nSee [skills/CONTEXT.md](file://./skills/CONTEXT.md)", encoding="utf-8")
    (ws_dir / "CONTEXT.md").write_text("# Test Context\n", encoding="utf-8")
    
    # 1. Add community skill from GitHub repository
    github_url = "https://github.com/UditAkhourii/adhd"
    success = add_skill(
        name="adhd",
        url=github_url,
        commit="a1b2c3d",
        trigger="adhd mode, tree of thought, prune decisions",
        description="Tree-of-Thought exploration and decision pruning for complex brainstorming",
        workspace_dir=ws_dir,
    )
    assert success, "Failed to add skill via GitHub URL"
    
    # 2. Verify file structure
    skill_file = ws_dir / "skills" / "adhd" / "SKILL.md"
    assert skill_file.is_file(), "SKILL.md was not created in skills/adhd/"
    
    # 3. Verify YAML frontmatter parsing
    parsed = parse_skill_md(skill_file)
    assert parsed["name"] == "adhd"
    assert parsed["url"] == github_url
    assert parsed["version"] == "a1b2c3d"
    assert "tree of thought" in parsed["trigger"]
    
    # 4. Verify skills/CONTEXT.md contains real metadata
    manifest_file = ws_dir / "skills" / "CONTEXT.md"
    assert manifest_file.is_file(), "skills/CONTEXT.md was not created"
    manifest_text = manifest_file.read_text(encoding="utf-8")
    assert "`adhd`" in manifest_text
    assert "github.com/UditAkhourii/adhd" in manifest_text
    assert "a1b2c3d" in manifest_text


def test_add_skill_via_package_name_and_custom_trigger(tmp_path):
    """
    Practical Test 2: Real-world addition of a community skill via package name.
    Verifies that trigger phrases and descriptions are preserved and indexed.
    """
    ws_dir = tmp_path / "app_with_pkg_skill"
    ws_dir.mkdir(parents=True)
    
    success = add_skill(
        name="graphify",
        url="https://github.com/obra/graphify",
        commit="v2.0.1",
        trigger="graphify, extract AST, visual dependencies",
        description="AST parsing and code relationship knowledge graph generator",
        workspace_dir=ws_dir,
    )
    assert success
    
    skills = list_skills(ws_dir)
    assert len(skills) == 1
    skill = skills[0]
    assert skill["name"] == "graphify"
    assert "extract AST" in skill["trigger"]
    assert skill["version"] == "v2.0.1"
    assert (ws_dir / "skills" / "graphify" / "SKILL.md").is_file()


def test_dynamic_sync_discovers_unregistered_community_skills(tmp_path):
    """
    Practical Test 3: Simulates a developer manually dropping a community skill into ./skills/.
    Verifies that sync_skills_manifest automatically discovers, parses, and catalogs it in CONTEXT.md.
    """
    ws_dir = tmp_path / "app_with_manual_skill"
    skills_dir = ws_dir / "skills"
    
    # Create community skill with full frontmatter
    caveman_dir = skills_dir / "caveman"
    caveman_dir.mkdir(parents=True)
    (caveman_dir / "SKILL.md").write_text(
        """---
name: caveman
description: Ultra-terse, high-density token-efficient response persona
trigger: caveman mode, terse response, token saver
url: https://github.com/JuliusBrussee/caveman
version: v1.0.0
---
# Caveman Skill
Strip filler words and pleasantries.
""",
        encoding="utf-8",
    )
    
    # Run dynamic sync
    synced = sync_skills_manifest(ws_dir)
    assert synced
    
    manifest_text = (skills_dir / "CONTEXT.md").read_text(encoding="utf-8")
    assert "`caveman`" in manifest_text
    assert "JuliusBrussee/caveman" in manifest_text
    assert "caveman mode" in manifest_text


def test_remove_skill_cleans_directory_and_manifest(tmp_path):
    """
    Practical Test 4: Verifies that removing a skill cleans up the folder and eliminates stale entries from CONTEXT.md.
    """
    ws_dir = tmp_path / "app_remove_skill"
    ws_dir.mkdir(parents=True)
    
    add_skill(name="tool_a", trigger="use tool_a", workspace_dir=ws_dir)
    add_skill(name="tool_b", trigger="use tool_b", workspace_dir=ws_dir)
    
    skills_initial = list_skills(ws_dir)
    assert len(skills_initial) == 2
    
    # Remove tool_a
    removed = remove_skill("tool_a", workspace_dir=ws_dir)
    assert removed
    assert not (ws_dir / "skills" / "tool_a").exists()
    
    # Verify manifest updated
    skills_after = list_skills(ws_dir)
    assert len(skills_after) == 1
    assert skills_after[0]["name"] == "tool_b"
    
    manifest_text = (ws_dir / "skills" / "CONTEXT.md").read_text(encoding="utf-8")
    assert "`tool_b`" in manifest_text
    assert "`tool_a`" not in manifest_text
