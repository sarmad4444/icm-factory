<!-- 💡 HOW THIS WORKS -->
<!-- This file tracks the live strategy, active sprint phase, and technical conventions for this project. -->

# Project Strategy & Live Status

**Project Name:** {WORKSPACE_NAME}  
**Active Phase:** `{ACTIVE_PHASE}`  
**Current Milestone:** {CURRENT_MILESTONE}

---

## 1. Active Objectives

- **Current Focus:** {CURRENT_FOCUS}
- **Active Phase Directory:** [`docs/phases/{ACTIVE_PHASE}/`](file://./docs/phases/{ACTIVE_PHASE}/)
- **Active Task Board:** [`docs/phases/{ACTIVE_PHASE}/tasks.md`](file://./docs/phases/{ACTIVE_PHASE}/tasks.md)

---

## 2. Technical Architecture & Decisions

- Architecture documents and Architecture Decision Records (ADRs) live in [`docs/architecture/`](file://./docs/architecture/).
- New architectural proposals follow the ADR template in `docs/architecture/adrs/`.

---

## 3. Project Phase Roadmap

| Phase | Name | Goal | Status |
|---|---|---|---|
{PHASE_ROADMAP_ROWS}

---

## 4. Work Conventions

- **Task IDs:** Use `TASK-[PHASE]-[CATEGORY]-[NUMBER]` format (e.g. `TASK-01-A01`).
- **Checkboxes:** Keep task completion accurate using `- [ ]` and `- [x]`.
- **Git Commit Association:** Tag commits with the task identifier (e.g. `feat(auth): TASK-01-A01 setup oauth provider`).
