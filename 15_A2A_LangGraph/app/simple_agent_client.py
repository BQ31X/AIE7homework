"""A minimal LangGraph client that uses the existing Agent Node via A2A.

PURPOSE: LangGraph-compatible Simple Agent that makes A2A API calls (vs test_client.py's manual tester)

Run against the main server (default http://localhost:10000):

  uv run python app/simple_agent_client.py --query "What can you do?"

Or specify a different base URL:

  uv run python app/simple_agent_client.py --base-url http://localhost:11000 --query "Hello"
"""
from __future__ import annotations

import argparse
import asyncio
import logging
from typing import Any, TypedDict
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import AgentCard, MessageSendParams, SendMessageRequest
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

from langgraph.graph import StateGraph


class ClientState(TypedDict, total=False):
    """State for the client LangGraph.
    
    STRUCTURE: Defines graph state schema (vs test_client.py's procedural variables)
    """
    query: str
    response_json: dict[str, Any]


async def _build_a2a_client(base_url: str) -> A2AClient:
    """Resolve the Agent Card and return an initialized A2A client."""
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as httpx_client:
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        # Fetch public agent card
        card: AgentCard = await resolver.get_agent_card(
            relative_card_path=AGENT_CARD_WELL_KNOWN_PATH
        )
        return A2AClient(httpx_client=httpx_client, agent_card=card)


def _build_graph(client: A2AClient):
    """Construct a minimal graph with a single node that calls the A2A server.
    
    GRAPH INTEGRATION: ✅ Yes — creates a StateGraph (vs test_client.py's procedural flow)
    REUSABILITY: ✅ High — returns compiled graph for use in workflows
    """

    async def call_agent_node(state: ClientState) -> dict[str, Any]:
        """Core node that makes the A2A API call.
        
        OUTPUT HANDLING: Returns structured state for downstream processing
        (vs test_client.py's terminal printing)
        """
        query = state.get("query", "").strip()
        if not query:
            raise ValueError("Query text is required")

        payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": query}],
                "message_id": uuid4().hex,
            }
        }
        request = SendMessageRequest(id=str(uuid4()), params=MessageSendParams(**payload))
        response = await client.send_message(request)
        return {"response_json": response.model_dump(mode="json", exclude_none=True)}

    graph = StateGraph(ClientState)
    graph.add_node("call", call_agent_node)
    graph.set_entry_point("call")
    return graph.compile()


async def _amain(base_url: str, query: str) -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f"Resolving Agent Card at {base_url}{AGENT_CARD_WELL_KNOWN_PATH}")
    # Build client and graph
    # Note: Keep one AsyncClient context for the lifetime of the call
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as httpx_client:
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        card: AgentCard = await resolver.get_agent_card(
            relative_card_path=AGENT_CARD_WELL_KNOWN_PATH
        )
        client = A2AClient(httpx_client=httpx_client, agent_card=card)
        app = _build_graph(client)

        # INVOCATION: Uses graph.ainvoke() for LangGraph integration
        # (vs test_client.py's direct function calls)
        result: ClientState = await app.ainvoke({"query": query})
        
        # NOTE: Only prints for CLI demo; in workflows, return result for downstream processing
        print(result.get("response_json"))


def main() -> None:
    """CLI entry point for standalone testing.
    
    AGENT ROLE: Active participant — can be embedded in larger workflows
    EVALUATION SUPPORT: 🟡 Possible — graph can be plugged into helpfulness loops
    """
    parser = argparse.ArgumentParser(description="LangGraph Simple Agent Client (A2A)")
    parser.add_argument(
        "--base-url",
        default="http://localhost:10000",
        help="Base URL of the Agent Node (default: http://localhost:10000)",
    )
    parser.add_argument(
        "--query",
        required=False,
        help="User query to send to the Agent Node. If omitted, you will be prompted.",
    )
    args = parser.parse_args()

    query = args.query or input("Enter your query: ").strip()
    asyncio.run(_amain(args.base_url, query))


if __name__ == "__main__":
    main()


