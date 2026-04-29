import re

from .common import normalize_text


JD_SKILL_HINTS = [
    "python", "django", "react", "sql", "aws", "docker", "communication",
    "leadership", "nlp", "machine learning", "recruiting", "screening",
]


def parse_job_description(title: str, text: str) -> dict:
    normalized = normalize_text(text)
    lowered = normalized.lower()
    required_skills = [skill for skill in JD_SKILL_HINTS if skill in lowered]
    exp_match = re.search(r"(\d+)\+?\s+years", lowered)
    return {
        "job_id": f"job-{abs(hash(title)) % 100000}",
        "title": title,
        "department": "General",
        "experience_required_years": int(exp_match.group(1)) if exp_match else 0,
        "required_skills": required_skills,
        "preferred_skills": [],
        "education_preferences": ["Bachelor's degree preferred"] if "bachelor" in lowered else [],
        "keywords": required_skills,
        "responsibilities": [line.strip("- ").strip() for line in normalized.splitlines() if line.strip()][:10],
        "location": "Flexible",
        "normalized_text": normalized,
    }

