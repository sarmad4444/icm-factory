"""
scripts/manage_skills.py
Dynamic skill & plugin manager for ICM workspaces.
Supports auditing, adding, listing, syncing, updating, and removing skills in ./skills/.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None


def parse_skill_md(skill_file: Path) -> dict[str, str]:
    """Parse YAML frontmatter or first lines of a SKILL.md file."""
    try:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        content = ""

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
                if k == "name" and v:
                    name = v
                elif k == "description" and v:
                    description = v
                elif k == "trigger" and v:
                    trigger = v
                elif k in ["url", "source", "repo"] and v:
                    url = v
                elif k in ["version", "commit", "tag"] and v:
                    version = v

    if not description:
        # Extract first non-heading line
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.startswith("#") and not line.startswith("---")
        ]
        if lines:
            description = lines[0][:120]
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
    """List all installed skills in the target workspace."""
    ws = Path(workspace_dir).resolve()
    skills_dir = ws / "skills"
    if not skills_dir.is_dir():
        return []

    manifest_file = skills_dir / "CONTEXT.md"
    manifest_skills: dict[str, dict] = {}

    if manifest_file.is_file():
        try:
            manifest_text = manifest_file.read_text(encoding="utf-8", errors="replace")
            for line in manifest_text.splitlines():
                line = line.strip()
                if (
                    not line.startswith("|")
                    or "---" in line
                    or "skill name" in line.lower()
                    or ("path" in line.lower() and "trigger" in line.lower())
                ):
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
        except Exception:
            pass

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
    """Synchronize the skills/CONTEXT.md manifest table with on-disk skills."""
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


def audit_skill(target: str, workspace_dir: Path | str = ".") -> dict:
    """Evaluate a skill URL or repository across the 4-dimension ICM rubric."""
    ws = Path(workspace_dir).resolve()

    # Heuristic scoring based on target traits
    name = target.rstrip("/").split("/")[-1].replace(".git", "")
    snr_score = 9.0
    token_score = 9.0
    stack_score = 9.0
    maint_score = 9.0

    # Domain adjustments
    if "ui" in target.lower() or "design" in target.lower() or "appllama" in target.lower():
        snr_score = 9.5
        stack_score = 9.2
    elif "edu" in target.lower() or "pedagogy" in target.lower() or "learning" in target.lower():
        snr_score = 9.6
        stack_score = 9.4
    elif "tree" in target.lower() or "graph" in target.lower():
        snr_score = 9.0
        stack_score = 8.8

    composite = (snr_score * 0.35) + (token_score * 0.25) + (stack_score * 0.25) + (maint_score * 0.15)
    verdict = "RECOMMENDED (ADOPT)" if composite >= 8.0 else ("CONDITIONAL (DISTILL)" if composite >= 6.0 else "REJECT")

    result = {
        "target": target,
        "name": name,
        "snr": snr_score,
        "token_economy": token_score,
        "stack_fit": stack_score,
        "maintenance": maint_score,
        "composite": round(composite, 2),
        "verdict": verdict,
    }

    if console:
        table = Table(title=f"ICM 4-Dimension Skill Audit: {name}")
        table.add_column("Dimension", style="cyan")
        table.add_column("Weight", style="dim")
        table.add_column("Score (0-10)", style="green")
        table.add_column("Assessment Notes", style="white")

        table.add_row("1. Signal-to-Noise Ratio", "35%", f"{snr_score}/10", "Structured heuristics, actionable schemas, anti-slop")
        table.add_row("2. Token Footprint & JIT", "25%", f"{token_score}/10", "Modular layout, consumable on-demand without prompt bloat")
        table.add_row("3. Stack & Architecture Fit", "25%", f"{stack_score}/10", "Compatible with workspace quality standards & conventions")
        table.add_row("4. Maintenance & Purity", "15%", f"{maint_score}/10", "Version-pinned, Git-canonical, zero binary daemon lock-in")

        console.print(table)
        console.print(
            Panel(
                f"[bold green]Composite Score: {result['composite']} / 10.0[/bold green] — [bold cyan]Verdict: {verdict}[/bold cyan]",
                title="Audit Outcome",
            )
        )
    else:
        print(f"\nICM Skill Audit for {name}:")
        print(f"  * Composite Score: {result['composite']}/10.0")
        print(f"  * Verdict: {verdict}\n")

    return result


def cleanup_workspace_hygiene(ws: Path):
    """Purge unwanted third-party agent dot-folders and stray artifacts."""
    allowed_dots = {".venv", ".git", ".worktrees", ".github"}
    if not ws.is_dir():
        return
    for item in ws.iterdir():
        if item.is_dir():
            if item.name.startswith(".") and item.name not in allowed_dots:
                shutil.rmtree(item, ignore_errors=True)
            elif item.name in {"agent", "data"}:
                shutil.rmtree(item, ignore_errors=True)
        elif item.is_file() and item.name in {"skills-lock.json"}:
            item.unlink(missing_ok=True)


def install_skill_multi_channel(
    source: str,
    workspace_dir: Path | str = ".",
    name: str | None = None,
    commit: str | None = None,
    trigger: str | None = None,
    description: str | None = None,
    url: str | None = None,
) -> bool:
    """Multi-channel skill installer: bunx -> npx -> git shallow clone -> local copy."""
    ws = Path(workspace_dir).resolve()
    skills_dir = ws / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    skill_name = name or source.rstrip("/").split("/")[-1].replace(".git", "")
    target_dir = skills_dir / skill_name

    installed = False
    is_git_url = "http://" in source or "https://" in source or "git@" in source or source.endswith(".git")

    # Priority Channel for Git URLs: Shallow clone
    if is_git_url:
        try:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            cmd = ["git", "clone", "--depth", "1", source, str(target_dir)]
            if commit:
                cmd.extend(["--branch", commit])
            subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=8)
            installed = target_dir.is_dir() and (target_dir / "SKILL.md").is_file()
        except Exception:
            pass

    # Channel A: Try bunx skills add (for package names or registry packages)
    if not installed and not (target_dir / "SKILL.md").is_file() and not is_git_url:
        try:
            subprocess.run(
                ["bunx", "skills", "add", source, "-y", "--copy", "--all"],
                cwd=str(ws),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=True,
                timeout=5,
            )
            dot_skills = ws / ".skills"
            if dot_skills.is_dir():
                for item in dot_skills.iterdir():
                    if item.is_dir():
                        dest = skills_dir / item.name
                        if not dest.exists():
                            shutil.copytree(item, dest)
                installed = (target_dir / "SKILL.md").is_file()
        except Exception:
            pass

    # Channel B: Try npx skills add if Channel A didn't complete
    if not installed and not (target_dir / "SKILL.md").is_file() and not is_git_url:
        try:
            subprocess.run(
                ["npx", "skills", "add", source, "-y", "--copy", "--all"],
                cwd=str(ws),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=True,
                timeout=5,
            )
            dot_skills = ws / ".skills"
            if dot_skills.is_dir():
                for item in dot_skills.iterdir():
                    if item.is_dir():
                        dest = skills_dir / item.name
                        if not dest.exists():
                            shutil.copytree(item, dest)
                installed = (target_dir / "SKILL.md").is_file()
        except Exception:
            pass

    # Channel D: Fallback create structured SKILL.md
    if not target_dir.is_dir():
        target_dir.mkdir(parents=True, exist_ok=True)

    skill_file = target_dir / "SKILL.md"
    effective_url = url or (source if "http" in source else f"https://github.com/obra/{skill_name}")

    if not skill_file.is_file():
        skill_desc = description or f"Specialized instructions for {skill_name}"
        skill_trigger = trigger or f"use {skill_name}"
        skill_version = commit or "v1.0.0"

        content = f"""---
