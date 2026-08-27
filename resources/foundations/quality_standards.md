# Interpretable Context Methodology (ICM) — Quality Standards & Governance

**Purpose:** Master framework rules, 5 core architectural principles, directory hierarchy contracts, and quality verification standards.

---

## 1. The Five Core Principles

| Principle | Name | Architectural Rule |
| :--- | :--- | :--- |
| **Principle 1** | **One Stage, One Job** | Decompose sequential pipelines into isolated, focused single-responsibility stages |
| **Principle 2** | **Plain Text as Universal Interface** | All contracts, state, and deliverables are written in standard Markdown/JSON |
| **Principle 3** | **Layered Context Loading** | Load only Layer 0, Layer 1, Layer 2, and explicitly referenced Layer 3/4 files |
| **Principle 4** | **Every Output is an Edit Surface** | Save intermediate artifacts to disk in `output/` for human review and revision |
| **Principle 5** | **Configure Factory, Not Product** | Define constraints (Layer 3) once at setup; runs only produce working deliverables (Layer 4) |

---

## 2. The 5-Tier Directory Hierarchy

| Layer | Path Pattern | Responsibility |
| :--- | :--- | :--- |
| **Layer 0** | `AGENTS.md` (root standard) / `AGENT.md` (chambers & legacy) | Master workspace identity, operating constraints, and topologies |
| **Layer 1** | `CONTEXT.md` (root) | Master intent router and task dispatcher |
| **Layer 2** | `stages/NN_<stagename>/CONTEXT.md` | Local stage contracts defining `## Inputs`, `## Process`, and `## Outputs` |
| **Layer 3** | `resources/` or `skills/` | Static constraints, conventions, quality standards, and dynamic JIT tools |
| **Layer 4** | `stages/NN_<stagename>/output/` | Per-run intermediate and final deliverables |

---

## 3. Stage Numbering & Invariants

* **Sequential Numbering:** All stage directories must use 2-digit sequential prefixes (`01_`, `02_`, `03_`, ...).
* **No Numbering Gaps:** Stages must follow contiguous sequence without skipped indices.
* **Contract Completeness:** Every stage `CONTEXT.md` must declare `## Inputs`, `## Process`, and `## Outputs`.
* **Output Folders:** Every stage must have an `output/` directory containing working deliverables or a `.gitkeep`.

---

## 4. Universal Skill & Plugin Governance Standards (Layer 3)

| Standard Invariant | Rule Description | Verification Criteria |
| :--- | :--- | :--- |
| **Single Source of Truth** | Canonical tool instructions live in `skills/<name>/SKILL.md` | Zero prompt text duplicated across stage contracts |
| **Manifest Synchronization** | All installed skills must be cataloged in `skills/CONTEXT.md` | Automatically verified and synced via `manage_skills.py sync` |
| **YAML Frontmatter** | Every skill must have `name`, `description`, `trigger`, `url`, `version` | Checked by Tier 3 compliance linter |
| **Just-In-Time (JIT) Loading** | Skills are loaded only when their trigger phrase is active | Never loaded unconditionally into root prompts |
| **Multi-Channel Installation** | Supported via `bunx skills add`, `npx`, git clone, or local sync | Non-destructive targeting of `./skills/` directory |

---

## 5. High-Signal Documentation & Agent Voice Invariants

| Standard Invariant | Rule Description | Verification Criteria |
| :--- | :--- | :--- |
| **Top-Level Purpose** | Single-sentence mission immediately beneath H1 | Starts with `**Purpose:**` or `**Mission:**` |
| **Tabular Structure** | Multi-variable interfaces rendered as Markdown tables | Avoids narrative prose walls |
| **Bold Lead Anchors** | Instructions/constraints lead with bold keywords | `* **Scope:**`, `* **Forbidden:**` |
| **Zero-Jargon Rule** | No third-party meta-tags or conversational filler | Rejects meta-labels and conversational noise |

---

## 6. Multi-Agent Chamber & Handoff Invariants

| Chamber Invariant | Rule Description | Verification Criteria |
| :--- | :--- | :--- |
| **Chamber Identity** | Every agent in `agents/<name>/` has a dedicated contract | Requires `agents/<name>/AGENT.md` |
| **Scoped Skill Envelope** | Agents mount only authorized dynamic skills from `skills/` | Verified against `skills/` directory on disk |
| **Explicit Guardrails** | Every agent declares negative boundary constraints | Must contain `* **Forbidden:**` anchors |
| **Plain-Text Handoffs** | Inter-agent requests written to disk in Markdown | Output to `docs/phases/*/handoffs/` |

---

