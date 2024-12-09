"""UnifiedContext class for managing the context in natural language understanding."""
from typing import List, Dict, Optional

from core.entity.agent import Agent
from core.entity.role import State
from core.entity.target import Target


class UnifiedContext:
    """
    current_state
    reference: role, target, interaction_his
    """

    agent: Agent
    target: Target
    interaction_his: List[Dict]
    engagement_id: Optional[str]

    def __init__(
        self,
        agent: Agent,
        target: Target,
        interaction_his: List[Dict],
        engagement_id: Optional[str] = None,
    ):
        """Initialize UnifiedContext with agent, target, interaction history, and engagement ID."""
        self.agent = agent
        self.target = target
        self.interaction_his = interaction_his
        self.engagement_id = engagement_id

    @classmethod
    def from_config(
        cls,
        agent: Agent,
        target: Target,
        interaction_his: List[Dict],
        engagement_id: Optional[str] = None,
    ) -> "UnifiedContext":
        """Create a UnifiedContext instance from configuration with an engagement ID."""
        return cls(agent, target, interaction_his, engagement_id)

    def _get_current_state(self) -> State:
        """Get the current state of the role"""
        return self.agent.get_current_state()

    def _get_role(self) -> Agent:
        """Get the role"""
        return self.agent

    def _get_target(self) -> Target:
        """Get the target"""
        return self.target

    def _get_interaction_his(self) -> List[Dict]:
        """Get the interaction history"""
        return self.interaction_his

    def __str__(self):
        return f"Agent: {self.agent}, Target: {self.target}, Interaction history: {self.interaction_his}"
