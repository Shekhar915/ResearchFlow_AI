import logging
import time

from ResearchFlow.graphs.main_graph import main_graph

logger = logging.getLogger(__name__)

MAX_QUESTION_CHARS = 2000

ANSWER_NODES = ('answer', 'generate_answer', 'final_answer')

NODE_LABELS = {
    'analyze_question': 'Analyzed the question',
    'research': 'Gathered research notes',
    'tools': 'Ran helper tools',
    'analysis': 'Analyzed the notes',
    'evaluation': 'Evaluated the analysis',
    'human_review': 'Reviewed by a human',
    'answer': 'Wrote the final answer',
}


def validate_question(question: str) -> str:
    """Return the stripped question, or raise ValueError if it is invalid."""
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty.")
    if len(question) > MAX_QUESTION_CHARS:
        raise ValueError(f"Question must be at most {MAX_QUESTION_CHARS} characters.")

    return question


def run_research(question: str) -> dict:
    """Run the graph for a question and return the final state."""
    question = validate_question(question)

    return main_graph.invoke({'question': question})


def message_text(content) -> list[str]:
    """Extract the text pieces from a message chunk's content."""
    if isinstance(content, str):
        return [content] if content else []

    texts = []
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get('type') == 'text':
                text = part.get('text', '')
                if text:
                    texts.append(text)
    return texts


def stream_research_events(question: str):
    """Yield (kind, text) events while the graph runs.

    kind is 'status' for a finished step (progress messages) or 'token' for
    a piece of the final answer. If the model produced no token stream, the
    answer node's finished output is yielded as one 'token' event instead.
    """
    question = validate_question(question)
    started = time.perf_counter()
    logger.info("Research started (%d characters)", len(question))

    streamed = False
    fallback = ''

    for mode, data in main_graph.stream(
        {'question': question}, stream_mode=['messages', 'updates']
    ):
        if mode == 'messages':
            message_chunk, metadata = data
            if metadata.get('langgraph_node', '') not in ANSWER_NODES:
                continue
            for text in message_text(message_chunk.content):
                streamed = True
                yield 'token', text
        elif mode == 'updates':
            for node_name, update in data.items():
                yield 'status', NODE_LABELS.get(node_name, f'Finished {node_name}')
                if node_name in ANSWER_NODES and isinstance(update, dict):
                    fallback = update.get('final_answer', fallback)

    if not streamed and fallback:
        yield 'token', fallback

    logger.info("Research finished in %.1fs", time.perf_counter() - started)


def stream_research(question: str):
    """Yield only the answer text, for callers that don't need progress."""
    for kind, text in stream_research_events(question):
        if kind == 'token':
            yield text
