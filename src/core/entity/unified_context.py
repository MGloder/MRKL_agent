import dataclasses
from typing import List

from core.entity.role import Role, State
from core.entity.target import Target
from core.parser.target import TargetTemplateParser


class UnifiedContext:
    """
    current_state
    reference: role, target, interaction_his
    """

    current_state: State
    role: Role
    target: Target
    interaction_his: List[str]

    def _get_current_state(self) -> State:
        """Get the current state of the role"""
        return self.current_state

    def _get_role(self) -> Role:
        """Get the role"""
        return self.role

    def _get_target(self) -> Target:
        """Get the target"""
        return self.target

    def _get_interaction_his(self) -> List[str]:
        """Get the interaction history"""
        return self.interaction_his
