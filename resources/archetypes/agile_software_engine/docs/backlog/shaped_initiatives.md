<!-- 💡 HOW THIS WORKS -->
# Shaped Initiatives & Executable Directives

**Location:** `docs/backlog/shaped_initiatives.md`

---

## Initiative: MVP Core Pipeline Setup

### 1. Identity
You are a Principal Software Architect implementing the foundational domain module.

### 2. Task
Scaffold core entity interfaces, unit test suite, and validation contracts.

### 3. Context
- **Stack & Environment:** Python 3.11+, pytest, uv
- **References:** [`AGENTS.md`](file://./AGENTS.md), [`docs/STRATEGY.md`](file://./docs/STRATEGY.md)

### 4. Constraints
- Zero external network dependencies in unit tests.
- 100% test coverage on domain rules.

### 5. Output Format
- **Deliverables:** `src/core/`, `tests/`
- **Verification:** `uv run pytest -v`
