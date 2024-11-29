from dataclasses import dataclass
from typing import Dict, List, Optional
from src.core.parser.role import RoleTemplateParser, State


@dataclass
class Role:
    """Data class representing a role with its state machine."""

    states: Dict[str, State]
    init_state: Optional[State] = None
    end_states: List[State] = None

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
            if state.type == "start":
                init_state = state
            elif state.type == "end":
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
