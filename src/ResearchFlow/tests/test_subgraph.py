from ResearchFlow.nodes import analysis, research
from ResearchFlow.subgraphs.research_graph import research_subgraph


class _FakeLLM:
    def invoke(self, messages):
        class _Response:
            content = "- fact one\n- fact two"
        return _Response()


def test_subgraph_has_no_answer_node():
    nodes = set(research_subgraph.get_graph().nodes)
    assert {'research', 'analysis', 'evaluation'} <= nodes
    assert 'answer' not in nodes


def test_subgraph_collects_notes_and_analysis(monkeypatch):
    for module in (research, analysis):
        monkeypatch.setattr(module, 'LLM', _FakeLLM())

    result = research_subgraph.invoke({'question': 'any question'})

    assert result['research_notes'] == ['fact one', 'fact two']
    assert result['analysis']
    assert result['analysis_attempts'] == 2
    assert 'final_answer' not in result
