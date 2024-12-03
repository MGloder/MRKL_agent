from core.entity.role import Role, State, Transition


def test_role_initialization(mock_role):
    """Test basic role initialization"""
    assert isinstance(mock_role, Role)
    assert len(mock_role.states) == 2
    assert mock_role.init_state.name == "start"
    assert len(mock_role.end_states) == 1


def test_get_init_state(mock_role):
    """Test getting initial state"""
    init_state = mock_role.get_init_state()
    assert init_state.name == "start"
    assert init_state.type == "start"


def test_get_end_states(mock_role):
    """Test getting end states"""
    end_states = mock_role.get_end_states()
    assert len(end_states) == 1
    assert end_states[0].name == "next"


def test_get_state(mock_role):
    """Test getting state by name"""
    state = mock_role.get_state("start")
    assert state.name == "start"
    assert state.type == "start"

    # Test non-existent state
    assert mock_role.get_state("invalid") is None


def test_get_next_states(mock_role):
    """Test getting next possible states"""
    next_states = mock_role.get_next_states("start")
    assert len(next_states) == 1
    assert next_states[0].name == "next"

    # Test state with no transitions
    assert len(mock_role.get_next_states("next")) == 0

    # Test non-existent state
    assert len(mock_role.get_next_states("invalid")) == 0


def test_custom_role():
    """Test creating a custom role"""
    # Create states
    state1 = State(
        name="state1",
        type="normal",
        transitions=[Transition(to="state2", priority=1, condition="test")],
    )
    state2 = State(name="state2", type="end", transitions=[])

    # Create role
    role = Role(
        states={"state1": state1, "state2": state2},
        init_state=state1,
        end_states=[state2],
    )

    assert len(role.states) == 2
    assert role.init_state == state1
    assert role.end_states == [state2]
    assert role.get_state("state1") == state1
    assert role.get_state("state2") == state2
