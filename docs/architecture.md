# Architecture

## State

The graph shares a single typed state, `Research_state`
(`src/ResearchFlow/state/research_state.py`):

| Field               | Type        | Purpose                                      |
|---------------------|-------------|----------------------------------------------|
| `question`          | `str`       | The user's question                          |
| `research_required` | `bool`      | Whether the question needs a research pass   |
| `research_notes`    | `list[str]` | Notes collected during research              |
| `analysis`          | `str`       | Structured analysis of the notes             |
| `final_answer`      | `str`       | The answer returned to the user              |

## Nodes

| Node       | File                | Status      | Responsibility                                                  |
|------------|---------------------|-------------|-----------------------------------------------------------------|
| question   | `nodes/question.py` | Implemented | Sets `research_required` (true when the question exceeds 10 words) |
| analysis   | `nodes/analysis.py` | Implemented | Prompts the LLM to analyze the notes into four sections         |
| research   | `nodes/research.py` | Planned     | Collect research notes                                          |
| tool_call  | `nodes/tool_call.py`| Planned     | Call external tools                                             |
| evaluation | `nodes/evaluation.py`| Planned    | Check the quality of the analysis                               |
| human_review | `nodes/human_review.py` | Planned | Optional human approval step                                  |
| answer     | `nodes/answer.py`   | Planned     | Compose the final answer                                        |

The analysis node returns four sections: Main Finding, Important
Observation, Limitations and Final Conclusion.

## Planned flow

```
question -> [research_required?]
    yes -> research -> analysis -> evaluation -> (human_review) -> answer
    no  ----------------------------------------------------------> answer
```

Routing decisions live in `routers/`, and the graphs in `graphs/` and
`subgraphs/` wire the nodes together.

## Configuration

`config/settings.py` loads `.env` and requires `GEMINI_API_KEY`; the app
fails fast with a clear error when it is missing.
