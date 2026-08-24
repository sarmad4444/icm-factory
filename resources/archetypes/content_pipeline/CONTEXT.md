# Content Pipeline — Task Routing

**Layer:** Layer 1 (Workspace Task Routing)

## Routing Map

| Task Goal | Stage Directory | Contract | Outputs |
|---|---|---|---|
| Conduct research on a topic | `stages/01_research/` | [`CONTEXT.md`](file://./stages/01_research/CONTEXT.md) | `stages/01_research/output/research_brief.md` |
| Draft narration script | `stages/02_script/` | [`CONTEXT.md`](file://./stages/02_script/CONTEXT.md) | `stages/02_script/output/script.md` |
| Generate production visuals & code | `stages/03_production/` | [`CONTEXT.md`](file://./stages/03_production/CONTEXT.md) | `stages/03_production/output/production_spec.md` |
