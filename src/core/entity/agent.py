"""Agent entity module."""
from dataclasses import dataclass
from typing import Optional

import yaml

from core.entity.role import Role, State
from utils.logging import logging

logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """Data class representing an agent with its role, goal, and current state."""

    goal: str
    role: Role
    current_state: Optional[State] = None
    engagement_id: Optional[str] = None

    def __init__(self, goal, role, current_state, engagement_id=None):
        """Initialize the agent with its goal, role, and current state."""
        self.goal = goal
        self.role = role
        self.current_state = current_state
        self.engagement_id = engagement_id
        self._init_agent()

    @classmethod
    def from_template(
        cls, agent_template_path: str, role_template_path: str
    ) -> "Agent":
        """Create an Agent instance from template files.

        Args:
            cls: The class itself (automatically passed)
            agent_template_path: Path to the agent template YAML file
            role_template_path: Path to the role template YAML file

        Returns:
            Agent: Initialized agent with goal, role, and initial state from templates
        """
        # Parse agent template
        with open(agent_template_path, "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)

        agent_data = template["agent"]

        role = Role.from_template(role_template_path)

        return cls(
            goal=agent_data["goal"], role=role, current_state=role.get_init_state()
        )

    def get_goal(self) -> str:
        """Get the agent's goal.

        Returns:
            str: The agent's goal
        """
        return self.goal

    def get_role(self) -> Role:
        """Get the agent's role.

        Returns:
            Role: The agent's role
        """
        return self.role

    def get_current_state(self) -> Optional[State]:
        """Get the agent's current state.

        Returns:
            Optional[State]: The current state of the agent
        """
        return self.current_state

    def set_state(self, state: State) -> None:
        """Set the agent's current state.

        Args:
            state: The new state to set
        """
        self.current_state = state

    def transition_to(self, state_name: str) -> bool:
        """Attempt to transition to a new state.

        Args:
            state_name: Name of the state to transition to

        Returns:
            bool: True if transition was successful, False otherwise
        """
        if not self.current_state:
            return False

        next_states = self.role.get_next_states(self.current_state.name)
        for next_state in next_states:
            if next_state.name == state_name:
                self.current_state = next_state
                return True
        return False

    def is_in_end_state(self) -> bool:
        """Check if the agent is in an end state.

        Returns:
            bool: True if the agent is in an end state, False otherwise
        """
        return self.current_state in self.role.get_end_states()

    def _init_agent(self):
        """Initialize the agent with the role's initial state."""
        self.current_state = self.role.get_init_state()
        if not self.current_state:
            raise ValueError("Role does not have an initial state")
        if self.current_state.state_type != "start":
            raise ValueError("Role's initial state is not a start state")
        # Get transitions from current state
        transitions = self.current_state.transitions

        # Filter transitions with no conditions and non-zero priority
        available_transitions = [
            t for t in transitions if not t.condition and t.priority > 0
        ]

        if available_transitions:
            # Sort by priority and select smallest non-zero priority
            next_transition = min(available_transitions, key=lambda x: x.priority)
            next_state = self.role.get_state(next_transition.to)
            if next_state:
                self.current_state = next_state
