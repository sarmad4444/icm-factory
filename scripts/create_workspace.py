"""
scripts/create_workspace.py
Scaffolds and configures new ICM workspaces inside ./workspaces/[workspace-name].
Supports pre-built archetypes, custom stage lists, and interactive CLI questionnaires.
"""

from __future__ import annotations
import argparse
import shutil
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

ARCHETYPES_DIR = ROOT_DIR / "_config" / "archetypes"
TEMPLATES_DIR = ROOT_DIR / "shared" / "templates"
DEFAULT_WORKSPACES_DIR = ROOT_DIR / "workspaces"


def scaffold_from_archetype(
    archetype_name: str,
    target_dir: Path | str,
    workspace_name: str | None = None,
    description: str | None = None,
) -> bool:
    target = Path(target_dir).resolve()
    arch_source = ARCHETYPES_DIR / archetype_name
    if not arch_source.is_dir():
        print(f"[ERROR] Archetype '{archetype_name}' does not exist in {ARCHETYPES_DIR}")
        return False

    if target.exists() and any(target.iterdir()):
        print(f"[ERROR] Target directory '{target}' already exists and is not empty.")
        return False

    target.mkdir(parents=True, exist_ok=True)
    # Copy all archetype files
    shutil.copytree(arch_source, target, dirs_exist_ok=True)

    ws_name = workspace_name or target.name
    ws_desc = description or f"ICM Workspace instantiated from archetype '{archetype_name}'"

    # Customize Layer 0 AGENT.md
    agent_file = target / "AGENT.md"
    if agent_file.is_file():
        content = agent_file.read_text(encoding="utf-8")
        content = f"# {ws_name} — Agent Identity\n\n**Mission:** {ws_desc}\n**Framework:** Interpretable Context Methodology (ICM)\n**Layer:** Layer 0\n\n" + content[content.find("## Stages Overview") if "## Stages Overview" in content else 0:]
        agent_file.write_text(content, encoding="utf-8")

    # Add setup questionnaire
    setup_dir = target / "setup"
    setup_dir.mkdir(exist_ok=True)
    q_tmpl = TEMPLATES_DIR / "questionnaire.md"
    if q_tmpl.is_file():
        shutil.copy(q_tmpl, setup_dir / "questionnaire.md")

    return True


def scaffold_custom_workspace(
    name: str,
    target_dir: Path | str,
    description: str,
    stages: list[dict[str, str] | str],
) -> bool:
    target = Path(target_dir).resolve()
    if target.exists() and any(target.iterdir()):
        print(f"[ERROR] Target directory '{target}' already exists and is not empty.")
        return False

    target.mkdir(parents=True, exist_ok=True)
    (target / "_config").mkdir(exist_ok=True)
    (target / "_config" / "rules.md").write_text(
        "# Factory Rules (Layer 3)\n\nDefine global rules, voice, and quality constraints here.",
        encoding="utf-8",
    )
    (target / "shared").mkdir(exist_ok=True)
    (target / "setup").mkdir(exist_ok=True)

    # Copy questionnaire
    q_tmpl = TEMPLATES_DIR / "questionnaire.md"
    if q_tmpl.is_file():
        shutil.copy(q_tmpl, target / "setup" / "questionnaire.md")

    # Parse stages
    parsed_stages = []
    for idx, s in enumerate(stages, start=1):
        if isinstance(s, dict):
            s_name = s.get("name", f"stage_{idx}")
            s_title = s.get("title", s_name.replace("_", " ").title())
            s_inputs = s.get("inputs", "- Layer 3: _config/rules.md\n- Layer 4: Previous output")
            s_process = s.get("process", f"Execute the {s_title} task.")
            s_outputs = s.get("outputs", f"- {s_name}_output.md -> output/")
        else:
            s_name = str(s).strip()
            s_title = s_name.replace("_", " ").title()
            s_inputs = "- Layer 3: _config/rules.md"
            s_process = f"Process step for {s_title}."
            s_outputs = f"- {s_name}_artifact.md -> output/"
        
        dir_name = f"{idx:02d}_{s_name}"
        parsed_stages.append({
            "idx": f"{idx:02d}",
            "name": s_name,
            "dir_name": dir_name,
            "title": s_title,
            "inputs": s_inputs,
            "process": s_process,
            "outputs": s_outputs,
        })

    # Render Stages
    stages_summary_lines = []
    routing_rows = []
    for ps in parsed_stages:
        s_dir = target / "stages" / ps["dir_name"]
        s_dir.mkdir(parents=True, exist_ok=True)
        (s_dir / "references").mkdir(exist_ok=True)
        (s_dir / "output").mkdir(exist_ok=True)
        (s_dir / "output" / ".gitkeep").write_text(f"# Output for {ps['dir_name']}\n", encoding="utf-8")

        contract_content = f"""# Stage {ps['idx']}: {ps['title']} — Contract

**Layer:** Layer 2 (Stage Execution Contract)  
**Stage Name:** `{ps['dir_name']}`

---

## Inputs

{ps['inputs']}

---

## Process

{ps['process']}

---

## Outputs

{ps['outputs']}
"""
        (s_dir / "CONTEXT.md").write_text(contract_content, encoding="utf-8")

        stages_summary_lines.append(f"- `stages/{ps['dir_name']}`: {ps['title']}")
        routing_rows.append(f"| {ps['title']} | `stages/{ps['dir_name']}/` | [`CONTEXT.md`](file://./stages/{ps['dir_name']}/CONTEXT.md) | `stages/{ps['dir_name']}/output/` |")

    # Render Layer 0 AGENT.md
    agent_tmpl = TEMPLATES_DIR / "child_agent_md.tmpl"
    if agent_tmpl.is_file():
        agent_content = agent_tmpl.read_text(encoding="utf-8")
        agent_content = (
            agent_content.replace("{WORKSPACE_NAME}", name)
            .replace("{WORKSPACE_DESCRIPTION}", description)
            .replace("{STAGES_SUMMARY}", "\n".join(stages_summary_lines))
        )
    else:
        agent_content = f"# {name}\n\n{description}\n\n" + "\n".join(stages_summary_lines)
    (target / "AGENT.md").write_text(agent_content, encoding="utf-8")

    # Render Layer 1 CONTEXT.md
    context_tmpl = TEMPLATES_DIR / "child_context_l1.tmpl"
    if context_tmpl.is_file():
        ctx_content = context_tmpl.read_text(encoding="utf-8")
        ctx_content = (
            ctx_content.replace("{WORKSPACE_NAME}", name)
            .replace("{WORKSPACE_DESCRIPTION}", description)
            .replace("{ROUTING_TABLE_ROWS}", "\n".join(routing_rows))
        )
    else:
        ctx_content = f"# {name} Task Routing\n\n" + "\n".join(routing_rows)
    (target / "CONTEXT.md").write_text(ctx_content, encoding="utf-8")

    return True


