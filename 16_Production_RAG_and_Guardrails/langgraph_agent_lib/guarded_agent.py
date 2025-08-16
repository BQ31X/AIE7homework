"""
Implementation of an agent with input and output guardrails.
"""

from typing import Dict, Any, List, Optional, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.language_models import BaseChatModel

from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

# Temporary: Define AgentState here instead of importing
class AgentState(TypedDict):
    """Type definition for agent state."""
    messages: List[BaseMessage]
    next: Optional[str]
    needs_refinement: Optional[bool]
    refinement_feedback: Optional[str]
    used_rag: Optional[bool]

from .rag import ProductionRAGChain
from .guardrails import check_message, GuardrailResult

def guardrail_node(state: AgentState) -> Dict[str, Any]:
    """
    Node that validates messages against guardrails.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with validation results
    """
    messages = state["messages"]
    if not messages:
        return {"messages": messages}
    
    latest_message = messages[-1]
    
    # Build context for validation
    context = {
        "requires_aid_info": any(
            keyword in latest_message.content.lower()
            for keyword in ["loan", "grant", "aid", "fafsa", "student"]
        ) if isinstance(latest_message, HumanMessage) else False
    }
    
    # Run guardrail checks
    result = check_message(latest_message, context)
    
    if not result.passed:
        # For failed pre-checks (user input), end the conversation with an error
        if isinstance(latest_message, HumanMessage):
            messages.append(AIMessage(content=result.message))
            return {"messages": messages, "next": END}
        
        # For failed post-checks (agent output), mark for refinement
        state["needs_refinement"] = result.refinement_needed
        state["refinement_feedback"] = result.message
    
    return state

def should_refine(state: AgentState) -> str:
    """Determine if the agent's response needs refinement."""
    if state.get("needs_refinement", False):
        return "refine"
    return "end"

def call_model(state: AgentState) -> Dict[str, Any]:
    """Invoke the model with the accumulated messages and append its response."""
    model = state.get("model")  # Get model from state
    if not model:
        raise ValueError("Model not found in state")
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": messages + [response]}

def should_use_tools(state: AgentState) -> str:
    """Route to 'action' if the last message includes tool calls; else continue."""
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "action"
    return "post_guard"

def create_guarded_agent(
    model: BaseChatModel,
    tools: Optional[List] = None,
    rag_chain: Optional[ProductionRAGChain] = None
) -> StateGraph:
    """
    Create a LangGraph agent with guardrail validation.
    
    Args:
        model: The language model to use
        tools: Optional list of tools available to the agent
        rag_chain: Optional RAG chain for retrieving context
        
    Returns:
        A StateGraph configured with guardrails
    """
    # Create a closure to capture the model
    def call_model_with_model(state: AgentState) -> Dict[str, Any]:
        """Call model with the captured model instance."""
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": messages + [response]}
    
    # Initialize the graph
    graph = StateGraph(AgentState)
    
    # Create nodes
    graph.add_node("pre_guard", guardrail_node)
    graph.add_node("agent", call_model_with_model)  # Use the closure that has access to model
    graph.add_node("action", ToolNode(tools or []))  # For handling tool calls
    graph.add_node("post_guard", guardrail_node)
    
    # Add edges with conditional routing
    graph.add_edge("pre_guard", "agent")
    graph.add_conditional_edges(
        "agent",
        should_use_tools,
        {
            "action": "action",
            "post_guard": "post_guard"
        }
    )
    graph.add_edge("action", "agent")
    
    # Add conditional edges for post-guard
    graph.add_conditional_edges(
        "post_guard",
        should_refine,
        {
            "refine": "agent",  # Loop back for refinement
            "end": END  # End conversation
        }
    )
    
    # Set entry point
    graph.set_entry_point("pre_guard")
    
    return graph.compile()
