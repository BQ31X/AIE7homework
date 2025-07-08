# Environment and Tooling Notes (AIM Engineering Bootcamp)

## Runtime Environment

- Running Jupyter notebooks inside **Cursor** (v1.2.1)
- MacOS **Sequoia (15.5)**
- Python virtual environment:
  - Default: Python 3.12.11
  - Occasionally: Python 3.13.x for other assignments
- Using Claude 4 Sonnet via Cursor inline chat to help draft and debug code cells
- Using this ChatGPT project to explain, analyze, and break down code and concepts interactively
- Local machine (Intel iMac, 2023 model)

## Notebook Behavior

- Notebooks launched from **the current assignment folder** in Cursor (per TA recommendation)
- Notebook kernels connected to the virtual environment’s `.venv`
- Environment variables (`LANGSMITH_API_KEY`, etc.) set within the notebook with `os.environ` for repeatable runs
- Local vector stores (e.g., Qdrant `:memory:` mode) used for testing
- For cloned repos (like the LangChain Cookbook), `git clone` will place them inside the current working directory where Jupyter was launched — usually:
~/AIE7homework/04_Production_RAG/

if working on Session 4

- All code and data are running *locally* (not in Colab or a remote notebook service)


- `main` branch for stable progress
- `s0x-assignment` branches for feature/assignment work
- committed regularly to GitHub (`BQ31X/AIE7homework`)

## Additional Notes

- LangSmith project names generated with UUIDs for trace isolation
- Graph tracing (LangGraph) requires explicit callbacks to appear in LangSmith
- I generally test queries interactively and then commit results after verifying responses

**This document is intended to provide context for instructors, TAs, or future reference across all AIE7 homeworks, even ones that do not use Jupyter.**
