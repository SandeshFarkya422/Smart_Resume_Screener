from typing import Optional
from pydantic import BaseModel


class ParsedResume(BaseModel):
    filename: str
    candidate_name: str
    raw_text: str
    skills: list[str]
    experience_years: Optional[int] = None


class ResumeInput(BaseModel):
    filename: str
    content: str


class ScreeningRequest(BaseModel):
    job_description: str
    resumes: list[ResumeInput]


class ResumeResult(BaseModel):
    filename: str
    candidate_name: str
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    experience_years: Optional[int]
    explanation: str


class ScreeningResponse(BaseModel):
    total_resumes: int
    job_skills_required: list[str]
    results: list[ResumeResult]
