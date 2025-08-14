| Category           | test_client.py                                       | simple_agent_client.py                                      |
|:-------------------|:-----------------------------------------------------|:------------------------------------------------------------|
| Purpose            | Manual tester to send a query to the A2A Agent Node. | LangGraph-compatible Simple Agent that makes A2A API calls. |
| Structure          | Procedural script — no graph or reusable structure.  | Structured as a LangGraph graph (e.g. `StateGraph`).        |
| Invocation         | Run from CLI: `python app/test_client.py`.           | Invoked via `graph.invoke(...)` or LangGraph orchestration. |
| Output Handling    | Prints output to terminal.                           | Returns structured output for use in downstream agents.     |
| Graph Integration  | ❌ None                                              | ✅ Yes — integrated with LangGraph.                         |
| Agent Role         | Passive: developer-triggered script.                 | Active: participates in agent workflows.                    |
| Reusability        | ❌ Low — not reusable in workflows.                  | ✅ High — composable and reusable.                          |
| Evaluation Support | ❌ No evaluation logic.                              | 🟡 Possible — can be plugged into helpfulness loops.        |