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
| **Turn Token Economy** | Tokens generated during this turn | Estimated `~XXX` output tokens |
| **ICM Stage & Task** | Active stage contract and sprint task | e.g. `workflow/stage` and `Phase-NN/TASK-NN-XXX` |
| **Utilized References** | Specific Layer 3 files consulted | Explicit filenames from `resources/` or `references/` |

### Supported Styles:
1. `pill-bar`: Minimalist Unicode pill bar (Option 5).
2. `terminal-box`: Cyberpunk ASCII wireframe box (Option 1 / Style 3).
3. `cockpit-hud`: IDE blockquote alert callout (Option 2).
4. `monospace-grid`: 3-line clean monospace backtick grid (Option 3).
5. `micro-table`: 3-column markdown table (Option 4).

