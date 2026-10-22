# question, research_required, research_notes, analysis, final_answer

from typing import TypedDict
class Research_state(TypedDict):
    question : str
    research_required : bool
    research_notes : list[str]
    analysis : str
    final_answer : str
    analysis_complete : bool
    missing_sections : list[str]
