from unittest.mock import mock_open, patch

import pytest
import yaml

from src.core.entity.agent import Agent
from src.core.entity.role import Role, State


def test_agent_initialization(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )
    assert agent.get_goal() == "test goal"
    assert agent.get_role() == mock_role
    assert agent.get_current_state() == mock_role.get_state(
        "next"
    )  # Due to _init_agent transition


def test_agent_from_template():
    mock_yaml = yaml.dump({"agent": {"goal": "test goal"}})

    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        with patch(
            "src.core.entity.role.Role.from_template"
        ) as mock_role_from_template:
            mock_role = Role(
                name="test_role",
                states=[State(name="start", type="start", transitions=[])],
                init_state="start",
                end_states=[],
            )
            mock_role_from_template.return_value = mock_role

            agent = Agent.from_template("fake_agent.yaml", "fake_role.yaml")

            assert agent.get_goal() == "test goal"
            assert agent.get_role() == mock_role


def test_transition_to(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )

    # Test successful transition
    success = agent.transition_to("next")
    assert success
    assert agent.get_current_state().name == "next"

    # Test failed transition to non-existent state
    success = agent.transition_to("nonexistent")
    assert not success
    assert agent.get_current_state().name == "next"


def test_is_in_end_state(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )

    # Should transition to "next" state during initialization
    assert agent.is_in_end_state()  # "next" is an end state


def test_set_state(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )
    new_state = State(name="new", type="normal", transitions=[])

    agent.set_state(new_state)
    assert agent.get_current_state() == new_state


def test_init_agent_invalid_state():
    invalid_role = Role(
        name="invalid_role",
        states=[
            State(name="invalid", type="normal", transitions=[])  # Not a start state
        ],
        init_state="invalid",
        end_states=[],
    )

    with pytest.raises(ValueError, match="Role's initial state is not a start state"):
        Agent(
            goal="test goal",
            role=invalid_role,
            current_state=invalid_role.get_init_state(),
        )
