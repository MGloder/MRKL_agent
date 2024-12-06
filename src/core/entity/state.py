"""State entity module."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class StateStatus(Enum):
    """Enum representing the possible statuses of a state."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Action:
    """Data class representing an action that can be taken in response to an event."""

    name: str
    description: Optional[str] = None


@dataclass
class Transition:
    """Data class representing a transition from one state to another."""

    to: str
    condition: Optional[str] = None
    priority: int = 0


@dataclass
class State:
    """Data class representing a state with its description, events/actions, and status."""

    name: str
    state_type: str
    description: str
    event_actions: Dict[str, List[Action]]
    transitions: List[Transition]
    status: StateStatus = StateStatus.NOT_STARTED

    def __init__(
        self,
        name: str,
        state_type: str,
        description: str,
        event_actions: Dict[str, List[Action]],
        transitions: List[Transition],
        status: StateStatus = StateStatus.NOT_STARTED,
    ):
        """Initialize a state with description, event-action mappings and status.

        Args:
            description: Description of what this state represents
            event_actions: Dictionary mapping events to lists of possible actions
            status: Current status of the state (defaults to NOT_STARTED)
        """
        self.name = name
        self.state_type = state_type
        self.description = description
        self.event_actions = event_actions
        self.transitions = transitions
        self.status = status

    def get_actions_for_event(self, event: str) -> List[Action]:
        """Get all possible actions for a given event.

        Args:
            event: The event to get actions for

        Returns:
            List of actions associated with the event, or empty list if event not found
        """
        return self.event_actions.get(event, [])

    def update_status(self, new_status: StateStatus) -> None:
        """Update the status of this state.

        Args:
            new_status: The new status to set
        """
        self.status = new_status

    def get_formatted_event_list(self) -> str:
        """Get a formatted list of event:actions from event_actions.

        Returns:
            A formatted string of actions associated with the event
        """
        result = ""
        for index, (event, actions) in enumerate(self.event_actions.items()):
            result = (
                result
                + f"{index + 1}. Event: {event}: Actions: {', '.join(action.name for action in actions)}"
            )
            if index != len(self.event_actions.items()) - 1:
                result = result + "\n"
        return result

    def get_formatted_current_state(self):
        """Get the formatted current state"""
        return f"State Name: {self.name}, Description: {self.description}"
