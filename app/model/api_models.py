# app/models/api_models.py
from pydantic import BaseModel

class TailorRequest(BaseModel):
    resume_latex: str
    job_description: str

class TailorResponse(BaseModel):
    final_latex: str
