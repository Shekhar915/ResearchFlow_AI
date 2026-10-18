from ResearchFlow.nodes.question import analyze_question


def test_short_question_needs_no_research():
    assert analyze_question({'question': 'What is LangGraph?'}) == {'research_required': False}


def test_long_question_needs_research():
    q = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"
    assert analyze_question({'question': q}) == {'research_required': True}


class _FakeLLM:
    def invoke(self, messages):
        class _Response:
            content = "final answer"
        return _Response()


def test_answer_uses_llm_output(monkeypatch):
    from ResearchFlow.nodes import answer

    monkeypatch.setattr(answer, 'LLM', _FakeLLM())
    result = answer.generate_answer({
        'question': 'q',
        'research_notes': ['note'],
        'analysis': 'analysis',
    })
    assert result == {'final_answer': 'final answer'}


def test_answer_handles_skipped_research(monkeypatch):
    from ResearchFlow.nodes import answer

    monkeypatch.setattr(answer, 'LLM', _FakeLLM())
    result = answer.generate_answer({'question': 'What is LangGraph?'})
    assert result == {'final_answer': 'final answer'}
