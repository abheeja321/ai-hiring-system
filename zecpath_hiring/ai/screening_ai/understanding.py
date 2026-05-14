import re
from functools import lru_cache


INTENT_KEYWORDS = {
    "skills": ["skill", "python", "django", "sql", "aws", "react", "communication", "leadership", "technical", "proficient", "expert"],
    "experience": ["experience", "worked", "years", "project", "engineer", "developer", "role", "background"],
    "location": ["bengaluru", "hyderabad", "remote", "location", "relocate", "willing to", "based in", "city"],
    "salary": ["salary", "ctc", "compensation", "lpa", "package", "expectation", "k", "lakh"],
    "notice_period": ["notice", "join", "joining", "immediately", "days", "weeks", "months", "availability"],
    "education": ["degree", "bachelor", "master", "university", "college", "graduated", "b.tech", "m.tech", "bsc"],
    "introduction": ["i am", "my background", "myself", "currently", "working as"],
    "cultural_fit": ["culture", "team", "values", "mission", "collaboration", "environment", "growth", "mentor"],
}


KNOWN_SKILLS = {"python", "django", "sql", "aws", "react", "communication", "leadership", "nlp"}


@lru_cache(maxsize=1024)
def classify_intent(text: str, question_category: str | None = None) -> str:
    lowered = text.lower()
    if len(lowered.split()) < 2:
        return "vague"
    expected_category = str(question_category or "").lower().replace(" ", "_")
    scores = {intent: sum(1 for keyword in keywords if keyword in lowered) for intent, keywords in INTENT_KEYWORDS.items()}
    best_intent = max(scores, key=scores.get)
    if scores[best_intent] == 0:
        return "off_topic"
    if expected_category and expected_category in scores and scores.get(expected_category.replace("_", " "), 0):
        return expected_category
    if expected_category in INTENT_KEYWORDS and scores.get(expected_category, 0) > 0:
        return expected_category
    return best_intent


@lru_cache(maxsize=1024)
def extract_semantic_entities(text: str) -> dict:
    lowered = text.lower()
    skills = sorted({skill for skill in KNOWN_SKILLS if skill in lowered})
    experience_details = [m for m in re.findall(r"\b\d+(?:\.\d+)?\+?\s*(?:years?|yrs?|months?)\b", lowered) if not m.startswith("0")]
    salary_matches = re.findall(r"\b\d+(?:\.\d+)?\s*(?:lpa|lakhs?|k|thousand)\b", lowered)
    notice_matches = re.findall(r"\b\d+\s*(?:days?|weeks?|months?)\b", lowered)
    availability = "immediate" if "immediate" in lowered else (notice_matches[0] if notice_matches else "")
    return {
        "skills": skills,
        "experience_details": experience_details,
        "availability": availability,
        "salary_expectation": salary_matches[0] if salary_matches else "",
    }


def understand_answer(question: dict, normalized_text: str) -> dict:
    intent = classify_intent(normalized_text, question.get("category"))
    entities = extract_semantic_entities(normalized_text)
    missing_information = []
    vagueness_flags = []
    if question.get("mandatory") and len(normalized_text.split()) < 5:
        vagueness_flags.append("answer_too_short")
    if question.get("category") == "Skills" and not entities["skills"]:
        missing_information.append("skills_not_identified")
    if question.get("category") == "Experience" and not entities["experience_details"]:
        missing_information.append("experience_duration_missing")
    if question.get("category") == "Salary" and not entities["salary_expectation"]:
        missing_information.append("salary_expectation_missing")
    if question.get("category") == "Notice period" and not entities["availability"]:
        missing_information.append("availability_missing")
    return {
        "question_id": question.get("id"),
        "category": question.get("category"),
        "intent": intent,
        "entities": entities,
        "off_topic": intent == "off_topic",
        "missing_information": missing_information,
        "vagueness_flags": vagueness_flags,
        "semantic_object": {
            "answer_summary": normalized_text,
            "evidence_count": len(entities["skills"]) + len(entities["experience_details"]),
        },
    }

