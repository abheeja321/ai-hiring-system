from datetime import UTC, datetime


def build_screening_report(candidate: dict, job: dict, screening: dict) -> dict:
    understanding_items = screening.get("understanding", [])
    score_items = screening.get("score_breakdown", {}).get("per_question_scores", [])
    signal_items = screening.get("signal_analysis", [])
    strengths = []
    risks = []
    missing_data = []
    key_answers = []
    skill_confirmations = sorted(
        {skill for item in understanding_items for skill in item.get("entities", {}).get("skills", [])}
    )
    salary_expectation = _first_non_empty(
        item.get("entities", {}).get("salary_expectation", "") for item in understanding_items
    )
    availability = _first_non_empty(
        item.get("entities", {}).get("availability", "") for item in understanding_items
    )

    for item in understanding_items:
        if item.get("semantic_object", {}).get("answer_summary"):
            key_answers.append(
                {
                    "question_id": item.get("question_id"),
                    "category": item.get("category"),
                    "summary": item["semantic_object"]["answer_summary"],
                }
            )
        missing_data.extend(item.get("missing_information", []))
        if item.get("off_topic"):
            risks.append(f"{item.get('category')} response was off-topic.")

    for item in signal_items:
        band = item.get("behavioral_indicators", {}).get("confidence_band")
        if band == "high":
            strengths.append(f"{item.get('question_id')} showed high confidence.")
        if item.get("contradictions"):
            risks.append(f"{item.get('question_id')} contains possible contradictions.")
        if item.get("behavioral_indicators", {}).get("hesitation_risk") == "high":
            risks.append(f"{item.get('question_id')} contains repeated hesitation.")

    if screening.get("screening_score", 0) >= 80:
        strengths.append("Overall screening score is strong.")
    if skill_confirmations:
        strengths.append(f"Confirmed skills: {', '.join(skill_confirmations)}.")

    report = {
        "report_id": f"screen-{candidate.get('candidate_id', 'cand')}-{job.get('job_id', 'job')}",
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "candidate": {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("full_name"),
        },
        "job": {
            "job_id": job.get("job_id"),
            "title": job.get("title"),
        },
        "screening_score": screening.get("screening_score"),
        "summary": {
            "salary_expectation": salary_expectation,
            "availability": availability,
            "skill_confirmations": skill_confirmations,
        },
        "key_answers": key_answers[:7],
        "strengths": _dedupe(strengths),
        "risks": _dedupe(risks),
        "missing_data": sorted(set(item for item in missing_data if item)),
        "recommendation": _recommendation(screening),
        "report_format": {
            "exportable": True,
            "sections": ["summary", "key_answers", "strengths", "risks", "missing_data", "recommendation"],
        },
        "per_question_scores": score_items,
    }
    return report


def _dedupe(items: list[str]) -> list[str]:
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def _first_non_empty(values) -> str:
    for value in values:
        if value:
            return value
    return ""


def _recommendation(screening: dict) -> str:
    score = screening.get("screening_score", 0)
    if score >= 80:
        return "Proceed to next interview stage."
    if score >= 65:
        return "Manual recruiter review recommended."
    return "Do not advance without clarification."
