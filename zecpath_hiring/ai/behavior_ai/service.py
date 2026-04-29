def run_behavior_analysis(candidate: dict) -> dict:
    bias_masking_applied = True
    collaboration = 82 if "leadership" in {skill["name"] for skill in candidate.get("skills", [])} else 70
    stability = 76 if len(candidate.get("experience", [])) >= 2 else 65
    behavior_score = round((collaboration + stability) / 2, 2)
    return {
        "behavior_score": behavior_score,
        "fairness": {
            "bias_masking_applied": bias_masking_applied,
            "excluded_fields": ["name", "email", "location"],
        },
    }

