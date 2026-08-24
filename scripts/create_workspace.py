"""
scripts/create_workspace.py
Scaffolds and configures new ICM workspaces inside ./workspaces/[workspace-name].
Supports 4 Modular Topologies (Lean, Managed, Multi-Workflow, Enterprise),
Pluggable Add-Ons (--with-pm, --with-compiler, --with-skills, --with-governance),
Codebase Adoption (--adopt), and Interactive Socratic Questionnaire.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
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

ARCHETYPES_DIR = ROOT_DIR / "resources" / "archetypes"
TEMPLATES_DIR = ROOT_DIR / "resources" / "templates"
MASTER_SKILLS_DIR = ROOT_DIR / "skills"
DEFAULT_WORKSPACES_DIR = ROOT_DIR / "workspaces"


def inject_skills(target: Path):
    target_skills = target / "skills"
    target_skills.mkdir(parents=True, exist_ok=True)
    if MASTER_SKILLS_DIR.is_dir():
        for item in MASTER_SKILLS_DIR.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_skills / item.name, dirs_exist_ok=True)
            elif item.is_file() and item.name == "CONTEXT.md":
                shutil.copy(item, target_skills / "CONTEXT.md")
    if not (target_skills / "CONTEXT.md").exists():
        from scripts.manage_skills import sync_skills_manifest
        sync_skills_manifest(target)


def inject_pm(target: Path, workspace_name: str):
    docs_dir = target / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # 1. STRATEGY.md
    strat_tmpl = TEMPLATES_DIR / "STRATEGY.md.tmpl"
    if strat_tmpl.is_file():
        strat_content = (
            strat_tmpl.read_text(encoding="utf-8")
            .replace("{WORKSPACE_NAME}", workspace_name)
            .replace("{ACTIVE_PHASE}", "phase_01_mvp_core")
            .replace("{CURRENT_MILESTONE}", "Foundation & Core Capabilities")
            .replace("{CURRENT_FOCUS}", "MVP Architecture and Core Execution Engine")
            .replace(
                "{PHASE_ROADMAP_ROWS}",
                "| Phase 01 | `phase_01_mvp_core` | Foundational system and testing harness | In Progress |\n"
                "| Phase 02 | `phase_02_integration` | External integration & production readiness | Planned |",
            )
        )
    else:
        strat_content = f"""<!-- 💡 HOW THIS WORKS -->
# Project Strategy & Live Status

**Project Name:** {workspace_name}  
**Active Phase:** `phase_01_mvp_core`  
**Current Milestone:** Foundation & Core Capabilities

---

## 1. Active Objectives

