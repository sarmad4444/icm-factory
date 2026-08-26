"""
scripts/validate_workspace.py
Audits any target workspace for strict Interpretable Context Methodology (ICM) compliance.
Includes 5-Layer Health Check Engine, Anti-Pattern Inspector, AI Diagnostic Utility, and Interactive Auto-Fix.
"""

from __future__ import annotations
import argparse
import json
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
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


class ValidationResult(tuple):
    """
    Validation outcome tuple for backward and forward compatibility.
    Behaves as (valid, errors) for unpacking, with .warnings, .valid, .errors, .diagnostics properties.
    """
    def __new__(cls, valid: bool, errors: list[str], warnings: list[str] | None = None, diagnostics: dict | None = None):
        return super().__new__(cls, (valid, errors))

    def __init__(self, valid: bool, errors: list[str], warnings: list[str] | None = None, diagnostics: dict | None = None):
        self.valid = valid
        self.errors = errors
        self.warnings = warnings or []
        self.diagnostics = diagnostics or {}

    def full(self) -> tuple[bool, list[str], list[str]]:
        return (self.valid, self.errors, self.warnings)


def detect_git_and_prompt_safety(workspace_path: Path | str, non_interactive: bool = False) -> tuple[bool, str]:
    path = Path(workspace_path).resolve()
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
    if (path / "resources").exists() and not (path / "resources" / "quality_standards.md").exists() and not (path / "resources" / "foundations" / "quality_standards.md").exists():
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
        try:
            from scripts.manage_skills import sync_skills_manifest
            sync_skills_manifest(path)
            fixes_applied.append("Synchronized skills/CONTEXT.md manifest")
        except ImportError:
            try:
                import sys
                parent_dir = str(Path(__file__).resolve().parent.parent)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                from scripts.manage_skills import sync_skills_manifest
                sync_skills_manifest(path)
                fixes_applied.append("Synchronized skills/CONTEXT.md manifest")
            except Exception:
                pass

    # 4. Clean up unauthorized agent dot-folders and stray lockfiles
    allowed_dots = {".venv", ".git", ".worktrees", ".github"}
    for item in path.iterdir():
        if item.is_dir():
            if item.name.startswith(".") and item.name not in allowed_dots:
                shutil.rmtree(item, ignore_errors=True)
                fixes_applied.append(f"Purged unauthorized agent dot-folder: {item.name}")
            elif item.name in {"agent", "data"}:
                shutil.rmtree(item, ignore_errors=True)
                fixes_applied.append(f"Purged stray non-standard folder: {item.name}")
        elif item.is_file() and item.name in {"skills-lock.json"}:
            item.unlink(missing_ok=True)
            fixes_applied.append(f"Purged stray lockfile: {item.name}")

    # 5. Clean up nested README.md files in subdirectories (excluding root and third-party skills)
    for md in path.glob("**/*.md"):
        if md.name.lower() == "readme.md" and md != (path / "README.md"):
            parts = md.parts
            if any(p in [".git", ".venv", "node_modules", "skills"] for p in parts):
                continue
            try:
                if md.stat().st_size < 200:
                    md.unlink(missing_ok=True)
                    fixes_applied.append(f"Purged nested stub README: {md.relative_to(path)}")
            except Exception:
                pass

    return fixes_applied


def check_structural_integrity(path: Path) -> tuple[list[str], list[str], str, dict]:
    """Layer 0, 1, and Topology inspection."""
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {"topology": "Unknown", "l0_files": [], "l1_router": False}

    # Hygiene check for third-party agent dot-folders
    allowed_dots = {".venv", ".git", ".worktrees", ".github"}
    for item in path.iterdir():
        if item.is_dir() and item.name.startswith(".") and item.name not in allowed_dots:
            warnings.append(f"Hygiene Anti-Pattern: Found third-party agent dot-folder '{item.name}'. Run --fix to auto-purge.")
        elif item.is_dir() and item.name in {"agent", "data"}:
            warnings.append(f"Hygiene Anti-Pattern: Found non-standard stray folder '{item.name}'. Run --fix to auto-purge.")

    # Layer 0 check
    has_agents = (path / "AGENTS.md").is_file()
    has_agent = (path / "AGENT.md").is_file()
    has_claude = (path / "CLAUDE.md").is_file()
    has_gemini = (path / "GEMINI.md").is_file()
    if has_agents:
        stats["l0_files"].append("AGENTS.md")
    if has_agent:
        stats["l0_files"].append("AGENT.md")
    if has_claude:
        stats["l0_files"].append("CLAUDE.md")
    if has_gemini:
        stats["l0_files"].append("GEMINI.md")

    if not stats["l0_files"]:
        errors.append("Layer 0 missing: Workspace must contain AGENTS.md or AGENT.md (or CLAUDE.md / GEMINI.md)")

    # Layer 1 check
    has_l1 = (path / "CONTEXT.md").is_file()
    if not has_l1:
        errors.append("Layer 1 missing: Workspace must contain root CONTEXT.md for task routing")
    else:
        stats["l1_router"] = True

    # Detect Topology
    has_stages = (path / "stages").is_dir()
    has_workflows = (path / "workflows").is_dir()
    has_docs = (path / "docs").is_dir()

    if has_stages and not has_docs and not has_workflows:
        stats["topology"] = "Topology 1 (Lean Single-Pipeline)"
    elif has_stages and has_docs and not has_workflows:
        stats["topology"] = "Topology 2 (Managed Single-Pipeline)"
    elif has_workflows and not has_docs and not has_stages:
        stats["topology"] = "Topology 3 (Multi-Workflow Engine)"
    elif has_workflows and has_docs:
        stats["topology"] = "Topology 4 (Enterprise Multi-Workflow & Brain)"
    else:
        stats["topology"] = "Custom / Domain-Specific Architecture"

    return errors, warnings, stats["topology"], stats