def interactive_wizard():
    print("\n" + "=" * 60)
    print(" [*] ICM Workspace Creation Wizard")
    print("=" * 60 + "\n")

    print("Choose workspace creation method:")
    print("  1. Archetype Fast-Track (Pre-configured pipeline)")
    print("  2. Custom Staged Workflow (Interactive definition)")
    print("  3. Exit")

    choice = input("\nSelect an option [1-3]: ").strip()

    if choice == "1":
        archetypes = [d.name for d in ARCHETYPES_DIR.iterdir() if d.is_dir()]
        print("\nAvailable Archetypes:")
        for idx, arch in enumerate(archetypes, start=1):
            print(f"  {idx}. {arch}")
        
        arch_idx = int(input("\nSelect archetype number: ").strip()) - 1
        arch_name = archetypes[arch_idx]

        ws_name = input("\nEnter workspace name (e.g. tech_explainer_v1): ").strip()
        ws_desc = input("Enter brief workspace description: ").strip()

        target_path = DEFAULT_WORKSPACES_DIR / ws_name
        print(f"\n[+] Scaffolding workspace at {target_path}...")
        success = scaffold_from_archetype(arch_name, target_path, ws_name, ws_desc)
        if success:
            valid, errors = validate_workspace(target_path)
            if valid:
                print(f"\n[PASS] Successfully created and validated ICM workspace: {target_path}")
            else:
                print(f"\n[WARN] Workspace created with warnings: {errors}")

    elif choice == "2":
        ws_name = input("\nEnter workspace name: ").strip()
        ws_desc = input("Enter workspace description: ").strip()
        stages_input = input("Enter stage names comma-separated (e.g. research, draft, polish): ").strip()
        stage_names = [s.strip() for s in stages_input.split(",") if s.strip()]

        target_path = DEFAULT_WORKSPACES_DIR / ws_name
        print(f"\n[+] Scaffolding custom workspace at {target_path}...")
        success = scaffold_custom_workspace(ws_name, target_path, ws_desc, stage_names)
        if success:
            valid, errors = validate_workspace(target_path)
            if valid:
                print(f"\n[PASS] Successfully created and validated ICM workspace: {target_path}")
            else:
                print(f"\n[WARN] Workspace created with warnings: {errors}")
    else:
        print("Cancelled.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new ICM workspace.")
    parser.add_argument("--name", help="Workspace folder name (inside ./workspaces/)")
    parser.add_argument("--description", default="Custom ICM Workspace", help="Description of purpose")
    parser.add_argument("--archetype", help="Archetype template name (e.g. content_pipeline, minimal_starter)")
    parser.add_argument("--stages", help="Comma-separated list of stage names for custom workspace")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive creation wizard")
    args = parser.parse_args()

    if args.interactive or (not args.name and not args.archetype):
        interactive_wizard()
        return

    target_dir = DEFAULT_WORKSPACES_DIR / args.name

    if args.archetype:
        print(f"[+] Scaffolding from archetype '{args.archetype}' into {target_dir}...")
        success = scaffold_from_archetype(args.archetype, target_dir, args.name, args.description)
    elif args.stages:
        stages = [s.strip() for s in args.stages.split(",") if s.strip()]
        print(f"[+] Scaffolding custom workspace with {len(stages)} stages into {target_dir}...")
        success = scaffold_custom_workspace(args.name, target_dir, args.description, stages)
    else:
        print("[ERROR] Must specify either --archetype, --stages, or --interactive")
        sys.exit(1)

    if not success:
        sys.exit(1)

    valid, errors = validate_workspace(target_dir)
    if valid:
        print(f"[PASS] Workspace '{args.name}' successfully scaffolded and verified compliant!")
    else:
        print(f"[FAIL] Scaffolding validation failed: {errors}")
        sys.exit(1)


if __name__ == "__main__":
    main()
