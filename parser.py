import re
from typing import Optional
from models import ParsedResume


SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "ruby", "php", "scala", "r", "matlab",
    "html", "css", "react", "angular", "vue", "nextjs", "svelte", "bootstrap",
    "tailwind", "jquery", "graphql", "rest", "restful",
    "django", "flask", "fastapi", "spring", "express", "nodejs", "laravel",
    "rails", "asp.net", "gin",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sqlite", "oracle", "cassandra", "dynamodb", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "ci/cd", "jenkins", "github actions", "circleci", "helm", "nginx",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "spark", "hadoop", "airflow", "mlflow", "huggingface", "langchain",
    "llm", "openai", "data analysis", "data science",
    "tableau", "power bi", "dbt",
    "agile", "scrum", "kanban", "jira", "git", "github", "gitlab",
    "linux", "bash",
    "cybersecurity", "oauth", "jwt",
    "android", "ios", "flutter", "react native",
    "microservices", "kafka", "rabbitmq", "websockets", "api design",
    "system design", "unit testing", "pytest", "jest",
]


def extract_skills(text):
    text_lower = text.lower()
    found = set()
    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.add(skill)
    return sorted(found)


def extract_experience(text):
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?(?:work\s+)?experience',
        r'experience[:\s]+(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s+(?:in|of)\s+\w+',
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return int(m.group(1))
    return None


def extract_name(text):
    for line in text.splitlines():
        line = line.strip()
        if line and not any(c.isdigit() for c in line) and len(line.split()) <= 5:
            return line
    return "Unknown"


def parse_resume(raw_text, filename="resume.txt"):
    cleaned = " ".join(raw_text.split())
    return ParsedResume(
        filename=filename,
        candidate_name=extract_name(raw_text),
        raw_text=cleaned,
        skills=extract_skills(raw_text),
        experience_years=extract_experience(raw_text),
    )
