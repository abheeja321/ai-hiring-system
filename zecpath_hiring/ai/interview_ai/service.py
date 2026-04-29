def run_interview_intelligence(candidate: dict, job: dict) -> dict:
    technical_depth = 80 if any(skill["name"] in {"python", "django", "sql"} for skill in candidate.get("skills", [])) else 55
    hr_readiness = 78 if candidate.get("summary") else 60
    problem_solving = 82 if candidate.get("projects") else 58
    interview_score = round((technical_depth + hr_readiness + problem_solving) / 3, 2)
    return {
        "interview_score": interview_score,
        "hr_interview_ai": {"fit": hr_readiness, "behavioral_prompt_set": 6},
        "technical_interview_ai": {"depth": technical_depth, "question_set": 8},
        "machine_test_ai": {"problem_solving": problem_solving, "assessment_required": True},
    }

