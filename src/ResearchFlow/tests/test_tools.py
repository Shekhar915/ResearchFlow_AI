from datetime import date

from ResearchFlow.nodes import tool_call
from ResearchFlow.nodes.tool_call import call_tools, extract_numbers, today, word_count


def test_word_count_counts_words():
    assert word_count("one two three") == "The question has 3 words."


def test_extract_numbers_handles_negatives_and_decimals():
    assert extract_numbers("temps -4 and 2.5") == "Numbers found: -4, 2.5."


def test_extract_numbers_reports_none():
    assert extract_numbers("no digits here") == "No numbers found."


def test_today_uses_the_current_date(monkeypatch):
    class _FixedDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 15)

    monkeypatch.setattr(tool_call, 'date', _FixedDate)
    assert today("") == "Today's date is 2026-01-15."


def test_multiple_tools_can_fire_for_one_question():
    result = call_tools({'question': 'How many words are there today?'})
    assert len(result['research_notes']) == 2