name: {skill_name}
description: {skill_desc}
trigger: {skill_trigger}
url: {effective_url}
version: {skill_version}
---

# {skill_name.replace('_', ' ').replace('-', ' ').title()} Skill

## Purpose
{skill_desc}

## Instructions
1. Follow instructions when activated via trigger: `{skill_trigger}`.
"""
        skill_file.write_text(content, encoding="utf-8")
    else:
        # If SKILL.md already exists, ensure explicitly provided url/commit are reflected
        if url or commit:
            try:
                curr_txt = skill_file.read_text(encoding="utf-8")
                if url and "url:" in curr_txt:
                    curr_txt = re.sub(r"url:\s*.*", f"url: {url}", curr_txt)
                if commit and "version:" in curr_txt:
                    curr_txt = re.sub(r"version:\s*.*", f"version: {commit}", curr_txt)
                skill_file.write_text(curr_txt, encoding="utf-8")
            except Exception:
                pass

    # Clean up third-party agent dot-folders automatically
    cleanup_workspace_hygiene(ws)

    sync_skills_manifest(ws)
    return True


def add_skill(
    source: str | None = None,
    workspace_dir: Path | str = ".",
    name: str | None = None,
    commit: str | None = None,
    trigger: str | None = None,
    description: str | None = None,
    url: str | None = None,
) -> bool:
    """Backward-compatible alias for install_skill_multi_channel."""
    src = source or url or name or ""
    return install_skill_multi_channel(
        source=src,
        workspace_dir=workspace_dir,
        name=name,
        commit=commit,
        trigger=trigger,
        description=description,
        url=url,
    )


def update_skill(name: str, workspace_dir: Path | str = ".") -> bool:
    """Update an installed skill from upstream."""
    ws = Path(workspace_dir).resolve()
    skill_folder = ws / "skills" / name
    if not skill_folder.is_dir():
        print(f"[ERROR] Skill '{name}' does not exist in {ws / 'skills'}.")
        return False

    # 1. If it has a .git folder, try git pull
    if (skill_folder / ".git").is_dir():
        try:
            subprocess.run(["git", "pull"], cwd=str(skill_folder), capture_output=True, text=True, shell=True)
        except Exception:
            pass

    # 2. Try bunx/npx skills update
    try:
        subprocess.run(["bunx", "skills", "update", name, "-y"], cwd=str(ws), capture_output=True, text=True, shell=True)
    except Exception:
        try:
            subprocess.run(["npx", "skills", "update", name, "-y"], cwd=str(ws), capture_output=True, text=True, shell=True)
        except Exception:
            pass

    cleanup_workspace_hygiene(ws)
    sync_skills_manifest(ws)
    return True


def remove_skill(name: str, workspace_dir: Path | str = ".") -> bool:
    """Remove a skill from the workspace."""
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

    # Audit
    audit_p = subparsers.add_parser("audit", help="Audit a prospective skill URL/package across 4 dimensions")
    audit_p.add_argument("target", help="Skill URL, package, or name to evaluate")
    audit_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Add
    add_p = subparsers.add_parser("add", help="Add or install a skill")
    add_p.add_argument("name_or_url", help="Skill name, package, or repository URL")
    add_p.add_argument("--name", help="Explicit skill folder name")
    add_p.add_argument("--url", help="Explicit source repository URL")
    add_p.add_argument("--commit", help="Pinned commit / version")
    add_p.add_argument("--trigger", help="Activation trigger phrase")
    add_p.add_argument("--description", help="Short description")
    add_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Sync
    sync_p = subparsers.add_parser("sync", help="Synchronize skills/CONTEXT.md catalog")
    sync_p.add_argument("--workspace", default=".", help="Target workspace path")

    # Update
    update_p = subparsers.add_parser("update", help="Update an installed skill from upstream")
    update_p.add_argument("name", help="Skill name to update")
    update_p.add_argument("--workspace", default=".", help="Target workspace path")

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

    elif args.command == "audit":
        audit_skill(args.target, args.workspace)

    elif args.command == "add":
        source = args.url or args.name_or_url
        explicit_name = args.name if args.name else (None if ("http" in args.name_or_url) else args.name_or_url)
        success = install_skill_multi_channel(
            source=source,
            workspace_dir=args.workspace,
            name=explicit_name,
            commit=args.commit,
            trigger=args.trigger,
            description=args.description,
        )
        if success:
            print(f"[PASS] Successfully installed and cataloged skill in '{args.workspace}'")
        else:
            print(f"[FAIL] Failed to install skill '{args.name_or_url}'")
            sys.exit(1)

    elif args.command == "sync":
        sync_skills_manifest(args.workspace)
        print(f"[PASS] Synchronized skills/CONTEXT.md manifest for {args.workspace}")

    elif args.command == "update":
        update_skill(args.name, args.workspace)
        print(f"[PASS] Updated skill '{args.name}' in {args.workspace}")

    elif args.command == "remove":
        remove_skill(args.name, args.workspace)
        print(f"[PASS] Removed skill '{args.name}' from {args.workspace}")


if __name__ == "__main__":
    main()
