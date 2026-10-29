from ResearchFlow.nodes.question import analyze_question


def test_short_question_needs_no_research():
    assert analyze_question({'question': 'What is LangGraph?'}) == {'research_required': False}


def test_long_question_needs_research():
    q = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"
    assert analyze_question({'question': q}) == {'research_required': True}


class _FakeLLM:
    def invoke(self, messages, config=None):
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
    }, {})
    assert result == {'final_answer': 'final answer'}


def test_answer_handles_skipped_research(monkeypatch):
    from ResearchFlow.nodes import answer

    monkeypatch.setattr(answer, 'LLM', _FakeLLM())
    result = answer.generate_answer({'question': 'What is LangGraph?'}, {})
    assert result == {'final_answer': 'final answer'}


def test_evaluation_passes_complete_analysis():
    from ResearchFlow.nodes.evaluation import evaluate_analysis

    text = "Main Finding\nImportant Observation\nLimitations\nFinal Conclusion"
    result = evaluate_analysis({'analysis': text})
    assert result == {
        'analysis_attempts': 1,
        'analysis_complete': True,
        'missing_sections': [],
    }


def test_evaluation_reports_missing_sections():
    from ResearchFlow.nodes.evaluation import evaluate_analysis

    result = evaluate_analysis({'analysis': "Main Finding only"})
    assert result['analysis_complete'] is False
    assert 'Limitations' in result['missing_sections']


def test_tool_call_adds_matching_tool_notes():
    from ResearchFlow.nodes.tool_call import call_tools

    result = call_tools({'question': 'How many words are in this sentence?'})
    assert result['research_notes'] == ['The question has 7 words.']


def test_tool_call_keeps_existing_notes_and_skips_unmatched():
    from ResearchFlow.nodes.tool_call import call_tools

    result = call_tools({'question': 'Explain LangGraph', 'research_notes': ['old']})
    assert result['research_notes'] == ['old']


def test_tool_call_extracts_numbers():
    from ResearchFlow.nodes.tool_call import call_tools

    result = call_tools({'question': 'List the numbers in 12 apples and 3.5 pears'})
    assert result['research_notes'] == ['Numbers found: 12, 3.5.']
