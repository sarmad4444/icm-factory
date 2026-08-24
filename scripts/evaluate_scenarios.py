"""
scripts/evaluate_scenarios.py
Automated End-to-End AI and Logical Scenario Evaluation Runner.
Simulates and validates 5 real-world developer workflows across all 4 ICM Topologies.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
import tempfile

# Ensure root is in sys.path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from scripts.create_workspace import scaffold_workspace, adopt_existing_codebase
from scripts.validate_workspace import validate_workspace
from scripts.init_phase import init_phase
from scripts.manage_skills import add_skill, list_skills

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


def run_scenario_1_lean_utility(target_path: Path) -> tuple[bool, str]:
    """Scenario 1: Scaffolds Topology 1 Lean Single-Pipeline & validates structural compliance."""
    try:
        success = scaffold_workspace(
            name="lean_utility_service",
            target_dir=target_path,
            topology="1",
            description="High-speed data ingestion and batch transformation utility",
            stages=["fetch_data", "transform", "export"],
            with_skills=True,
        )
        if not success:
            return False, "scaffold_workspace returned False"

        valid, errors, warnings = validate_workspace(target_path).full()
        if not valid:
            return False, f"Validation failed with errors: {errors}"

        if not (target_path / "stages" / "01_fetch_data" / "CONTEXT.md").is_file():
            return False, "Missing stage 01 contract"
        if not (target_path / "skills" / "CONTEXT.md").is_file():
            return False, "Missing skills catalog"

        return True, "Topology 1 Lean Single-Pipeline scaffolded and 100% compliant."
    except Exception as e:
        return False, f"Exception in Scenario 1: {e}"


def run_scenario_2_enterprise_engine(target_path: Path) -> tuple[bool, str]:
    """Scenario 2: Scaffolds Topology 4 Enterprise Multi-Workflow & PM Engine with objective sprint phase."""
    try:
        workflows = {
            "backend_core": ["api_design", "tdd_harness", "service_impl"],
            "deployment_infra": ["terraform_plan", "canary_release"],
        }
        success = scaffold_workspace(
            name="enterprise_billing_platform",
            target_dir=target_path,
            topology="4",
            description="Multi-workflow distributed billing system with agile governance",
            workflows=workflows,
            with_pm=True,
            with_compiler=True,
            with_skills=True,
            with_governance=True,
        )
        if not success:
            return False, "scaffold_workspace returned False"

        # Initialize a new sprint phase
        phase_dir = init_phase(
            name="stripe_webhook_engine",
            number=2,
            workspace_dir=target_path,
            goal="Implement and verify Stripe webhook event receiver with idempotent storage",
        )

        valid, errors, warnings = validate_workspace(target_path).full()
        if not valid:
            return False, f"Validation failed with errors: {errors}"

        tasks_file = phase_dir / "tasks.md"
        if not tasks_file.is_file() or "TASK-02-A01" not in tasks_file.read_text(encoding="utf-8"):
            return False, "Phase 2 tasks.md missing valid TASK-02-A01 identifier"

        return True, "Topology 4 Enterprise Multi-Workflow Engine & Sprint Phase 02 validated."
    except Exception as e:
        return False, f"Exception in Scenario 2: {e}"


def run_scenario_3_codebase_adoption(target_path: Path) -> tuple[bool, str]:
    """Scenario 3: Non-destructively wraps an existing codebase into ICM without touching application files."""
    try:
        # Create a mock existing repository
        with tempfile.TemporaryDirectory() as temp_repo:
            src = Path(temp_repo)
            (src / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
            (src / "pyproject.toml").write_text("[project]\nname = 'existing-api'\n", encoding="utf-8")
            services_dir = src / "services"
            services_dir.mkdir()
            (services_dir / "payment.py").write_text("def process_payment(): return True\n", encoding="utf-8")

            # Adopt into target path
            success = adopt_existing_codebase(
                source_dir=src,
                target_dir=target_path,
                workspace_name="adopted_payment_api",
                description="Payment API adopted into ICM Topology 2",
                topology="managed",
                stages=["discovery", "tdd", "implementation", "verification"],
            )
            if not success:
                return False, "adopt_existing_codebase returned False"

            # Check original code preservation
            if (target_path / "app.py").read_text(encoding="utf-8") != "from fastapi import FastAPI\napp = FastAPI()\n":
                return False, "Source file app.py was modified during adoption!"
            if (target_path / "services" / "payment.py").read_text(encoding="utf-8") != "def process_payment(): return True\n":
                return False, "Source file payment.py was modified during adoption!"

            # Check ICM compliance
            valid, errors, warnings = validate_workspace(target_path).full()
            if not valid:
                return False, f"Adopted workspace failed validation: {errors}"

            return True, "Existing codebase non-destructively wrapped in ICM control plane."
    except Exception as e:
        return False, f"Exception in Scenario 3: {e}"


def run_scenario_4_governance_conflicts(target_path: Path) -> tuple[bool, str]:
    """Scenario 4: Tests deep rule contradiction detection, dead links, and auto-fix recovery."""
    try:
        # Scaffold valid base workspace
        scaffold_workspace(
            name="governance_test_ws",
            target_dir=target_path,
            topology="1",
            stages=["stage_one", "stage_two"],
        )

        # Inject forbidden command (npm install) and broken link into AGENT.md
        agent_file = target_path / "AGENT.md"
        agent_text = agent_file.read_text(encoding="utf-8")
        corrupted_agent = (
            agent_text
            + "\n\n## Temporary Rule\nRun `npm install dangerous-pkg` for tooling.\n"
            + "See also [`missing_doc.md`](file://./missing_doc.md).\n"
        )
        agent_file.write_text(corrupted_agent, encoding="utf-8")

        # Remove output directory from stage_two to test auto-fix
        stage2_output = target_path / "stages" / "02_stage_two" / "output"
        if stage2_output.is_dir():
            shutil.rmtree(stage2_output)

        # Run validation - must catch errors
        res_corrupted = validate_workspace(target_path)
        if res_corrupted.valid:
            return False, "Validator failed to catch injected npm contradiction and missing output folder!"

        has_rule_err = any("npm" in e.lower() for e in res_corrupted.errors)
        has_output_err = any("output" in e.lower() for e in res_corrupted.errors)
        has_dead_link_warn = any("missing_doc.md" in w for w in res_corrupted.warnings)

        if not (has_rule_err and has_output_err and has_dead_link_warn):
            return False, f"Missing expected error/warning categories. Errors: {res_corrupted.errors}, Warnings: {res_corrupted.warnings}"

        # Clean the rule contradiction and run auto-fix
        clean_agent = corrupted_agent.replace("Run `npm install dangerous-pkg` for tooling.\n", "").replace("See also [`missing_doc.md`](file://./missing_doc.md).\n", "")
        agent_file.write_text(clean_agent, encoding="utf-8")

        res_fixed = validate_workspace(target_path, fix=True, non_interactive=True)
        if not res_fixed.valid:
            return False, f"Auto-fix failed to restore workspace compliance: {res_fixed.errors}"

        return True, "Rule contradictions, dead links, and auto-fix recovery verified."
    except Exception as e:
        return False, f"Exception in Scenario 4: {e}"


def run_scenario_5_skills_sync(target_path: Path) -> tuple[bool, str]:
    """Scenario 5: Verifies dynamic skill addition, JIT discovery metadata, and catalog sync."""
    try:
        scaffold_workspace(
            name="skills_dynamic_ws",
            target_dir=target_path,
            topology="1",
            stages=["spec", "run"],
            with_skills=True,
        )

        # Add custom skill dynamically
        add_skill(
            name="distributed_tracer",
            url="https://github.com/obra/distributed_tracer",
            commit="v2.1.0",
            trigger="trace latency, trace spans",
            description="Distributed OpenTelemetry tracing and span inspector",
            workspace_dir=target_path,
        )

        skills = list_skills(target_path)
        tracer_skill = next((s for s in skills if s["name"] == "distributed_tracer"), None)
        if not tracer_skill:
            return False, "distributed_tracer not found in list_skills"

        if tracer_skill["version"] != "v2.1.0" or "trace latency" not in tracer_skill["trigger"]:
            return False, f"Skill metadata mismatch: {tracer_skill}"

        manifest_text = (target_path / "skills" / "CONTEXT.md").read_text(encoding="utf-8")
        if "distributed_tracer" not in manifest_text:
            return False, "skills/CONTEXT.md was not updated with distributed_tracer"

        valid, errors, _ = validate_workspace(target_path).full()
        if not valid:
            return False, f"Validation failed after adding skill: {errors}"

        return True, "Dynamic skills installation, metadata pinning, and catalog sync verified."
    except Exception as e:
        return False, f"Exception in Scenario 5: {e}"


def run_all_scenarios(base_dir: Path | None = None) -> bool:
    print("\n" + "=" * 80)
    print(" [*] Running ICM End-to-End AI & Logical Scenario Evaluations")
    print("=" * 80 + "\n")

    scenarios = [
        ("Scenario 1: Lean Utility Creation (Topology 1)", run_scenario_1_lean_utility),
        ("Scenario 2: Enterprise Multi-Workflow & PM Engine (Topology 4)", run_scenario_2_enterprise_engine),
        ("Scenario 3: Existing Codebase Adoption (--adopt)", run_scenario_3_codebase_adoption),
        ("Scenario 4: Governance Contradiction Audit & Auto-Fix", run_scenario_4_governance_conflicts),
        ("Scenario 5: Dynamic Skills JIT Discovery & Manifest Sync", run_scenario_5_skills_sync),
    ]

    all_passed = True
    results = []

    with tempfile.TemporaryDirectory() as temp_root:
        root_path = Path(base_dir) if base_dir else Path(temp_root)

        for idx, (title, runner_fn) in enumerate(scenarios, start=1):
            scen_dir = root_path / f"scenario_{idx}"
            scen_dir.mkdir(parents=True, exist_ok=True)

            print(f"[*] Executing {title}...")
            passed, detail = runner_fn(scen_dir)
            results.append((title, passed, detail))
            if not passed:
                all_passed = False
                print(f"  [FAIL] {detail}\n")
            else:
                print(f"  [PASS] {detail}\n")

    # Render summary table
    if console:
        table = Table(title="ICM End-to-End Scenario Evaluation Results", expand=True)
        table.add_column("Scenario", style="bold cyan")
        table.add_column("Result", justify="center")
        table.add_column("Details", style="dim")

        for title, passed, detail in results:
            res_str = "[bold green]PASS[/bold green]" if passed else "[bold red]FAIL[/bold red]"
            table.add_row(title, res_str, detail)

        console.print(table)
        if all_passed:
            console.print(Panel("[bold green]100% SUCCESS: All 5 ICM Scenarios Passed Verification![/bold green]"))
        else:
            console.print(Panel("[bold red]EVALUATION FAILURE: One or more scenarios failed.[/bold red]"))
    else:
        print("\n" + "=" * 80)
        print("Summary of Results:")
        for title, passed, detail in results:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {title}: {detail}")
        print("=" * 80 + "\n")

    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Run ICM End-to-End Logical Scenarios.")
    parser.add_argument("--dir", help="Optional specific directory to execute scenarios in")
    args = parser.parse_args()

    success = run_all_scenarios(Path(args.dir) if args.dir else None)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
