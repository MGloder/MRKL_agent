import dataclasses

from core.entity.role import Role
from core.entity.target import Target


@dataclasses
class UnifiedContext:
    role: Role
    target: Target
