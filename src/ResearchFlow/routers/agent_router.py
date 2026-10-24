from ResearchFlow.state.research_state import Research_state


def route_after_review(state: Research_state) -> str:
    """Approved analyses go to the answer; rejected ones are re-analyzed."""
    return "answer" if state.get('approved') else "analysis"
