"""memory cache service module."""
from core.entity.response import TaskStatus
from core.entity.state import State


class MemoryCacheService:
    """In-memory cache service to keep track of status in Role."""

    def __init__(self):
        self.cache = {}

    def set_status(self, event_name: str, action_name: str, status: TaskStatus):
        """Set the status of an action in the cache."""
        if event_name not in self.cache:
            self.cache[event_name] = {}
        self.cache[event_name][action_name] = status

    def get_status(self, event_name: str, action_name: str) -> str:
        """Get the status of an action from the cache."""
        if event_name in self.cache and action_name in self.cache[event_name]:
            return self.cache[event_name][action_name]
        return "Unknown"

    def set_status_with_state(
        self, state_name: State, target_action: str, status: TaskStatus
    ):
        """Set the status of a state in the cache."""
        events = state_name.event_actions
        for event in events:
            for action in events[event].actions:
                if target_action == action.name:
                    self.set_status(event, action.name, status)
