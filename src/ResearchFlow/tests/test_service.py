import pytest

from ResearchFlow.services.research_service import run_research


def test_empty_question_is_rejected():
    with pytest.raises(ValueError):
        run_research("   ")
