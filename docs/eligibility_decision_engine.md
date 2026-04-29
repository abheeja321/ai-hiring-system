# Eligibility Decision Engine

## Objective

Automatically decide which candidates qualify for AI screening calls after ATS evaluation and recruiter-defined job rules.

## Eligibility parameters

- `minimum_ats_score`
- `mandatory_skills`
- `minimum_experience_years`
- `maximum_experience_years`
- `allowed_locations`
- `availability_required`

## Decision tags

- `ELIGIBLE`
- `REVIEW`
- `REJECTED`

## Rule configuration format

```json
{
  "minimum_ats_score": 70,
  "mandatory_skills": ["python", "django", "sql"],
  "minimum_experience_years": 3,
  "maximum_experience_years": 10,
  "allowed_locations": ["bengaluru", "hyderabad"],
  "availability_required": true
}
```

## Candidate eligibility result structure

```json
{
  "status": "ELIGIBLE",
  "ats_score": 82.4,
  "experience_years": 4.5,
  "missing_mandatory_skills": [],
  "location_match": true,
  "availability_match": true,
  "experience_match": true,
  "score_match": true,
  "eligible_for_ai_screening_call": true,
  "rules_applied": {}
}
```

