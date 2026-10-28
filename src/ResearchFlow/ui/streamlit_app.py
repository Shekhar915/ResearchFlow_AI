import re

import streamlit as st

from ResearchFlow.services.research_service import run_research


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """Split markdown on '#' headings into (title, body) pairs."""
    parts = re.split(r'^#{1,4}\s*(.+?)\s*$', markdown, flags=re.MULTILINE)
    if len(parts) == 1:
        return [('', markdown.strip())]

    sections = []
    if parts[0].strip():
        sections.append(('', parts[0].strip()))
    for title, body in zip(parts[1::2], parts[2::2]):
        sections.append((title, body.strip()))
    return sections


def show_answer(answer: str):
    st.subheader("Answer")
    with st.container(border=True):
        st.markdown(answer)


def show_notes(notes: list[str]):
    with st.expander(f"Research notes ({len(notes)})"):
        for note in notes:
            st.markdown(f"- {note}")


def show_analysis(analysis: str):
    with st.expander("Analysis", expanded=True):
        for title, body in split_sections(analysis):
            if title:
                st.markdown(f"**{title}**")
            st.markdown(body)


def main():
    st.set_page_config(page_title="ResearchFlow AI", page_icon="🔎")
    st.title("ResearchFlow AI")
    st.caption("Ask a question and get a researched, analyzed answer.")

    question = st.text_area("Your question", height=120)

    if st.button("Run research", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        with st.spinner("Researching..."):
            try:
                result = run_research(question)
            except Exception as error:
                st.error(f"Something went wrong: {error}")
                return

        show_answer(result.get('final_answer', ''))

        if result.get('research_notes'):
            show_notes(result['research_notes'])

        if result.get('analysis'):
            show_analysis(result['analysis'])
