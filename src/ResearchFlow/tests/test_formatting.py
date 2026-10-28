from ResearchFlow.llm.text import content_to_text
from ResearchFlow.ui.streamlit_app import split_sections


def test_plain_string_is_trimmed():
    assert content_to_text("  hello \n") == "hello"


def test_list_of_parts_is_joined():
    parts = [{'type': 'text', 'text': 'Hello '}, 'world']
    assert content_to_text(parts) == "Hello world"


def test_wrapping_code_fence_is_removed():
    assert content_to_text("```markdown\n### Title\nBody\n```") == "### Title\nBody"


def test_indentation_is_removed():
    assert content_to_text("    ### Title\n    Body") == "### Title\nBody"


def test_none_becomes_empty_string():
    assert content_to_text(None) == ""


def test_split_sections_by_headings():
    text = "### 1. Main Finding\nA\n\n### 2. Limitations\nB"
    assert split_sections(text) == [("1. Main Finding", "A"), ("2. Limitations", "B")]


def test_split_sections_without_headings():
    assert split_sections("just text") == [("", "just text")]
