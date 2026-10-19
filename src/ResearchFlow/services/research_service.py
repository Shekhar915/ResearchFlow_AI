from ResearchFlow.graphs.main_graph import main_graph


def run_research(question: str) -> dict:
    """Run the graph for a question and return the final state."""
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty.")

    return main_graph.invoke({'question': question})
