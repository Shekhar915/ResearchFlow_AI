from ResearchFlow.nodes.question import analyze_question


def test_short_question_needs_no_research():
    assert analyze_question({'question': 'What is LangGraph?'}) == {'research_required': False}


def test_long_question_needs_research():
    q = "Explain in detail how conditional routing works between nodes in a LangGraph state graph"
    assert analyze_question({'question': q}) == {'research_required': True}
