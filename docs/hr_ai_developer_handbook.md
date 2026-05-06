# HR AI Developer Handbook

## Purpose

This guide helps developers integrate, maintain, test, and troubleshoot the HR Interview AI and hiring intelligence modules.

## Local Setup

1. Install dependencies from `requirements.txt`.
2. Run migrations if database models changed.
3. Start Django with:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

4. Open the dashboard at `/`.
5. Use the API under `/api/v1/`.

## Primary Integration Path

Use:

```text
POST /api/v1/runs/run_pipeline/
```

This creates:

- `JobProfile`
- `CandidateProfile`
- `HiringRun`
- `AIArtifact`

The response contains ATS, screening, interview, behavior, final score, decision, and full explanation payload.

## Core Maintenance Areas

### Scoring

Relevant modules:

- `zecpath_hiring.ai.ats_engine.scoring`
- `zecpath_hiring.ai.screening_ai.scoring`
- `zecpath_hiring.ai.hr_interview.scoring_engine`
- `zecpath_hiring.ai.scoring.unified`

Rules:

- Keep component scores between `0` and `100`.
- Normalize weights before final score calculation.
- Add tests for every threshold or weight change.
- Preserve explainability fields such as component scores, applied weights, and risk flags.

### HR Interview Flow

Relevant modules:

- `zecpath_hiring.ai.hr_interview.flow_controller`
- `zecpath_hiring.ai.hr_interview.state_manager`
- `zecpath_hiring.ai.hr_interview.question_bank`
- `zecpath_hiring.ai.hr_interview.follow_up_engine`

Rules:

- Keep interview phase transitions deterministic.
- Avoid unlimited follow-ups.
- Treat complete structured answers as sufficient.
- Add new categories in `categories.py` before using them in the flow.

### Transcript Processing

Relevant module:

- `zecpath_hiring.ai.screening_ai.transcript_processing`

Rules:

- Clean filler words and repeated words.
- Preserve meaning while normalizing punctuation.
- Keep interrupted/partial speech flags separate from candidate quality scores.

### Ethics & Compliance

Relevant module:

- `zecpath_hiring.ai.ethics.compliance`

Rules:

- Validate consent before AI screening or automated scoring.
- Remove protected demographic signals from payloads.
- Include explainability notes and retention policy in production reports.
- Route fairness risk flags to manual recruiter review.

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Focused test areas:

- `test_hr_interview.py`: interview phases and state
- `test_follow_up_engine.py`: follow-up stability
- `test_scoring_engine.py`: HR scoring math and anomaly handling
- `test_aptitude_evaluator.py`: aptitude logic and scenario scoring
- `test_hr_interview_simulation.py`: end-to-end simulation
- `test_unified_scoring.py`: cross-round hiring fit
- `test_ethics_compliance.py`: consent, fairness, retention, explainability

## Release Checklist

- All tests pass.
- API docs match current serializers and routes.
- Scoring weights are documented.
- New data fields are included in data-format docs.
- Compliance report is generated for production decision flows.
- AI artifacts include model version and payload traceability.

## Troubleshooting

### `pytest` is not recognized

Use the project virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### `.pytest_cache` permission warning

Tests can still pass. Fix by deleting or changing permissions on `.pytest_cache` if cache persistence is needed.

### API returns `400`

Check required fields for `run_pipeline`:

- `candidate_name`
- `resume_text`
- `job_title`
- `job_description`

### Scores look too high or too low

Check:

- component score ranges
- applied weights
- contradiction penalties
- role-based unified scoring adjustments
- risk flags in unified score and compliance review

### Too many follow-ups

Check:

- answer word count
- vagueness markers
- structure markers
- detail markers
- `max_follow_ups_per_category` in interview state

### Candidate transcript looks noisy

Inspect:

- `raw_text`
- `normalized_text`
- `normalization.partial_answer`
- `normalization.interrupted_speech`
- confidence level

### Compliance status is `action_required`

Check:

- missing consent flags
- removed protected demographic signals
- fairness review risk flags
- retention metadata

## Extension Guide

When adding a new scoring dimension:

1. Create a deterministic evaluator.
2. Add component-level tests.
3. Clamp component scores to `0-100`.
4. Add explainability output.
5. Add unified scoring integration only after the standalone evaluator is stable.
6. Update API, architecture, and data-format documentation.
