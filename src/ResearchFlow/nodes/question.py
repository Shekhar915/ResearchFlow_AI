from ResearchFlow.state.research_state import Research_state

def analyze_question(state:Research_state):
    question = state['question']
    research_required = len(question.split())>10

    return {
        'research_required' : research_required
    }