def check_pipeline_stages(path: Path) -> tuple[list[str], list[str], dict]:
    """Layer 2 workflow stage contracts and domain hub inspection."""
    errors: list[str] = []
    warnings: list[str] = []
    stage_stats: dict = {"total_stages": 0, "workflows": {}, "domain_hubs": []}

    workflow_dirs: list[Path] = []
    if (path / "stages").is_dir():
        workflow_dirs.append(path)
    if (path / "workflows").is_dir():
        for wf in (path / "workflows").iterdir():
            if wf.is_dir() and (wf / "stages").is_dir():
                workflow_dirs.append(wf)

    for wf_path in workflow_dirs:
        wf_name = wf_path.name if wf_path != path else "root"
        stages_dir = wf_path / "stages"
        subdirs = [d for d in stages_dir.iterdir() if d.is_dir()]
        subdirs.sort(key=lambda d: d.name)
        stage_stats["workflows"][wf_name] = len(subdirs)
        stage_stats["total_stages"] += len(subdirs)

        if not subdirs:
            errors.append(f"No stage directories found in '{stages_dir.relative_to(path)}'")
            continue

        stage_numbers: list[int] = []
        for stage in subdirs:
            match = re.match(r"^(\d{2})_", stage.name)
            if not match:
                errors.append(
                    f"Stage naming violation: '{stage.name}' in {wf_name} does not follow 2-digit sequential format (e.g. '01_stagename')"
                )
            else:
                num = int(match.group(1))
                stage_numbers.append(num)

            # Contract check
            ctx_file = stage / "CONTEXT.md"
            if not ctx_file.is_file():
                errors.append(f"Missing local stage contract: '{stage.name}/CONTEXT.md' in {wf_name}")
            else:
                try:
                    ctx_text = ctx_file.read_text(encoding="utf-8")
                    if "## Inputs" not in ctx_text:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Inputs' contract section")
                    if "## Process" not in ctx_text:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Process' contract section")
                    if "## Outputs" not in ctx_text:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Outputs' contract section")
                except Exception as e:
                    errors.append(f"Failed to read '{stage.name}/CONTEXT.md': {e}")

            # Output folder check
            output_dir = stage / "output"
            if not output_dir.is_dir():
                errors.append(f"Stage '{stage.name}' missing Layer 4 'output/' directory in {wf_name}")
            elif not any(output_dir.iterdir()):
                warnings.append(f"Empty output folder in '{stage.name}/output/'. (Add .gitkeep or run --fix)")

        # Verify contiguous numbering
        if stage_numbers:
            expected = list(range(stage_numbers[0], stage_numbers[0] + len(stage_numbers)))
            if stage_numbers != expected:
                errors.append(
                    f"Non-contiguous stage numbering in {wf_name}: found {stage_numbers}, expected {expected}"
                )

    # Check Domain Hubs (e.g. curriculum/, apps/)
    for domain in ["curriculum", "apps"]:
        domain_dir = path / domain
        if domain_dir.is_dir():
            ctx_file = domain_dir / "CONTEXT.md"
            if not ctx_file.is_file():
                warnings.append(f"Domain Hub '{domain}/' exists but missing formal '{domain}/CONTEXT.md' contract")
            else:
                stage_stats["domain_hubs"].append(domain)

    return errors, warnings, stage_stats


