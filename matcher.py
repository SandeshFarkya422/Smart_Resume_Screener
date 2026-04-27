from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import ParsedResume, ResumeResult
from parser import extract_skills


def get_cosine_score(jd, resume_text):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([jd, resume_text])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except ValueError:
        return 0.0


def get_skill_overlap(jd_skills, resume_skills):
    jd_set = set(jd_skills)
    resume_set = set(resume_skills)
    matched = sorted(jd_set & resume_set)
    missing = sorted(jd_set - resume_set)
    return matched, missing


def blend_score(cosine, matched, jd_skills, exp_years, jd_text):
    skill_ratio = (len(matched) / len(jd_skills) * 100) if jd_skills else cosine
    score = 0.60 * cosine + 0.40 * skill_ratio
    if exp_years and exp_years >= 3:
        if any(w in jd_text.lower() for w in ["senior", "lead", "3+", "5+"]):
            score = min(100, score + 3)
    return round(score, 2)


def build_explanation(score, matched, missing, exp_years, name):
    if score >= 75:
        level = "Excellent match"
    elif score >= 55:
        level = "Good match"
    elif score >= 35:
        level = "Partial match"
    else:
        level = "Weak match"

    exp_str = f"{exp_years} year(s) of experience" if exp_years else "unspecified experience"
    matched_str = ", ".join(matched[:5]) if matched else "none of the required skills"
    missing_str = ", ".join(missing[:4]) if missing else "none"

    lines = [
        f"{level} (score: {score}/100). {name} has {exp_str}.",
        f"Matching skills: {matched_str}.",
    ]

    if missing:
        lines.append(f"Missing: {missing_str} — worth discussing in the interview.")
    else:
        lines.append("All required skills are covered, candidate looks like a strong fit.")

    return " ".join(lines)


def screen_resumes(job_description, resumes):
    jd_skills = extract_skills(job_description)
    results = []

    for resume in resumes:
        cosine = get_cosine_score(job_description, resume.raw_text)
        matched, missing = get_skill_overlap(jd_skills, resume.skills)
        score = blend_score(cosine, matched, jd_skills, resume.experience_years, job_description)
        explanation = build_explanation(score, matched, missing, resume.experience_years, resume.candidate_name)

        results.append(ResumeResult(
            filename=resume.filename,
            candidate_name=resume.candidate_name,
            match_score=score,
            matched_skills=matched,
            missing_skills=missing,
            experience_years=resume.experience_years,
            explanation=explanation,
        ))

    results.sort(key=lambda r: r.match_score, reverse=True)
    return jd_skills, results
