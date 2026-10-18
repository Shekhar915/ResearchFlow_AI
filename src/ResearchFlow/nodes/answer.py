from ResearchFlow.state.research_state import Research_state


# def build_answer(state: Research_state):
#     analysis = state.get('analysis')

#     if analysis:
#         final_answer = analysis
#     else:
#         final_answer = f"No research was required for: {state['question']}"

#     return {
#         'final_answer': final_answer
#     }

from langchain_core.messages import HumanMessage
from ResearchFlow.llm.model import LLM

from ResearchFlow.state.research_state import Research_state

def generate_answer(state: Research_state):
   question = state['question']
   notes = "\n".join(state.get('research_notes', []))
   analysis = state.get('analysis', '')

   prompt = f"""
        You are a helpful research assistant.

        user question : 
        {question}
        research notes:
         {notes}
        analysis:
        {analysis}

    Generate a concise, clear and useful final answer to the user's question, try to
    avoid anything irrelevant.

    """
   response = LLM.invoke(
      [HumanMessage(content = prompt)]
   )
   return {
      "final_answer" : response.content
   }