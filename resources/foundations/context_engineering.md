# ICM Framework & Context Engineering References

**Domain:** Master Architectural Foundations, Context Engineering Principles & Video Masterclasses  
**Layer:** Layer 3 (Global Framework References)

---

## 1. Foundational Theory & Manifesto

* **[`methodology.md`](file://./methodology.md)**: The original Interpretable Context Methodology (ICM) whitepaper and manifesto. Defines the 5-Layer Context Hierarchy, the "Factory vs. Product" separation, the edit-surface principle, and the philosophy of using the filesystem as the AI agent architecture.

---

## 2. Modern Context Engineering Principles (Anthropic)

* **Article Reference:** *"The new rules of context engineering for Claude 5 generation models"* by Thariq Shihipar (Anthropic)  
* **URL:** `https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models`  
* **Core Principles Applied to ICM:**
  1. **Rules $\rightarrow$ Judgment**: Remove rigid constraint walls; provide clear principles and allow modern frontier models to exercise architectural judgment.
  2. **Examples $\rightarrow$ Expressive Interfaces**: Replace bulky few-shot examples with expressive schema definitions, status enums, and clear stage contracts (`Inputs`, `Process`, `Outputs`).
  3. **Upfront Dump $\rightarrow$ Progressive Disclosure**: Never dump entire handbooks into root `AGENT.md`. Keep root prompts ultra-light and load context on-demand through hierarchical file trees and just-in-time skills.
  4. **Simple Tool Descriptions**: Avoid repeating instructions across system prompts; keep tool documentation directly inside tool definitions.
  5. **Rich References & Rubrics**: Reference high-fidelity specifications, Architecture Decision Records (ADRs), and evaluation rubrics dynamically during verification passes.

---

## 3. Jake Van Clief Masterclass Video Series

### Video 1: Foundational ICM Masterclass
* **Title:** *The AI Folder & Agentic Workflow System (Interpretable Context Methodology)*
* **URL:** [`https://www.youtube.com/watch?v=KPVaUuBkPz8`](https://www.youtube.com/watch?v=KPVaUuBkPz8)
* **Key Takeaway:** Organizing AI pair-programming through numbered directories and markdown contracts eliminates brittle orchestration frameworks. Demonstrates how any agent can pick up or hand off project context seamlessly.

### Video 2: The 3-Tier "Folder as App" Hierarchy
* **Title:** *Stop Building AI Agents. Use This Folder System Instead.*
* **URL:** [`https://www.youtube.com/watch?v=MkN-ss2Nl10`](https://www.youtube.com/watch?v=MkN-ss2Nl10)
* **Key Takeaway:** The "House" analogy for context engineering:
  - **Layer 1 (The Floor Plan):** Top-level identity and navigation (`AGENT.md`, root `CONTEXT.md`).
  - **Layer 2 (The Rooms):** Specific stage and sprint directories with local contracts.
  - **Layer 3 (The Tools & Furniture):** Plug-and-play skills, ADRs, and references.

### Video 3: Automating the Coordination Layer
* **Title:** *You're Automating The Wrong Layer (How 30,000 People Build AI Without Frameworks)*
* **URL:** [`https://www.youtube.com/watch?v=956DPSPX4wg`](https://www.youtube.com/watch?v=956DPSPX4wg)
* **Key Takeaway:** Dialogue + Skills + Filesystem coordination. Demonstrates the canonical 5-Part Prompt Architecture (Identity, Task, Context, Constraints, Output Format) for compiling fuzzy thoughts into deterministic execution contracts.
