# Stage 03: Scaffolding Generation

**Purpose:** Scaffold the directory tree and render Layer 0, Layer 1, and Layer 2 contracts for the target workspace.

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Layer 3 (Reference)** | `references/standards.md` | Scaffolding directory layout and file standards |
| **Layer 3 (Reference)** | `../../resources/templates/` | Master contract templates (`AGENT.template.md`, `CONTEXT.template.md`) |
| **Layer 4 (Working)** | `../02_stage_mapping/output/stage_blueprint.md` | Validated stage blueprint from Stage 02 |

---

## Process

1. **Create Directories:** Generate `stages/`, `resources/`, `docs/`, and `skills/` under `workspaces/[name]/`.
2. **Render Contracts:** Populate Layer 0 (`AGENTS.md`), Layer 1 (`CONTEXT.md`), and stage Layer 2 (`CONTEXT.md`).
3. **Log Manifest:** Output the generation manifest and file creation record.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `scaffolding_plan.md` | `output/scaffolding_plan.md` | Rendered workspace directories and contract manifest |
