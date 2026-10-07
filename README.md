# ResearchFlow AI

A LangGraph-based research assistant that takes a question, decides whether
deeper research is needed, gathers notes, analyzes them with an LLM
(Google Gemini), and produces a final answer. A Streamlit interface is
planned as the front end.

> Status: work in progress. The state definition, the question-routing node
> and the analysis node are implemented; the remaining nodes, routers and
> graphs are scaffolded and will be filled in step by step.

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
