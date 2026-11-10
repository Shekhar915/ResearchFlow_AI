# Helper tools

The `tools` step (`nodes/tool_call.py`) runs between `research` and
`analysis`. It checks the question for trigger phrases and, for each match,
appends the tool's result to `research_notes`.

| Tool | Trigger phrases | Result |
|------|-----------------|--------|
| `word_count` | "how many words", "word count" | Number of words in the question |
| `today` | "today", "current date", "what date" | Today's date (ISO format) |
| `numbers` | "numbers in", "extract numbers" | Numbers found in the question |

## Adding a tool

1. Write a function that takes the question text and returns a string.
2. Register it in the `TOOLS` dictionary with its trigger phrases.
3. Add a unit test in `tests/test_tools.py`.

Several tools can run for the same question, and existing notes are kept.
