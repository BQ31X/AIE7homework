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
    task_id: str  # For task continuity
    context_id: str  # For task continuity


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
        TASK CONTINUITY: Uses stored task_id/context_id for follow-up messages
        """
        query = state.get("query", "").strip()
        if not query:
            raise ValueError("Query text is required")

        # Build message payload
        message_payload: dict[str, Any] = {
            "role": "user",
            "parts": [{"kind": "text", "text": query}],
            "message_id": uuid4().hex,
        }
        
        # Add task continuity if we have previous context
        existing_task_id = state.get("task_id")
        existing_context_id = state.get("context_id")
        if existing_task_id and existing_context_id:
            message_payload["task_id"] = existing_task_id
            message_payload["context_id"] = existing_context_id

        payload: dict[str, Any] = {"message": message_payload}
        request = SendMessageRequest(id=str(uuid4()), params=MessageSendParams(**payload))
        response = await client.send_message(request)
        
        response_data = response.model_dump(mode="json", exclude_none=True)
        
        # Extract task/context IDs for future continuity
        result = response_data.get("result", {})
        new_task_id = result.get("id")
        new_context_id = result.get("contextId")
        
        return {
            "response_json": response_data,
            "task_id": new_task_id,
            "context_id": new_context_id,
        }

    graph = StateGraph(ClientState)
    graph.add_node("call", call_agent_node)
    graph.set_entry_point("call")
    return graph.compile()


def _pretty_print_response(response_json: dict[str, Any]) -> None:
    """Extract and pretty print just the agent's response text."""
    try:
        result = response_json.get("result", {})
        
        # Check for completed tasks (artifacts)
        artifacts = result.get("artifacts", [])
        if artifacts and len(artifacts) > 0:
            parts = artifacts[0].get("parts", [])
            if parts and len(parts) > 0:
                text = parts[0].get("text", "")
                if text:
                    print("🤖 Agent Response:")
                    print("-" * 50)
                    print(text)
                    print("-" * 50)
                    return
        
        # Check for input-required status (clarification requests)
        status = result.get("status", {})
        if status.get("state") == "input-required":
            message = status.get("message", {})
            parts = message.get("parts", [])
            if parts and len(parts) > 0:
                text = parts[0].get("text", "")
                if text:
                    print("🤖 Agent Response (needs clarification):")
                    print("-" * 50)
                    print(text)
                    print("-" * 50)
                    return
        
        # Fallback: show the full JSON if we can't extract the text
        print("🤖 Raw Response:")
        import json
        print(json.dumps(response_json, indent=2))
        
    except Exception as e:
        print(f"❌ Error formatting response: {e}")
        print("🤖 Raw Response:")
        import json
        print(json.dumps(response_json, indent=2))


async def _amain(base_url: str, query: str | None = None) -> None:
    # Suppress verbose logging for cleaner output
    logging.basicConfig(level=logging.WARNING)
    
    # Suppress deprecation warnings for cleaner startup
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    # Show connection status
    print("🔗 Connecting to Agent Node...")
    
    # Build client and graph once
    # Note: Keep one AsyncClient context for the lifetime of the session
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as httpx_client:
        try:
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
            card: AgentCard = await resolver.get_agent_card(
                relative_card_path=AGENT_CARD_WELL_KNOWN_PATH
            )
            client = A2AClient(httpx_client=httpx_client, agent_card=card)
            app = _build_graph(client)
            
            print(f"✅ Connected to: {card.name}")
            print(f"📍 Server: {base_url}")
            
        except Exception as e:
            print(f"❌ Failed to connect to {base_url}")
            print(f"   Error: {e}")
            print("\n💡 Make sure the server is running:")
            print("   uv run python -m app --host localhost --port 10000")
            return

        # If query provided via CLI, run once and exit
        if query:
            result: ClientState = await app.ainvoke({"query": query})
            _pretty_print_response(result.get("response_json", {}))
            return

        # Interactive loop mode with task continuity
        print("\n" + "="*60)
        print("🤖 Simple Agent Client (A2A)")
        print("="*60)
        print("💡 Tips:")
        print("   • Type your questions normally")
        print("   • Follow-up clarifications continue the same task")
        print("   • New questions after completed answers start fresh")
        print("   • Type 'exit' or 'quit' to quit")
        print("="*60 + "\n")

        # Track conversation state
        current_state: ClientState = {}

        while True:
            try:
                user_input = input("🧠 You: ").strip()
                if user_input.lower() in ["exit", "quit", ""]:
                    print("👋 Goodbye!")
                    break

                # Update state with new query while preserving context
                current_state["query"] = user_input

                # INVOCATION: Uses graph.ainvoke() for LangGraph integration
                result: ClientState = await app.ainvoke(current_state)
                
                # Check if task completed - if so, reset context for next query
                response_json = result.get("response_json", {})
                task_status = response_json.get("result", {}).get("status", {}).get("state")
                
                if task_status == "completed":
                    # Task completed - reset context so next query starts fresh
                    current_state = {}
                elif task_status == "input-required":
                    # Task needs clarification - maintain context for follow-up
                    current_state.update(result)
                else:
                    # Unknown status - maintain context to be safe
                    current_state.update(result)
                
                # Pretty print the response
                _pretty_print_response(response_json)
                print()  # Extra newline for readability

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print()


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

    # If no query provided, run in interactive mode
    asyncio.run(_amain(args.base_url, args.query))


if __name__ == "__main__":
    main()


