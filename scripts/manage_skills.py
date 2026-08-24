"""
scripts/manage_skills.py
Dynamic skill manager for ICM workspaces.
Supports adding, listing, syncing, updating, and removing skills in ./skills/.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


def parse_skill_md(skill_file: Path) -> dict[str, str]:
    content = skill_file.read_text(encoding="utf-8")
    name = skill_file.parent.name
    description = ""
    trigger = f"use {name}"
    url = "local"
    version = "v1.0.0"

    # Parse YAML frontmatter if present
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                k = key.strip().lower()
                v = val.strip().strip("'\"")
                if k == "name":
                    name = v
                elif k == "description":
                    description = v
                elif k == "trigger":
                    trigger = v
                elif k == "url":
                    url = v
                elif k in ["version", "commit"]:
                    version = v

    if not description:
        # Extract first non-heading line
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#") and not line.startswith("---")]
        if lines:
            description = lines[0]
        else:
            description = f"{name} skill"

    return {
        "name": name,
        "path": f"skills/{skill_file.parent.name}/SKILL.md",
        "description": description,
        "trigger": trigger,
        "url": url,
        "version": version,
    }


def get_skills_manifest_path(workspace_dir: Path | str = ".") -> Path:
    ws = Path(workspace_dir).resolve()
    return ws / "skills" / "CONTEXT.md"


def list_skills(workspace_dir: Path | str = ".") -> list[dict]:
    ws = Path(workspace_dir).resolve()
    skills_dir = ws / "skills"
    if not skills_dir.is_dir():
        return []

    manifest_file = skills_dir / "CONTEXT.md"
    manifest_skills: dict[str, dict] = {}

    if manifest_file.is_file():
        manifest_text = manifest_file.read_text(encoding="utf-8")
        for line in manifest_text.splitlines():
            line = line.strip()
            if not line.startswith("|") or "---" in line or "skill name" in line.lower() or ("path" in line.lower() and "trigger" in line.lower()):
                continue
            cols = [c.strip().strip("`") for c in line.split("|")[1:-1]]
            if len(cols) >= 5:
                s_name = cols[0]
                if s_name and s_name.lower() not in ["skill name", "---", "_none_"]:
                    manifest_skills[s_name] = {
                        "name": s_name,
                        "path": cols[1],
                        "trigger": cols[2].strip("'\""),
                        "url": cols[3],
                        "version": cols[4],
                    }

    # Discover skills on disk
    skills_on_disk = []
    for s_dir in sorted(skills_dir.iterdir()):
        if s_dir.is_dir() and (s_dir / "SKILL.md").is_file():
            parsed = parse_skill_md(s_dir / "SKILL.md")
            if s_dir.name in manifest_skills:
                m = manifest_skills[s_dir.name]
                if not parsed.get("trigger") or parsed.get("trigger") == f"use {s_dir.name}":
                    parsed["trigger"] = m.get("trigger", parsed["trigger"]).replace("`", "")
                if not parsed.get("url") or parsed.get("url") == "local":
                    parsed["url"] = m.get("url", parsed["url"]).replace("`", "")
                if not parsed.get("version") or parsed.get("version") == "v1.0.0":
                    parsed["version"] = m.get("version", parsed["version"]).replace("`", "")
            skills_on_disk.append(parsed)

    return skills_on_disk


def sync_skills_manifest(workspace_dir: Path | str = ".") -> bool:
    ws = Path(workspace_dir).resolve()
    skills_dir = ws / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = skills_dir / "CONTEXT.md"

    skills = list_skills(ws)
    
    rows = []
    for s in skills:
        c_name = s["name"].strip("`")
        c_path = s["path"].strip("`")
        c_trigger = s["trigger"].strip("\"'")
        c_url = s["url"].strip("`")
        c_ver = s["version"].strip("`")
        rows.append(f"| `{c_name}` | `{c_path}` | \"{c_trigger}\" | `{c_url}` | `{c_ver}` |")

    table_content = "\n".join(rows) if rows else "| _none_ | - | - | - | - |"

    content = f"""# Project Skills Manifest & Catalog

**Location:** `./skills/`  
**Purpose:** On-demand capabilities, specialized instructions, and trigger routing.

---

## Skills Catalog

| Skill Name | Path | Trigger Phrase | Source / Repository | Pinned Version / Commit |
|---|---|---|---|---|
{table_content}

---

## Activating a Skill

