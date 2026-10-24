from langgraph.types import interrupt

from ResearchFlow.state.research_state import Research_state


def human_review(state: Research_state):
    """Pause the graph and ask a human to approve the analysis."""
    decision = interrupt({
        'question': state['question'],
        'analysis': state.get('analysis', ''),
        'prompt': 'Approve this analysis? (true/false)',
    })

    return {
        'approved': bool(decision)
    }
