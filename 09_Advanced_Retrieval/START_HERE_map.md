### Dear grader, 

This week's assignment has more separate files than usual.

Here is an index to help you navigate.

![File index](START_HERE.png)

## 🧭 LangSmith Journey (Context for Reviewers)
Getting LangSmith to work this week was a challenge. Here’s what happened:

Initial attempts (Monday night):
LangSmith traces failed to appear. I verified my OpenAI key, project setup, and tracing config, but nothing worked. 
While experimenting, I hit an OpenAI rate limit.

Support session (Tuesday morning):
During office hours Allan, we switched to Anthropic and Cohere keys. This worked temporarily, and traces started showing up. (As demonstrated in my screenshot)

New issues emerged:
I hit Anthropic rate limits shortly after, which broke LangSmith again. Because I was trying things live, some cell states and config changes weren’t cleanly saved or documented.

Notebook state drifted:
The “live” notebook contains partially working code mixed with failed experiments. Outputs became inconsistent likely due to improper cell execution order.

Final approach:
I preserved a working state of the notebook (prior to the LangSmith issues) in Advanced_Retrieval_with_LangChain_Assignment_point_in_time.ipynb, and used this for my Loom video.


Thanks!

