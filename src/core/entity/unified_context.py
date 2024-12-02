import dataclasses
from typing import List

from core.entity.role import Role, State
from core.entity.target import Target


class UnifiedContext:
    """
    current_state
    reference: role, target, interaction_his
    """

    current_state: State
    role: Role
    target: Target
    interaction_his: List[str]

    def get_current_state(self) -> State:
        """Get the current state of the role"""
        return self.current_state
