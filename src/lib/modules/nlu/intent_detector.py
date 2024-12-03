"""Intent detector module for natural language understanding.

This module provides functionality to detect user intents from natural language input
by analyzing the raw query text and contextual information.
"""

from core.entity.unified_context import UnifiedContext
from service.context import get_context_by_session_id
from utils.logging import logging

logger = logging.getLogger(__name__)


class IntentDetector:
    """Intent detector class to detect intents from raw queries."""

    def get_current_context(self, session_id: str) -> UnifiedContext:
        """Get context for intent detector to infer the relevant information."""
        return get_context_by_session_id(session_id)

    def detect_intent(self, unified_context: UnifiedContext, raw_query: str) -> str:
        """Detect intent from the given message."""
        logger.debug("Detecting intent for query: %s", raw_query)
        logger.debug("context: %s", unified_context)
        return "default intent"
