# ICM Workspace Builder & Multi-Workspace Architecture Design

**Date:** 2026-08-19  
**Status:** Validated / Ready for Implementation  
**Root Workspace:** `d:/AI Projects/icm-generated`  
**Philosophy Reference:** [`SOUL.md`](file:///d:/AI%20Projects/icm-generated/SOUL.md)

---

## 1. Overview & Objectives

Interpretable Context Methodology (ICM) replaces code-heavy agent orchestration frameworks with an organized filesystem hierarchy:
- Numbered folders dictate stage order.
- Plain markdown files define prompt contracts, routing, and reference constraints.
- Local scripts handle purely mechanical automation without AI overhead.
- Human review gates at each stage boundary provide complete glass-box observability and editability.

This project (`./icm-generated`) is the **Master Workspace Builder**. It operates on ICM principles to discover, map, scaffold, configure, and validate standalone child ICM workspaces inside `./workspaces/[workspace-name]`.

---

## 2. Five-Layer Context Hierarchy

Both the Master Builder and all child workspaces strictly adhere to the 5-Layer Context Hierarchy:

| Layer | Name | File/Path | Role & Description |
|---|---|---|---|
| **Layer 0** | Global Identity | `AGENT.md` / `GEMINI.md` / `CLAUDE.md` | Defines agent identity, workspace mission, directory topology, and core rules. |
| **Layer 1** | Task Routing | Root `CONTEXT.md` | Routes user tasks to the appropriate stage or tool based on current intent. |
| **Layer 2** | Stage Contracts | `stages/NN_<name>/CONTEXT.md` | Specifies strict contract: `Inputs` (Layer 3 & 4 files), `Process` rules, and `Outputs`. |
| **Layer 3** | The Factory (Reference) | `_config/`, `shared/`, `stages/*/references/` | Stable reference material: voice guides, rules, templates, conventions. Configured once. |
| **Layer 4** | The Product (Working) | `stages/*/output/` | Per-run dynamic inputs and outputs passed sequentially across stage review gates. |

---

## 3. Directory Layout of Master Builder (`./icm-generated`)

```
d:/AI Projects/icm-generated/
├── SOUL.md                          # ICM Manifesto & Theoretical Foundation
├── AGENT.md                         # [Layer 0] Master Builder Agent Identity & Guide
├── GEMINI.md                        # [Layer 0] Gemini compatibility link/identity
├── CONTEXT.md                       # [Layer 1] Master Task Router
│
├── stages/                          # Master ICM Generation Pipeline (5 Stages)
│   ├── 01_discovery/
│   │   ├── CONTEXT.md               # [Layer 2] Discovery Stage Contract
│   │   ├── references/              # [Layer 3] Domain questioning heuristics
│   │   └── output/                  # [Layer 4] Domain & workflow requirement briefs
│   │
│   ├── 02_stage_mapping/
│   │   ├── CONTEXT.md               # [Layer 2] Stage Mapping Contract
│   │   ├── references/              # [Layer 3] Stage decomposition patterns
│   │   └── output/                  # [Layer 4] Stage blueprint & handoff matrix
│   │
│   ├── 03_scaffolding/
│   │   ├── CONTEXT.md               # [Layer 2] Scaffolding Contract
│   │   ├── references/              # [Layer 3] File naming and folder structure rules
│   │   └── output/                  # [Layer 4] Scaffolding manifest & scripts
│   │
│   ├── 04_factory_setup/
│   │   ├── CONTEXT.md               # [Layer 2] Factory Setup Contract
│   │   ├── references/              # [Layer 3] Archetype configs & questionnaire templates
│   │   └── output/                  # [Layer 4] Child Layer 3 reference files
│   │
│   └── 05_validation/
│       ├── CONTEXT.md               # [Layer 2] Validation Contract
│       ├── references/              # [Layer 3] ICM compliance checklist
│       └── output/                  # [Layer 4] Validation audit reports
│
├── _config/                         # [Layer 3] Master Configuration & Archetypes
│   ├── icm_rules.md                 # Definitive ICM structural and contract rules
│   └── archetypes/                  # Ready-to-use template archetypes
│       ├── content_pipeline/        # 3 Stages: Research -> Script -> Production
│       ├── research_synthesis/      # 4 Stages: Ingestion -> Extraction -> Synthesis -> Report
│       ├── course_deck/             # 5 Stages: Content -> Structure -> Slides -> Visuals -> Assembly
│       ├── software_feature/        # 4 Stages: Spec -> TDD -> Implementation -> Verification
│       └── minimal_starter/         # 2 Stages: Ingest -> Process
│
├── shared/                          # [Layer 3] Reusable Templates
│   └── templates/
│       ├── child_agent_md.tmpl      # Template for child Layer 0 AGENT.md
│       ├── child_context_l1.tmpl    # Template for child Layer 1 CONTEXT.md
│       ├── child_stage_l2.tmpl      # Template for child Layer 2 stage CONTEXT.md
│       └── questionnaire.md         # Onboarding questionnaire for child workspace setup
│
├── scripts/                         # Mechanical Automation Tools (Python 3)
│   ├── create_workspace.py          # Interactive wizard & CLI to generate child workspaces
│   ├── validate_workspace.py        # Audits child workspaces for strict ICM compliance
│   └── list_workspaces.py           # Summarizes all workspaces in ./workspaces
│
└── workspaces/                      # Destination directory for generated child workspaces
    └── [workspace-name]/            # Self-contained child ICM workspace
```

---

## 4. Child Workspace Topology (`./workspaces/[workspace-name]`)

Each child workspace is completely autonomous and portable:

```
workspaces/[workspace-name]/
├── AGENT.md                         # [Layer 0] Workspace Identity & Purpose
├── CONTEXT.md                       # [Layer 1] Workspace Task Routing
├── _config/                         # [Layer 3] Workspace-level reference & rules (The Factory)
│   ├── rules.md
│   └── conventions.md
├── shared/                          # [Layer 3] Shared assets & templates
├── stages/
│   ├── 01_[stage_name]/
│   │   ├── CONTEXT.md               # [Layer 2] Stage Contract (Inputs, Process, Outputs)
│   │   ├── references/              # [Layer 3] Stage-specific reference constraints
│   │   └── output/                  # [Layer 4] Stage working artifacts & edit surface
│   ├── 02_[stage_name]/
│   │   ├── CONTEXT.md
│   │   ├── references/
│   │   └── output/
│   └── ...
└── setup/
    └── questionnaire.md             # Initial domain configuration answers
```

---

## 5. Three-Option Workspace Initialization Flow

Whenever a workspace is to be created or configured, the system offers 3 distinct paths:

1. **Option 1: Interactive Custom Pipeline (5-Stage ICM)**
   - Used for complex or novel workflows.
   - Executes through the master stages `01_discovery` $\rightarrow$ `02_stage_mapping` $\rightarrow$ `03_scaffolding` $\rightarrow$ `04_factory_setup` $\rightarrow$ `05_validation`.
   - Produces detailed blueprints and tailor-made stage contracts with human review at each step.

2. **Option 2: Archetype Fast-Track (Instant Scaffolding)**
   - Clones one of the pre-built, tested archetypes (`content_pipeline`, `research_synthesis`, `course_deck`, `software_feature`, or `minimal_starter`).
   - Automatically renames, customizes identities, and generates clean directories in seconds.

3. **Option 3: Quick CLI Questionnaire (Script-Assisted)**
   - Runs `python scripts/create_workspace.py --interactive`.
   - Interactively queries workspace name, stage names, and purpose, generating valid contracts and folders immediately.

---

## 6. Python Automation Scripts Specification

1. **`scripts/create_workspace.py`**:
   - Accepts flags (`--name`, `--archetype`, `--interactive`, `--stages`).
   - Creates full folder tree including `.gitkeep` files in `output/`.
   - Renders templates for `AGENT.md`, `CONTEXT.md`, and stage contracts.
   - Validates the resulting workspace immediately upon creation.

2. **`scripts/validate_workspace.py`**:
   - Takes `--path` or `--name`.
   - Audits:
     - Existence of Layer 0 (`AGENT.md`).
     - Existence of Layer 1 (`CONTEXT.md`).
     - Sequential numbering of `stages/` (`01_*`, `02_*`, etc.).
     - Existence of Layer 2 `CONTEXT.md` in every stage with valid `## Inputs`, `## Process`, and `## Outputs` sections.
     - Separation of `references/` (Layer 3) and `output/` (Layer 4).
   - Outputs a detailed color-coded compliance report and exit code `0` (pass) or `1` (fail).

3. **`scripts/list_workspaces.py`**:
   - Scans `./workspaces/` directory.
   - Prints a formatted table of all child workspaces, their description, stage count, and ICM validation status.

---

## 7. Verification Plan

1. **Self-Consistency & Rule Verification**:
   - Run `python scripts/validate_workspace.py` against the root master builder itself to verify root ICM compliance.
2. **Archetype Generation Tests**:
   - Test generating all 5 archetypes into `./workspaces/test_*` and validate each with `validate_workspace.py`.
3. **Interactive Script Tests**:
   - Execute CLI creation with custom stages and verify output structure and contract contents.
4. **Clean-Up**:
   - Remove temporary test workspaces after validation, ensuring a pristine clean project repository.
