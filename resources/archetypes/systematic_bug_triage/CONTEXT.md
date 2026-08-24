<!-- 💡 HOW THIS WORKS -->
# Systematic Bug Triage — Task Routing Guide

**Purpose:** Task router for the bug triage and repair pipeline.

---

## 1. Intent Router

| Stage / Action | Directory | Contract | Deliverables |
|---|---|---|---|
| 01. Bug Reproduction | `stages/01_reproduction/` | [`CONTEXT.md`](file://./stages/01_reproduction/CONTEXT.md) | `stages/01_reproduction/output/reproduction_steps.md` |
| 02. Root Cause Analysis | `stages/02_root_cause/` | [`CONTEXT.md`](file://./stages/02_root_cause/CONTEXT.md) | `stages/02_root_cause/output/root_cause_analysis.md` |
| 03. Regression Test | `stages/03_regression_test/` | [`CONTEXT.md`](file://./stages/03_regression_test/CONTEXT.md) | `stages/03_regression_test/output/regression_test_plan.md` |
| 04. Fix & Verification | `stages/04_fix_and_review/` | [`CONTEXT.md`](file://./stages/04_fix_and_review/CONTEXT.md) | `stages/04_fix_and_review/output/triage_summary.md` |
