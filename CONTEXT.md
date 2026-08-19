# Master Workspace Builder — Task Routing Guide

**Layer:** Layer 1 (Master Task Routing)  
**Domain:** Interpretable Context Methodology (ICM) Workspace Generation & Management

---

## 1. Routing by User Intent

| Intent / Goal | Recommended Action / Stage | Contract / Script | Outputs / Handoff |
|---|---|---|---|
| **Create custom novel workspace** | Master Pipeline Stage 01 | [`stages/01_discovery/CONTEXT.md`](file://./stages/01_discovery/CONTEXT.md) | `stages/01_discovery/output/domain_brief.md` |
| **Map stages & handoffs** | Master Pipeline Stage 02 | [`stages/02_stage_mapping/CONTEXT.md`](file://./stages/02_stage_mapping/CONTEXT.md) | `stages/02_stage_mapping/output/stage_blueprint.md` |
| **Generate folder tree & contracts** | Master Pipeline Stage 03 | [`stages/03_scaffolding/CONTEXT.md`](file://./stages/03_scaffolding/CONTEXT.md) | `stages/03_scaffolding/output/scaffolding_plan.md` |
| **Configure Layer 3 factory reference** | Master Pipeline Stage 04 | [`stages/04_factory_setup/CONTEXT.md`](file://./stages/04_factory_setup/CONTEXT.md) | `stages/04_factory_setup/output/factory_configs.md` |
| **Validate ICM compliance of workspace** | Master Pipeline Stage 05 | [`stages/05_validation/CONTEXT.md`](file://./stages/05_validation/CONTEXT.md) | `stages/05_validation/output/audit_report.md` |
| **Fast-track archetype instantiation** | Fast CLI Automation | `uv run python scripts/create_workspace.py --archetype [name]` | `workspaces/[workspace-name]/` |
| **Audit an existing child workspace** | CLI Validation Tool | `uv run python scripts/validate_workspace.py [path]` | Terminal Audit Report |
| **List and inspect all workspaces** | CLI Inspection Tool | `uv run python scripts/list_workspaces.py` | Terminal Summary Table |

---

## 2. Archetype Catalog (Layer 3)

Located in [`_config/archetypes/`](file://./_config/archetypes/):
- `content_pipeline`: 3-stage Video & Script production pipeline
- `research_synthesis`: 4-stage Literature & Document extraction/synthesis
- `course_deck`: 5-stage Educational slide presentation builder
- `software_feature`: 4-stage Specification -> TDD -> Implementation -> Verification
- `minimal_starter`: 2-stage Clean starter pipeline