Skills in this directory are loaded **Just-In-Time (JIT)**. When a prompt or stage contract mentions a trigger phrase, load and execute `skills/<name>/SKILL.md`.
"""
    manifest_file.write_text(content, encoding="utf-8")
    return True


import subprocess


def install_community_skill_via_bunx(package_or_url: str, workspace_dir: Path | str = ".") -> bool:
    """Install or pull a community skill directly from GitHub using bunx skills add."""
    ws = Path(workspace_dir).resolve()
    try:
        res = subprocess.run(
            ["bunx", "skills", "add", package_or_url, "-y", "--copy", "--all"],
            cwd=str(ws),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
            timeout=10,
        )
        # If bunx placed files in .skills/, ensure they are synced to skills/
        dot_skills = ws / ".skills"
        skills_dir = ws / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        if dot_skills.is_dir():
            for item in dot_skills.iterdir():
                if item.is_dir():
                    dest = skills_dir / item.name
                    if not dest.exists():
                        shutil.copytree(item, dest)
        if res.returncode == 0:
            sync_skills_manifest(ws)
            return True
        else:
            print(f"[WARN] bunx skills add returned code {res.returncode}: {res.stderr}")
    except Exception as e:
        print(f"[WARN] Could not execute bunx skills: {e}")
    return False


def add_skill(
    name: str,
    url: str | None = None,
    commit: str | None = None,
    trigger: str | None = None,
    description: str | None = None,
    workspace_dir: Path | str = ".",
    use_bunx: bool = False,
) -> bool:
    ws = Path(workspace_dir).resolve()
    skills_dir = ws / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    if use_bunx:
        target_pkg = url if (url and "http" in url) else name
        bunx_success = install_community_skill_via_bunx(target_pkg, ws)
        if bunx_success and (skills_dir / name / "SKILL.md").is_file():
            return True

    skill_folder = skills_dir / name
    skill_folder.mkdir(parents=True, exist_ok=True)

    skill_file = skill_folder / "SKILL.md"
    skill_desc = description or f"Specialized instructions for {name}"
    skill_trigger = trigger or f"use {name}"
    skill_url = url or f"https://github.com/obra/{name}"
    skill_version = commit or "v1.0.0"

    if not skill_file.is_file():
        content = f"""---
name: {name}
description: {skill_desc}
trigger: {skill_trigger}
url: {skill_url}
version: {skill_version}
---

# {name.replace('_', ' ').title()} Skill

## Purpose
{skill_desc}

## Instructions
1. Follow instructions when activated.
"""
        skill_file.write_text(content, encoding="utf-8")

    # Update manifest
    sync_skills_manifest(ws)
    return True


def update_skill(name: str, workspace_dir: Path | str = ".") -> bool:
    ws = Path(workspace_dir).resolve()
    skill_folder = ws / "skills" / name
    if not skill_folder.is_dir() or not (skill_folder / "SKILL.md").is_file():
        print(f"[ERROR] Skill '{name}' does not exist.")
        return False

    # Try updating via bunx skills update if installed from community
    try:
        subprocess.run(
            ["bunx", "skills", "update", name, "-y"],
            cwd=str(ws),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
        )
    except Exception:
        pass

    sync_skills_manifest(ws)
    return True


def remove_skill(name: str, workspace_dir: Path | str = ".") -> bool:
    ws = Path(workspace_dir).resolve()
    skill_folder = ws / "skills" / name
    if skill_folder.is_dir():
        shutil.rmtree(skill_folder)
    sync_skills_manifest(ws)
    return True


def main():
    parser = argparse.ArgumentParser(description="Manage dynamic skills in ICM workspaces.")
    subparsers = parser.add_subparsers(dest="command", help="Skill management sub-command")

    # List
    list_p = subparsers.add_parser("list", help="List installed skills")
    list_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Add
    add_p = subparsers.add_parser("add", help="Add or install a skill")
    add_p.add_argument("name", help="Skill name")
    add_p.add_argument("--url", help="Source repository URL")
    add_p.add_argument("--commit", help="Pinned commit / version")
    add_p.add_argument("--trigger", help="Activation trigger phrase")
    add_p.add_argument("--description", help="Short description")
    add_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Sync
    sync_p = subparsers.add_parser("sync", help="Synchronize skills/CONTEXT.md catalog")
    sync_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Remove
    rm_p = subparsers.add_parser("remove", help="Remove an installed skill")
    rm_p.add_argument("name", help="Skill name to remove")
    rm_p.add_argument("--workspace", default=".", help="Target workspace path")

    args = parser.parse_args()

    if args.command == "list" or not args.command:
        ws_dir = getattr(args, "workspace", ".")
        skills = list_skills(ws_dir)
        if console:
            table = Table(title="Installed ICM Skills")
            table.add_column("Skill Name", style="cyan", no_wrap=True)
            table.add_column("Trigger Phrase", style="green")
            table.add_column("Source", style="dim")
            table.add_column("Version", style="magenta")
            table.add_column("Path", style="dim")
            for s in skills:
                table.add_row(s["name"], s["trigger"], s["url"], s["version"], s["path"])
            console.print(table)
        else:
            print("\nInstalled ICM Skills:\n" + "-" * 70)
            for s in skills:
                print(f"  * {s['name']:<15} | {s['trigger']:<25} | {s['version']:<8} | {s['path']}")
            print("-" * 70 + "\n")

    elif args.command == "add":
        success = add_skill(
            name=args.name,
            url=args.url,
            commit=args.commit,
            trigger=args.trigger,
            description=args.description,
            workspace_dir=args.workspace,
        )
        if success:
            print(f"[PASS] Successfully added and cataloged skill '{args.name}'")
        else:
            print(f"[FAIL] Failed to add skill '{args.name}'")
            sys.exit(1)

    elif args.command == "sync":
        sync_skills_manifest(args.workspace)
        print(f"[PASS] Synchronized skills/CONTEXT.md manifest for {args.workspace}")

    elif args.command == "remove":
        remove_skill(args.name, args.workspace)
        print(f"[PASS] Removed skill '{args.name}'")


if __name__ == "__main__":
    main()
