from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScreeningRequest, ScreeningResponse
from parser import parse_resume
from matcher import screen_resumes

app = FastAPI(title="Smart Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Resume Screener is running"}


@app.post("/screen-resumes", response_model=ScreeningResponse)
def screen(request: ScreeningRequest):
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    if not request.resumes:
        raise HTTPException(status_code=400, detail="At least one resume is required.")

    parsed = [parse_resume(r.content, r.filename) for r in request.resumes]
    jd_skills, results = screen_resumes(request.job_description, parsed)

    return ScreeningResponse(
        total_resumes=len(results),
        job_skills_required=jd_skills,
        results=results,
    )
