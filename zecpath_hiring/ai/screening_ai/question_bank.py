from copy import deepcopy


BASE_QUESTION_BANK = {
    "general": [
        {
            "id": "intro_001",
            "category": "Introduction",
            "question": "Please introduce yourself and summarize your recent professional background.",
            "expected_answer_type": "narrative",
            "mandatory": True,
            "importance": "high",
            "languages": ["en"],
            "template_key": "introduction_summary",
        },
        {
            "id": "edu_001",
            "category": "Education",
            "question": "What is your highest qualification and how does it support this role?",
            "expected_answer_type": "structured_narrative",
            "mandatory": False,
            "importance": "medium",
            "languages": ["en"],
            "template_key": "education_alignment",
        },
        {
            "id": "exp_001",
            "category": "Experience",
            "question": "Tell us about the experience that is most relevant to this position.",
            "expected_answer_type": "narrative",
            "mandatory": True,
            "importance": "high",
            "languages": ["en"],
            "template_key": "experience_relevance",
        },
        {
            "id": "loc_001",
            "category": "Location",
            "question": "What is your current location and are you open to the job location requirements?",
            "expected_answer_type": "short_text",
            "mandatory": True,
            "importance": "medium",
            "languages": ["en"],
            "template_key": "location_availability",
        },
        {
            "id": "sal_001",
            "category": "Salary",
            "question": "What is your expected compensation for this role?",
            "expected_answer_type": "numeric_range",
            "mandatory": False,
            "importance": "medium",
            "languages": ["en"],
            "template_key": "salary_expectation",
        },
        {
            "id": "notice_001",
            "category": "Notice period",
            "question": "What is your notice period or earliest joining date?",
            "expected_answer_type": "date_or_duration",
            "mandatory": True,
            "importance": "high",
            "languages": ["en"],
            "template_key": "notice_period",
        },
    ],
    "engineering": [
        {
            "id": "skill_tech_001",
            "category": "Skills",
            "question": "Which of the required technical skills have you used most recently, and in what kind of projects?",
            "expected_answer_type": "narrative_list",
            "mandatory": True,
            "importance": "high",
            "languages": ["en"],
            "template_key": "technical_skill_recency",
        }
    ],
    "non_technical": [
        {
            "id": "skill_nt_001",
            "category": "Skills",
            "question": "Which of the required business or operational skills are your strongest, and where have you applied them?",
            "expected_answer_type": "narrative_list",
            "mandatory": True,
            "importance": "high",
            "languages": ["en"],
            "template_key": "business_skill_recency",
        }
    ],
}


def role_family_for_job(job: dict) -> str:
    title = str(job.get("title", "")).lower()
    keywords = " ".join(job.get("required_skills", [])).lower()
    if any(item in f"{title} {keywords}" for item in ["engineer", "developer", "python", "django", "sql", "aws"]):
        return "engineering"
    return "non_technical"


def build_screening_questions(job: dict, eligibility: dict | None = None) -> dict:
    role_family = role_family_for_job(job)
    questions = deepcopy(BASE_QUESTION_BANK["general"]) + deepcopy(BASE_QUESTION_BANK[role_family])
    required_skills = job.get("required_skills", [])
    for question in questions:
        if "{required_skills}" in question["question"]:
            question["question"] = question["question"].format(required_skills=", ".join(required_skills))
    return {
        "role_family": role_family,
        "eligibility_status": (eligibility or {}).get("status", "UNKNOWN"),
        "question_count": len(questions),
        "questions": questions,
        "category_mapping": {item["id"]: item["category"] for item in questions},
    }

