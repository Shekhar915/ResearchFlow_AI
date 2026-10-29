from ResearchFlow.routers.research_router import route_after_question


def test_routes_to_research_when_required():
    assert route_after_question({'research_required': True}) == "research"


def test_routes_to_answer_when_not_required():
    assert route_after_question({'research_required': False}) == "answer"


def test_evaluation_routes_to_answer_when_complete():
    from ResearchFlow.routers.research_router import route_after_evaluation

    state = {'analysis_complete': True, 'analysis_attempts': 1}
    assert route_after_evaluation(state) == "answer"


def test_evaluation_retries_when_incomplete():
    from ResearchFlow.routers.research_router import route_after_evaluation

    state = {'analysis_complete': False, 'analysis_attempts': 0}
    assert route_after_evaluation(state) == "analysis"


def test_evaluation_stops_retrying_at_limit():
    from ResearchFlow.routers.research_router import route_after_evaluation

    state = {'analysis_complete': False, 'analysis_attempts': 1}
    assert route_after_evaluation(state) == "answer"
