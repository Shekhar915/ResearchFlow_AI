from ResearchFlow.graphs import research_graph as rg
from ResearchFlow.nodes import answer, analysis, research


class _FakeLLM:
    def invoke(self, messages):
        class _Response:
            content = "- fact one\n- fact two"
        return _Response()


def _patch_llm(monkeypatch):
    for module in (research, analysis, answer):
        monkeypatch.setattr(module, 'LLM', _FakeLLM())


def test_graph_compiles_with_expected_nodes():
    nodes = set(rg.research_graph.get_graph().nodes)
    assert {'analyze_question', 'research', 'analysis', 'answer'} <= nodes


def test_short_question_skips_research(monkeypatch):
    _patch_llm(monkeypatch)
    result = rg.research_graph.invoke({'question': 'What is LangGraph?'})
    assert result['research_required'] is False
    assert 'research_notes' not in result
    assert result['final_answer']


def test_long_question_runs_full_flow(monkeypatch):
    _patch_llm(monkeypatch)
    question = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"
    result = rg.research_graph.invoke({'question': question})
    assert result['research_required'] is True
    assert result['research_notes'] == ['fact one', 'fact two']
    assert result['analysis']
    assert result['final_answer']
