# Project Skills Manifest & Catalog

**Location:** `./skills/`  
**Purpose:** On-demand capabilities, specialized instructions, and trigger routing.

---

## Skills Catalog

| Skill Name | Path | Trigger Phrase | Source / Repository | Pinned Version / Commit |
|---|---|---|---|---|
| `adhd` | `skills/adhd/SKILL.md` | "adhd mode, tree of thought, prune decisions, concise focus, tldr bullets" | `https://github.com/obra/adhd` | `v1.2.0` |
| `caveman` | `skills/caveman/SKILL.md` | "caveman mode, ultra terse, token efficient, terse mode" | `https://github.com/JuliusBrussee/caveman` | `v1.0.0 (789abc0)` |
| `graphify` | `skills/graphify/SKILL.md` | "graphify", "knowledge graph", "code relationships" | `https://github.com/obra/graphify` | `v2.0.1 (e4f5g6h)` |
| `superpowers` | `skills/superpowers/SKILL.md` | "superpowers, tdd, test-driven-development, systematic-debugging, writing-plans, executing-plans" | `https://github.com/obra/superpowers` | `v3.4.0` |
| `workspace-architect` | `skills/workspace-architect/SKILL.md` | "create workspace, design architecture, brainstorm project, configure workspace, enhance workspace, install skill, audit skill, should we install" | `local/master` | `v1.1.0` |

---

## Activating a Skill

Skills in this directory are loaded **Just-In-Time (JIT)**. When a prompt or stage contract mentions a trigger phrase, load and execute `skills/<name>/SKILL.md`.