## 7. Universal Response Telemetry Standards (Layer 0 Invariant)

When configured in `AGENTS.md`, AI assistants must dynamically prepend an execution telemetry header to **every single response**.

| Telemetry Dimension | Measurement Description | Evaluation Criteria |
| :--- | :--- | :--- |
| **Active Persona / Chamber** | `@Chamber` persona governing the turn | Declared in `agents/` or `@Generalist` |
| **Mounted JIT Skills** | Skills loaded for this specific turn | Verified against `skills/` or `none` |
| **Grounding / Evidence** | Provenance of statements or code | `Verified (Tests Pass)`, `Grounded (Disk Read)`, `Design (Planning)` |
| **Calibrated Confidence %** | Self-assessed epistemic certainty | Explicit percentage ($<90\%$ triggers user caution) |
| **Context Window Budget** | Active context window fill | Estimated `~X.Xk / 200k (X.X%)` |
| **Turn Compute Economy** | Compute tokens utilized during this turn (reasoning scratchpad + visible output) | Estimated `[~X.Xk think | ~XXX out]` tokens |
| **ICM Stage & Task** | Active stage contract and sprint task | e.g. `workflow/stage` and `Phase-NN/TASK-NN-XXX` |
| **Utilized References** | Specific Layer 3 files consulted | Explicit filenames from `resources/` or `references/` |

### Supported Styles:
1. `pill-bar`: Minimalist Unicode pill bar (Option 5).
2. `terminal-box`: Cyberpunk ASCII wireframe box (Option 1 / Style 3).
3. `cockpit-hud`: IDE blockquote alert callout (Option 2).
4. `monospace-grid`: 3-line clean monospace backtick grid (Option 3).
5. `micro-table`: 3-column markdown table (Option 4).

---

## 8. The 2-Tier Change Management Protocol

Whenever a structural change occurs in ICM-Factory or child workspaces (e.g. adding workflows, modifying templates, editing rules), the change MUST be verified via this 2-tier protocol:

* **Tier A (Mechanical Python Gate):** Run `uv run python scripts/validate_workspace.py [target]`. Fast, deterministic checks for directory existence, contiguous stage prefixes (`01_`, `02_`), dead file links, and git cleanliness.
* **Tier B (Semantic AI Audit):** The AI agent audits contracts against this document (§5, §9, §10):
  1. Verifies 5-part prompt architecture compliance.
  2. Confirms read-friendly link anchors in context.
  3. Validates lean Layer 0 floor plan without prompt bloat.
  4. Checks for explicit negative guardrails (`* **Forbidden:**`).
* **Intelligent Auto-Correction:** The AI agent directly refactors any non-compliant link anchors or prompt structures.
* **Knowledge Graph Sync:** Execute Graphify incremental update (`graphify --update`) and verify graph health before committing.

---

## 9. The Canonical 5-Part Prompt Architecture for Contracts

All `AGENTS.md` operating guides and specialist chambers must strictly follow the Jake Van Clief 5-Part Prompt Architecture in pure Markdown (zero HTML comments, zero emojis in document text):

1. **`## 1. Identity`**: Bounded role, expertise level, authority, and tone standard.
2. **`## 2. Task`**: Core operating mandate, continuous mission, stage dispatch rules, and managed code object principle.
3. **`## 3. Context & Floor Plan`**: Markdown table of the 5-Layer Context Hierarchy mapped across the 3 Tiers (Layer 0 Operating Contract, Layer 1 Floor Plan & Map, Layer 2 Rooms, Layer 3 Tools, Layer 4 Deliverables).
4. **`## 4. Constraints`**: Tooling standards (`uv run`, `bun`), positive navigation affordances (`graphify query`), verification invariants, and clean operational guardrails.
5. **`## 5. Output Format & Protocol`**: Response telemetry protocol header and strict link anchor rules.

---

## 10. Read-Friendly Link Anchor Invariants

* **Human-Readable Anchors:** When citing skills, workflows, stages, or documents in markdown links, it is **FORBIDDEN** to display generic filenames (`[SKILL.md]`, `[CONTEXT.md]`, `[README.md]`) as the link text.
* **Format Standard:** Always display the specific, human-readable name of the module, skill, or topic:
  * Correct: `[`ui-ux-pro-max`](file://./skills/ui-ux-pro-max/SKILL.md)`
  * Correct: `[`design_studio`](file://./workflows/design_studio/CONTEXT.md)`
  * Forbidden: `[`SKILL.md`](file://./skills/ui-ux-pro-max/SKILL.md)`
* **Clickable Links:** All code symbols, files, and referenced skills must use valid clickable file links (`file://...`).

