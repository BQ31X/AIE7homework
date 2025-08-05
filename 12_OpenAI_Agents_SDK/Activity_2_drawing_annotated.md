
#### Mermaid Rendering of the Agentic Reasoning Flow

![Agentic Reasoning Flow](./Untitled%20diagram%20_%20Mermaid%20Chart-2025-08-05-195554.png)




| **Color / Shape**   | **Represents**                                         | **Examples**                                   |
| ------------------- | ------------------------------------------------------ | ---------------------------------------------- |
| 🟦 **Blue Box**     | **Agents** — autonomous reasoning units                | `PlannerAgent`, `SearchAgent`, `WriterAgent`   |
| 🟪 **Purple Box**   | **Orchestration / Coordination Logic**                 | `ResearchManager.run`, `_perform_searches`     |
| ⚪ **White Box**     | *Generic functions or helper methods*                  | `_plan_searches`, `_search_method`             |
| ⬜ **Gray Box**      | **Instructional prompts** passed to LLM agents         | “Instructions: Generate 5–20 search terms”     |
| 🟧 **Orange Box**   | **Tool invocation** (e.g. external API or hosted tool) | `WebSearchTool`                                |
| 🟩 **Green Box**    | **Outputs / Display steps**                            | `WebSearchPlan Output`, `Display Final Report` |
| ◇ **Diamond Shape** | **Control flow / Decision points**                     | “More searches?”                               |
