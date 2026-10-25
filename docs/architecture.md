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
| research   | `nodes/research.py` | Implemented | Collect research notes                                          |
| tool_call  | `nodes/tool_call.py`| Planned     | Call external tools                                             |
| evaluation | `nodes/evaluation.py`| Implemented | Check the quality of the analysis                               |
| human_review | `nodes/human_review.py` | Implemented | Optional human approval step                                  |
| answer     | `nodes/answer.py`   | Implemented | Compose the final answer                                        |

The analysis node returns four sections: Main Finding, Important
Observation, Limitations and Final Conclusion.

## Planned flow

```
question -> [research_required?]
    yes -> research -> analysis -> evaluation -> answer
    no  ----------------------------------------------------------> answer
```

Routing decisions live in `routers/`, and the graphs in `graphs/` and
`subgraphs/` wire the nodes together.

## Configuration

`config/settings.py` loads `.env` and requires `GEMINI_API_KEY`; the app
fails fast with a clear error when it is missing.

## Evaluation retry loop

After `analysis`, the `evaluation` node checks that all four sections are
present. `route_after_evaluation` sends the flow back to `analysis` when
sections are missing, and moves on to `answer` once the analysis is complete
or `MAX_ANALYSIS_ATTEMPTS` (2) is reached, so the loop always terminates.

## Human review graph

`graphs/agent_graph.py` builds a variant of the research flow with an
approval step. After evaluation passes, `human_review` calls LangGraph's
`interrupt`, which pauses the run and saves its state in a checkpointer.
Resuming with `Command(resume=True)` approves the analysis and continues to
`answer`; `Command(resume=False)` routes back to `analysis` for another pass.
Each run needs a `thread_id` in its config so the paused state can be found.

## Research subgraph

`subgraphs/research_graph.py` packages `research -> analysis -> evaluation`
(including the retry loop) as a standalone compiled graph that stops before
the answer step. It can be reused as a node inside a larger graph, or run on
its own when only notes and an analysis are needed.
