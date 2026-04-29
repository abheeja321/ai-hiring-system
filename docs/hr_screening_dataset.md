# HR Screening Dataset Creation

## Question categories

- `Introduction`
- `Education`
- `Experience`
- `Skills`
- `Location`
- `Salary`
- `Notice period`

## Conversation-ready question object

```json
{
  "id": "intro_001",
  "category": "Introduction",
  "question": "Please introduce yourself and summarize your recent professional background.",
  "expected_answer_type": "narrative",
  "mandatory": true,
  "importance": "high",
  "languages": ["en"],
  "template_key": "introduction_summary"
}
```

## Design notes

- The dataset is reusable across job roles through a base question bank plus role-family overlays.
- Questions are tagged with expected answer type, mandatory/optional status, and scoring importance.
- The structure is multilingual-ready through the `languages` field and template keys.
- Engineering and non-technical roles can receive different skill questions while sharing the same HR core.

