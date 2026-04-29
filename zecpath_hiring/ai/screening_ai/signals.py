POSITIVE_WORDS = {
    "confident", "strong", "delivered", "led", "achieved", "improved", "built", "ready", "clear",
}

NEGATIVE_WORDS = {
    "not sure", "maybe", "difficult", "struggled", "uncertain", "confused", "problem", "can't",
}

UNCERTAINTY_PATTERNS = {
    "i think", "maybe", "not sure", "probably", "kind of", "sort of", "approximately",
}

CONTRADICTION_PAIRS = [
    ("immediate", "30 days"),
    ("fresher", "4 years"),
    ("remote only", "open to relocate"),
]


def analyze_confidence_and_sentiment(transcript: dict, understanding: dict) -> dict:
    text = transcript.get("normalized_text", "").lower()
    words = text.split()
    hesitation_count = sum(1 for pattern in UNCERTAINTY_PATTERNS if pattern in text)
    positive_hits = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_hits = sum(1 for word in NEGATIVE_WORDS if word in text)
    contradictions = [pair for pair in CONTRADICTION_PAIRS if pair[0] in text and pair[1] in text]
    response_length = len(words)
    estimated_duration_seconds = max(transcript.get("segments", [{}])[0].get("end_ms", 0) / 1000, 1)
    response_pace_wpm = round((response_length / estimated_duration_seconds) * 60, 2)
    uncertainty_score = max(0, 100 - (hesitation_count * 18) - (len(understanding.get("vagueness_flags", [])) * 15))
    sentiment_score = max(0, min(100, 50 + (positive_hits * 12) - (negative_hits * 14)))
    confidence_score = max(
        0,
        min(
            100,
            78
            - (hesitation_count * 12)
            - (len(contradictions) * 18)
            + (positive_hits * 6)
            - (negative_hits * 8),
        ),
    )
    communication_strength = _communication_band(confidence_score, response_length, response_pace_wpm)
    return {
        "hesitation_patterns": hesitation_count,
        "response_length_words": response_length,
        "response_pace_wpm": response_pace_wpm,
        "sentiment_score": sentiment_score,
        "sentiment_label": _sentiment_label(sentiment_score),
        "uncertainty_score": uncertainty_score,
        "contradictions": [{"left": left, "right": right} for left, right in contradictions],
        "confidence_score": confidence_score,
        "communication_strength": communication_strength,
        "behavioral_indicators": _behavioral_indicators(
            confidence_score, sentiment_score, hesitation_count, len(contradictions), understanding
        ),
    }


def _sentiment_label(score: float) -> str:
    if score >= 65:
        return "positive"
    if score <= 40:
        return "negative"
    return "neutral"


def _communication_band(confidence_score: float, response_length: int, pace_wpm: float) -> str:
    if confidence_score >= 80 and response_length >= 8 and 90 <= pace_wpm <= 180:
        return "strong"
    if confidence_score >= 60:
        return "moderate"
    return "weak"


def _behavioral_indicators(
    confidence_score: float,
    sentiment_score: float,
    hesitation_count: int,
    contradiction_count: int,
    understanding: dict,
) -> dict:
    return {
        "confidence_band": "high" if confidence_score >= 80 else ("medium" if confidence_score >= 60 else "low"),
        "sentiment_band": _sentiment_label(sentiment_score),
        "hesitation_risk": "high" if hesitation_count >= 2 else ("medium" if hesitation_count == 1 else "low"),
        "contradiction_risk": "high" if contradiction_count else "low",
        "missing_data_risk": "medium" if understanding.get("missing_information") else "low",
    }

