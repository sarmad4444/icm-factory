"""
scripts/validate_workspace.py
Audits any target workspace for strict Interpretable Context Methodology (ICM) compliance.
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


def validate_workspace(workspace_path: Path | str) -> tuple[bool, list[str]]:
    path = Path(workspace_path).resolve()
    errors: list[str] = []
    
    if not path.exists() or not path.is_dir():
        return False, [f"Directory does not exist: {path}"]
        
    # Check Layer 0: AGENT.md or CLAUDE.md or GEMINI.md
    has_l0 = (path / "AGENT.md").is_file() or (path / "CLAUDE.md").is_file() or (path / "GEMINI.md").is_file()
    if not has_l0:
        errors.append("Layer 0 missing: Workspace must contain AGENT.md (or CLAUDE.md / GEMINI.md)")
        
    # Check Layer 1: Root CONTEXT.md
    has_l1 = (path / "CONTEXT.md").is_file()
    if not has_l1:
        errors.append("Layer 1 missing: Workspace must contain root CONTEXT.md for task routing")
        
    # Check stages directory
    stages_dir = path / "stages"
    if not stages_dir.is_dir():
        errors.append("Stages directory missing: Workspace must contain a 'stages/' folder")
    else:
        stage_dirs = sorted([d for d in stages_dir.iterdir() if d.is_dir()])
        if not stage_dirs:
            errors.append("No stages found in 'stages/' folder")
        else:
            for idx, stage in enumerate(stage_dirs, start=1):
                # Check numbering format: 01_name, 02_name, etc.
                match = re.match(r"^(\d{2})_(.+)$", stage.name)
                if not match:
                    errors.append(f"Stage '{stage.name}' violates numbering pattern (must be NN_stagename e.g. 01_discovery)")
                else:
                    stage_num = int(match.group(1))
                    if stage_num != idx:
                        errors.append(f"Stage '{stage.name}' is out of sequence (expected {idx:02d}, got {stage_num:02d})")
                
                # Check Layer 2 contract: CONTEXT.md
                stage_context = stage / "CONTEXT.md"
                if not stage_context.is_file():
                    errors.append(f"Stage '{stage.name}' missing Layer 2 contract: CONTEXT.md")
                else:
                    content = stage_context.read_text(encoding="utf-8")
                    if "## Inputs" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Inputs' section")
                    if "## Process" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Process' section")
                    if "## Outputs" not in content:
                        errors.append(f"Stage '{stage.name}' CONTEXT.md missing '## Outputs' section")
                
                # Check Layer 4 output directory
                output_dir = stage / "output"
                if not output_dir.is_dir():
                    errors.append(f"Stage '{stage.name}' missing Layer 4 'output/' folder")
                    
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Audit a workspace for ICM compliance.")
    parser.add_argument("path", nargs="?", default=".", help="Path to workspace directory (default: current dir)")
    args = parser.parse_args()
    
    target_path = Path(args.path).resolve()
    print(f"\n[*] Auditing ICM Workspace: {target_path}\n" + "-" * 60)
    
    valid, errors = validate_workspace(target_path)
    if valid:
        print("[PASS] Workspace is 100% ICM Compliant!\n")
        sys.exit(0)
    else:
        print("[FAIL] Workspace has compliance violations:\n")
        for err in errors:
            print(f"  * {err}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
