from langgraph.graph import (
    StateGraph,
    START,
    END
)

from ResearchFlow.state.research_state import Research_state
from ResearchFlow.nodes.question import analyze_question
from ResearchFlow.nodes.research import research_question
from ResearchFlow.nodes.analysis import analyze_notes
from ResearchFlow.nodes.answer import generate_answer
from ResearchFlow.routers.research_router import route_after_question

builder = StateGraph(Research_state)

builder.add_node('analyze_question', analyze_question)
builder.add_node('research', research_question)
builder.add_node('analysis', analyze_notes)
builder.add_node('answer', generate_answer)

builder.add_edge(START, 'analyze_question')
builder.add_conditional_edges(
    'analyze_question',
    route_after_question,
    {
        'research': 'research',
        'answer': 'answer'
    }
)
builder.add_edge('research', 'analysis')
builder.add_edge('analysis', 'answer')
builder.add_edge('answer', END)

research_graph = builder.compile()
