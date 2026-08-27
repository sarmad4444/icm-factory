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

1. **Step 1 (Tier A Mechanical Gate):** Run `uv run python scripts/validate_workspace.py [target_path]`.
2. **Step 2 (Tier B Semantic AI Audit):** Review contracts against `resources/foundations/quality_standards.md` (§8, §9, §10 checklist).
3. **Step 3 (Intelligent Auto-Correction):** AI directly refactors any non-compliant link anchors or prompt structures.
4. **Step 4 (Knowledge Graph Sync):** Run `graphify --update` and verify knowledge graph health.
5. **Step 5 (Generate Report):** Compile final audit summary to `output/audit_report.md`.

---

## Outputs

| Output Deliverable | Target Path | Success Criteria |
| :--- | :--- | :--- |
| `audit_report.md` | `output/audit_report.md` | 100% 4-tier health compliance and clean contract audit |
