"""A minimal LangGraph agent wired to the A2A protocol.

This file provides a simpler alternative to the main agent, for quick demos:
- SimpleAgent: React-style agent with the existing tool belt
- SimpleAgentExecutor: Bridges SimpleAgent to A2A protocol
- Optional CLI: start a small A2A server on a different port
"""
from __future__ import annotations

import logging
import os

from collections.abc import AsyncIterable
from typing import Any

import httpx
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
    TaskUpdater,
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    InternalError,
    InvalidParamsError,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError

from langchain_core.messages import AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.tools import get_tool_belt
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()


class SimpleAgent:
    """A minimal agent that uses `create_react_agent` with the existing tool belt.

    It streams progress updates suitable for A2A consumption.
    """

    def __init__(self):
        self.model = ChatOpenAI(
            model=os.getenv("TOOL_LLM_NAME", "gpt-4o-mini"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("TOOL_LLM_URL", "https://api.openai.com/v1"),
            temperature=0,
        )
        self.memory = MemorySaver()
        self.graph = create_react_agent(self.model, tools=get_tool_belt(), checkpointer=self.memory)

    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]:
        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": context_id}}

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if (
                isinstance(message, AIMessage)
                and getattr(message, "tool_calls", None)
                and len(message.tool_calls) > 0
            ):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Searching for information...",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Processing the results...",
                }

        # Get final assistant message and return as completed
        current_state = self.graph.get_state(config)
        final_message = current_state.values.get("messages", [])[-1]
        final_text = getattr(final_message, "content", "") if final_message else ""
        yield {
            "is_task_complete": True,
            "require_user_input": False,
            "content": final_text or "Done.",
        }


class SimpleAgentExecutor(AgentExecutor):
    """A2A executor that wraps the SimpleAgent."""

    def __init__(self) -> None:
        self.agent = SimpleAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)  # type: ignore[arg-type]
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        try:
            logger.info(f"Starting simple agent stream for query: {query}")
            async for item in self.agent.stream(query, task.context_id):
                is_task_complete = item["is_task_complete"]
                require_user_input = item["require_user_input"]

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item["content"],
                            task.context_id,
                            task.id,
                        ),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            item["content"],
                            task.context_id,
                            task.id,
                        ),
                        final=True,
                    )
                    break
                else:
                    await updater.add_artifact(
                        [Part(root=TextPart(text=item["content"]))],
                        name="result",
                    )
                    await updater.complete()
                    break
        except Exception as e:
            logger.error(f"An error occurred while streaming the response: {e}")
            raise ServerError(error=InternalError()) from e

    def _validate_request(self, context: RequestContext) -> bool:  # noqa: ARG002
        # Accept all requests for the simple agent demo
        return False

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:  # noqa: ARG002
        raise ServerError(error=UnsupportedOperationError())


def _build_simple_agent_card(host: str, port: int) -> AgentCard:
    capabilities = AgentCapabilities(streaming=True, push_notifications=True)
    skills = [
        AgentSkill(
            id="web_search",
            name="Web Search Tool",
            description="Search the web for current information",
            tags=["search", "web", "internet"],
            examples=["What are the latest news about AI?"],
        ),
        AgentSkill(
            id="arxiv_search",
            name="Academic Paper Search",
            description="Search for academic papers on arXiv",
            tags=["research", "papers", "academic"],
            examples=["Find recent papers on large language models"],
        ),
        AgentSkill(
            id="rag_search",
            name="Document Retrieval",
            description="Search through loaded documents for specific information",
            tags=["documents", "rag", "retrieval"],
            examples=["What do the policy documents say about student loans?"],
        ),
    ]
    return AgentCard(
        name="Simple Agent",
        description="A minimal AI agent with web search, arXiv and RAG tools",
        url=f"http://{host}:{port}/",
        version="0.1.0",
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=capabilities,
        skills=skills,
    )


def run_simple_server(host: str = "localhost", port: int = 11000) -> None:
    """Start a small A2A server exposing the SimpleAgentExecutor.

    Defaults to port 11000 to avoid clashing with the main server.
    """
    import uvicorn

    httpx_client = httpx.AsyncClient()
    push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(
        httpx_client=httpx_client, config_store=push_config_store
    )
    request_handler = DefaultRequestHandler(
        agent_executor=SimpleAgentExecutor(),
        task_store=InMemoryTaskStore(),
        push_config_store=push_config_store,
        push_sender=push_sender,
    )
    server = A2AStarletteApplication(
        agent_card=_build_simple_agent_card(host, port),
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    # Quick manual run: `uv run python simple.py`
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable not set. Create a .env file or export the variable in your shell.")
    run_simple_server()


