from ResearchFlow.llm.text import content_to_text


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
