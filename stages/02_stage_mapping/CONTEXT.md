# Stage 02: Stage Mapping & Blueprinting — Contract

**Layer:** Layer 2 (Stage Execution Contract)  
**Stage Name:** `02_stage_mapping`

---

## Inputs

- **Layer 3 (Reference):** `references/patterns.md`
- **Layer 3 (Reference):** `../../_config/icm_rules.md`
- **Layer 4 (Working):** `../01_discovery/output/domain_brief.md`

---

## Process

1. Read the domain brief from Stage 01.
2. Decompose the workflow into discrete sequential stages following the "one stage, one job" rule.
3. For every stage, define:
   - Stage folder name (`NN_stagename`)
   - Stage title and role
   - Explicit Layer 3 (reference) and Layer 4 (working upstream) inputs
   - Execution transformation process
   - Explicit Layer 4 output file names and review criteria
4. Produce the Stage Blueprint and Handoff Matrix.

---

## Outputs

- `stage_blueprint.md` -> `output/stage_blueprint.md`