- **Current Focus:** MVP Core Execution
- **Active Phase Directory:** [`docs/phases/phase_01_mvp_core/`](file://./docs/phases/phase_01_mvp_core/)
"""
    (docs_dir / "STRATEGY.md").write_text(strat_content, encoding="utf-8")

    # 2. Architecture ADR 001
    adrs_dir = docs_dir / "architecture" / "adrs"
    adrs_dir.mkdir(parents=True, exist_ok=True)
    adr_content = f"""# ADR 001: Architecture Baseline for {workspace_name}

## Status
Accepted

## Context
Initial technical architecture baseline for {workspace_name}.

## Decision
Modular decoupled architecture adhering to ICM conventions.
"""
    (adrs_dir / "001_baseline_architecture.md").write_text(adr_content, encoding="utf-8")

    # 3. Phase 01
    from scripts.init_phase import init_phase
    init_phase("mvp_core", number=1, workspace_dir=target, goal="Foundational system setup and initial deliverable")


def inject_compiler(target: Path, workspace_name: str):
    backlog_dir = target / "docs" / "backlog"
    backlog_dir.mkdir(parents=True, exist_ok=True)

    # 1. raw_ideas.md
    raw_tmpl = TEMPLATES_DIR / "raw_ideas.md.tmpl"
    if raw_tmpl.is_file():
        raw_content = (
            raw_tmpl.read_text(encoding="utf-8")
            .replace("{SAMPLE_IDEA_TITLE}", "Initial System Capability")
            .replace("{SAMPLE_PROBLEM_DESC}", f"Initial requirement for {workspace_name}")
            .replace("{SAMPLE_PROPOSED_SOL}", "Implement via structured ICM workflow")
        )
    else:
        raw_content = f"# Backlog Ideas\n\n- Initial idea for {workspace_name}\n"
    (backlog_dir / "raw_ideas.md").write_text(raw_content, encoding="utf-8")

    # 2. shaped_initiatives.md
    shaped_tmpl = TEMPLATES_DIR / "shaped_initiatives.md.tmpl"
    if shaped_tmpl.is_file():
        shaped_content = (
            shaped_tmpl.read_text(encoding="utf-8")
            .replace("{INITIATIVE_TITLE}", "Core MVP Setup")
            .replace("{INITIATIVE_IDENTITY}", f"Principal Engineer building {workspace_name}.")
            .replace("{INITIATIVE_TASK}", "Implement and verify initial feature set.")
            .replace("{INITIATIVE_STACK}", "Python 3.11+, pytest, uv / bun")
            .replace("{INITIATIVE_CONSTRAINT_1}", "Strict test-driven development (TDD)")
            .replace("{INITIATIVE_CONSTRAINT_2}", "100% test pass rate required")
            .replace("{INITIATIVE_DELIVERABLE}", "src/, tests/")
            .replace("{INITIATIVE_VERIFICATION}", "uv run pytest -v")
        )
    else:
        shaped_content = f"# Shaped Initiatives\n\n## Initiative: Core MVP Setup\n"
    (backlog_dir / "shaped_initiatives.md").write_text(shaped_content, encoding="utf-8")


def inject_governance(target: Path):
    scripts_dir = target / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    val_source = ROOT_DIR / "scripts" / "validate_workspace.py"
    if val_source.is_file():
        shutil.copy(val_source, scripts_dir / "validate_workspace.py")


def scaffold_workspace(
    name: str,
    target_dir: Path | str,
    topology: str = "1",
    description: str | None = None,
    stages: list[str | dict] | None = None,
    workflows: dict[str, list[str]] | None = None,
    with_pm: bool = False,
    with_compiler: bool = False,
    with_skills: bool = False,
    with_governance: bool = False,
    allow_existing: bool = False,
) -> bool:
    target = Path(target_dir).resolve()
    if not allow_existing and target.exists() and any(target.iterdir()):
        print(f"[ERROR] Target directory '{target}' already exists and is not empty.")
        return False

    target.mkdir(parents=True, exist_ok=True)
    ws_desc = description or f"ICM Workspace for {name}"

    # Normalize topology
    topo_str = str(topology).lower().strip()
    if topo_str in ["1", "lean"]:
        topo_num = 1
    elif topo_str in ["2", "managed"]:
        topo_num = 2
        with_pm = True
    elif topo_str in ["3", "multi-workflow", "multi_workflow"]:
        topo_num = 3
    elif topo_str in ["4", "enterprise"]:
        topo_num = 4
        with_pm = True
    else:
        topo_num = 1

    # Base folders
    (target / "resources").mkdir(exist_ok=True)
    (target / "resources" / "quality_standards.md").write_text(
        f"# Project Quality Standards\n\n1. Enforce rigorous testing before committing.\n2. Keep contracts and documentation in sync.\n",
        encoding="utf-8",
    )
    (target / "setup").mkdir(exist_ok=True)

    stages_summary_lines = []
    routing_rows = []

    # Scaffold single-pipeline stages (Topologies 1 & 2)
    if topo_num in [1, 2]:
        stage_list = stages or ["specification", "implementation", "verification"]
        for idx, s in enumerate(stage_list, start=1):
            if isinstance(s, dict):
                s_name = s.get("name", f"stage_{idx}")
                s_title = s.get("title", s_name.replace("_", " ").title())
                s_inputs = s.get("inputs", "- resources/quality_standards.md\n- Preceding stage output")
                s_process = s.get("process", f"Execute the {s_title} task.")
                s_outputs = s.get("outputs", f"- {s_name}_artifact.md -> output/")
            else:
                s_name = str(s).strip()
                s_title = s_name.replace("_", " ").title()
                s_inputs = "- resources/quality_standards.md"
                s_process = f"Execute steps for {s_title}."
                s_outputs = f"- {s_name}_artifact.md -> output/"

            dir_name = f"{idx:02d}_{s_name}"
            s_dir = target / "stages" / dir_name
            s_dir.mkdir(parents=True, exist_ok=True)
            (s_dir / "output").mkdir(exist_ok=True)
            (s_dir / "output" / ".gitkeep").write_text(f"# Output for {dir_name}\n", encoding="utf-8")

            contract = f"""<!-- 💡 HOW THIS WORKS -->
# Stage {idx:02d}: {s_title}

**Purpose:** {s_process}

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Reference** | `resources/quality_standards.md` | Quality rules and project guidelines |

---

## Process

1. {s_process}

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `{s_name}_artifact.md` | `stages/{dir_name}/output/` | Completed stage deliverable |
"""
            (s_dir / "CONTEXT.md").write_text(contract, encoding="utf-8")
            stages_summary_lines.append(f"- `stages/{dir_name}`: {s_title}")
            routing_rows.append(f"| {s_title} | `stages/{dir_name}/` | [`CONTEXT.md`](file://./stages/{dir_name}/CONTEXT.md) | `stages/{dir_name}/output/` |")

    # Scaffold multi-workflow stages (Topologies 3 & 4)
    elif topo_num in [3, 4]:
        wf_dict = workflows or {
            "software_dev": ["spec", "implementation", "verification"],
            "deployment": ["staging", "production"],
        }
        for wf_name, wf_stages in wf_dict.items():
            wf_dir = target / "workflows" / wf_name / "stages"
            wf_dir.mkdir(parents=True, exist_ok=True)
            stages_summary_lines.append(f"- `workflows/{wf_name}/`: {wf_name.replace('_', ' ').title()} Workflow")
            for idx, s in enumerate(wf_stages, start=1):
                s_name = str(s).strip()
                s_title = s_name.replace("_", " ").title()
                dir_name = f"{idx:02d}_{s_name}"
                s_path = wf_dir / dir_name
                s_path.mkdir(parents=True, exist_ok=True)
                (s_path / "output").mkdir(exist_ok=True)
                (s_path / "output" / ".gitkeep").write_text(f"# Output for {wf_name}/{dir_name}\n", encoding="utf-8")

                contract = f"""<!-- 💡 HOW THIS WORKS -->
# {wf_name.title()} — Stage {idx:02d}: {s_title}

**Purpose:** Execute tasks for {s_title} in {wf_name} workflow.

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Reference** | `resources/quality_standards.md` | Quality rules and workflow guidelines |

---

## Process

1. Execute tasks for {s_title}.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `{s_name}_artifact.md` | `workflows/{wf_name}/stages/{dir_name}/output/` | Completed workflow deliverable |
"""
                (s_path / "CONTEXT.md").write_text(contract, encoding="utf-8")
                routing_rows.append(f"| {wf_name.title()} / {s_title} | `workflows/{wf_name}/stages/{dir_name}/` | [`CONTEXT.md`](file://./workflows/{wf_name}/stages/{dir_name}/CONTEXT.md) | Output artifact |")

    # Apply add-ons
    if with_pm:
        inject_pm(target, name)
        routing_rows.insert(0, "| Active Sprint & Tasks | `docs/phases/` | [`STRATEGY.md`](file://./docs/STRATEGY.md) | Phase Deliverables |")
    if with_compiler:
        inject_compiler(target, name)
        routing_rows.append("| Prompt Backlog & Initiatives | `docs/backlog/` | [`shaped_initiatives.md`](file://./docs/backlog/shaped_initiatives.md) | 5-part prompt contracts |")
    if with_skills:
        inject_skills(target)
    if with_governance:
        inject_governance(target)

    # Render AGENT.md
    docs_summary = "- `docs/`: Live strategy, objective sprint phases, and backlog." if (with_pm or with_compiler) else ""
    skills_summary = "- `skills/`: On-demand dynamic skills catalog." if with_skills else ""
    workflows_summary = "## Stages & Workflows\n\n" + "\n".join(stages_summary_lines)

    agent_tmpl = TEMPLATES_DIR / "AGENT.md.tmpl"
    if agent_tmpl.is_file():
        agent_content = (
            agent_tmpl.read_text(encoding="utf-8")
            .replace("{WORKSPACE_NAME}", name)
            .replace("{WORKSPACE_DESCRIPTION}", ws_desc)
            .replace("{OPTIONAL_DOCS_SUMMARY}", docs_summary)
            .replace("{OPTIONAL_SKILLS_SUMMARY}", skills_summary)
            .replace("{WORKFLOW_OR_STAGES_SUMMARY}", workflows_summary)
        )
    else:
        agent_content = f"# {name}\n\n{ws_desc}\n\n" + workflows_summary
    (target / "AGENT.md").write_text(agent_content, encoding="utf-8")

    # Render CLAUDE.md pointer
    claude_content = f"# {name}\n\nPlease refer to [`AGENT.md`](file://./AGENT.md) for operating rules and floor plan.\nRefer to [`CONTEXT.md`](file://./CONTEXT.md) for task routing.\n"
    (target / "CLAUDE.md").write_text(claude_content, encoding="utf-8")

    # Render CONTEXT.md
    context_tmpl = TEMPLATES_DIR / "CONTEXT.md.tmpl"
    res_summary = "- `resources/quality_standards.md`: Project constraints and formatting guidelines."
    if with_skills:
        res_summary += "\n- `skills/CONTEXT.md`: Dynamic skills manifest."
    if with_pm:
        res_summary += "\n- `docs/STRATEGY.md`: Active phase status and sprint roadmap."

    if context_tmpl.is_file():
        ctx_content = (
            context_tmpl.read_text(encoding="utf-8")
            .replace("{WORKSPACE_NAME}", name)
            .replace("{ROUTING_TABLE_ROWS}", "\n".join(routing_rows))
            .replace("{PROJECT_RESOURCES_SUMMARY}", res_summary)
        )
    else:
        ctx_content = f"# {name} Task Routing\n\n" + "\n".join(routing_rows)
    (target / "CONTEXT.md").write_text(ctx_content, encoding="utf-8")

    return True


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
    shutil.copytree(arch_source, target, dirs_exist_ok=True)

    ws_name = workspace_name or target.name
    ws_desc = description or f"ICM Workspace instantiated from archetype '{archetype_name}'"

    agent_file = target / "AGENT.md"
    if agent_file.is_file():
        content = agent_file.read_text(encoding="utf-8")
        content = f"# {ws_name} — Agent Operating Guide\n\n**Mission:** {ws_desc}\n**Framework:** Interpretable Context Methodology (ICM)\n\n" + content[content.find("## ") if "## " in content else 0:]
        agent_file.write_text(content, encoding="utf-8")

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
    return scaffold_workspace(
        name=name,
        target_dir=target_dir,
        topology="1",
        description=description,
        stages=stages,
        with_skills=False,
    )


def adopt_existing_codebase(
    source_dir: Path | str,
    target_dir: Path | str,
    workspace_name: str | None = None,
    description: str | None = None,
    topology: str = "managed",
    stages: list[str] | None = None,
    with_pm: bool = True,
    with_compiler: bool = True,
    with_skills: bool = True,
    with_governance: bool = False,
) -> bool:
    src = Path(source_dir).resolve()
    dst = Path(target_dir).resolve()

    if not src.is_dir():
        print(f"[ERROR] Source codebase directory '{src}' does not exist.")
        return False

    ws_name = workspace_name or dst.name or src.name
    ws_desc = description or f"Existing codebase {ws_name} adopted into ICM"

    # Copy source directory to destination if not in-place
    if src != dst:
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.name in [".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"]:
                continue
            dest_item = dst / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)

    # Scaffolding default stages for adopted codebase if none provided
    adopted_stages = stages or ["discovery", "tdd", "implementation", "verification"]

    # Wrap in ICM structure non-destructively
    scaffold_workspace(
        name=ws_name,
        target_dir=dst,
        topology=topology,
        description=ws_desc,
        stages=adopted_stages,
        with_pm=with_pm,
        with_compiler=with_compiler,
        with_skills=with_skills,
        with_governance=with_governance,
        allow_existing=True,
    )
    return True


def interactive_wizard():
    print("\n" + "=" * 65)
    print(" [*] Interpretable Context Methodology (ICM) — Workspace Wizard")
    print("=" * 65 + "\n")

    print("Choose workspace creation method:")
    print("  1. Archetype Fast-Track (Pre-configured domain preset)")
    print("  2. Socratic Custom Workspace (Topology 1-4 selection)")
    print("  3. Adopt Existing Codebase (--adopt non-destructive)")
    print("  4. Exit")

    choice = input("\nSelect an option [1-4]: ").strip()

    if choice == "1":
        archetypes = [d.name for d in ARCHETYPES_DIR.iterdir() if d.is_dir()]
        print("\nAvailable Archetypes:")
        for idx, arch in enumerate(archetypes, start=1):
            print(f"  {idx}. {arch}")

        arch_idx = int(input("\nSelect archetype number: ").strip()) - 1
        arch_name = archetypes[arch_idx]
        ws_name = input("\nEnter workspace name: ").strip()
        ws_desc = input("Enter brief workspace description: ").strip()

        target_path = DEFAULT_WORKSPACES_DIR / ws_name
        print(f"\n[+] Scaffolding workspace at {target_path}...")
        success = scaffold_from_archetype(arch_name, target_path, ws_name, ws_desc)
        if success:
            valid, errors = validate_workspace(target_path)
            if valid:
                print(f"\n[PASS] Successfully created and validated ICM workspace: {target_path}")
            else:
                print(f"\n[WARN] Validation warnings: {errors}")

    elif choice == "2":
        ws_name = input("\nEnter workspace name: ").strip()
        ws_desc = input("Enter workspace description: ").strip()
        print("\nSelect Topology:")
        print("  1. Lean Single-Pipeline (Stages only)")
        print("  2. Managed Single-Pipeline (Stages + docs/ STRATEGY & Sprints)")
        print("  3. Multi-Workflow Pipeline (workflows/ without PM)")
        print("  4. Enterprise Multi-Workflow & PM (workflows/ + docs/)")
        topo_choice = input("Select topology [1-4]: ").strip() or "2"

        stages_input = input("Enter stage names comma-separated (default: spec, tdd, impl, verify): ").strip()
        stage_names = [s.strip() for s in stages_input.split(",") if s.strip()] or ["spec", "tdd", "impl", "verify"]

        target_path = DEFAULT_WORKSPACES_DIR / ws_name
        print(f"\n[+] Scaffolding custom workspace at {target_path}...")
        success = scaffold_workspace(
            name=ws_name,
            target_dir=target_path,
            topology=topo_choice,
            description=ws_desc,
            stages=stage_names,
            with_pm=topo_choice in ["2", "4"],
            with_compiler=True,
            with_skills=True,
        )
        if success:
            valid, errors = validate_workspace(target_path)
            if valid:
                print(f"\n[PASS] Successfully created and validated ICM workspace: {target_path}")
            else:
                print(f"\n[WARN] Validation warnings: {errors}")

    elif choice == "3":
        src_path = input("\nEnter path to existing codebase: ").strip()
        ws_name = input("Enter workspace name: ").strip()
        target_path = DEFAULT_WORKSPACES_DIR / ws_name
        print(f"\n[+] Adopting codebase from {src_path} into {target_path}...")
        success = adopt_existing_codebase(src_path, target_path, workspace_name=ws_name)
        if success:
            valid, errors = validate_workspace(target_path)
            if valid:
                print(f"\n[PASS] Successfully adopted and validated ICM workspace: {target_path}")
            else:
                print(f"\n[WARN] Validation warnings: {errors}")
    else:
        print("Cancelled.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold or adopt an ICM workspace.")
    parser.add_argument("--name", help="Workspace folder name (inside ./workspaces/)")
    parser.add_argument("--description", help="Description of purpose")
    parser.add_argument("--topology", default="1", help="Topology type (1/lean, 2/managed, 3/multi-workflow, 4/enterprise)")
    parser.add_argument("--archetype", help="Archetype template name (e.g. software_feature, agile_software_engine)")
    parser.add_argument("--stages", help="Comma-separated list of stage names")
    parser.add_argument("--adopt", help="Path to existing codebase to adopt non-destructively")
    parser.add_argument("--with-pm", action="store_true", help="Add Project Management (docs/STRATEGY.md, phases)")
    parser.add_argument("--with-compiler", action="store_true", help="Add 5-Part Prompt Compiler (docs/backlog)")
    parser.add_argument("--with-skills", action="store_true", help="Add curated master skills bundle")
    parser.add_argument("--with-governance", action="store_true", help="Inject local validate_workspace.py")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive creation wizard")
    args = parser.parse_args()

    if args.interactive or (not args.name and not args.archetype and not args.adopt):
        interactive_wizard()
        return

    target_dir = DEFAULT_WORKSPACES_DIR / args.name if args.name else None

    if args.adopt:
        if not target_dir:
            target_dir = DEFAULT_WORKSPACES_DIR / Path(args.adopt).name
        print(f"[+] Adopting existing codebase from '{args.adopt}' into {target_dir}...")
        stages = [s.strip() for s in args.stages.split(",") if s.strip()] if args.stages else None
        success = adopt_existing_codebase(
            source_dir=args.adopt,
            target_dir=target_dir,
            workspace_name=args.name or target_dir.name,
            description=args.description,
            topology=args.topology,
            stages=stages,
            with_pm=args.with_pm,
            with_compiler=args.with_compiler,
            with_skills=args.with_skills,
            with_governance=args.with_governance,
        )
    elif args.archetype:
        print(f"[+] Scaffolding from archetype '{args.archetype}' into {target_dir}...")
        success = scaffold_from_archetype(args.archetype, target_dir, args.name, args.description)
    else:
        stages = [s.strip() for s in args.stages.split(",") if s.strip()] if args.stages else None
        print(f"[+] Scaffolding Topology {args.topology} workspace into {target_dir}...")
        success = scaffold_workspace(
            name=args.name,
            target_dir=target_dir,
            topology=args.topology,
            description=args.description,
            stages=stages,
            with_pm=args.with_pm,
            with_compiler=args.with_compiler,
            with_skills=args.with_skills,
            with_governance=args.with_governance,
        )

    if not success:
        sys.exit(1)

    valid, errors = validate_workspace(target_dir)
    if valid:
        print(f"[PASS] Workspace '{target_dir.name}' successfully scaffolded and verified compliant!")
    else:
        print(f"[FAIL] Scaffolding validation failed: {errors}")
        sys.exit(1)


if __name__ == "__main__":
    main()
