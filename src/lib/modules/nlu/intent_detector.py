"""Intent detector module for natural language understanding.

This module provides functionality to detect user intents from natural language input
by analyzing the raw query text and contextual information.
"""

from core.entity.unified_context import UnifiedContext
from service import prompt_service, llm_service
from utils.logging import logging

logger = logging.getLogger(__name__)


class IntentDetector:
    """Intent detector class to detect intents from raw queries."""

    def __init__(self):
        """Initialize the intent detector module."""

    def detect_intent_without(self, unified_context: UnifiedContext) -> str:
        """Detect intent without a raw query"""
        print(unified_context)

    def detect_intent(self, unified_context: UnifiedContext, raw_query: str) -> str:
        """Detect intent from the given message.
        Prompt template:
          Agent Name: {agent_name}
          Agent Description: {agent_description}
          Agent Goal: {agent_goal}
          Agent Current state: {current_state}
          Request from target: {raw_query}
          Event list options:
            {event_list}
          Task: return one or more events from the event list above; name only
        """
        logger.debug("Detecting intent for query: %s", raw_query)
        logger.debug("context: %s", unified_context)

        kwargs = {
            "agent_name": unified_context.agent.current_state.name,
            "agent_description": unified_context.agent.current_state.description,
            "agent_goal": unified_context.agent.goal,
            "current_state": unified_context.agent.current_state.get_formatted_current_state(),
            "raw_query": raw_query,
            "event_list": unified_context.agent.get_current_state().get_formatted_event_list(),
        }

        prompt = prompt_service.build_prompt_from_template("intent_detection", **kwargs)

        result = llm_service.completions(prompt=prompt)
        return result
