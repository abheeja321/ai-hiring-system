# HR AI Scoring Logic & Data Formats

## Scoring Overview

The HR AI system uses layered scoring. Each round remains explainable on its own, then the unified scoring engine combines the round scores into a hiring-fit percentage.

## ATS Score

Module: `zecpath_hiring.ai.ats_engine.scoring`

Components:

- skill match: `35%`
- experience relevance: `30%`
- education alignment: `15%`
- semantic similarity: `20%`

Output:

```json
{
  "final_score": 82.5,
  "components": {},
  "weights": {}
}
```

## Screening Score

Module: `zecpath_hiring.ai.screening_ai.scoring`

Per-answer components:

- clarity: `25%`
- relevance: `30%`
- completeness: `25%`
- consistency: `20%`

Question scores are aggregated using importance weights:

- high: `1.0`
- medium: `0.75`
- low: `0.5`

## HR Interview Score

Module: `zecpath_hiring.ai.hr_interview.scoring_engine`

Default components:

- relevance: `40%`
- communication: `30%`
- confidence: `20%`
- consistency: `10%`

Optional aptitude components:

- logical thinking
- problem-solving clarity

All inputs are clamped to `0-100`, and weights are normalized before final score calculation.

## Aptitude Score

Module: `zecpath_hiring.ai.hr_interview.aptitude_evaluator`

Components:

- logical thinking: `45%`
- problem-solving clarity: `35%`
- situational judgment: `20%`

## Unified Hiring Fit

Module: `zecpath_hiring.ai.scoring.unified`

Default cross-round weights:

- ATS: `35%`
- screening: `25%`
- HR interview: `40%`

Role adjustments:

- technical: higher ATS weight
- non-technical: higher screening and HR interview weight
- leadership: higher HR interview weight
- fresher: higher screening weight

Formula:

```text
hiring_fit =
  ats_score * adjusted_ats_weight +
  screening_score * adjusted_screening_weight +
  hr_interview_score * adjusted_hr_interview_weight
```

## Data Formats

### Screening Interaction

```json
{
  "question_id": "intro_001",
  "question_category": "Introduction",
  "transcript_text": "Um I built APIs...",
  "normalized_text": "I built apis.",
  "confidence_level": 0.91,
  "answer_payload": {},
  "scoring_payload": {}
}
```

### HR Interview Turn Evaluation

```json
{
  "turn_id": 1,
  "relevance_score": 85.0,
  "communication_score": 82.0,
  "confidence_score": 78.0,
  "contradiction_penalty": 5.0,
  "logical_thinking_score": 80.0,
  "problem_solving_clarity_score": 76.0
}
```

### Recruiter Summary

```json
{
  "candidate_strengths": [],
  "weaknesses": [],
  "cultural_fit_indicators": [],
  "risk_flags": [],
  "inconsistencies": [],
  "recommendation": "Proceed to next round.",
  "natural_language_report": "..."
}
```

### Compliance Readiness Report

```json
{
  "consent": {},
  "protected_signal_review": {},
  "fairness_review": {},
  "explainability": {},
  "retention_policy": {},
  "compliance_status": "ready",
  "blocking_items": []
}
```

## Auditability Requirements

- Store model version on every `AIArtifact`.
- Keep applied weights in scoring outputs.
- Keep risk flags attached to score objects.
- Keep consent and retention metadata available before production decisioning.
