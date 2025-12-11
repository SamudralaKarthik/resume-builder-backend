# app/graph/state.py
from typing import TypedDict, Dict

class ResumeState(TypedDict, total=False):
    """
    Carries all data through the LangGraph pipeline.
    """
    job_description: str
    resume_sections: Dict[str, str]
    tailored_sections: Dict[str, str]
