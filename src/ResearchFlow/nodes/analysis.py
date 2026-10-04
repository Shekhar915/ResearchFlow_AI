
from langchain_core.messages import HumanMessage 
from ResearchFlow.llm.llm import LLM

from ResearchFlow.state.research_state import Research_state

def analyze_question(state:Research_state):
    notes = '\n'.join(
        state['research_notes']
    )

    prompt = f"""
You are a senior research analyst. Your task is to critically analyze the provided research notes and extract key insights.

Analyze the notes provided inside the <notes> tags below:

<notes>
{notes}
</notes>

Provide your analysis strictly adhering to the following four sections. Do not include any introductory or concluding conversational text.

### 1. Main Finding
[Provide a clear, high-level summary of the primary discovery or core insight discovered in the notes.]

### 2. Important Observation
[Highlight 2-3 critical data points, unexpected trends, or significant pieces of supporting evidence found in the text.]

### 3. Limitations
[Identify gaps in the data, potential biases, methodological shortcomings, or areas where the information is incomplete.]

### 4. Final Conclusion
[Deliver a definitive, forward-looking synthesis of what these notes mean for broader research or decision-making.]
"""
    response = LLM.invoke(
        [HumanMessage(content = prompt)]
    )

    return {
        'analysis' : response.content
    }