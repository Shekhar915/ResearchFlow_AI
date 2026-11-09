# ResearchFlow AI

A LangGraph-based research assistant that takes a question, decides whether
deeper research is needed, gathers notes, analyzes them with an LLM
(Google Gemini), and produces a final answer. A Streamlit interface is
provides the front end.

> Status: work in progress. The core flow (question, research, analysis, answer),
> routing, service layer and Streamlit UI are implemented; tool-call wiring,
> and LLM-driven tool selection are still planned.

## Project structure

```
ResearchFLow_AI/
├── app.py                     # Entry point (launches the Streamlit UI)
├── requirements.txt
├── .env.example               # Template for required environment variables
├── docs/architecture.md       # Design notes and planned graph flow
└── src/ResearchFlow/
    ├── config/                # Settings and environment loading
    ├── llm/                   # LLM wrapper
    ├── state/                 # Graph state definitions
    ├── nodes/                 # Graph nodes (question, research, analysis, ...)
    ├── routers/               # Conditional routing between nodes
    ├── subgraphs/             # Reusable research subgraph
    ├── graphs/                # Main, research and agent graphs
    ├── services/              # Service layer used by the UI
    ├── ui/                    # Streamlit app
    └── tests/                 # Unit tests
```

## Getting started

1. Create and activate a virtual environment

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies

   ```powershell
   pip install -r requirements.txt
   ```

3. Configure your API key

   ```powershell
   copy .env.example .env
   ```

   Then edit `.env` and set `GEMINI_API_KEY` to your Google Gemini key.
   The `.env` file is git-ignored and must never be committed.

4. Run the app

   ```powershell
   streamlit run app.py
   ```

## Tech stack

- LangGraph and LangChain for orchestration
- Google Gemini via `langchain-google-genai`
- Streamlit for the user interface
- python-dotenv for configuration

## Running the tests

The tests use a fake LLM, so they run offline and need no API key:

```powershell
python -m pytest -q src/ResearchFlow/tests
```

## Graph variants

| Graph | File | Flow |
|-------|------|------|
| Main | `graphs/research_graph.py` | question -> research -> tools -> analysis -> evaluation -> answer |
| Review | `graphs/agent_graph.py` | same flow, with a human approval pause before the answer |
| Subgraph | `subgraphs/research_graph.py` | research -> tools -> analysis -> evaluation (no answer step) |

## Configuration

| Variable | Required | Purpose |
|----------|----------|---------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key; the app stops at startup without it |
| `LOG_LEVEL` | No | Console log verbosity (default `INFO`) |
| `LANGSMITH_TRACING` | No | Set to `true` to send traces to LangSmith |
| `LANGSMITH_API_KEY` | No | LangSmith API key, only needed when tracing is on |
| `LANGSMITH_PROJECT` | No | LangSmith project name |

Questions are limited to 2000 characters (`MAX_QUESTION_CHARS` in
`services/research_service.py`).
