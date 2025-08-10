<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 14: Build & Serve Agentic Graphs with LangGraph</h1>

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| – | – | – | – | You are here! | – | – |

# Build 🏗️

Run the repository and complete the following:

- 🤝 Breakout Room Part #1 — Building and serving your LangGraph Agent Graph
  - Task 1: Getting Dependencies & Environment
    - Configure `.env` (OpenAI, Tavily, optional LangSmith)
  - Task 2: Serve the Graph Locally
    - `uv run langgraph dev` (API on http://localhost:2024)
  - Task 3: Call the API
    - `uv run test_served_graph.py` (sync SDK example)
  - Task 4: Explore assistants (from `langgraph.json`)
    - `agent` → `simple_agent` (tool-using agent)
    - `agent_helpful` → `agent_with_helpfulness` (separate helpfulness node)

- 🤝 Breakout Room Part #2 — Using LangGraph Studio to visualize the graph
  - Task 1: Open Studio while the server is running
    - https://smith.langchain.com/studio?baseUrl=http://localhost:2024
  - Task 2: Visualize & Stream
    - Start a run and observe node-by-node updates
  - Task 3: Compare Flows
    - Contrast `agent` vs `agent_helpful` (tool calls vs helpfulness decision)

<details>
<summary>🚧 Advanced Build 🚧 (OPTIONAL - <i>open this section for the requirements</i>)</summary>

- Create and deploy a locally hosted MCP server with FastMCP.
- Extend your tools in `tools.py` to allow your LangGraph to consume the MCP Server.
</details>

# Ship 🚢

- Running local server (`langgraph dev`)
- Short demo showing both assistants responding

# Share 🚀
- Walk through your graph in Studio
- Share 3 lessons learned and 3 lessons not learned


#### ❓ Question1 :

What is the purpose of the `chunk_overlap` parameter when using `RecursiveCharacterTextSplitter` to prepare documents for RAG, and what trade-offs arise as you increase or decrease its value?

#### ✅ Answer 1:

##### Part 1: What is the purpose of the chunk_overlap parameter in the RecursiveCharacterTextSplitter to prepare documents for RAG?

(Answer re-used from HW8)

> Overlap prevents loss of context across chunking boundaries. It ensures that context can span across chunks.

At face value, it was a simple enough answer, but I was struggling to wrap my head around why this really helped. Consider this case: a sentence that is too long for one chunk and gets split into two chunks.

It seemed to me that even with overlap, both chunks might very well still have an incomplete thought — or rather, that neither chunk would contain the full thought.

So, I kept prodding my AI tutors with follow-up questions, until I finally got an explanation (from Perplexity) that clarified my concern:

> **Why, Then, Is Overlap Still Helpful?**  
> Even if a sentence is not whole in one chunk, more of its context will often be present in at least one chunk — giving downstream retrieval or models a better chance at recognizing and using the information.  
>  
> The probability that an important detail at the edge is completely cut away (i.e., lost by both chunks) is reduced by overlap.
>
> Overlap reduces—but does not eliminate—the possibility of splitting sentences or concepts.

##### Part 2: and what trade-offs arise as you increase or decrease its value?

Higher overlap: means decreased chance of cut-off ideas, leaeding to better recall, but it will have more duplicate content, use more tokens and be potentially slower to load

Lower overlap: will be faster and cheaper (fewer tokens) but minimizes the intended benefit of overlap, and might increase risk of ideas being cutoff mid-boundaray

#### ❓ Question 2:

Your retriever is configured with `search_kwargs={"k": 5}`. How would adjusting `k` likely affect RAGAS metrics such as Context Precision and Context Recall in practice, and why?

#### ✅ Answer 2:

K represents the number of chunks to retrieve. More chunks (higher k) might improve recall (more likely to include the needed chunk), but precision might suffer, because you're also more likely to get irrelevant chunks. 
Reducing K would have the opposite effect.

#### ❓ Question 3:

Compare the `agent` and `agent_helpful` assistants defined in `langgraph.json`. Where does the helpfulness evaluator fit in the graph, and under what condition should execution route back to the agent vs. terminate?


#### ✅Answer #3:
##### Part 1: Compare the `agent` and `agent_helpful` assistants defined in `langgraph.json`.

**Simple agent workflow**

- Starts at the `agent` node.
    
- If the agent decides it needs to call a tool, it follows a conditional edge to the `action` node.
    
- Once the action completes, control returns to the `agent` node.
    
- If the agent determines it has a final answer for the user, it follows the edge to the `END` node.
    

**Agent with helpfulness workflow**

- Starts at the `agent` node.
    
- If the agent needs a tool, it moves to the `action` node, just like the simple workflow.
    
- After the action completes, control returns to the `agent` node, again just like the simple version.
    
- If the agent has an answer, instead of ending immediately, it sends the output to the `helpfulness` node.
    
- The `helpfulness` node evaluates the response and uses an additional conditional edge:
    
    - If the helpfulness criteria are not met, it loops back to the `agent` node to revise or improve the answer.
        
    - If the helpfulness criteria are met, it moves to the `END` node.

##### Part 2: Where does the helpfulness evaluator fit in the graph, 

The helpfulness evaluator runs after the agent produces a draft answer

##### Part 3: and under what condition should execution route back to the agent vs. terminate?
    

The helpfulness decision is driven by this docstring:

    >"""An agent graph with a post-response helpfulness check loop.

    > After the agent responds, a secondary node evaluates helpfulness ('Y'/'N').

    > If helpful, end; otherwise, continue the loop or terminate after a safe limit.

    > """
    
There is no explicit criteria; it is left up to the LLM to judge helpfulness.