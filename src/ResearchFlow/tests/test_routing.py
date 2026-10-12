from ResearchFlow.routers.research_router import route_after_question


def test_routes_to_research_when_required():
    assert route_after_question({'research_required': True}) == "research"


def test_routes_to_answer_when_not_required():
    assert route_after_question({'research_required': False}) == "answer"
