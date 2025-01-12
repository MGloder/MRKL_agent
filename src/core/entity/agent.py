"""Agent entity module."""
from dataclasses import dataclass
from typing import Optional

import yaml

from core.entity.response import AgentResponse
from core.entity.role import Role, State
from service import service_center
from utils.logging import logging
from utils.response_type import EventActions

logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """Data class representing an agent with its role, goal, and current state."""

    name: str
    description: str
    goal: str
    role: Role
    current_state: Optional[State] = None
    engagement_id: Optional[str] = None

    def __init__(
        self, goal, agent_name, description, role, current_state, engagement_id=None
    ):
        """Initialize the agent with its goal, role, and current state."""
        self.name = agent_name
        self.description = description
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
            goal=agent_data["goal"],
            agent_name=agent_data["name"],
            description=agent_data["description"],
            role=role,
            current_state=role.get_init_state(),
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

    def interact(self, user_query: str) -> AgentResponse:
        """
        Interact with the user involve 5 steps:
        1. Get the event from the raw query with intent detection
        2. Find action with event from the event-action registry
        3. Execute actions
        4. Update the current state
        5. Return the response

        :param user_query:
        :return: AgentResponse
        """
        try:
            # Step 1: Get the event from the raw query with intent detection
            args = {
                "agent_name": self.name,
                "agent_description": self.description,
                "agent_goal": self.goal,
                "current_state": self.current_state.get_formatted_current_state(),
                "raw_query": user_query,
                "event_list": self.current_state.get_formatted_event_list(),
            }

            event: EventActions = (
                service_center.intent_detection_service.detect_intent_with_args(
                    EventActions, **args
                )
            )

            # Step 2: Find action with event from the event-action registry & filter based on the role's requriements
            filtered_actions = self.filter_pre_authorized_actions(event)

            # Step 3: Execute actions
            responses = []
            for _, action in filtered_actions.items():
                response = action()
                responses.append(response)

            # Step 4: Update the current state // TODO - Update based on the action's effect
            self.current_state.mark_completed()

            # Step 4.1 Get next state based on transitions and transition to it
            self.transit_to_next_state(event)

            # Step 5: Return the response as an AgentResponse
            return AgentResponse(message="; ".join(responses), success=True)

        except Exception as e:  # pylint:disable=broad-exception-caught
            logger.error("Error during interaction: %s", str(e))
            return AgentResponse(
                message="An error occurred during interaction.",
                success=False,
                error=str(e),
            )

    def transit_to_next_state(self, event):
        """Transit to the next state based on the event."""
        transitions = self.current_state.get_transitions()
        if transitions:
            # Filter transitions based on conditions
            valid_transitions = [
                t for t in transitions if self._check_condition(t.condition, event.name)
            ]
            if valid_transitions:
                # Get highest priority transition
                next_transition = max(valid_transitions, key=lambda t: t.priority)
                self.transition_to(next_transition.to)

    def filter_pre_authorized_actions(self, event) -> dict:
        """Filter actions based on the current state's event actions."""
        actions = service_center.event_action_registry.get_actions_from_scope(
            scope=event.name
        )

        # Filter actions based on the current state's event actions
        current_state_actions = self.current_state.event_actions.get(event.name, [])

        filtered_actions = {}
        for action_config in current_state_actions.actions:
            if action_config.name in actions:
                filtered_actions[action_config.name] = actions[action_config.name]
        return filtered_actions

    def _check_condition(self, condition: str, event_name: str) -> bool:
        """Check if a given condition is met.

        Args:
            condition: The condition to check.
            event_name: The name of the event to compare with the condition.

        Returns:
            bool: True if the condition is met, False otherwise.
        """
        # Check if the condition matches the event name
        if condition == event_name:
            return True
        # Add more conditions as needed
        return False
