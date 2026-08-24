"""
scripts/list_workspaces.py
Lists and audits all ICM child workspaces located in ./workspaces/.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import sys

# Ensure root is in sys.path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from scripts.dashboard import get_workspaces_summary

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
except ImportError:
    console = None

WORKSPACES_DIR = ROOT_DIR / "workspaces"


def get_workspaces_data(workspaces_dir: Path | str = WORKSPACES_DIR) -> list[dict]:
    return get_workspaces_summary(workspaces_dir)


def list_workspaces(workspaces_dir: Path | str = WORKSPACES_DIR):
    ws_dir = Path(workspaces_dir).resolve()
    if not ws_dir.exists():
        print(f"No {ws_dir} directory found.")
        return

    data = get_workspaces_data(ws_dir)
    if not data:
        print(f"\n[*] No child workspaces found in {ws_dir}\n")
        return

    if console:
        table = Table(title=f"ICM Child Workspaces ({ws_dir.name}/)", expand=True)
        table.add_column("Workspace Name", style="bold cyan")
        table.add_column("Topology", style="blue")
        table.add_column("Phase / Stages", style="yellow")
        table.add_column("Task Progress", style="magenta")
        table.add_column("ICM Compliance", justify="center")
        table.add_column("Path", style="dim")

        for ws in data:
            status = "[green]PASS (Valid)[/green]" if ws["valid"] else f"[red]FAIL ({ws['errors_count']} err)[/red]"
            table.add_row(
                ws["name"],
                ws["topology"],
                ws["active_phase"],
                ws["tasks_progress"],
                status,
                ws["path"],
            )
        console.print(table)
    else:
        print("\n" + "=" * 90)
        print(f"{'Workspace Name':<25} | {'Topology':<20} | {'Phase / Stages':<18} | {'ICM Status':<15} | {'Path'}")
        print("=" * 90)
        for ws in data:
            status = "PASS (Valid)" if ws["valid"] else f"FAIL ({ws['errors_count']} err)"
            print(f"{ws['name']:<25} | {ws['topology']:<20} | {ws['active_phase']:<18} | {status:<15} | {ws['path']}")
        print("=" * 90 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List all child workspaces in ./workspaces/.")
    parser.add_argument("--workspaces", default=str(WORKSPACES_DIR), help="Path to workspaces directory")
    args = parser.parse_args()
    list_workspaces(args.workspaces)
