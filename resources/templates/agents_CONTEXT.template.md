<!-- 💡 HOW THIS WORKS -->
<!-- This is the Master Agent Task Router for multi-agent task dispatching. -->

# Agent Directory & Task Routing Matrix

**Purpose:** Master Layer 1 routing matrix that maps task categories, intent triggers, and file glob patterns to specialized agent chambers in `agents/`.

---

## 1. Active Agent Roster & Dispatch Matrix

| Task Category / Trigger | File Pattern Glob | Assigned Agent | Agent Chamber Location |
| :--- | :--- | :--- | :--- |
| **Architecture & Systems Design** | `docs/architecture/**`, `adrs/**` | `@architect` | [`agents/architect/AGENT.md`](file://./agents/architect/AGENT.md) |
| **Core Engineering & Implementation** | `src/**`, `lib/**` | `@lead_engineer` | [`agents/lead_engineer/AGENT.md`](file://./agents/lead_engineer/AGENT.md) |
| **Quality & Verification** | `tests/**`, `pytest.ini` | `@qa_engineer` | [`agents/qa_engineer/AGENT.md`](file://./agents/qa_engineer/AGENT.md) |

---

## 2. Inter-Agent Handoff Directory

All cross-agent requests, schema handshakes, and reviews are written to the active sprint phase handoff folder (e.g., [`docs/phases/phase_01_mvp_core/handoffs/`](file://./docs/phases/phase_01_mvp_core/handoffs/)) using the standard handoff contract.
