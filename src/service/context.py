context = {
    "session_a": {"state": "state_a", "user": {"name": "user_a"}},
}


def get_context_by_session_id(session_id: str):
    return context.get(session_id)


context_service = {"get_context": get_context_by_session_id}


def get_active_user_context():
    pass
