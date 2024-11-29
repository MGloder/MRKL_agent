from dataclasses import dataclass
from typing import Optional

from src.core.entity.role import Role, State
from src.core.parser.agent import AgentTemplateParser


@dataclass
class Agent:
    """Data class representing an agent with its role, goal, and current state."""

    goal: str
    role: Role
    current_state: Optional[State] = None

    @classmethod
    def from_template(
        cls, agent_template_path: str, role_template_path: str
    ) -> "Agent":
        """Create an Agent instance from template files.

        Args:
            agent_template_path: Path to the agent template YAML file
            role_template_path: Path to the role template YAML file

        Returns:
            Agent: Initialized agent with goal, role, and initial state from templates
        """
        # Parse agent template
        agent_parser = AgentTemplateParser(agent_template_path)
        agent_parser.parse()
        agent_data = agent_parser.get_agent()

        # Parse role template
        role = Role.from_template(role_template_path)

        return cls(goal=agent_data.goal, role=role, current_state=role.get_init_state())

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
