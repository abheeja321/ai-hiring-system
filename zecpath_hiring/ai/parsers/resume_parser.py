import re
from collections import Counter

from .common import normalize_text, split_sections


MASTER_SKILLS = {
    "python", "django", "flask", "sql", "postgresql", "java", "javascript", "react",
    "aws", "docker", "kubernetes", "communication", "leadership", "excel", "sales",
    "recruiting", "screening", "analytics", "machine learning", "nlp", "mern", "mean",
}


def _extract_skills(text: str) -> list[dict]:
    normalized = normalize_text(text).lower()
    found = []
    for skill in sorted(MASTER_SKILLS):
        if skill in normalized:
            found.append(
                {
                    "name": skill,
                    "category": "technical" if skill not in {"communication", "leadership", "sales", "recruiting"} else "business",
                    "confidence": 0.93 if skill in normalized else 0.0,
                }
            )
    return found


def _extract_experience(section_text: str) -> list[dict]:
    entries = []
    chunks = [chunk.strip() for chunk in section_text.split("\n") if chunk.strip()]
    for chunk in chunks[:5]:
        years = re.findall(r"(20\d{2}|19\d{2})", chunk)
        duration_months = 12
        if len(years) >= 2:
            duration_months = max((int(years[-1]) - int(years[0])) * 12, 12)
        elif len(years) == 1:
            duration_months = 12
        entries.append(
            {
                "company": chunk.split("-")[0].strip()[:60],
                "title": "Role inferred",
                "start_date": years[0] if years else "unknown",
                "end_date": years[-1] if len(years) > 1 else "present",
                "duration_months": duration_months,
                "highlights": [chunk],
            }
        )
    return entries


def parse_resume_text(candidate_name: str, text: str) -> dict:
    normalized = normalize_text(text)
    sections = split_sections(normalized)
    words = re.findall(r"[A-Za-z][A-Za-z+.#-]+", normalized.lower())
    keywords = [word for word, _ in Counter(words).most_common(20)]
    return {
        "candidate_id": f"cand-{abs(hash(candidate_name)) % 100000}",
        "full_name": candidate_name,
        "contact": {"email": "", "phone": "", "location": ""},
        "summary": sections.get("summary", "")[:500],
        "sections": sections,
        "skills": _extract_skills(sections.get("skills", normalized)),
        "experience": _extract_experience(sections.get("experience", normalized)),
        "education": [{"degree": "Unknown", "field": "Unknown", "institution": "Unknown", "graduation_year": 0}],
        "certifications": [{"name": line, "issuer": "Unknown", "year": 0, "relevance": "general"} for line in sections.get("certifications", "").splitlines() if line.strip()],
        "projects": [{"name": "Project", "description": line, "skills": []} for line in sections.get("projects", "").splitlines() if line.strip()],
        "keywords": keywords,
    }
