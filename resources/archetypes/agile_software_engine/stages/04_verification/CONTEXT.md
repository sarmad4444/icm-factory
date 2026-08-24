# Stage 04: Verification & Signoff — Contract

**Stage:** `stages/04_verification`  
**Purpose:** Run complete regression test suite and verify Definition of Done.

---

## Inputs

- `stages/03_implementation/output/impl_summary.md`
- `docs/phases/phase_01_mvp_core/goals.md`

---

## Process

1. Execute full verification suite (`uv run pytest -v`).
2. Verify all acceptance criteria and Definition of Done items.
3. Update task status in `docs/phases/phase_01_mvp_core/tasks.md`.

---

## Outputs

- `stages/04_verification/output/verification_report.md`
