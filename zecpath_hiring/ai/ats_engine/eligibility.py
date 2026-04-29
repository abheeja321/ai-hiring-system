DEFAULT_ELIGIBILITY_RULES = {
    "minimum_ats_score": 65.0,
    "mandatory_skills": [],
    "minimum_experience_years": 0,
    "maximum_experience_years": 50,
    "allowed_locations": [],
    "availability_required": False,
}


def _candidate_skill_names(candidate: dict) -> set[str]:
    return {skill.get("name", "").lower() for skill in candidate.get("skills", [])}


def _candidate_location(candidate: dict) -> str:
    contact = candidate.get("contact", {})
    return str(contact.get("location", "")).strip().lower()


def _candidate_experience_years(candidate: dict) -> float:
    months = sum(int(item.get("duration_months", 0)) for item in candidate.get("experience", []))
    return round(months / 12, 2)


def _candidate_available(candidate: dict) -> bool:
    availability = candidate.get("availability")
    if availability is None:
        return True
    return bool(availability)


def build_role_eligibility_rules(job: dict, overrides: dict | None = None) -> dict:
    rules = {
        **DEFAULT_ELIGIBILITY_RULES,
        "mandatory_skills": list(job.get("required_skills", [])),
        "minimum_experience_years": job.get("experience_required_years", 0),
        "allowed_locations": [job.get("location")] if job.get("location") and job.get("location") != "Flexible" else [],
    }
    if overrides:
        rules.update(overrides)
    return rules


def evaluate_candidate_eligibility(candidate: dict, job: dict, ats_result: dict, rules: dict | None = None) -> dict:
    active_rules = build_role_eligibility_rules(job, rules)
    candidate_skills = _candidate_skill_names(candidate)
    mandatory_skills = {skill.lower() for skill in active_rules.get("mandatory_skills", [])}
    missing_skills = sorted(mandatory_skills - candidate_skills)

    ats_score = float(ats_result.get("final_score", 0.0))
    experience_years = _candidate_experience_years(candidate)
    location = _candidate_location(candidate)
    allowed_locations = [str(item).strip().lower() for item in active_rules.get("allowed_locations", []) if item]
    location_match = True if not allowed_locations else location in allowed_locations
    availability_match = True if not active_rules.get("availability_required") else _candidate_available(candidate)
    experience_match = active_rules["minimum_experience_years"] <= experience_years <= active_rules["maximum_experience_years"]
    score_match = ats_score >= active_rules["minimum_ats_score"]

    if score_match and not missing_skills and experience_match and location_match and availability_match:
        status = "ELIGIBLE"
    elif ats_score >= active_rules["minimum_ats_score"] - 10 and experience_match:
        status = "REVIEW"
    else:
        status = "REJECTED"

    return {
        "status": status,
        "rules_applied": active_rules,
        "ats_score": ats_score,
        "experience_years": experience_years,
        "missing_mandatory_skills": missing_skills,
        "location_match": location_match,
        "availability_match": availability_match,
        "experience_match": experience_match,
        "score_match": score_match,
        "eligible_for_ai_screening_call": status == "ELIGIBLE",
        "reasons": [
            f"ATS score {ats_score} vs cutoff {active_rules['minimum_ats_score']}",
            f"Missing mandatory skills: {', '.join(missing_skills) if missing_skills else 'none'}",
            f"Experience years: {experience_years}",
            f"Location matched: {location_match}",
            f"Availability matched: {availability_match}",
        ],
    }

