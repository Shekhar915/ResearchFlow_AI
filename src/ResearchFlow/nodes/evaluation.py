from ResearchFlow.state.research_state import Research_state

REQUIRED_SECTIONS = (
    "Main Finding",
    "Important Observation",
    "Limitations",
    "Final Conclusion",
)


def evaluate_analysis(state: Research_state):
    """Check that the analysis contains every required section."""
    analysis = state.get('analysis', '')
    missing = [name for name in REQUIRED_SECTIONS if name not in analysis]

    return {
        'analysis_attempts': state.get('analysis_attempts', 0) + 1,
        'analysis_complete': not missing,
        'missing_sections': missing,
    }
