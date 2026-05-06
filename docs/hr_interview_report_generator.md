# HR Interview Report Generator

## Objective

Convert HR interview analysis into recruiter-ready insights that can be displayed in dashboards, exported to reports, or reviewed before moving a candidate forward.

## Structured summary template

```json
{
  "candidate_strengths": [],
  "weaknesses": [],
  "cultural_fit_indicators": [],
  "risk_flags": [],
  "overall_hr_performance": "",
  "recruiter_recommendation": ""
}
```

## Generated sections

- candidate strengths
- weaknesses
- cultural fit indicators
- risk flags
- highlighted inconsistencies
- overall HR performance
- natural-language recruiter report
- recommendation

## Inconsistency handling

The generator highlights inconsistencies from explicit evaluation notes and high contradiction penalties. These are promoted into recruiter risk flags so a reviewer knows what to clarify before advancing the candidate.

## Sample HR summary report

Strong candidate:

> Sample Strong delivered a strong HR interview with an overall score of 88/100. Strengths include structured examples, collaborative decision-making, clear communication, and steady confidence. Recommendation: proceed to next round.

Needs review:

> Sample Review delivered a recruiter-review HR interview with an overall score of 67/100. Strengths include relevant motivation, but answers need sharper examples and the interview contains consistency risks. Recommendation: proceed only after recruiter clarification.

Implementation lives in `zecpath_hiring.ai.hr_interview.report_generator`.
