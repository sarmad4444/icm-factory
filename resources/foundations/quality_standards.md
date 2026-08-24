# Interpretable Context Methodology (ICM) — Structural Rules & Conventions

## 1. The Five Principles
1. **One stage, one job**: Decompose sequential pipelines into isolated, focused steps.
2. **Plain text as universal interface**: All artifacts and contracts are written in Markdown/JSON.
3. **Layered context loading**: An agent must load only Layer 0, Layer 1, Layer 2, and explicitly declared Layer 3/4 files. Never dump entire repositories into the prompt.
4. **Every output is an edit surface**: Every intermediate artifact is saved to disk in `output/` so humans can inspect and modify it before the next stage consumes it.
5. **Configure the factory, not the product**: Reference constraints (Layer 3) are defined once at setup; runs only produce working artifacts (Layer 4).

## 2. Directory Hierarchy
- **Layer 0**: `AGENT.md` (or `CLAUDE.md` / `GEMINI.md`) in workspace root.
- **Layer 1**: `CONTEXT.md` in workspace root for routing.
- **Layer 2**: `stages/NN_<stagename>/CONTEXT.md` defining `## Inputs`, `## Process`, and `## Outputs`.
- **Layer 3**: `resources/`, `shared/`, or `stages/NN_<stagename>/references/` holding static constraints.
- **Layer 4**: `stages/NN_<stagename>/output/` holding per-run intermediate and final deliverables.

## 3. Stage Numbering
- Stages must be sequentially numbered with 2 digits: `01_`, `02_`, `03_`, etc.
- No skipped numbers.
