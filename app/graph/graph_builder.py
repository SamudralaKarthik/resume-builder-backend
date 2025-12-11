# app/graph/graph_builder.py
from langgraph.graph import StateGraph, END
from .state import ResumeState
from .nodes import (
    tailor_summary_node,
    tailor_skills_node,
    tailor_experience_node,
    tailor_projects_node,
    tailor_certifications_node,
)

def build_resume_graph():
    graph = StateGraph(ResumeState)

    # Add nodes
    graph.add_node("summary", tailor_summary_node)
    graph.add_node("skills", tailor_skills_node)
    graph.add_node("experience", tailor_experience_node)
    graph.add_node("projects", tailor_projects_node)
    graph.add_node("certifications", tailor_certifications_node)

    # Entry
    graph.set_entry_point("summary")

    # Linear flow
    graph.add_edge("summary", "skills")
    graph.add_edge("skills", "experience")
    graph.add_edge("experience", "projects")
    graph.add_edge("projects", "certifications")
    graph.add_edge("certifications", END)

    # Compile
    return graph.compile()
