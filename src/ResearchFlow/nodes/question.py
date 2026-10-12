from ResearchFlow.state.research_state import Research_state

RESEARCH_WORD_THRESHOLD = 10


def analyze_question(state: Research_state):
    question = state['question']
    research_required = len(question.split()) > RESEARCH_WORD_THRESHOLD

    return {
        'research_required': research_required
    }
