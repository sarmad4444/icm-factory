---
name: superpowers
description: "Rigorous agentic software engineering system: Test-Driven Development (TDD), step-by-step implementation plans, systematic debugging, and subagent orchestration."
trigger: "superpowers, tdd, test-driven-development, systematic-debugging, writing-plans, executing-plans"
url: "https://github.com/obra/superpowers"
version: "v3.4.0"
---

# Superpowers Agentic Software Engineering Suite

When activated, this skill enforces rigorous engineering disciplines across the entire software development lifecycle.

---

## 1. Core Disciplines

### Discipline 1: Test-Driven Development (TDD)
- **Iron Rule**: Never write production implementation code before writing a failing test.
- **Red-Green-Refactor Cycle**:
  1. **Red**: Write a minimal, focused test capturing acceptance criteria. Run `pytest` to confirm failure.
  2. **Green**: Write the simplest code to make the test pass. Run test to verify 100% green output.
  3. **Refactor**: Clean up code and eliminate duplication while keeping tests passing.

### Discipline 2: Structured Implementation Plans
- Break complex initiatives into small, atomic tasks.
- For each task, specify:
  - Exact file paths to create/modify.
  - Interface contracts (inputs & outputs).
  - Explicit test command with expected result.
  - Verification checkpoint.

### Discipline 3: Systematic Debugging
- **Four-Step Protocol**:
  1. **Reproduce**: Write an automated reproduction script or test.
  2. **Isolate**: Inspect logs, variable states, and root causes before touching code.
  3. **Fix**: Apply minimal targeted fix.
  4. **Verify**: Run full test suite to ensure zero regressions.

### Discipline 4: Evidence-Based Verification Before Claims
- Never claim a task is completed, fixed, or passing without executing the real test command and inspecting stdout/stderr.
- Evidence before assertions always.
