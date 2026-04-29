VOICE_TRANSCRIPT_SCHEMA = {
    "candidate_id": "string",
    "job_id": "string",
    "question_id": "string",
    "question_category": "string",
    "timestamp": "ISO-8601 datetime",
    "confidence_level": 0.0,
    "audio_metadata": {
        "source_format": "wav|mp3|webm",
        "duration_seconds": 0,
        "accent_hint": "string",
        "noise_level": "low|medium|high",
    },
    "segments": [
        {
            "speaker": "candidate",
            "start_ms": 0,
            "end_ms": 0,
            "text": "string",
            "confidence": 0.0,
            "silence_before_ms": 0,
            "interrupted": False,
            "partial": False,
        }
    ],
    "raw_text": "string",
    "normalized_text": "string",
}


AI_SCREENING_DATA_STRUCTURE = {
    "transcript": VOICE_TRANSCRIPT_SCHEMA,
    "understanding": {
        "intent": "introduction|education|experience|skills|location|salary|notice_period|off_topic",
        "entities": {
            "skills": ["string"],
            "experience_details": ["string"],
            "availability": "string",
            "salary_expectation": "string",
        },
        "missing_information": ["string"],
        "vagueness_flags": ["string"],
        "off_topic": False,
    },
    "scoring": {
        "clarity": 0.0,
        "relevance": 0.0,
        "completeness": 0.0,
        "consistency": 0.0,
        "final_score": 0.0,
        "explanation": ["string"],
    },
}

