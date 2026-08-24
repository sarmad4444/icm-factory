# Caveman Mode Syntax & Compression Rules

**Skill:** `caveman`  
**Location:** `skills/caveman/references/syntax_rules.md`

---

## 1. Compression Grammars

| Standard Construct | Caveman Compression |
|---|---|
| "The issue is caused by the database pool being exhausted." | "Issue: DB pool exhausted." |
| "I have updated the test file to assert that the return code is 200." | "Updated `test_api.py`. Assert `code == 200`." |
| "In order to resolve this problem, we need to run the following command:" | "Run: `uv run pytest`" |

---

## 2. Unbreakable Safety Rules
- **Preserve identifiers:** Never compress variable names, method signatures, or file paths.
- **Preserve commands:** Shell commands must be exact, copy-pasteable strings.
- **Preserve error traces:** Do not truncate stack traces or line numbers.
