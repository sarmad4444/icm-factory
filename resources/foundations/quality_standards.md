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
| **Layer 0** | `AGENT.md` (or `CLAUDE.md` / `GEMINI.md`) | Master workspace identity, operating constraints, and topologies |
| **Layer 1** | `CONTEXT.md` (root) | Master intent router and task dispatcher |
| **Layer 2** | `stages/NN_<stagename>/CONTEXT.md` | Local stage contracts defining `## Inputs`, `## Process`, and `## Outputs` |
| **Layer 3** | `resources/` or `stages/NN_*/references/` | Static constraints, conventions, and quality standards |
| **Layer 4** | `stages/NN_<stagename>/output/` | Per-run intermediate and final deliverables |

---

## 3. Stage Numbering & Invariants

* **Sequential Numbering:** All stage directories must use 2-digit sequential prefixes (`01_`, `02_`, `03_`, ...).
* **No Numbering Gaps:** Stages must follow contiguous sequence without skipped indices.
* **Contract Completeness:** Every stage `CONTEXT.md` must declare `## Inputs`, `## Process`, and `## Outputs`.
* **Output Folders:** Every stage must have an `output/` directory containing working deliverables or a `.gitkeep`.

---

## 4. High-Signal Documentation & Agent Voice Invariants

| Standard Invariant | Rule Description | Verification Criteria |
| :--- | :--- | :--- |
| **Top-Level Purpose** | Single-sentence mission immediately beneath H1 | Starts with `**Purpose:**` or `**Mission:**` |
| **Tabular Structure** | Multi-variable interfaces rendered as Markdown tables | Avoids narrative prose walls |
| **Bold Lead Anchors** | Instructions/constraints lead with bold keywords | `* **Scope:**`, `* **Forbidden:**` |
| **Zero-Jargon Rule** | No third-party meta-tags or conversational filler | Rejects meta-labels and conversational noise |
