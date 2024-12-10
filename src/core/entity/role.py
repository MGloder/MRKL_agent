"""Role entity module."""
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml

from core.entity.state import State, Transition, Action, Event
from utils.logging import logging

logger = logging.getLogger(__name__)


@dataclass
class Role:
    """Data class representing a role with its state machine."""

    states: Dict[str, State]
    init_state: Optional[State] = None
    end_states: List[State] = None

    def __init__(
        self,
        states: Dict[str, State],
        init_state: Optional[State] = None,
        end_states: List[State] = None,
    ):
        """Initialize the role with its states, initial state, and end states."""
        self.states = states
        self.init_state = init_state
        self.end_states = end_states or []

    @classmethod
    def from_template(cls, template_path: str) -> "Role":
        """Create a Role instance from a template file.

        Args:
            template_path: Path to the role template YAML file

        Returns:
            Role: Initialized role with states from template
        """
        parser = RoleTemplateParser(template_path)
        parser.parse()

        states = parser.get_all_states()

        # Find init and end states
        init_state = None
        end_states = []

        for state in states.values():
            if state.state_type == "start":
                init_state = state
            elif state.state_type == "end":
                end_states.append(state)

        return cls(states=states, init_state=init_state, end_states=end_states)

    def get_init_state(self) -> Optional[State]:
        """Get the initial state of the role.

        Returns:
            Optional[State]: The initial state if it exists
        """
        return self.init_state

    def get_end_states(self) -> List[State]:
        """Get all end states of the role.

        Returns:
            List[State]: List of end states
        """
        return self.end_states

    def get_state(self, state_name: str) -> Optional[State]:
        """Get a state by name.

        Args:
            state_name: Name of the state to retrieve

        Returns:
            Optional[State]: The requested state if it exists
        """
        return self.states.get(state_name)

    def get_next_states(self, current_state_name: str) -> List[State]:
        """Get all possible next states from the current state.

        Args:
            current_state_name: Name of the current state

        Returns:
            List[State]: List of possible next states
        """
        current_state = self.get_state(current_state_name)
        if not current_state:
            return []

        next_states = []
        for transition in current_state.transitions:
            next_state = self.get_state(transition.to)
            if next_state:
                next_states.append(next_state)

        return next_states


class RoleTemplateParser:
    """Parser for role template files."""

    def __init__(self, template_path: str):
        """Initialize the parser with the path to the template file."""
        self.template_path = template_path
        self.states: Dict[str, State] = {}
        self.properties: Dict[str, Dict] = {}

    def parse(self) -> None:
        """Parse the YAML template file and populate the states and properties"""
        with open(self.template_path, "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)
        # Parse properties
        self.properties = template.get("properties", {})

        # Parse states
        for state_data in template["states"]:
            transitions = [
                Transition(**transition)
                for transition in state_data.get("transitions", [])
            ]

            event_actions = {}
            if "event_actions" in state_data:
                for event_name, event_data in state_data["event_actions"].items():
                    actions = [Action(**action) for action in event_data]
                    description = self.properties.get(event_name, {}).get(
                        "description", ""
                    )
                    event_actions[event_name] = Event(
                        description=description, actions=actions
                    )

            state = State(
                name=state_data["name"],
                state_type=state_data["state_type"],
                description="",
                transitions=transitions,
                event_actions=event_actions,
            )

            self.states[state.name] = state

        # Add descriptions to states
        for state_name, state in self.states.items():
            if state_name in self.properties:
                state.description = self.properties[state_name]["description"]

    def get_state(self, state_name: str) -> Optional[State]:
        """Get a state by name"""
        return self.states.get(state_name)

    def get_all_states(self) -> Dict[str, State]:
        """Get all states"""
        return self.states

    def get_properties(self) -> Dict[str, Dict]:
        """Get all properties"""
        return self.properties
