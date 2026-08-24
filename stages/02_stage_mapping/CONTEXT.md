# Stage 02: Stage Mapping & Blueprinting

**Purpose:** Decompose the domain brief into discrete sequential stages following the "one stage, one job" rule to produce the workspace blueprint.

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Layer 3 (Reference)** | `references/patterns.md` | Pipeline decomposition and stage boundary patterns |
| **Layer 3 (Reference)** | `../../resources/foundations/quality_standards.md` | Interface validation standards and contract rules |
| **Layer 4 (Working)** | `../01_discovery/output/domain_brief.md` | Domain requirements brief from Stage 01 |

---

## Process

1. **Deconstruct Workflow:** Break requirements into sequential `NN_stagename` folders.
2. **Define Stage Contracts:** Specify explicit Layer 3 references and Layer 4 inputs/outputs for each stage.
3. **Build Blueprint:** Generate the complete pipeline topology and handoff matrix.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `stage_blueprint.md` | `output/stage_blueprint.md` | Verified stage list, numbering, inputs, processes, and outputs |
