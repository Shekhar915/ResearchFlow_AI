from langchain_core.messages import HumanMessage

from ResearchFlow.llm.model import LLM
from ResearchFlow.state.research_state import Research_state


def gather_research(state: Research_state):
    prompt = f"""
You are a research assistant. Collect concise, factual research notes for the question inside the <question> tags.

<question>
{state['question']}
</question>

Return 3 to 5 notes, one per line, each starting with "- ". No introduction or conclusion.
"""
    response = LLM.invoke([HumanMessage(content=prompt)])
    notes = [
        line.lstrip('- ').strip()
        for line in response.content.splitlines()
        if line.strip()
    ]

    return {
        'research_notes': notes
    }
