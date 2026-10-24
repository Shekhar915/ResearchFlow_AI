from langgraph.types import Command

from ResearchFlow.graphs.agent_graph import build_review_graph
from ResearchFlow.nodes import answer, analysis, research
from ResearchFlow.routers.agent_router import route_after_review

LONG_QUESTION = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"


class _FakeLLM:
    def invoke(self, messages):
        class _Response:
            content = "Main Finding Important Observation Limitations Final Conclusion"
        return _Response()


def _patch_llm(monkeypatch):
    for module in (research, analysis, answer):
        monkeypatch.setattr(module, 'LLM', _FakeLLM())


def test_review_router():
    assert route_after_review({'approved': True}) == "answer"
    assert route_after_review({'approved': False}) == "analysis"


def test_graph_pauses_then_finishes_after_approval(monkeypatch):
    _patch_llm(monkeypatch)
    graph = build_review_graph()
    config = {'configurable': {'thread_id': 'approve'}}

    paused = graph.invoke({'question': LONG_QUESTION}, config)
    assert '__interrupt__' in paused
    assert 'final_answer' not in paused

    result = graph.invoke(Command(resume=True), config)
    assert result['approved'] is True
    assert result['final_answer']


def test_rejection_loops_back_to_analysis(monkeypatch):
    _patch_llm(monkeypatch)
    graph = build_review_graph()
    config = {'configurable': {'thread_id': 'reject'}}

    graph.invoke({'question': LONG_QUESTION}, config)
    paused_again = graph.invoke(Command(resume=False), config)

    assert '__interrupt__' in paused_again
    assert paused_again['analysis_attempts'] == 2
