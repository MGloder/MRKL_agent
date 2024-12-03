from core.entity.unified_context import UnifiedContext
from service.context import get_context_by_session_id


class IntentDetector:
    def __init__(self):
        ...

    def _get_current_context(self, session_id: str) -> UnifiedContext:
        """Get context for intent detector to infer the relevant information."""
        return get_context_by_session_id(session_id)

    def detect_intent(self, unified_context: UnifiedContext, raw_query: str) -> str:
        """Detect intent from the given message."""
        ...
