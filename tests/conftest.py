import os
import sys

import pytest

from src.core.entity.role import Role, State, Transition

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root to Python path
sys.path.append(project_root)


@pytest.fixture
def mock_role():
    start_state = State(
        name="start",
        type="start",
        transitions=[Transition(to="next", priority=1, condition="completed")],
    )
    next_state = State(name="next", type="normal", transitions=[])

    role = Role(
        states={"start": start_state, "next": next_state},
        init_state=start_state,
        end_states=[next_state],
    )
    return role


@pytest.fixture
def mock_agent_template():
    return {"agent": {"goal": "test goal"}}