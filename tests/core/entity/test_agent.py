from unittest.mock import mock_open, patch

import pytest
import yaml

from core.entity.state import State, StateStatus
from src.core.entity.agent import Agent
from src.core.entity.role import Role


def test_agent_initialization(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )
    assert agent.get_goal() == "test goal"
    assert agent.get_role() == mock_role
    assert agent.get_current_state() == mock_role.get_state("start")


def test_agent_from_template():
    mock_agent_yaml = yaml.dump({"agent": {"goal": "test goal"}})

    mock_role_yaml = yaml.dump(
        {
            "states": [
                {
                    "name": "start",
                    "state_type": "start",
                    "description": "start",
                    "transitions": [{"to": "next", "priority": 1}],
                    "event_actions": {"completed": [{"name": "complete_action"}]},
                    "status": "NOT_STARTED",
                }
            ]
        }
    )

    # Use nested context managers to mock both file opens
    with patch("builtins.open") as mock_open_func:
        # Configure mock to return different content for different files
        mock_open_func.side_effect = [
            mock_open(read_data=mock_agent_yaml).return_value,
            mock_open(read_data=mock_role_yaml).return_value,
        ]

        with patch(
            "src.core.entity.role.Role.from_template"
        ) as mock_role_from_template:
            mock_role = Role(
                states={
                    "start": State(
                        name="start",
                        state_type="start",
                        description="example",
                        transitions=[],
                        event_actions={},
                        status=StateStatus.NOT_STARTED,
                    )
                },
                init_state=State(
                    name="start",
                    state_type="start",
                    description="example",
                    transitions=[],
                    event_actions={},
                    status=StateStatus.NOT_STARTED,
                ),
                end_states=[],
            )
            mock_role_from_template.return_value = mock_role

            agent = Agent.from_template("fake_agent.yaml", "fake_role.yaml")

            assert agent.get_goal() == "test goal"


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
    assert not agent.is_in_end_state()


def test_set_state(mock_role):
    agent = Agent(
        goal="test goal", role=mock_role, current_state=mock_role.get_init_state()
    )
    new_state = State(
        name="new",
        state_type="normal",
        description="",
        transitions=[],
        event_actions={},
        status=StateStatus.NOT_STARTED,
    )

    agent.set_state(new_state)
    assert agent.get_current_state() == new_state


def test_init_agent_invalid_state():
    invalid_role = Role(
        states={
            "invalid": State(
                name="invalid",
                state_type="normal",
                description="",
                transitions=[],
                event_actions={},
                status=StateStatus.IN_PROGRESS,
            )  # Not a start state
        },
        init_state=State(
            name="invalid",
            state_type="normal",
            description="",
            transitions=[],
            event_actions={},
            status=StateStatus.NOT_STARTED,
        ),
        end_states=[],
    )

    with pytest.raises(ValueError, match="Role's initial state is not a start state"):
        Agent(
            goal="test goal",
            role=invalid_role,
            current_state=invalid_role.get_init_state(),
        )
