# Stage 05: Validation & Quality Audit

**Purpose:** Run automated compliance audits and cross-stage contract verifications to validate workspace health.

---

## Inputs

| Layer | Source File | Description |
| :--- | :--- | :--- |
| **Layer 3 (Reference)** | `references/checklist.md` | Pre-flight validation checklist and heuristics |
| **Layer 3 (Reference)** | `../../resources/foundations/quality_standards.md` | Master quality thresholds and test gates |
| **Layer 4 (Working)** | `../04_factory_setup/output/factory_configs.md` | Configured workspace files from Stage 04 |

---

## Process

1. **Run Compliance Audit:** Execute `uv run python scripts/validate_workspace.py [target_path]`.
2. **Verify Interfaces:** Confirm sequential handoffs between all stage outputs and downstream inputs.
3. **Generate Report:** Compile the 4-tier validation audit results.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `audit_report.md` | `output/audit_report.md` | 100% 4-tier health compliance and clean contract audit |
