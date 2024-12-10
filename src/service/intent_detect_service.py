"""Intent detector module for natural language understanding.

This module provides functionality to detect user intents from natural language input
by analyzing the raw query text and contextual information.
"""
from service.llm_service import AdHocInference
from utils.logging import logging

logger = logging.getLogger(__name__)


class IntentDetectService:
    """Intent detector class to detect intents from raw queries."""

    def __init__(self, llm_service: AdHocInference, prompt_service):
        """Initialize the intent detector module."""
        self.llm_service = llm_service
        self.prompt_service = prompt_service

    def detect_intent_with_args(self, response_format: type, **kwargs) -> type:
        """Detect intent without a raw query"""
        prompt = self.prompt_service.build_prompt_from_template(
            "intent_detection", **kwargs
        )

        result = self.llm_service.completion_with_object(
            prompt=prompt, response_format=response_format
        )
        return result

    def place_holder_function(self):
        """Place holder function for future implementation."""
