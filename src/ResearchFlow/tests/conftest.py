import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault("GEMINI_API_KEY", "test-key")


import pytest


@pytest.fixture(autouse=True)
def research_threshold(monkeypatch):
    """Pin the research threshold so tests don't depend on the app setting."""
    from ResearchFlow.nodes import question

    monkeypatch.setattr(question, 'RESEARCH_WORD_THRESHOLD', 10)
