def analyze_edge_case_risk(transcript: dict, understanding: dict) -> dict:
    normalization = transcript.get("normalization", {})
    raw_text = transcript.get("raw_text", "")
    confidence = transcript.get("segments", [{}])[0].get("confidence", 0.0)
    mixed_language = any(token in raw_text.lower() for token in ["haan", "nahi", "achha", "theek"])
    poor_audio = confidence < 0.7
    background_noise = transcript.get("audio_metadata", {}).get("noise_level") == "high"
    missing_answer = normalization.get("silence_detected") or len(transcript.get("normalized_text", "").split()) == 0
    return {
        "poor_audio": poor_audio,
        "language_mixing": mixed_language,
        "background_noise": background_noise,
        "missing_answer": missing_answer,
        "safety_fallback_required": poor_audio or background_noise or missing_answer,
        "clarification_required": mixed_language or understanding.get("off_topic") or understanding.get("missing_information"),
    }


def fallback_strategy(edge_case_risk: dict) -> dict:
    if edge_case_risk["missing_answer"]:
        return {
            "action": "retry_question",
            "message": "I did not catch an answer. Could you please repeat that clearly?",
        }
    if edge_case_risk["poor_audio"] or edge_case_risk["background_noise"]:
        return {
            "action": "switch_to_manual_or_retry",
            "message": "The audio quality is affecting analysis. Please move to a quieter place or continue later.",
        }
    if edge_case_risk["language_mixing"]:
        return {
            "action": "clarify_language",
            "message": "Could you continue in one language so I can capture your answer accurately?",
        }
    return {
        "action": "continue",
        "message": "Proceed with the next step.",
    }

