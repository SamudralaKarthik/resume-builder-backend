# app/graph/nodes.py
from typing import Dict
from .state import ResumeState
from app.core.llm_client import call_llm
from langsmith import traceable

BASE_SYSTEM_PROMPT = """
You are an expert resume writing assistant.
Your job is to TAILOR a specific section of a LaTeX resume
to match a given job description while:
- preserving truthful experience
- using ATS-friendly keywords
- keeping LaTeX-safe output
- returning ONLY the section content, no explanations.
"""

def _build_user_prompt(section_name: str, original_text: str, jd: str) -> str:
    return f"""
Section to tailor: {section_name.upper()}

Original section:
----------------
{original_text}

Job Description:
----------------
{jd}

INSTRUCTIONS:
- Rewrite ONLY this section.
- Maintain LaTeX syntax.
- DO NOT hallucinate or invent new companies.
- Add missing ATS keywords when appropriate.
- Return only the updated section content.
""".strip()


def tailor_section_generic(state: ResumeState, section: str) -> Dict:
    """Common node function for summary, skills, experience, etc."""
    sections = state.get("resume_sections", {})
    jd = state.get("job_description", "")

    if section not in sections:
        return {"tailored_sections": state.get("tailored_sections", {})}

    original = sections[section]
    prompt = _build_user_prompt(section, original, jd)

    tailored = call_llm(BASE_SYSTEM_PROMPT, prompt).strip()

    updated = {
        **state.get("tailored_sections", {}),
        section: tailored
    }

    return {"tailored_sections": updated}


# ------ NODE WRAPPERS -------
@traceable(name="node_summary")
def tailor_summary_node(state: ResumeState) -> ResumeState:
    print("sum")
    return tailor_section_generic(state, "summary")

@traceable(name="node_skills")
def tailor_skills_node(state: ResumeState) -> ResumeState:
    print("skil")
    return tailor_section_generic(state, "skills")

@traceable(name="node_experience")
def tailor_experience_node(state: ResumeState) -> ResumeState:
    print("exp")
    return tailor_section_generic(state, "experience")

@traceable(name="node_projects")
def tailor_projects_node(state: ResumeState) -> ResumeState:
    print("pro")
    return tailor_section_generic(state, "projects")

@traceable(name="node_certifications")
def tailor_certifications_node(state: ResumeState) -> ResumeState:
    print("cer")
    return tailor_section_generic(state, "certifications")
