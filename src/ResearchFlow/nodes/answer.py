from ResearchFlow.state.research_state import Research_state


def build_answer(state: Research_state):
    analysis = state.get('analysis')

    if analysis:
        final_answer = analysis
    else:
        final_answer = f"No research was required for: {state['question']}"

    return {
        'final_answer': final_answer
    }
