from ResearchFlow.nodes.question import analyze_question


def test_short_question_needs_no_research():
    assert analyze_question({'question': 'What is LangGraph?'}) == {'research_required': False}


def test_long_question_needs_research():
    q = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"
    assert analyze_question({'question': q}) == {'research_required': True}


def test_answer_uses_analysis_when_present():
    from ResearchFlow.nodes.answer import build_answer

    result = build_answer({'question': 'q', 'analysis': 'detailed analysis'})
    assert result == {'final_answer': 'detailed analysis'}


def test_answer_falls_back_without_analysis():
    from ResearchFlow.nodes.answer import build_answer

    result = build_answer({'question': 'What is LangGraph?'})
    assert 'What is LangGraph?' in result['final_answer']
