"""Service for managing user engagement sessions with agents and targets."""
import uuid
from typing import Dict, List, Optional

from core.entity.agent import Agent
from core.entity.target import Target
from core.entity.unified_context import UnifiedContext


class UserEngagementService:
    """Service for managing user engagement sessions."""

    def __init__(self):
        """Initialize the engagement service with empty storage."""
        self._engagements: Dict[str, UnifiedContext] = {}

    def create_engagement(
        self,
        agent_template_path: str,
        role_template_path: str,
        target_template_path: str,
    ) -> str:
        """Create a new engagement session.

        Args:
            agent_template_path: Path to agent template file
            role_template_path: Path to role template file
            target_template_path: Path to target template file

        Returns:
            str: Unique engagement ID
        """
        # Generate unique ID
        engagement_id = str(uuid.uuid4())

        # Create agent and target with engagement ID
        agent = Agent.from_template(
            agent_template_path=agent_template_path,
            role_template_path=role_template_path,
        )
        agent.engagement_id = engagement_id

        target = Target.from_template(
            target_template_path=target_template_path, engagement_id=engagement_id
        )

        # Initialize empty interaction history
        interaction_history: List[Dict] = []

        # Create unified context
        context = UnifiedContext.from_config(
            agent=agent,
            target=target,
            interaction_his=interaction_history,
            engagement_id=engagement_id,
        )

        # Store context
        self._engagements[engagement_id] = context

        return engagement_id

    def get_context(self, engagement_id: str) -> Optional[UnifiedContext]:
        """Get the unified context for an engagement.

        Args:
            engagement_id: Unique engagement ID

        Returns:
            Optional[UnifiedContext]: The unified context if found, None otherwise
        """
        return self._engagements.get(engagement_id)

    def update_interaction_history(self, engagement_id: str, interaction: Dict) -> None:
        """Update the interaction history for an engagement.

        Args:
            engagement_id: Unique engagement ID
            interaction: New interaction to add to history
        """
        if context := self._engagements.get(engagement_id):
            context.interaction_his.append(interaction)

    def delete_engagement(self, engagement_id: str) -> None:
        """Delete an engagement session.

        Args:
            engagement_id: Unique engagement ID
        """
        if engagement_id in self._engagements:
            del self._engagements[engagement_id]

    def get_agent_with_engagement_id(self, engagement_id) -> Optional[Agent]:
        """Get the agent associated with an engagement ID.

        Args:
            engagement_id: Unique engagement ID

        Returns:
            Agent: The agent associated with the engagement ID
        """
        if context := self._engagements.get(engagement_id):
            return context.agent
        return None
