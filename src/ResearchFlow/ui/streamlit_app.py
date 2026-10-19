import streamlit as st

from ResearchFlow.services.research_service import run_research


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

        st.subheader("Answer")
        st.write(result.get('final_answer', ''))

        if result.get('research_notes'):
            with st.expander("Research notes"):
                for note in result['research_notes']:
                    st.markdown(f"- {note}")

        if result.get('analysis'):
            with st.expander("Analysis"):
                st.markdown(result['analysis'])
