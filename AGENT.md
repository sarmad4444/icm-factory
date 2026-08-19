# Interpretable Context Methodology (ICM) — Master Workspace Builder

**Mission:** Design, initialize, configure, and maintain child ICM workspaces in `./workspaces/[workspace-name]` adhering strictly to the ICM philosophy defined in [`SOUL.md`](file:///d:/AI%20Projects/icm-generated/SOUL.md).  
**Framework:** Interpretable Context Methodology (ICM)  
**Layer:** Layer 0 (Master Workspace Identity & Operating Contract)

---

## 1. Operating Rules

1. **Root Role**: This root workspace (`./icm-generated`) is itself an ICM workspace whose domain is **Workspace Generation & Configuration** (The Factory of Workspaces).
2. **Child Isolation**: All child workspaces created by this master builder reside in `./workspaces/[workspace-name]`. Each child workspace is completely autonomous, containing its own Layer 0 `AGENT.md`, Layer 1 `CONTEXT.md`, Layer 2 stage contracts, Layer 3 `_config/` references, and Layer 4 `output/` directories.
3. **5-Layer Context Hierarchy**:
   - **Layer 0**: `AGENT.md` / `GEMINI.md`
   - **Layer 1**: `CONTEXT.md`
   - **Layer 2**: `stages/NN_<stagename>/CONTEXT.md`
   - **Layer 3**: `_config/`, `shared/`, `stages/NN_<stagename>/references/`
   - **Layer 4**: `stages/NN_<stagename>/output/`
4. **Tooling & Environment Constraints**:
   - All Python scripts MUST run in the project's dedicated `uv` environment (`uv run python ...`).
   - Platform is Windows PowerShell.
   - If JavaScript tooling is needed, use `bun` and `bunx` (never npm/npx/yarn/pnpm).

---

## 2. Directory Layout of Master Builder

- `SOUL.md`: ICM Manifesto and theoretical paper.
- `AGENT.md` / `GEMINI.md` (Layer 0): Master identity and rules.
- `CONTEXT.md` (Layer 1): Master task router for building workspaces.
- `_config/` (Layer 3): Master ICM rules and pre-built archetypes (`content_pipeline`, `research_synthesis`, `course_deck`, `software_feature`, `minimal_starter`).
- `shared/templates/` (Layer 3): Reusable contract templates and questionnaires.
- `scripts/` (Local Mechanical Tools):
  - `validate_workspace.py`: Audits any workspace for strict ICM compliance.
  - `create_workspace.py`: Scaffolds child workspaces via archetypes or interactive wizard.
  - `list_workspaces.py`: Inspects and tables all child workspaces in `./workspaces/`.
- `stages/` (Layer 2 & 4):
  - `01_discovery`: Domain & workflow requirement analysis.
  - `02_stage_mapping`: Breakpoint and handoff contract blueprinting.
  - `03_scaffolding`: Folder structure and contract generation.
  - `04_factory_setup`: Layer 3 reference configuration & questionnaire onboarding.
  - `05_validation`: ICM contract verification and readiness audit.
- `workspaces/`: Destination for all generated child workspaces.

---

## 3. Workspace Initialization Flow (The 3 Options)

When asked to create a new workspace, always prompt the user to choose their preferred approach:
1. **Interactive Custom Pipeline (5-Stage ICM)**: Full discovery, mapping, scaffolding, factory setup, and validation through stages `01` to `05`.
2. **Archetype Fast-Track**: Rapidly scaffold a pre-tested archetype from `_config/archetypes/`.
3. **Quick CLI Questionnaire**: Run `uv run python scripts/create_workspace.py --interactive`.