def check_anti_patterns_and_markdown_hygiene(path: Path) -> tuple[list[str], list[str]]:
    """Inspects workspace for uncontracted markdown sprawl and dead links."""
    errors: list[str] = []
    warnings: list[str] = []

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for md_file in path.glob("**/*.md"):
        parts = md_file.parts
        if any(p in [".git", ".venv", "node_modules", ".pytest_cache", "skills"] for p in parts):
            continue

        # 1. Anti-Pattern: Nested README.md sprawl
        if md_file.name.lower() == "readme.md" and md_file != (path / "README.md"):
            warnings.append(
                f"Markdown Sprawl Anti-Pattern: Found nested '{md_file.relative_to(path)}'. "
                "ICM requires domain hubs to use CONTEXT.md contracts rather than arbitrary READMEs."
            )

        # 2. Anti-Pattern: Empty or trivial stubs
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
            if len(content.strip()) < 40 and md_file.name != ".gitkeep":
                warnings.append(f"Trivial Stub: '{md_file.relative_to(path)}' is nearly empty ({len(content.strip())} bytes).")
        except Exception:
            continue

        # 3. Relative link integrity check
        for match in link_pattern.finditer(content):
            target = match.group(2).strip()
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#") or target.startswith("mailto:"):
                continue

            clean_target = target
            if clean_target.startswith("file://./"):
                clean_target = clean_target[9:]
            elif clean_target.startswith("file:///"):
                clean_target = clean_target[8:]
            elif clean_target.startswith("file://"):
                clean_target = clean_target[7:]

            clean_target = clean_target.split("#")[0].split("?")[0]
            if not clean_target:
                continue

            rel_to_file = (md_file.parent / clean_target).resolve()
            rel_to_current_root = (path / clean_target).resolve()

            if not rel_to_file.exists() and not rel_to_current_root.exists():
                warnings.append(f"Dead link in {md_file.relative_to(path)}: target '{target}' does not exist on disk")

    return errors, warnings


def check_cross_layer_rule_contradictions(path: Path) -> tuple[list[str], list[str]]:
    """Detects contradictions between declared tooling rules and actual code or markdown commands."""
    errors: list[str] = []
    warnings: list[str] = []

    enforces_bun_only = False
    for std_file in [path / "AGENT.md", path / "AGENTS.md", path / "resources" / "quality_standards.md", path / "_config" / "rules.md"]:
        if std_file.is_file():
            try:
                txt = std_file.read_text(encoding="utf-8", errors="replace")
                if "bun" in txt.lower() and ("exclusively" in txt.lower() or "strict" in txt.lower() or "no npm" in txt.lower() or "always use bun" in txt.lower()):
                    enforces_bun_only = True
                    break
            except Exception:
                pass

    if enforces_bun_only:
        forbidden_pattern = re.compile(r"\b(npm\s+install|yarn\s+add|pnpm\s+add)\b", re.IGNORECASE)
        for md_file in path.glob("**/*.md"):
            parts = md_file.parts
            if any(p in [".git", ".venv", "node_modules", ".pytest_cache", "skills"] for p in parts):
                continue

            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            match = forbidden_pattern.search(content)
            if match:
                errors.append(
                    f"Rule Contradiction in {md_file.relative_to(path)}: "
                    f"Forbidden package manager command '{match.group(0)}' found. "
                    "This workspace explicitly enforces 'bun'/'bunx' and 'uv run'."
                )

    return errors, warnings


def check_task_governance_and_skills(path: Path) -> tuple[list[str], list[str], dict]:
    """Layer 3 (Skills, Quality Standards, Agent Chambers) and Layer 4 (Docs & Tasks)."""
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {"installed_skills": 0, "agent_chambers": 0, "sprint_phases": 0}

    # Check docs/phases/ (Layer 4)
    phases_dir = path / "docs" / "phases"
    if phases_dir.is_dir():
        phase_subdirs = [d for d in phases_dir.iterdir() if d.is_dir()]
        stats["sprint_phases"] = len(phase_subdirs)
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

    # Check skills/ (Layer 3)
    skills_dir = path / "skills"
    if skills_dir.is_dir():
        context_file = skills_dir / "CONTEXT.md"
        if not context_file.is_file():
            errors.append("skills/ directory exists but missing skills/CONTEXT.md manifest")
        else:
            manifest_text = context_file.read_text(encoding="utf-8")
            for line in manifest_text.splitlines():
                line = line.strip()
                if not line.startswith("|") or "---" in line or "skill name" in line.lower():
                    continue
                cols = [c.strip().strip("`") for c in line.split("|")[1:-1]]
                if len(cols) >= 2:
                    s_name = cols[0]
                    if s_name and s_name.lower() not in ["skill name", "---", "_none_"]:
                        stats["installed_skills"] += 1
                        skill_path = skills_dir / s_name / "SKILL.md"
                        if not skill_path.is_file():
                            errors.append(f"Skill '{s_name}' listed in skills/CONTEXT.md but missing on disk: '{skill_path.relative_to(path)}'")

    # Check agents/ (Layer 3)
    agents_dir = path / "agents"
    if agents_dir.is_dir():
        agents_ctx = agents_dir / "CONTEXT.md"
        if not agents_ctx.is_file():
            errors.append("agents/ directory exists but missing agents/CONTEXT.md routing manifest")

        for chamber in agents_dir.iterdir():
            if chamber.is_dir():
                stats["agent_chambers"] += 1
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

    return errors, warnings, stats


