from pathlib import Path
import pdfplumber
from parser import parse_resume
from matcher import screen_resumes

SAMPLE_DIR = Path(__file__).parent / "sample_data"

JD = """
We are looking for a Senior Python Backend Engineer with 3+ years of experience.
Required: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS, Redis, CI/CD, Git, Agile, Scrum.
"""

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def main():
    pdf_files = list(SAMPLE_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF found in sample_data/")
        return

    parsed = [parse_resume(read_pdf(f), f.name) for f in pdf_files]
    jd_skills, results = screen_resumes(JD, parsed)

    print("=" * 60)
    print("RESUME SCREENING RESULTS")
    print("=" * 60)
    print(f"JD Skills: {', '.join(jd_skills)}\n")

    for i, r in enumerate(results, 1):
        print(f"#{i} {r.candidate_name} ({r.filename})")
        print(f"   Score     : {r.match_score}/100")
        print(f"   Experience: {r.experience_years or 'N/A'} years")
        print(f"   Matched   : {', '.join(r.matched_skills) or 'None'}")
        print(f"   Missing   : {', '.join(r.missing_skills) or 'None'}")
        print(f"   Note      : {r.explanation}")
        print("-" * 60)


if __name__ == "__main__":
    main()
