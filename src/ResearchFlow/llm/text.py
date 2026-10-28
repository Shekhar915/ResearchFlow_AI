import re
import textwrap

_FENCE = re.compile(r'^\s*```[a-zA-Z]*\n(.*?)\n```\s*$', re.DOTALL)


def content_to_text(content) -> str:
    """Normalize an LLM response into clean markdown text.

    Handles plain strings and lists of content parts, removes a wrapping
    code fence, and strips stray indentation that would make markdown
    render as a code block.
    """
    if isinstance(content, list):
        content = "".join(
            part if isinstance(part, str) else part.get('text', '')
            for part in content
        )

    text = str(content or '').replace('\r\n', '\n').strip()

    fenced = _FENCE.match(text)
    if fenced:
        text = fenced.group(1)

    return textwrap.dedent(text).strip()
