"""Intent detector module for natural language understanding.

This module provides functionality to detect user intents from natural language input
by analyzing the raw query text and contextual information.
"""

from utils.logging import logging

logger = logging.getLogger(__name__)


class IntentDetectService:
    """Intent detector class to detect intents from raw queries."""

    def __init__(self, llm_service, prompt_service):
        """Initialize the intent detector module."""
        self.llm_service = llm_service
        self.prompt_service = prompt_service

    def detect_intent_with_args(self, **kwargs) -> str:
        """Detect intent without a raw query"""
        prompt = self.prompt_service.build_prompt_from_template(
            "intent_detection", **kwargs
        )

        result = self.llm_service.completions(prompt=prompt)
        return result

    def detect_intent(self, raw_query: str) -> str:
        """Detect intent from the given raw query."""
        args = {"raw_query": raw_query}
        return self.detect_intent_with_args(**args)
