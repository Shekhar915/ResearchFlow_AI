from ResearchFlow.state.research_state import Research_state


def route_after_question(state: Research_state) -> str:
    """Send long questions to research, short ones straight to the answer."""
    return "research" if state['research_required'] else "answer"


MAX_ANALYSIS_ATTEMPTS = 1


def route_after_evaluation(state: Research_state) -> str:
    """Retry the analysis when sections are missing, up to a fixed limit."""
    if state['analysis_complete']:
        return "answer"
    if state['analysis_attempts'] >= MAX_ANALYSIS_ATTEMPTS:
        return "answer"
    return "analysis"
