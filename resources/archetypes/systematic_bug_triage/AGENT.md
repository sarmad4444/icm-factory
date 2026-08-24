<!-- 💡 HOW THIS WORKS -->
# Systematic Bug Triage — Diagnostic & Fix Engine

**Mission:** Methodically reproduce bugs, diagnose root causes, write regression tests, and implement verified fixes.  
**Framework:** Interpretable Context Methodology (ICM)  
**Status:** Active

---

## 1. Operating Rules

1. Never attempt a fix without an isolated reproduction and failing regression test.
2. Formulate explicit hypotheses and test them against runtime evidence.
3. Verify fixes against the entire test suite before closing triage.

---

## 2. Stages Overview

- `stages/01_reproduction`: Minimal Reproduction & Environment Setup
- `stages/02_root_cause`: Root-Cause Hypothesis & Code Trace
- `stages/03_regression_test`: Automated Regression Test Creation
- `stages/04_fix_and_review`: Fix Implementation & Full Suite Verification
