"""
Guardrails for validating agent inputs and outputs using Guardrails.ai API.

This module integrates with specific guards from Guardrails Hub:
1. restricttotopic - Ensure responses stay on topic
2. detect_jailbreak - Prevent prompt injection and jailbreaking
3. competitor_check - Prevent discussion of competitors
4. llm_rag_evaluator - Evaluate RAG response quality
5. profanity_free - Filter out profanity
6. guardrails_pii - Protect PII data
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import os
from guardrails import Guard

# Import guards individually to handle missing ones gracefully
try:
    from guardrails.validators import RestrictToTopic
except ImportError:
    RestrictToTopic = None

try:
    from guardrails.validators import DetectJailbreak
except ImportError:
    DetectJailbreak = None

try:
    from guardrails.validators import CompetitorCheck
except ImportError:
    CompetitorCheck = None

try:
    from guardrails.validators import ProfanityCheck as ProfanityFree
except ImportError:
    ProfanityFree = None

try:
    from guardrails.validators import PIIDetector as GuardrailsPII
except ImportError:
    GuardrailsPII = None

@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    passed: bool
    message: str = ""
    refinement_needed: bool = False

class GuardrailsManager:
    """Manages Guardrails.ai API guards for input and output validation."""
    
    def __init__(self):
        """Initialize available guards."""
        # Ensure API key is set
        if not os.getenv("GUARDRAILS_API_KEY"):
            raise ValueError("GUARDRAILS_API_KEY environment variable must be set")
            
        # Initialize available guards
        self.guards = {}
        
        if RestrictToTopic:
            self.guards['topic'] = Guard().use(RestrictToTopic())
            
        if DetectJailbreak:
            self.guards['jailbreak'] = Guard().use(DetectJailbreak())
            
        if CompetitorCheck:
            self.guards['competitor'] = Guard().use(CompetitorCheck())
            
        if ProfanityFree:
            self.guards['profanity'] = Guard().use(ProfanityFree())
            
        if GuardrailsPII:
            self.guards['pii'] = Guard().use(GuardrailsPII())
        
    def validate_input(self, message: HumanMessage) -> GuardrailResult:
        """
        Validate user input using Guardrails.ai guards.
        
        Args:
            message: The user's input message
            
        Returns:
            GuardrailResult indicating if the input passed validation
        """
        content = message.content
        
        try:
            # Run available input guards
            if 'jailbreak' in self.guards:
                try:
                    result = self.guards['jailbreak'].guard(content)
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Input contains potential security risks."
                        )
                except Exception as e:
                    print(f"Warning: Jailbreak guard error: {str(e)}")
            
            if 'profanity' in self.guards:
                try:
                    result = self.guards['profanity'].guard(content)
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Please maintain professional language."
                        )
                except Exception as e:
                    print(f"Warning: Profanity guard error: {str(e)}")
            
            if 'pii' in self.guards:
                try:
                    result = self.guards['pii'].guard(content)
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Please do not include personal identifiable information."
                        )
                except Exception as e:
                    print(f"Warning: PII guard error: {str(e)}")
            
            # Input passed all checks
            return GuardrailResult(passed=True)
            
        except Exception as e:
            # Log the error but allow the message through
            print(f"Warning: Guard validation error: {str(e)}")
            return GuardrailResult(passed=True)
    
    def validate_output(self, message: AIMessage, context: Dict[str, Any]) -> GuardrailResult:
        """
        Validate agent output using Guardrails.ai guards.
        
        Args:
            message: The agent's output message
            context: Additional context about the conversation
            
        Returns:
            GuardrailResult indicating if the output passed validation
        """
        content = message.content
        
        try:
            # Run available output guards
            if 'topic' in self.guards:
                try:
                    result = self.guards['topic'].guard(
                        content,
                        metadata={"allowed_topics": ["student loans", "financial aid", "education"]}
                    )
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Response contains off-topic information.",
                            refinement_needed=True
                        )
                except Exception as e:
                    print(f"Warning: Topic guard error: {str(e)}")
            
            if 'competitor' in self.guards:
                try:
                    result = self.guards['competitor'].guard(content)
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Response contains competitor information.",
                            refinement_needed=True
                        )
                except Exception as e:
                    print(f"Warning: Competitor guard error: {str(e)}")
            
            if 'pii' in self.guards:
                try:
                    result = self.guards['pii'].guard(content)
                    if not result.passed:
                        return GuardrailResult(
                            passed=False,
                            message="Response contains personal identifiable information.",
                            refinement_needed=True
                        )
                except Exception as e:
                    print(f"Warning: PII guard error: {str(e)}")
            
            # Output passed all checks
            return GuardrailResult(passed=True)
            
        except Exception as e:
            # Log the error but allow the message through
            print(f"Warning: Guard validation error: {str(e)}")
            return GuardrailResult(passed=True)

_guardrails_manager = None

def get_guardrails_manager() -> GuardrailsManager:
    """Get or create the GuardrailsManager singleton."""
    global _guardrails_manager
    if _guardrails_manager is None:
        _guardrails_manager = GuardrailsManager()
    return _guardrails_manager

def check_message(
    message: BaseMessage,
    context: Optional[Dict[str, Any]] = None
) -> GuardrailResult:
    """
    Main entry point for guardrail validation using Guardrails.ai API.
    
    Args:
        message: The message to validate
        context: Optional context about the conversation
        
    Returns:
        GuardrailResult indicating if the message passed validation
    """
    manager = get_guardrails_manager()
    
    if isinstance(message, HumanMessage):
        return manager.validate_input(message)
    elif isinstance(message, AIMessage):
        return manager.validate_output(message, context or {})
    else:
        return GuardrailResult(passed=True)  # System messages pass through
