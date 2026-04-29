# Transcript Data Architecture

## Voice transcript schema

```json
{
  "candidate_id": "cand-1001",
  "job_id": "job-2001",
  "question_id": "intro_001",
  "question_category": "Introduction",
  "timestamp": "2026-04-28T10:30:00Z",
  "confidence_level": 0.93,
  "audio_metadata": {
    "source_format": "webm",
    "duration_seconds": 18,
    "accent_hint": "Indian English",
    "noise_level": "medium"
  },
  "segments": [
    {
      "speaker": "candidate",
      "start_ms": 0,
      "end_ms": 11200,
      "text": "I have four years of experience in Python and Django.",
      "confidence": 0.92,
      "silence_before_ms": 300,
      "interrupted": false,
      "partial": false
    }
  ],
  "raw_text": "I have four years of experience in Python and Django.",
  "normalized_text": "I have four years of experience in python and django."
}
```

## Metadata standards

- `candidate_id`
- `job_id`
- `question_id`
- `question_category`
- `timestamp`
- `confidence_level`
- `model_version`
- `source_format`
- `duration_seconds`
- `accent_hint`
- `noise_level`

## Normalization rules

- remove filler words like `um`, `uh`, `like`, `you know`
- collapse repeated whitespace
- normalize interrupted fragments marked by pauses or ellipses
- restore sentence punctuation where possible
- normalize case to sentence case
- tag silence, partial answers, and interrupted speech explicitly

## Screening interaction schema

Database entity: `ScreeningInteraction`

- candidate reference
- job reference
- question ID
- question category
- raw transcript text
- normalized transcript text
- confidence level
- interaction timestamp
- answer payload JSON
- scoring payload JSON

