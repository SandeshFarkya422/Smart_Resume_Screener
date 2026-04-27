
Matches resumes against a job description using TF-IDF + Cosine Similarity.


Swagger UI → http://127.0.0.1:8000/docs

# run test_demo

python test_demo.py

# API

**POST** `/screen-resumes`


**Response**

```json
{
  "total_resumes": 2,
  "job_skills_required": ["docker", "fastapi", "postgresql", "python"],
  "results": [
    {
      "filename": "alice.txt",
      "candidate_name": "Alice Johnson",
      "match_score": 91.5,
      "matched_skills": ["docker", "fastapi", "postgresql", "python"],
      "missing_skills": [],
      "experience_years": 5,
      "explanation": "Excellent match (score: 91.5/100)..."
    }
  ]
}
```
