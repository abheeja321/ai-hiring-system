# Answer Understanding and Screening Scoring

## Intent classifier outputs

- `introduction`
- `education`
- `experience`
- `skills`
- `location`
- `salary`
- `notice_period`
- `off_topic`
- `vague`

## Structured answer format

```json
{
  "question_id": "skill_tech_001",
  "category": "Skills",
  "intent": "skills",
  "entities": {
    "skills": ["python", "django", "sql"],
    "experience_details": ["4 years"],
    "availability": "",
    "salary_expectation": ""
  },
  "off_topic": false,
  "missing_information": [],
  "vagueness_flags": [],
  "semantic_object": {
    "answer_summary": "My strongest skills are python, django, and sql.",
    "evidence_count": 4
  }
}
```

## Screening scoring parameters

- `clarity`
- `relevance`
- `completeness`
- `consistency`

## Final screening score object

```json
{
  "screening_score": 81.25,
  "per_question_scores": [
    {
      "question_id": "intro_001",
      "category": "Introduction",
      "final_score": 84.5
    }
  ],
  "summary": "Aggregated 7 screening answers into final score 81.25."
}
```

