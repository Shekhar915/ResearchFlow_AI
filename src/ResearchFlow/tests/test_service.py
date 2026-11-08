import pytest

from ResearchFlow.services.research_service import (
    message_text,
    run_research,
    stream_research,
    validate_question,
)


def test_empty_question_is_rejected():
    with pytest.raises(ValueError):
        run_research("   ")


def test_validate_question_strips_whitespace():
    assert validate_question("  hi  ") == "hi"


def test_stream_rejects_empty_question():
    with pytest.raises(ValueError):
        list(stream_research(" "))


def test_message_text_handles_strings_and_parts():
    assert message_text("abc") == ["abc"]
    assert message_text("") == []
    parts = [{'type': 'text', 'text': 'a'}, {'type': 'image'}, {'type': 'text', 'text': ''}]
    assert message_text(parts) == ["a"]
    assert message_text(None) == []


def test_too_long_question_is_rejected():
    from ResearchFlow.services.research_service import MAX_QUESTION_CHARS

    with pytest.raises(ValueError):
        validate_question("a" * (MAX_QUESTION_CHARS + 1))


def test_question_at_the_limit_is_accepted():
    from ResearchFlow.services.research_service import MAX_QUESTION_CHARS

    assert len(validate_question("a" * MAX_QUESTION_CHARS)) == MAX_QUESTION_CHARS
