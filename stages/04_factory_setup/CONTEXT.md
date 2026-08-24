# Stage 04: Factory Reference Configuration

**Purpose:** Configure Layer 3 reference files, quality standards, and onboarding questionnaires for the child workspace.

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Layer 3 (Reference)** | `references/guidelines.md` | Factory reference configuration guidelines |
| **Layer 3 (Reference)** | `../../resources/templates/` | Reference templates for standards, voice, and conventions |
| **Layer 4 (Working)** | `../03_scaffolding/output/scaffolding_plan.md` | Scaffolding generation manifest from Stage 03 |

---

## Process

1. **Configure Standards:** Populate `resources/quality_standards.md` and domain convention files.
2. **Setup Questionnaire:** Initialize `setup/questionnaire.md` for guided user onboarding.
3. **Export Summary:** Record configured tools, skills, and references.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `factory_configs.md` | `output/factory_configs.md` | Populated Layer 3 references and configured onboarding setup |
