<!-- 💡 HOW THIS WORKS -->
<!-- This file defines a specialized Agent Chamber persona, execution pipeline, and guardrails. -->

# Agent Identity: {AGENT_TITLE} (`@{AGENT_HANDLE}`)

**Purpose:** {AGENT_MISSION}

---

## 1. Allowed Skills & Tools (Mounted Envelope)

| Skill / Tool | Mount Location | Trigger Condition |
| :--- | :--- | :--- |
| `{SKILL_1_NAME}` | `{SKILL_1_PATH}` | {SKILL_1_TRIGGER} |
| `{SKILL_2_NAME}` | `{SKILL_2_PATH}` | {SKILL_2_TRIGGER} |

---

## 2. Private Execution Pipeline

1. **Context Ingestion:** Read input artifacts from `## Inputs` or assigned sprint task in `docs/phases/*/tasks.md`.
2. **Deterministic Processing:** Execute domain specialization tasks adhering strictly to project standards.
3. **Verification & Testing:** Run designated test and lint commands (`{SAMPLE_VERIFY_COMMAND}`).
4. **Deliverable Handshake:** Write verified outputs to designated `output/` path or log handoff deliverable.

---

## 3. Operating Constraints & Negative Guardrails

* **Scope Invariant:** {POSITIVE_CONSTRAINT_1}
* **Quality Invariant:** {POSITIVE_CONSTRAINT_2}
* **Forbidden:** {FORBIDDEN_ACTION_1}
* **Forbidden:** {FORBIDDEN_ACTION_2}
