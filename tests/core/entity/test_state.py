from core.entity.state import State, Action, Transition, StateStatus, Event


def test_state_initialization():
    """Test basic state initialization"""
    state = State(
        name="test_state",
        state_type="normal",
        description="Test state",
        event_actions={"event1": [Action(name="action1")]},
        transitions=[Transition(to="next_state")],
    )

    assert state.name == "test_state"
    assert state.state_type == "normal"
    assert state.description == "Test state"
    assert len(state.event_actions) == 1
    assert len(state.transitions) == 1
    assert state.status == StateStatus.NOT_STARTED


def test_get_actions_for_event():
    """Test getting actions for events"""
    actions = [
        Action(name="action1", description="First action"),
        Action(name="action2", description="Second action"),
    ]

    state = State(
        name="test_state",
        state_type="normal",
        description="Test state",
        event_actions={"test_event": Event(description="test_event", actions=actions)},
        transitions=[],
    )

    # Test existing event
    retrieved_actions = state.get_actions_for_event("test_event")
    assert len(retrieved_actions) == 2
    assert retrieved_actions[0].name == "action1"
    assert retrieved_actions[1].name == "action2"

    # Test non-existent event
    assert len(state.get_actions_for_event("invalid_event")) == 0


def test_state_status_updates():
    """Test state status transitions"""
    state = State(
        name="test_state",
        state_type="normal",
        description="Test state",
        event_actions={},
        transitions=[],
    )

    assert state.status == StateStatus.NOT_STARTED

    state.update_status(StateStatus.IN_PROGRESS)
    assert state.status == StateStatus.IN_PROGRESS

    state.update_status(StateStatus.COMPLETED)
    assert state.status == StateStatus.COMPLETED


def test_transition_initialization():
    """Test transition initialization"""
    transition = Transition(to="next_state", condition="test_condition", priority=1)

    assert transition.to == "next_state"
    assert transition.condition == "test_condition"
    assert transition.priority == 1

    # Test default values
    simple_transition = Transition(to="next_state")
    assert simple_transition.condition is None
    assert simple_transition.priority == 0


def test_action_initialization():
    """Test action initialization"""
    action = Action(name="test_action", description="Test description")

    assert action.name == "test_action"
    assert action.description == "Test description"

    # Test default values
    simple_action = Action(name="simple_action")
    assert simple_action.name == "simple_action"
    assert simple_action.description is None
