"""
scripts/init_phase.py
Initializes a new Objective Sprint Phase in docs/phases/phase_NN_<name>/
with goals.md and tasks.md, and updates docs/STRATEGY.md.
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

ROOT_DIR = Path(__file__).parent.parent.resolve()
TEMPLATES_DIR = ROOT_DIR / "resources" / "templates"


def get_template_path(name: str) -> Path:
    """Finds template file, checking *.template.md first, then *.md.tmpl or exact name."""
    cand1 = TEMPLATES_DIR / f"{name}.template.md"
    if cand1.is_file():
        return cand1
    cand2 = TEMPLATES_DIR / f"{name}.md.tmpl"
    if cand2.is_file():
        return cand2
    cand3 = TEMPLATES_DIR / f"{name}.tmpl"
    if cand3.is_file():
        return cand3
    cand4 = TEMPLATES_DIR / f"{name}.md"
    if cand4.is_file():
        return cand4
    return TEMPLATES_DIR / name


def init_phase(
    name: str,
    number: int | None = None,
    workspace_dir: Path | str = ".",
    goal: str | None = None,
) -> Path:
    ws = Path(workspace_dir).resolve()
    docs_dir = ws / "docs"
    phases_dir = docs_dir / "phases"
    phases_dir.mkdir(parents=True, exist_ok=True)

    # Determine phase number if not provided
    if number is None:
        existing_phases = [d.name for d in phases_dir.iterdir() if d.is_dir() and d.name.startswith("phase_")]
        max_num = 0
        for ep in existing_phases:
            m = re.match(r"^phase_(\d+)_", ep)
            if m:
                max_num = max(max_num, int(m.group(1)))
        number = max_num + 1

    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_")
    phase_dirname = f"phase_{number:02d}_{slug}"
    phase_dir = phases_dir / phase_dirname
    phase_dir.mkdir(parents=True, exist_ok=True)

    phase_title = name.replace("_", " ").title()
    phase_goal = goal or f"Achieve milestone objectives for {phase_title}"

    # Hydrate goals.md
    goals_tmpl_file = get_template_path("goals")
    if goals_tmpl_file.is_file():
        goals_tmpl = goals_tmpl_file.read_text(encoding="utf-8")
        goals_content = (
            goals_tmpl.replace("{PHASE_NUMBER}", f"{number:02d}")
            .replace("{PHASE_TITLE}", phase_title)
            .replace("{PHASE_OBJECTIVE}", phase_goal)
            .replace("{GOAL_1}", f"Implement core components for {phase_title}")
            .replace("{GOAL_2}", "Ensure 100% unit and integration test coverage")
            .replace("{GOAL_3}", "Update architectural documentation and references")
        )
    else:
        goals_content = f"""# Phase {number:02d}: {phase_title} — Goals & Definition of Done

**Sprint Objective:** {phase_goal}  
**Status:** In Progress

---

## 1. Objectives

1. Implement core components for {phase_title}.
2. Ensure 100% unit and integration test coverage.

---

## 2. Definition of Done (DoD)

- [ ] All tests pass.
- [ ] Code follows project standards.
"""
    (phase_dir / "goals.md").write_text(goals_content, encoding="utf-8")

    # Hydrate tasks.md
    tasks_tmpl_file = get_template_path("tasks")
    if tasks_tmpl_file.is_file():
        tasks_tmpl = tasks_tmpl_file.read_text(encoding="utf-8")
        tasks_content = (
            tasks_tmpl.replace("{PHASE_NUMBER}", f"{number:02d}")
            .replace("{PHASE_TITLE}", phase_title)
            .replace("{PHASE_SLUG}", slug)
            .replace("{SAMPLE_TASK_TITLE}", f"Initialize {phase_title} Implementation")
            .replace("{SAMPLE_TASK_SCOPE}", f"Scaffold and test core functionality for {phase_title}")
            .replace("{SAMPLE_VERIFY_COMMAND}", "uv run pytest -v")
        )
    else:
        tasks_content = f"""# Phase {number:02d}: {phase_title} — Task Board

**Phase Directory:** `docs/phases/{phase_dirname}/`  
**Parent Goals:** [`goals.md`](file://./goals.md)

---

## Task Board

### TASK-{number:02d}-A01: Initialize {phase_title} Implementation
- **Status:** `- [ ]` (Pending)
- **Assignee:** `@agent`
- **Scope:** Scaffold and test core functionality for {phase_title}
- **Git Commit:** `pending`
- **Verification:** `uv run pytest -v`

Checklist:
- [ ] Write failing test in `tests/`
- [ ] Implement required module
- [ ] Verify test passes
"""
    (phase_dir / "tasks.md").write_text(tasks_content, encoding="utf-8")

    # Update docs/STRATEGY.md if it exists
    strategy_file = docs_dir / "STRATEGY.md"
    if strategy_file.is_file():
        strat_text = strategy_file.read_text(encoding="utf-8")
        # Update Active Phase pointer
        strat_text = re.sub(
            r"\*\*Active Phase:\*\*\s*`[^`]+`",
            f"**Active Phase:** `{phase_dirname}`",
            strat_text,
        )
        strat_text = re.sub(
            r"docs/phases/phase_[^/]+/",
            f"docs/phases/{phase_dirname}/",
            strat_text,
        )
        strategy_file.write_text(strat_text, encoding="utf-8")

    return phase_dir


def main():
    parser = argparse.ArgumentParser(description="Initialize a new objective sprint phase.")
    parser.add_argument("name", help="Name of the sprint phase (e.g. billing_engine, auth_module)")
    parser.add_argument("--number", type=int, help="Optional explicit phase number (e.g. 2)")
    parser.add_argument("--goal", help="Sprint objective / goal description")
    parser.add_argument("--workspace", default=".", help="Target workspace root path")
    args = parser.parse_args()

    phase_dir = init_phase(
        name=args.name,
        number=args.number,
        workspace_dir=args.workspace,
        goal=args.goal,
    )
    print(f"[PASS] Successfully initialized sprint phase: {phase_dir}")


if __name__ == "__main__":
    main()
