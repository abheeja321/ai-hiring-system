from zecpath_hiring.ai.scoring.explainable import weighted_score


def calculate_ats_score(candidate: dict, job: dict) -> dict:
    candidate_skills = set()
    for skill in candidate.get("skills", []):
        if isinstance(skill, dict):
            candidate_skills.add(skill.get("name", ""))
        else:
            candidate_skills.add(str(skill))
    required_skills = set(job.get("required_skills", []))
    skill_match = round((len(candidate_skills & required_skills) / max(len(required_skills), 1)) * 100, 2)
    if "experience_years" in candidate:
        try:
            exp_years = float(candidate["experience_years"])
            experience = min(exp_years * 10, 100) # 10 points per year
        except (ValueError, TypeError):
            experience = 0
    else:
        experience_items = [e for e in candidate.get("experience", []) if isinstance(e, dict)]
        experience = min(len(experience_items) * 20, 100)
        
    education = 70 if candidate.get("education") else 30
    semantic = min((skill_match * 0.7) + (experience * 0.3), 100)
    return weighted_score(
        {
            "skill_match": skill_match,
            "experience_relevance": experience,
            "education_alignment": education,
            "semantic_similarity": semantic,
        },
        {
            "skill_match": 0.35,
            "experience_relevance": 0.30,
            "education_alignment": 0.15,
            "semantic_similarity": 0.20,
        },
    )


def shortlist_band(score: float) -> str:
    if score >= 80:
        return "SHORTLIST"
    if score >= 55:
        return "REVIEW"
    return "REJECT"

