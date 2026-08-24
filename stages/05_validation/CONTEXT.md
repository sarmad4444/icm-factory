# Stage 05: Validation & Quality Audit — Contract

**Layer:** Layer 2 (Stage Execution Contract)  
**Stage Name:** `05_validation`

---

## Inputs

- **Layer 3 (Reference):** `references/checklist.md`
- **Layer 3 (Reference):** `../../resources/foundations/quality_standards.md`
- **Layer 4 (Working):** `../04_factory_setup/output/factory_configs.md`

---

## Process

1. Run automated ICM compliance validator (`uv run python scripts/validate_workspace.py [target_path]`).
2. Audit cross-stage contracts (ensure Stage 02 inputs match Stage 01 outputs, etc.).
3. Verify that all required reference templates are populated.
4. Produce the final Validation and Readiness Audit Report.

---

## Outputs

- `audit_report.md` -> `output/audit_report.md`
