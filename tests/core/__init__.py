import pytest
import yaml
from src.core.entity.role import Role, State, Transition


@pytest.fixture
def mock_role():
    start_state = State(
        name="start", type="start", transitions=[Transition(to="next", priority=1)]
    )
    next_state = State(name="next", type="normal", transitions=[])
    role = Role(
        name="test_role",
        states=[start_state, next_state],
        init_state="start",
        end_states=["next"],
    )
    return role


@pytest.fixture
def mock_agent_template():
    return {"agent": {"goal": "test goal"}}
