# Unified Scoring Engine

## Objective

Combine all previous hiring rounds into a single hiring intelligence score that recruiters can use as a final fit signal.

## Integrated rounds

- **ATS score**: resume/job alignment, skills, experience relevance, education alignment, and semantic fit.
- **Screening score**: pre-interview answer clarity, relevance, completeness, consistency, and intent fit.
- **HR interview score**: live HR interview performance, communication, confidence, consistency, aptitude logic, and situational judgment.

## Cross-round weight system

Default weights:

```json
{
  "ats_weight": 0.35,
  "screening_weight": 0.25,
  "hr_interview_weight": 0.40
}
```

The weights are normalized after every adjustment so the total always equals `1.0`.

## Role-based adjustments

- **Technical**: increases ATS weight and reduces screening weight because hard-skill alignment is more important.
- **Non-technical**: reduces ATS weight and increases screening/interview weight because communication and live judgment carry more signal.
- **Leadership**: increases HR interview weight to emphasize judgment, culture, and stakeholder maturity.
- **Fresher**: increases screening weight and lowers ATS weight so potential is not over-penalized by limited experience.

## Hiring fit calculation

```text
hiring_fit_percentage =
  ats_score * adjusted_ats_weight +
  screening_score * adjusted_screening_weight +
  hr_interview_score * adjusted_hr_interview_weight
```

## Unified candidate score object

The engine returns:

- candidate ID
- role type
- hiring fit percentage
- decision band
- recommendation
- input scores
- applied weights
- weighted contributions
- role adjustments
- risk flags
- generated timestamp

## Decision bands

- `Strong hire`: 85+
- `Hire`: 75-84.99
- `Final review`: 65-74.99
- `Hold`: 55-64.99
- `Reject`: below 55

Implementation lives in `zecpath_hiring.ai.scoring.unified`.
