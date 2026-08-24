"""
scripts/dashboard.py
Rich Terminal UI Dashboard for ICM Child Workspaces.
Displays real-time topology, active sprint phase, task completion progress, skills, and compliance.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys
import time

# Ensure root is in sys.path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from scripts.validate_workspace import validate_workspace

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    console = Console()
except ImportError:
    console = None

DEFAULT_WORKSPACES_DIR = ROOT_DIR / "workspaces"


def get_workspaces_summary(workspaces_dir: Path | str = DEFAULT_WORKSPACES_DIR) -> list[dict]:
    ws_dir = Path(workspaces_dir).resolve()
    if not ws_dir.is_dir():
        return []

    summaries = []
    for sub in sorted(ws_dir.iterdir()):
        if not sub.is_dir() or sub.name.startswith("."):
            continue

        # 1. Detect Topology
        has_wf = (sub / "workflows").is_dir()
        has_stages = (sub / "stages").is_dir()
        has_docs = (sub / "docs").is_dir()

        if has_wf and has_docs:
            topology = "Topology 4 (Enterprise)"
        elif has_wf:
            topology = "Topology 3 (Multi-Workflow)"
        elif has_stages and has_docs:
            topology = "Topology 2 (Managed)"
        elif has_stages:
            topology = "Topology 1 (Lean)"
        else:
            topology = "Custom / Unstructured"

        # 2. Active Phase / Stage count
        active_phase = "N/A"
        strat_file = sub / "docs" / "STRATEGY.md"
        if strat_file.is_file():
            strat_text = strat_file.read_text(encoding="utf-8")
            m = re.search(r"\*\*Active Phase:\*\*\s*`?([^`\n\r]+)`?", strat_text)
            if m:
                active_phase = m.group(1).strip()
        elif has_stages:
            stages_count = len([d for d in (sub / "stages").iterdir() if d.is_dir()])
            active_phase = f"{stages_count} stages"
        elif has_wf:
            wf_count = len([d for d in (sub / "workflows").iterdir() if d.is_dir()])
            active_phase = f"{wf_count} workflows"

        # 3. Tasks Progress
        total_tasks = 0
        done_tasks = 0
        if has_docs and (sub / "docs" / "phases").is_dir():
            for tasks_md in (sub / "docs" / "phases").glob("**/tasks.md"):
                try:
                    text = tasks_md.read_text(encoding="utf-8")
                    total_tasks += len(re.findall(r"- \[[ xX]\]", text))
                    done_tasks += len(re.findall(r"- \[[xX]\]", text))
                except Exception:
                    pass

        if total_tasks > 0:
            pct = int((done_tasks / total_tasks) * 100)
            tasks_progress = f"{done_tasks}/{total_tasks} ({pct}%)"
        else:
            tasks_progress = "No tasks" if has_docs else "N/A (No PM)"

        # 4. Skills Count
        skills_dir = sub / "skills"
        skills_count = 0
        if skills_dir.is_dir():
            skills_count = len([d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()])

        # 5. Compliance Health
        valid, errors, warnings = validate_workspace(sub).full()

        summaries.append({
            "name": sub.name,
            "path": f"workspaces/{sub.name}",
            "topology": topology,
            "active_phase": active_phase,
            "tasks_progress": tasks_progress,
            "skills_count": skills_count,
            "valid": valid,
            "errors_count": len(errors),
            "warnings_count": len(warnings),
        })

    return summaries


def render_dashboard(workspaces_dir: Path | str = DEFAULT_WORKSPACES_DIR, once: bool = False) -> bool:
    summaries = get_workspaces_summary(workspaces_dir)

    if console:
        table = Table(title="ICM Child Workspaces — Control Plane Dashboard", expand=True)
        table.add_column("Workspace", style="bold cyan", no_wrap=True)
        table.add_column("Topology", style="blue")
        table.add_column("Active Phase / Focus", style="yellow")
        table.add_column("Task Progress", style="magenta")
        table.add_column("Skills", justify="center")
        table.add_column("Health Status", justify="center")
        table.add_column("Path", style="dim")

        for s in summaries:
            if s["valid"]:
                status = "[bold green]PASS (Compliant)[/bold green]"
            else:
                status = f"[bold red]FAIL ({s['errors_count']} err)[/bold red]"

            skills_str = f"{s['skills_count']} skills" if s["skills_count"] > 0 else "-"
            table.add_row(
                s["name"],
                s["topology"],
                s["active_phase"],
                s["tasks_progress"],
                skills_str,
                status,
                s["path"],
            )

        compliant_count = sum(1 for s in summaries if s["valid"])
        total_count = len(summaries)
        summary_panel = Panel(
            f"[bold white]Total Workspaces:[/bold white] {total_count}  |  "
            f"[bold green]Compliant:[/bold green] {compliant_count}  |  "
            f"[bold red]Violations:[/bold red] {total_count - compliant_count}",
            title="ICM Ecosystem Health Summary",
            border_style="green" if compliant_count == total_count else "yellow",
        )

        console.print(summary_panel)
        console.print(table)
    else:
        print("\n" + "=" * 90)
        print("ICM Child Workspaces — Control Plane Dashboard")
        print("=" * 90)
        print(f"{'Workspace':<24} | {'Topology':<24} | {'Phase / Stages':<18} | {'Progress':<12} | {'Status'}")
        print("-" * 90)
        for s in summaries:
            status = "PASS" if s["valid"] else f"FAIL ({s['errors_count']} err)"
            print(f"{s['name']:<24} | {s['topology']:<24} | {s['active_phase']:<18} | {s['tasks_progress']:<12} | {status}")
        print("=" * 90 + "\n")

    return True


def main():
    parser = argparse.ArgumentParser(description="Terminal Dashboard for ICM Workspaces.")
    parser.add_argument("--workspaces", default=str(DEFAULT_WORKSPACES_DIR), help="Workspaces container directory")
    parser.add_argument("--once", action="store_true", help="Render dashboard once and exit")
    args = parser.parse_args()

    render_dashboard(workspaces_dir=args.workspaces, once=args.once or not sys.stdin.isatty())


if __name__ == "__main__":
    main()
