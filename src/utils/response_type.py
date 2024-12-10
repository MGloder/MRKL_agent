"""Response type for event-action detection."""
from pydantic import BaseModel


class EventActions(BaseModel):
    """Model for event-action detection response."""

    name: str
