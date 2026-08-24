<!-- 💡 HOW THIS WORKS -->
<!-- This file defines who the AI is, what mission it is executing, and the overall rules and floor plan for this project. -->

# {WORKSPACE_NAME} — Agent Operating Guide

**Purpose:** {WORKSPACE_DESCRIPTION}

---

## 1. Operating Rules & Principles

* **Self-Contained Workspace:** All work, state, and outputs remain organized inside this project directory.
* **Predictable Pipeline:** Move sequentially through defined workflow stages or active sprint phases.
* **Evidence-Based Execution:** Write failing tests first, implement minimal code, and verify before completion.
* **Tooling Standard:** Run Python via `uv run` and Node tools via `bun`/`bunx`.

---

## 2. Workspace Floor Plan

| Resource / Directory | Role | Description |
| :--- | :--- | :--- |
| [`AGENT.md`](file://./AGENT.md) | Identity Contract | Project identity, operating rules, and floor plan |
| [`CONTEXT.md`](file://./CONTEXT.md) | Task Router | Master intent router mapping goals to stage contracts |
| `resources/quality_standards.md` | Quality Standards | Project-specific style rules and quality constraints |
{OPTIONAL_DOCS_SUMMARY}
{OPTIONAL_SKILLS_SUMMARY}
{OPTIONAL_AGENTS_SUMMARY}
{WORKFLOW_OR_STAGES_SUMMARY}

---

## 3. How to Start Work

1. **Find Intent:** Match your goal in [`CONTEXT.md`](file://./CONTEXT.md) to find the right directory.
2. **Read Contract:** Review the stage `CONTEXT.md` or initiative before executing.
3. **Execute & Verify:** Output deliverables to designated directories and run verification tests.
