import re
from datetime import date

from ResearchFlow.state.research_state import Research_state


def word_count(text: str) -> str:
    return f"The question has {len(text.split())} words."


def today(text: str) -> str:
    return f"Today's date is {date.today().isoformat()}."


def extract_numbers(text: str) -> str:
    numbers = re.findall(r'-?\d+(?:\.\d+)?', text)
    return f"Numbers found: {', '.join(numbers)}." if numbers else "No numbers found."


TOOLS = {
    'word_count': (('how many words', 'word count'), word_count),
    'today': (('today', 'current date', 'what date'), today),
    'numbers': (('numbers in', 'extract numbers'), extract_numbers),
}


def call_tools(state: Research_state):
    """Run every tool whose trigger phrase appears in the question."""
    question = state['question']
    lowered = question.lower()
    notes = [
        tool(question)
        for triggers, tool in TOOLS.values()
        if any(trigger in lowered for trigger in triggers)
    ]

    return {
        'research_notes': state.get('research_notes', []) + notes
    }
