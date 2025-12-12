# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from app.model.api_models import TailorRequest, TailorResponse
from app.services.latex_parser import parse_latex_sections
from app.services.latex_merge import merge_sections_into_latex
from app.graph.graph_builder import build_resume_graph
from app.graph.state import ResumeState

app = FastAPI(title="AI Resume Tailor (LangGraph Backend Code)")

# CORS – allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build workflow graph once
graph = build_resume_graph()


@app.post("/Generate", response_model=TailorResponse)
async def tailor_resume(req: TailorRequest) -> TailorResponse:
    # Step 1 – Parse LaTeX
    print("1:",req)
    sections = parse_latex_sections(req.resume_latex)
    print(sections)
    # Step 2 – Build initial state
    state: ResumeState = {
        "job_description": req.job_description,
        "resume_sections": sections,
        "tailored_sections": {},
    }
    print("2:",state)
    # Step 3 – Run graph
    final_state: ResumeState = await run_in_threadpool(graph.invoke, state)
    tailored = final_state.get("tailored_sections", {})
    print("3:",tailored)
    # Step 4 – Merge back into LaTeX
    final_tex = merge_sections_into_latex(req.resume_latex, tailored)

    return TailorResponse(final_latex=final_tex)