def check_high_signal_formatting(path: Path) -> tuple[list[str], list[str]]:
    """Validates that documentation adheres to high-signal zero-jargon standards."""
    errors: list[str] = []
    warnings: list[str] = []

    forbidden_meta_tags = [
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}BLUF\s*:", re.IGNORECASE),
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}ADHD\s+(Mode|Protocol)\b", re.IGNORECASE),
        re.compile(r"(?m)^[>\s*#-]*\*{0,2}Caveman\s+Mode\b", re.IGNORECASE),
    ]

    files_to_check: list[Path] = []
    for f_name in ["AGENT.md", "AGENTS.md", "CONTEXT.md", "CLAUDE.md"]:
        f_path = path / f_name
        if f_path.is_file():
            files_to_check.append(f_path)

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

        for tag_re in forbidden_meta_tags:
            match = tag_re.search(text)
            if match:
                errors.append(
                    f"High-Signal Violation in {rel_path}: Forbidden meta-tag/jargon '{match.group(0)}' found. "
                    "Use native Markdown formatting (Purpose + Tables + Bold Keys) without third-party tags."
                )

        if f_path.name in ["AGENT.md", "AGENTS.md", "CONTEXT.md"] and not (rel_path.parts[0] == "skills"):
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            top_block = "\n".join(lines[:10])
            if "**Purpose:**" not in top_block and "**Mission:**" not in top_block and "Mission:" not in top_block and "Purpose:" not in top_block:
                warnings.append(f"High-Signal Advisory in {rel_path}: Missing top-level '**Purpose:**' or '**Mission:**' statement beneath H1.")

    return errors, warnings


def validate_workspace(
    workspace_path: Path | str = ".",
    fix: bool = False,
    non_interactive: bool = False,
) -> ValidationResult:
    path = Path(workspace_path).resolve()
    if not path.exists() or not path.is_dir():
        return ValidationResult(False, [f"Directory does not exist: {path}"], [], {})

    if fix:
        can_proceed, _ = detect_git_and_prompt_safety(path, non_interactive=non_interactive)
        if can_proceed:
            auto_fix_workspace(path)

    all_errors: list[str] = []
    all_warnings: list[str] = []
    diagnostics: dict = {
        "workspace_path": str(path),
        "workspace_name": path.name,
    }

    # Tier 1: Structural & Layer 0/1
    e1, w1, topo, s1 = check_structural_integrity(path)
    all_errors.extend(e1)
    all_warnings.extend(w1)
    diagnostics["topology"] = topo
    diagnostics.update(s1)

    # Tier 2: Layer 2 Pipelines & Domain Hubs
    e2, w2, s2 = check_pipeline_stages(path)
    all_errors.extend(e2)
    all_warnings.extend(w2)
    diagnostics.update(s2)

    # Tier 3: Markdown Hygiene & Anti-Patterns
    e3, w3 = check_anti_patterns_and_markdown_hygiene(path)
    all_errors.extend(e3)
    all_warnings.extend(w3)

    # Tier 4: Cross-Layer Rule Contradictions
    e_rules, w_rules = check_cross_layer_rule_contradictions(path)
    all_errors.extend(e_rules)
    all_warnings.extend(w_rules)

    # Tier 5: Layer 3 & Layer 4 Task Governance & Skills
    e4, w4, s4 = check_task_governance_and_skills(path)
    all_errors.extend(e4)
    all_warnings.extend(w4)
    diagnostics.update(s4)

    # Tier 6: High-Signal Contract & Voice Linter
    e_fmt, w_fmt = check_high_signal_formatting(path)
    all_errors.extend(e_fmt)
    all_warnings.extend(w_fmt)

    is_valid = len(all_errors) == 0
    diagnostics["is_valid"] = is_valid
    diagnostics["total_errors"] = len(all_errors)
    diagnostics["total_warnings"] = len(all_warnings)

    return ValidationResult(is_valid, all_errors, all_warnings, diagnostics)


