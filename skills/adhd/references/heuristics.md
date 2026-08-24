# ADHD Tree-of-Thought & Decision Pruning Heuristics

**Skill:** `adhd`  
**Location:** `skills/adhd/references/heuristics.md`

---

## 1. Tree-of-Thought (ToT) Evaluation Matrix

When exploring multiple architectural or design approaches, construct the evaluation using this deterministic structure:

| Branch / Option | Core Advantage | Hidden Complexity / Failure Mode | Pruning Decision |
|---|---|---|---|
| **Branch A** | [Fastest to implement] | [Tight coupling / tech debt] | ❌ Pruned |
| **Branch B** | [High modularity, clean testability] | [Slightly more initial boilerplate] | ✅ **Selected** |
| **Branch C** | [Full distributed microservice] | [Premature optimization, operational burden] | ❌ Pruned |

---

## 2. Anti-Cognitive Load Rules
1. **Never exceed 3 branches simultaneously.**
2. **State the deciding trade-off explicitly** (e.g., *"We choose Branch B because test isolation outweighs the extra 10 lines of boilerplate"*).
3. **Cut dead branches immediately** without revisiting discarded paths unless core constraints change.
