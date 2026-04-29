from zecpath_hiring.ai.scoring.explainable import weighted_score


IMPORTANCE_WEIGHTS = {
    "high": 1.0,
    "medium": 0.75,
    "low": 0.5,
}


def score_screening_answer(question: dict, normalized_text: str, understanding: dict) -> dict:
    words = normalized_text.split()
    clarity = 85 if normalized_text and normalized_text[0].isupper() and normalized_text.endswith((".", "!", "?")) else 65
    relevance = 40 if understanding["off_topic"] else 85
    completeness = 90 - (len(understanding["missing_information"]) * 25)
    consistency = 90 - (len(understanding["vagueness_flags"]) * 20)
    completeness = max(min(completeness, 100), 20)
    consistency = max(min(consistency, 100), 20)
    if len(words) < 4:
        clarity -= 15
        completeness -= 20
    scored = weighted_score(
        {
            "clarity": max(clarity, 20),
            "relevance": relevance,
            "completeness": max(completeness, 20),
            "consistency": consistency,
        },
        {
            "clarity": 0.25,
            "relevance": 0.30,
            "completeness": 0.25,
            "consistency": 0.20,
        },
    )
    scored["question_id"] = question.get("id")
    scored["category"] = question.get("category")
    scored["importance"] = question.get("importance", "medium")
    return scored


def aggregate_screening_scores(question_scores: list[dict]) -> dict:
    if not question_scores:
        return {
            "screening_score": 0.0,
            "per_question_scores": [],
            "summary": "No screening answers available.",
        }
    weighted_total = 0.0
    weight_sum = 0.0
    for item in question_scores:
        importance_weight = IMPORTANCE_WEIGHTS.get(item.get("importance", "medium"), 0.75)
        weighted_total += item["final_score"] * importance_weight
        weight_sum += importance_weight
    final_score = round(weighted_total / max(weight_sum, 1.0), 2)
    return {
        "screening_score": final_score,
        "per_question_scores": question_scores,
        "summary": f"Aggregated {len(question_scores)} screening answers into final score {final_score}.",
    }