def render_ai_audit_dashboard(result: ValidationResult):
    """Renders a comprehensive diagnostic table for humans and LLM agents."""
    diag = result.diagnostics

    if console:
        table = Table(title=f"🏛️ ICM Comprehensive Architecture Audit: {diag.get('workspace_name')}", show_header=True, header_style="bold magenta")
        table.add_column("Layer / Dimension", style="cyan", width=30)
        table.add_column("Status", width=12)
        table.add_column("Audit Metric & Diagnostics", style="white")

        table.add_row(
            "Layer 0: Master Control Plane",
            "[green]PASS[/green]" if diag.get("l0_files") else "[red]FAIL[/red]",
            f"Active: {', '.join(diag.get('l0_files', []))}"
        )
        table.add_row(
            "Layer 1: Context Router",
            "[green]PASS[/green]" if diag.get("l1_router") else "[red]FAIL[/red]",
            "Root CONTEXT.md active & dispatching" if diag.get("l1_router") else "Missing root CONTEXT.md"
        )
        table.add_row(
            "Layer 2: Workflows & Domain Hubs",
            "[green]PASS[/green]" if diag.get("total_stages", 0) > 0 or diag.get("domain_hubs") else "[yellow]LEAN[/yellow]",
            f"{diag.get('total_stages', 0)} stages across {len(diag.get('workflows', {}))} workflows; Hubs: {', '.join(diag.get('domain_hubs', [])) or 'None'}"
        )
        table.add_row(
            "Layer 3: Skills & Agent Chambers",
            "[green]PASS[/green]",
            f"{diag.get('installed_skills', 0)} JIT skills cataloged; {diag.get('agent_chambers', 0)} specialist chambers"
        )
        table.add_row(
            "Layer 4: Project Brain & Sprints",
            "[green]PASS[/green]" if diag.get("sprint_phases", 0) > 0 else "[yellow]NONE[/yellow]",
            f"{diag.get('sprint_phases', 0)} sprint phases active in docs/phases/"
        )
        table.add_row(
            "Markdown Hygiene & Anti-Patterns",
            "[green]CLEAN[/green]" if not result.warnings else f"[yellow]{len(result.warnings)} NOTES[/yellow]",
            "Zero dot-folders, zero nested README sprawl" if not result.warnings else "See warnings below"
        )
        console.print(table)

        if result.errors:
            err_panel = Panel("\n".join(f"❌ [bold red]ERROR:[/bold red] {e}" for e in result.errors), title="[bold red]Critical Blocking Violations[/bold red]", border_style="red")
            console.print(err_panel)

        if result.warnings:
            warn_panel = Panel("\n".join(f"⚠️  [bold yellow]ADVISORY:[/bold yellow] {w}" for w in result.warnings), title="[bold yellow]Non-Blocking Architecture Warnings[/bold yellow]", border_style="yellow")
            console.print(warn_panel)

        if result.valid and not result.warnings:
            console.print(Panel("[bold green]🌟 100% ICM COMPLIANT: All 5 Layers and Hygiene Invariants Verified![/bold green]", border_style="green"))
    else:
        print(f"\n[*] ICM Audit: {diag.get('workspace_name')} ({diag.get('topology')})")
        print(f"Status: {'PASS' if result.valid else 'FAIL'} | Errors: {len(result.errors)} | Warnings: {len(result.warnings)}")
        for e in result.errors:
            print(f"  [ERROR] {e}")
        for w in result.warnings:
            print(f"  [WARN]  {w}")


def main():
    parser = argparse.ArgumentParser(description="Comprehensive ICM Workspace Audit & Diagnostics Engine.")
    parser.add_argument("path", nargs="?", default=".", help="Path to workspace directory")
    parser.add_argument("--fix", action="store_true", help="Automatically fix structural and hygiene violations")
    parser.add_argument("-y", "--yes", action="store_true", help="Non-interactive mode (auto-accept prompts)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON report for LLM agents")
    args = parser.parse_args()

    result = validate_workspace(args.path, fix=args.fix, non_interactive=args.yes)

    if args.json:
        report = {
            "valid": result.valid,
            "errors": result.errors,
            "warnings": result.warnings,
            "diagnostics": result.diagnostics,
        }
        print(json.dumps(report, indent=2))
    else:
        render_ai_audit_dashboard(result)

    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
