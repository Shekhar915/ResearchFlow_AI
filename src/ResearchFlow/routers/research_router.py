from ResearchFlow.state.research_state import Research_state


def route_after_question(state: Research_state) -> str:
    """Send long questions to research, short ones straight to the answer."""
    return "research" if state['research_required'] else "answer"
