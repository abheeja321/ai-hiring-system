import re


FILLER_WORDS = {
    "um", "uh", "like", "you know", "actually", "basically", "sort of", "kind of",
}


def simulate_stt_transcript(question_id: str, raw_voice_text: str, confidence: float = 0.91) -> dict:
    return {
        "question_id": question_id,
        "audio_metadata": {
            "source_format": "webm",
            "duration_seconds": max(len(raw_voice_text.split()) * 0.4, 1),
            "accent_hint": "general",
            "noise_level": "medium" if "--" in raw_voice_text or "..." in raw_voice_text else "low",
        },
        "segments": [
            {
                "speaker": "candidate",
                "start_ms": 0,
                "end_ms": max(len(raw_voice_text.split()) * 400, 1000),
                "text": raw_voice_text,
                "confidence": confidence,
                "silence_before_ms": 300,
                "interrupted": "--" in raw_voice_text or "..." in raw_voice_text,
                "partial": raw_voice_text.strip().endswith("..."),
            }
        ],
        "raw_text": raw_voice_text,
    }


def remove_fillers(text: str) -> str:
    normalized = text
    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        normalized = re.sub(rf"\b{re.escape(filler)}\b", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s{2,}", " ", normalized)
    return normalized.strip(" ,.")


def normalize_transcript_text(text: str) -> dict:
    cleaned = text.replace("\n", " ").replace("--", " ").replace("...", " ")
    cleaned = remove_fillers(cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    cleaned = cleaned.lower()
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
        if cleaned[-1] not in ".!?":
            cleaned = f"{cleaned}."
    silence_detected = text.strip() == "" or cleaned == ""
    return {
        "normalized_text": cleaned,
        "silence_detected": silence_detected,
        "partial_answer": text.strip().endswith("..."),
        "interrupted_speech": "--" in text or "..." in text,
    }


def build_clean_transcript(question_id: str, raw_voice_text: str, confidence: float = 0.91) -> dict:
    transcript = simulate_stt_transcript(question_id, raw_voice_text, confidence)
    normalization = normalize_transcript_text(raw_voice_text)
    transcript["normalized_text"] = normalization["normalized_text"]
    transcript["normalization"] = normalization
    return transcript
