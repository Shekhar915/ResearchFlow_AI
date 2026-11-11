import os

from dotenv import load_dotenv

from ResearchFlow.state.research_state import Research_state

load_dotenv()

DEFAULT_RESEARCH_WORD_THRESHOLD = 1000


def read_threshold() -> int:
    """Read RESEARCH_WORD_THRESHOLD from the environment, falling back to the default."""
    try:
        value = int(os.getenv("RESEARCH_WORD_THRESHOLD", DEFAULT_RESEARCH_WORD_THRESHOLD))
    except ValueError:
        return DEFAULT_RESEARCH_WORD_THRESHOLD
    return value if value >= 0 else DEFAULT_RESEARCH_WORD_THRESHOLD


RESEARCH_WORD_THRESHOLD = read_threshold()


def analyze_question(state: Research_state):
    question = state['question']
    research_required = len(question.split()) > RESEARCH_WORD_THRESHOLD

    return {
        'research_required': research_required
    }
