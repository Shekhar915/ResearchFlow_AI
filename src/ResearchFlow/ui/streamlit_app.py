import streamlit as st

from ResearchFlow.services.research_service import stream_research_events


def show_streamed_answer(question: str):
    """Show live progress while the graph runs, then stream the answer."""
    progress = st.status("Researching your question...", expanded=True)
    progress.write("Started. This can take a little while, please keep this page open.")

    st.subheader("Answer")
    answer_placeholder = st.empty()
    collected_answer = ""

    try:
        for kind, text in stream_research_events(question):
            if kind == 'status':
                progress.write(f"✔ {text}")
            else:
                if not collected_answer:
                    progress.update(label="Writing the answer...")
                collected_answer += text
                answer_placeholder.markdown(collected_answer + " ▌")
    except ValueError as e:
        progress.update(label="Invalid question", state="error")
        st.warning(str(e))
        return
    except Exception as e:
        progress.update(label="Research failed", state="error")
        st.error(f"An error occurred during research: {e}")
        return

    if collected_answer.strip():
        answer_placeholder.markdown(collected_answer)
        progress.update(label="Research complete", state="complete", expanded=False)
    else:
        answer_placeholder.empty()
        progress.update(label="No answer generated", state="error")
        st.warning("No answer generated. Please try again with a different question.")


def main():
    st.set_page_config(page_title="ResearchFlow AI", page_icon="🔎")
    st.title("ResearchFlow AI")
    st.caption("Ask a question and get a researched, analyzed answer.")

    question = st.text_area(
        "Your question", placeholder="For example: what is Python?", height=120
    )

    if st.button("Run research", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            show_streamed_answer(question)


if __name__ == "__main__":
    main()
