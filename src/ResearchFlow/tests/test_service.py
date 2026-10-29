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
