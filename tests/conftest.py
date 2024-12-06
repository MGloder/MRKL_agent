import os
import sys

import pytest

from core.entity.role import Role
from core.entity.state import State, Transition, Action

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root to Python path
sys.path.append(project_root)


@pytest.fixture
def mock_role():
    start_state = State(
        name="start",
        state_type="start",
        description="Initial starting state",
        event_actions={"completed": [Action(name="complete_action")]},
        transitions=[Transition(to="next", priority=1, condition="completed")],
    )
    next_state = State(
        name="next",
        state_type="normal",
        description="Next state",
        event_actions={},
        transitions=[],
    )

    role = Role(
        states={"start": start_state, "next": next_state},
        init_state=start_state,
        end_states=[next_state],
    )
    return role


@pytest.fixture
def mock_agent_template():
    return {"agent": {"goal": "test goal"}}


@pytest.fixture
def mock_template():
    """Mock template fixture."""
    return """Agent Name: {agent_name}
Agent Description: {agent_description}
Task: {task}"""
