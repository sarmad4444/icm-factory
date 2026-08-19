"""
scripts/list_workspaces.py
Lists and audits all ICM child workspaces located in ./workspaces/.
"""

from __future__ import annotations
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

from scripts.validate_workspace import validate_workspace

WORKSPACES_DIR = ROOT_DIR / "workspaces"


def list_workspaces():
    if not WORKSPACES_DIR.exists():
        print("No workspaces/ directory found.")
        return

    subdirs = [d for d in WORKSPACES_DIR.iterdir() if d.is_dir()]
    if not subdirs:
        print("\n[*] No child workspaces found in ./workspaces/\n")
        return

    print("\n" + "=" * 80)
    print(f"{'Workspace Name':<30} | {'Stages':<8} | {'ICM Compliance':<15} | {'Path'}")
    print("=" * 80)

    for ws in sorted(subdirs):
        stages_dir = ws / "stages"
        stage_count = len([d for d in stages_dir.iterdir() if d.is_dir()]) if stages_dir.exists() else 0
        valid, errors = validate_workspace(ws)
        status = "PASS (Valid)" if valid else f"FAIL ({len(errors)} err)"
        print(f"{ws.name:<30} | {stage_count:<8} | {status:<15} | workspaces/{ws.name}")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    list_workspaces()
