"""
scripts/validate_workspace.py
Audits any target workspace for strict Interpretable Context Methodology (ICM) compliance.
Includes 4-Tier Health Check Engine, Rule Contradiction Inspector, and Interactive Auto-Fix.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


class ValidationResult(tuple):
    """
    Validation outcome tuple for backward and forward compatibility.
    Behaves as (valid, errors) for unpacking, with .warnings, .valid, .errors properties.
    """
    def __new__(cls, valid: bool, errors: list[str], warnings: list[str] | None = None):
        return super().__new__(cls, (valid, errors))

    def __init__(self, valid: bool, errors: list[str], warnings: list[str] | None = None):
        self.valid = valid
        self.errors = errors
        self.warnings = warnings or []

    def full(self) -> tuple[bool, list[str], list[str]]:
        return (self.valid, self.errors, self.warnings)


def detect_git_and_prompt_safety(workspace_path: Path | str, non_interactive: bool = False) -> tuple[bool, str]:
    path = Path(workspace_path).resolve()
    # Check if inside git repository
    current = path
    is_git = False
    while current != current.parent:
        if (current / ".git").exists():
            is_git = True
            break
        current = current.parent

    if is_git:
        advice = (
            "[Git Safety Advisory]: Active git repository detected. "
            "It is strongly advised to run automated repairs on an isolated branch "
            "(e.g., `git checkout -b chore/icm-governance-fix`) or in a dedicated git worktree."
        )
        if not non_interactive and hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
            try:
                print(f"\n{advice}\n")
                ans = input("Proceed with auto-fix on current workspace state? [y/N]: ").strip().lower()
                if ans not in ["y", "yes"]:
                    print("Auto-fix aborted by user for git safety.")
                    return False, advice
            except (EOFError, KeyboardInterrupt):
                return False, advice
        return True, advice
    return True, "No git repository detected."


def auto_fix_workspace(workspace_path: Path | str) -> list[str]:
    path = Path(workspace_path).resolve()
    fixes_applied: list[str] = []

    # 1. Fix missing stage output directories
    stages_to_check: list[Path] = []
    if (path / "stages").is_dir():
        stages_to_check.extend([d for d in (path / "stages").iterdir() if d.is_dir()])
    if (path / "workflows").is_dir():
        for wf in (path / "workflows").iterdir():
            if wf.is_dir() and (wf / "stages").is_dir():
                stages_to_check.extend([d for d in (wf / "stages").iterdir() if d.is_dir()])

    for stage in stages_to_check:
        output_dir = stage / "output"
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / ".gitkeep").write_text(f"# Output directory for {stage.name}\n", encoding="utf-8")
            fixes_applied.append(f"Created missing output directory: {stage.name}/output/")
        elif not any(output_dir.iterdir()):
            (output_dir / ".gitkeep").write_text(f"# Output directory for {stage.name}\n", encoding="utf-8")
            fixes_applied.append(f"Added .gitkeep to empty output directory: {stage.name}/output/")

    # 2. Fix missing resources/quality_standards.md
    if (path / "resources").exists() and not (path / "resources" / "quality_standards.md").exists():
        (path / "resources" / "quality_standards.md").write_text(
            "# Project Quality Standards (Layer 3)\n\n1. Define project constraints and guidelines here.\n",
            encoding="utf-8",
        )
        fixes_applied.append("Created missing resources/quality_standards.md")
    elif (path / "resources" / "rules.md").exists():
        (path / "resources" / "rules.md").rename(path / "resources" / "quality_standards.md")
        fixes_applied.append("Migrated rules.md to quality_standards.md")

    # 3. Sync skills manifest if skills/ has subdirectories
    skills_dir = path / "skills"
    if skills_dir.is_dir() and any(d.is_dir() for d in skills_dir.iterdir()):
        from scripts.manage_skills import sync_skills_manifest
        sync_skills_manifest(path)
        fixes_applied.append("Synchronized skills/CONTEXT.md manifest")

    return fixes_applied


def check_structural_integrity(path: Path) -> tuple[list[str], list[str], str]:
    errors: list[str] = []
    warnings: list[str] = []
    topology = "Unknown"

    # Layer 0 check
    has_l0 = (path / "AGENT.md").is_file() or (path / "CLAUDE.md").is_file() or (path / "GEMINI.md").is_file()
    if not has_l0:
        errors.append("Layer 0 missing: Workspace must contain AGENT.md (or CLAUDE.md / GEMINI.md)")

    # Layer 1 check
    has_l1 = (path / "CONTEXT.md").is_file()
    if not has_l1:
        errors.append("Layer 1 missing: Workspace must contain root CONTEXT.md for task routing")

    # Check stages vs workflows
    has_stages = (path / "stages").is_dir()
    has_workflows = (path / "workflows").is_dir()
    has_docs = (path / "docs").is_dir()

    if has_workflows and has_docs:
        topology = "Topology 4 (Enterprise Multi-Workflow & PM)"
    elif has_workflows:
        topology = "Topology 3 (Multi-Workflow)"
    elif has_stages and has_docs:
        topology = "Topology 2 (Managed Single-Pipeline)"
    elif has_stages:
        topology = "Topology 1 (Lean Single-Pipeline)"
    else:
        errors.append("Structure missing: Workspace must contain either a 'stages/' or 'workflows/' directory")

    def audit_stage_list(stage_dirs: list[Path], prefix: str = ""):
        for idx, stage in enumerate(stage_dirs, start=1):
            match = re.match(r"^(\d{2})_(.+)$", stage.name)
            if not match:
                errors.append(f"Stage '{prefix}{stage.name}' violates numbering pattern (must be NN_stagename e.g. 01_discovery)")
            else:
                stage_num = int(match.group(1))
                if stage_num != idx:
                    errors.append(f"Stage '{prefix}{stage.name}' is out of sequence (expected {idx:02d}, got {stage_num:02d})")

            stage_context = stage / "CONTEXT.md"
            if not stage_context.is_file():
                errors.append(f"Stage '{prefix}{stage.name}' missing Layer 2 contract: CONTEXT.md")
            else:
                content = stage_context.read_text(encoding="utf-8")
                if "## Inputs" not in content:
                    errors.append(f"Stage '{prefix}{stage.name}' CONTEXT.md missing '## Inputs' section")
                if "## Process" not in content:
                    errors.append(f"Stage '{prefix}{stage.name}' CONTEXT.md missing '## Process' section")
                if "## Outputs" not in content:
                    errors.append(f"Stage '{prefix}{stage.name}' CONTEXT.md missing '## Outputs' section")

            output_dir = stage / "output"
            if not output_dir.is_dir():
                errors.append(f"Stage '{prefix}{stage.name}' missing Layer 4 'output/' folder")

    if has_stages:
        stage_dirs = sorted([d for d in (path / "stages").iterdir() if d.is_dir()])
        if not stage_dirs:
            errors.append("No stages found in 'stages/' folder")
        else:
            audit_stage_list(stage_dirs)

    if has_workflows:
        wf_dirs = sorted([d for d in (path / "workflows").iterdir() if d.is_dir()])
        if not wf_dirs:
            errors.append("No workflows found in 'workflows/' folder")
        else:
            for wf in wf_dirs:
                wf_stages_dir = wf / "stages"
                if not wf_stages_dir.is_dir():
                    errors.append(f"Workflow '{wf.name}' missing 'stages/' directory")
                else:
                    wf_stages = sorted([d for d in wf_stages_dir.iterdir() if d.is_dir()])
                    if not wf_stages:
                        errors.append(f"Workflow '{wf.name}' has no stages in 'stages/'")
                    else:
                        audit_stage_list(wf_stages, prefix=f"{wf.name}/")

    return errors, warnings, topology


def check_dead_context_and_orphans(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    link_pattern = re.compile(r"\[.*?\]\((?:file://)?(?:\./)?([a-zA-Z0-9_\-/\.]+)\)")

    # Scan markdown files for dead links (excluding third-party skills and build caches)
    for md_file in path.glob("**/*.md"):
        parts = md_file.parts
        if any(p in [".git", ".venv", "node_modules", ".pytest_cache", "templates", "skills"] for p in parts):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Strip fenced code blocks to avoid checking illustrative code examples
        clean_content = re.sub(r"```[\s\S]*?```", "", content)

        for match in link_pattern.finditer(clean_content):
            target = match.group(1).strip()
            # Skip URLs, anchor links, or template variables
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#") or "{" in target or "}" in target:
                continue

            # Determine nearest workspace or archetype root
            current_root = path
            for parent in md_file.parents:
                if (parent / "AGENT.md").is_file() or (parent / "CONTEXT.md").is_file():
                    current_root = parent
                    break

            rel_to_file = md_file.parent / target
            rel_to_current_root = current_root / target
            rel_to_root = path / target

            if not rel_to_file.exists() and not rel_to_current_root.exists() and not rel_to_root.exists():
                warnings.append(f"Dead link in {md_file.relative_to(path)}: target '{target}' does not exist")

    return errors, warnings


def check_cross_layer_rule_contradictions(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Check for forbidden package managers in workspace contracts (excluding third-party skills)
    forbidden_pattern = re.compile(r"\b(npm\s+install|npx\s+|yarn\s+add|pnpm\s+add)\b", re.IGNORECASE)

    for md_file in path.glob("**/*.md"):
        parts = md_file.parts
        if any(p in [".git", ".venv", "node_modules", ".pytest_cache", "skills"] for p in parts):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        match = forbidden_pattern.search(content)
        if match:
            errors.append(
                f"Rule Contradiction in {md_file.relative_to(path)}: "
                f"Forbidden package manager command '{match.group(0)}' found. "
                "ICM projects exclusively enforce 'bun'/'bunx' and 'uv run'."
            )

    return errors, warnings


def check_task_governance_and_skills(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Check docs/phases/ if present
    phases_dir = path / "docs" / "phases"
    if phases_dir.is_dir():
        phase_subdirs = [d for d in phases_dir.iterdir() if d.is_dir()]
        for phase in phase_subdirs:
            goals_file = phase / "goals.md"
            tasks_file = phase / "tasks.md"
            if not goals_file.is_file():
                errors.append(f"Phase '{phase.name}' missing goals.md")
            if not tasks_file.is_file():
                errors.append(f"Phase '{phase.name}' missing tasks.md")
            else:
                tasks_text = tasks_file.read_text(encoding="utf-8")
                if not re.search(r"TASK-\d{2}-[A-Z0-9]+", tasks_text) and "TASK-" not in tasks_text:
                    warnings.append(f"Phase '{phase.name}' tasks.md does not follow canonical TASK-NN-XXX formatting")

    # Check skills/ if present
    skills_dir = path / "skills"
    if skills_dir.is_dir():
        context_file = skills_dir / "CONTEXT.md"
        if not context_file.is_file():
            errors.append("skills/ directory exists but missing skills/CONTEXT.md manifest")
        else:
            manifest_text = context_file.read_text(encoding="utf-8")
            # Verify listed skills exist on disk
            for line in manifest_text.splitlines():
                line = line.strip()
                if not line.startswith("|") or "---" in line or "skill name" in line.lower() or ("path" in line.lower() and "trigger" in line.lower()):
                    continue
                cols = [c.strip().strip("`") for c in line.split("|")[1:-1]]
                if len(cols) >= 2:
                    s_name = cols[0]
                    if s_name and s_name.lower() not in ["skill name", "---", "_none_"]:
                        skill_path = skills_dir / s_name / "SKILL.md"
                        if not skill_path.is_file():
                            errors.append(f"Skill '{s_name}' is listed in skills/CONTEXT.md but missing '{skill_path.relative_to(path)}'")

    # Check agents/ if present
    agents_dir = path / "agents"
    if agents_dir.is_dir():
        agents_ctx = agents_dir / "CONTEXT.md"
        if not agents_ctx.is_file():
            errors.append("agents/ directory exists but missing agents/CONTEXT.md routing manifest")
        else:
            ctx_text = agents_ctx.read_text(encoding="utf-8")
            if not any(line.strip().startswith("|") for line in ctx_text.splitlines()):
                warnings.append("agents/CONTEXT.md does not contain a Markdown dispatch table")

        # Audit each agent chamber
        for chamber in agents_dir.iterdir():
            if chamber.is_dir():
                agent_file = chamber / "AGENT.md"
                if not agent_file.is_file():
                    errors.append(f"Agent chamber '{chamber.name}' missing AGENT.md contract")
                else:
                    agent_text = agent_file.read_text(encoding="utf-8")
                    lines = [l.strip() for l in agent_text.splitlines() if l.strip()]
                    top_block = "\n".join(lines[:10])
                    if "**Purpose:**" not in top_block and "**Mission:**" not in top_block:
                        warnings.append(f"Agent chamber '{chamber.name}' AGENT.md missing top-level '**Purpose:**' or '**Mission:**'")
                    if "* **Forbidden:**" not in agent_text and "**Forbidden:**" not in agent_text:
                        warnings.append(f"Agent chamber '{chamber.name}' AGENT.md missing explicit negative guardrails ('* **Forbidden:**')")

                    # Verify skills listed in chamber AGENT.md exist if pointing to workspace skills
                    if skills_dir.is_dir():
                        for line in agent_text.splitlines():
                            line = line.strip()
                            if line.startswith("|") and ("skills/" in line or "`skills/" in line):
                                for part in line.split("|"):
                                    m = re.search(r"skills/([a-zA-Z0-9_\-]+)", part)
                                    if m:
                                        skill_name = m.group(1)
                                        if not (skills_dir / skill_name).is_dir() and not (skills_dir / skill_name / "SKILL.md").is_file():
                                            warnings.append(f"Agent chamber '{chamber.name}' references skill '{skill_name}' not found in workspace skills/")

    return errors, warnings


def check_high_signal_formatting(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Forbidden meta-tags that violate zero-jargon standard (matched at tag positions)
    forbidden_meta_tags = [
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}BLUF\s*:", re.IGNORECASE),
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}ADHD\s+(Mode|Protocol)\b", re.IGNORECASE),
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}Caveman\s+Mode\b", re.IGNORECASE),
    ]

    # Files to check for high-signal formatting
    files_to_check: list[Path] = []
    for f_name in ["AGENT.md", "CONTEXT.md", "CLAUDE.md"]:
        f_path = path / f_name
        if f_path.is_file():
            files_to_check.append(f_path)

    # Check stage CONTEXT.md files
    if (path / "stages").is_dir():
        files_to_check.extend(path.glob("stages/*/CONTEXT.md"))
    if (path / "workflows").is_dir():
        files_to_check.extend(path.glob("workflows/*/stages/*/CONTEXT.md"))
    if (path / "agents").is_dir():
        files_to_check.extend(path.glob("agents/**/AGENT.md"))
        if (path / "agents" / "CONTEXT.md").is_file():
            files_to_check.append(path / "agents" / "CONTEXT.md")

    for f_path in files_to_check:
        try:
            text = f_path.read_text(encoding="utf-8")
        except Exception:
            continue

        rel_path = f_path.relative_to(path)

        # Check for forbidden meta-tags
        for tag_re in forbidden_meta_tags:
            match = tag_re.search(text)
            if match:
                errors.append(
                    f"High-Signal Violation in {rel_path}: Forbidden meta-tag/jargon '{match.group(0)}' found. "
                    "Use native Markdown formatting (Purpose + Tables + Bold Keys) without third-party tags."
                )

        # Check for Purpose / Mission in AGENT.md, CONTEXT.md, and stage CONTEXT.md
        if f_path.name in ["AGENT.md", "CONTEXT.md"] and not (rel_path.parts[0] == "skills"):
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            top_block = "\n".join(lines[:10])
            if "**Purpose:**" not in top_block and "**Mission:**" not in top_block and "Mission:" not in top_block and "Purpose:" not in top_block:
                warnings.append(f"High-Signal Advisory in {rel_path}: Missing top-level '**Purpose:**' or '**Mission:**' statement beneath H1.")

    return errors, warnings


def validate_workspace(
    workspace_path: Path | str,
    fix: bool = False,
    non_interactive: bool = True,
) -> ValidationResult:
    path = Path(workspace_path).resolve()
    
    if not path.exists() or not path.is_dir():
        return ValidationResult(False, [f"Directory does not exist: {path}"], [])

    if fix:
        allowed, _ = detect_git_and_prompt_safety(path, non_interactive=non_interactive)
        if allowed:
            auto_fix_workspace(path)

    all_errors: list[str] = []
    all_warnings: list[str] = []

    # Tier 1: Structural Integrity
    t1_errs, t1_warns, _ = check_structural_integrity(path)
    all_errors.extend(t1_errs)
    all_warnings.extend(t1_warns)

    # Tier 2: Dead Context & Orphans
    t2_errs, t2_warns = check_dead_context_and_orphans(path)
    all_errors.extend(t2_errs)
    all_warnings.extend(t2_warns)

    # Tier 3: Cross-Layer Rule Contradictions
    t3_errs, t3_warns = check_cross_layer_rule_contradictions(path)
    all_errors.extend(t3_errs)
    all_warnings.extend(t3_warns)

    # Tier 4: Task Governance & Skills Health
    t4_errs, t4_warns = check_task_governance_and_skills(path)
    all_errors.extend(t4_errs)
    all_warnings.extend(t4_warns)

    # Tier 5: High-Signal Contract & Voice Linter
    t5_errs, t5_warns = check_high_signal_formatting(path)
    all_errors.extend(t5_errs)
    all_warnings.extend(t5_warns)

    is_valid = len(all_errors) == 0
    return ValidationResult(is_valid, all_errors, all_warnings)


def main():
    parser = argparse.ArgumentParser(description="Audit an ICM workspace for 4-tier health compliance.")
    parser.add_argument("path", nargs="?", default=".", help="Path to workspace directory (default: current dir)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix repairable structure issues")
    parser.add_argument("--yes", "-y", action="store_true", help="Non-interactive mode (auto-accept git safety prompt)")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    print(f"\n[*] Auditing ICM Workspace: {target_path}\n" + "-" * 60)

    res = validate_workspace(target_path, fix=args.fix, non_interactive=args.yes)

    if console:
        if res.valid:
            console.print(Panel("[bold green]PASS: Workspace is 100% ICM Compliant![/bold green]"))
        else:
            console.print(Panel(f"[bold red]FAIL: Found {len(res.errors)} compliance violation(s)[/bold red]"))
            for err in res.errors:
                console.print(f"  [red]✗[/red] {err}")

        if res.warnings:
            console.print("\n[yellow]Warnings / Non-Blocking Issues:[/yellow]")
            for warn in res.warnings:
                console.print(f"  [yellow]![/yellow] {warn}")
    else:
        if res.valid:
            print("[PASS] Workspace is 100% ICM Compliant!\n")
        else:
            print("[FAIL] Workspace has compliance violations:\n")
            for err in res.errors:
                print(f"  * {err}")
            print()

        if res.warnings:
            print("Warnings / Non-Blocking Issues:\n")
            for warn in res.warnings:
                print(f"  ! {warn}")
            print()

    sys.exit(0 if res.valid else 1)


if __name__ == "__main__":
    main()
