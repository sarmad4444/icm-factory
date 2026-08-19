# Stage 03: Scaffolding Generation — Contract

**Layer:** Layer 2 (Stage Execution Contract)  
**Stage Name:** `03_scaffolding`

---

## Inputs

- **Layer 3 (Reference):** `references/standards.md`
- **Layer 3 (Reference):** `../../shared/templates/`
- **Layer 4 (Working):** `../02_stage_mapping/output/stage_blueprint.md`

---

## Process

1. Read the stage blueprint from Stage 02.
2. Generate all directories under `workspaces/[workspace-name]/` (`stages/`, `_config/`, `shared/`, `setup/`).
3. Render Layer 0 (`AGENT.md`), Layer 1 (`CONTEXT.md`), and each stage's Layer 2 (`CONTEXT.md`).
4. Output the generation manifest and scaffolding log.

---

## Outputs

- `scaffolding_plan.md` -> `output/scaffolding_plan.md`
