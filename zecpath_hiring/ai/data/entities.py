from typing import Any


def candidate_profile_schema() -> dict[str, Any]:
    return {
        "candidate_id": "string",
        "full_name": "string",
        "contact": {"email": "string", "phone": "string", "location": "string"},
        "summary": "string",
        "skills": [{"name": "string", "category": "technical|business|creative", "confidence": 0.0}],
        "experience": [
            {
                "company": "string",
                "title": "string",
                "start_date": "YYYY-MM",
                "end_date": "YYYY-MM|present",
                "duration_months": 0,
                "highlights": ["string"],
            }
        ],
        "education": [
            {
                "degree": "string",
                "field": "string",
                "institution": "string",
                "graduation_year": 0,
            }
        ],
        "certifications": [{"name": "string", "issuer": "string", "year": 0, "relevance": "string"}],
        "projects": [{"name": "string", "description": "string", "skills": ["string"]}],
    }


def job_profile_schema() -> dict[str, Any]:
    return {
        "job_id": "string",
        "title": "string",
        "department": "string",
        "experience_required_years": 0,
        "required_skills": ["string"],
        "preferred_skills": ["string"],
        "education_preferences": ["string"],
        "keywords": ["string"],
        "responsibilities": ["string"],
        "location": "string",
    }

