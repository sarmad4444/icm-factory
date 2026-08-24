# Stage 03: Regression Test — Contract

**Stage:** `stages/03_regression_test`  
**Purpose:** Create a standalone automated test that fails before the fix.

---

## Inputs

- `stages/02_root_cause/output/root_cause_analysis.md`
- Test framework configuration

---

## Process

1. Write a minimal unit/integration test capturing the defect.
2. Run the test suite and verify the test fails with the expected assertion error.
3. Document the failing test signature and failure output.

---

## Outputs

- `stages/03_regression_test/output/regression_test_plan.md`
