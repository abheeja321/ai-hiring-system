# Screening API Design Explanation

## Purpose

The screening subsystem should be consumable by backend services through a small set of stable endpoints and asynchronous event hooks.

## Suggested API surface

### `POST /api/screening/start/`

- Input:
  - `candidate_id`
  - `job_id`
  - `eligibility_status`
  - `question_pack_override` optional
- Output:
  - `screening_session_id`
  - `question_pack`
  - `conversation_flow`

### `POST /api/screening/transcript/`

- Input:
  - `screening_session_id`
  - `question_id`
  - `audio_reference` or `raw_text`
  - `timestamp`
  - `confidence_level`
- Output:
  - `normalized_transcript`
  - `understanding`
  - `signal_analysis`
  - `next_action`

### `POST /api/screening/finalize/`

- Input:
  - `screening_session_id`
  - `all_question_payloads`
- Output:
  - `screening_score`
  - `screening_report`
  - `recommendation`

### `GET /api/screening/report/<screening_session_id>/`

- Output:
  - recruiter-ready screening report JSON

## Synchronous vs asynchronous

- Synchronous:
  - question pack creation
  - transcript normalization
  - per-answer understanding
  - immediate next-action decision
- Asynchronous:
  - provider STT jobs
  - long call artifact persistence
  - bulk evaluation and audit export
  - notification webhooks to recruiter workflows

## Backend integration pattern

- Backend owns candidate/job/session records.
- Screening AI service owns transcript interpretation, signal scoring, and report generation.
- Artifacts are stored with candidate ID, job ID, question ID, timestamp, and model version.
- Frontend receives question-by-question updates and the final report payload from backend APIs.

