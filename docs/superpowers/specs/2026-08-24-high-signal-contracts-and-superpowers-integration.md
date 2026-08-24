# High-Signal ICM Contracts & Superpowers Integration Specification

**Purpose:** Define the architectural standard for zero-jargon, high-signal Markdown contracts across the master control plane, templates, foundations, and automate the "Spec $\rightarrow$ Plan $\rightarrow$ Execution" Superpowers lifecycle in child workspace generation and prompt compilation.

---

## 1. Problem Statement & Motivation

* **Context Bloat:** Traditional narrative Markdown causes token sprawl, slow human scannability, and high rates of LLM constraint slippage.
* **Jargon Pollution:** Using esoteric third-party meta-labels (e.g., explicit `BLUF:`, `ADHD Protocol`) creates unnecessary conceptual baggage for external users and developers.
* **Execution Disconnect:** Scaffolding tools often dump boilerplate code or templates without embedding the deterministic Superpowers workflow (Brainstorm/Spec $\rightarrow$ Bite-Sized Plan $\rightarrow$ TDD/Subagent Execution).

---

## 2. The Clean High-Signal Contract Standard

Every Markdown contract in the system (`AGENT.md`, `CONTEXT.md`, stage contracts, archetype templates, foundations) must adhere to these 4 visual and structural invariants:

| Structural Element | Format Rule | Transformer / Human Benefit |
| :--- | :--- | :--- |
| **H1 + Purpose** | Single-sentence mission statement immediately beneath H1 | Sets root attention weights (BLUF) with zero meta-labels |
| **Constraints Matrix** | Markdown table for multi-variable rules, topologies, or stage gates | 100% boundary recall; avoids parsing long narrative lists |
| **Keyed Bullet Leads** | Bold lead keywords: `* **Scope:**`, `* **Forbidden:**`, `* **Output:**` | Highlights negative constraints and deliverables |
| **Checklist / Next Action** | Max 4 prioritized items ending with a single concrete command | Eliminates ambiguity on the exact next operational step |

---

## 3. Scope of Standardization

### 3.1 Master Control Plane & Stage Rooms
* **Root Contracts:**
  * [`AGENT.md`](file://./AGENT.md): Master workspace identity, 4 topologies, 6 add-ons, and tooling constraints.
  * [`CONTEXT.md`](file://./CONTEXT.md): Master 4-category intent router and stage dispatcher.
  * [`CLAUDE.md`](file://./CLAUDE.md): Concise command runner cheatsheet (`uv run ...`, `bun ...`).
* **Stage Contracts (`stages/*/CONTEXT.md`):**
  * `stages/01_discovery/CONTEXT.md`: Problem space & stakeholder requirements gathering.
  * `stages/02_stage_mapping/CONTEXT.md`: Pipeline ordering & stage contract mapping.
  * `stages/03_scaffolding/CONTEXT.md`: Deterministic workspace and directory creation.
  * `stages/04_factory_setup/CONTEXT.md`: Tooling, scripts, and skills configuration.
  * `stages/05_validation/CONTEXT.md`: 4-tier validation suite and health gate.

### 3.2 Foundations & Quality Governance
* [`resources/foundations/methodology.md`](file://./resources/foundations/methodology.md): ICM Manifesto, 3-tier floor plan, and determinism laws.
* [`resources/foundations/context_engineering.md`](file://./resources/foundations/context_engineering.md): Anthropic context rules, token density heuristics, and Jake Van Clief masterclass principles.
* [`resources/foundations/quality_standards.md`](file://./resources/foundations/quality_standards.md): Master quality thresholds, test coverage gates, and anti-patterns.

### 3.3 Archetype Domain Templates
All 8 templates in [`resources/archetypes/`](file://./resources/archetypes/) updated to the new standard:
* `software_feature`, `agile_software_engine`, `minimal_starter`, `system_architecture_rfc`
* `systematic_bug_triage`, `content_pipeline`, `course_deck`, `research_synthesis`

---

## 4. Workspace Creator Integration (`scripts/create_workspace.py`)

When `scripts/create_workspace.py` scaffolds child workspaces:
1. **High-Signal Contract Generation:** Emits child `AGENT.md`, `CONTEXT.md`, and stage `CONTEXT.md` files conforming strictly to the new high-signal format.
2. **Superpowers Pre-Wiring:**
   * Injects `docs/superpowers/specs/` and `docs/superpowers/plans/` into generated child workspaces.
   * Updates child `AGENT.md` to declare the 3-step Superpowers execution contract.

---

## 5. Prompt Compiler Integration (`--with-compiler`)

When child workspaces are initialized with the `--with-compiler` add-on:
1. **`docs/backlog/raw_ideas.md`:** Captures raw feature/bug ideas.
2. **`docs/backlog/shaped_initiatives.md`:** Compiles ideas into canonical 5-part prompts configured to trigger:
   * **Phase 1 (Spec):** Generate formal architecture spec in `docs/superpowers/specs/`.
   * **Phase 2 (Plan):** Generate bite-sized TDD plan in `docs/superpowers/plans/`.
   * **Phase 3 (Execute):** Run execution via `superpowers:subagent-driven-development` or `superpowers:executing-plans`.

---

## 6. Verification & Quality Gates

* **Unit & Integration Tests:** Run `uv run pytest tests/` to ensure all existing workspace generators, validators, and skill management tests pass.
* **Workspace Validation:** Run `uv run python scripts/validate_workspace.py` to confirm 100% ICM 4-tier health compliance.
* **Graphify Audit (Optional):** Run `uv run python -m graphify.detect` to verify clean node extraction across all updated `.md` contracts.
