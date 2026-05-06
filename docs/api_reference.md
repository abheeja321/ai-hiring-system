# HR AI API Specification

## Base URL

`/api/v1/`

## Authentication

Development currently uses Django/DRF defaults. Before production integration, configure token, JWT, or service-to-service authentication in Django REST Framework.

## Content Type

Requests and responses use JSON unless the dashboard upload flow is used.

## Endpoints

### Jobs

#### `GET /api/v1/jobs/`

List job profiles.

#### `POST /api/v1/jobs/`

Create a job profile.

```json
{
  "title": "Backend Engineer",
  "department": "Engineering",
  "raw_description": "Need Python, Django, SQL, APIs...",
  "structured_profile": {}
}
```

#### `GET /api/v1/jobs/{id}/`

Retrieve one job profile.

#### `PUT/PATCH /api/v1/jobs/{id}/`

Update a job profile.

#### `DELETE /api/v1/jobs/{id}/`

Delete a job profile.

### Candidates

#### `GET /api/v1/candidates/`

List candidate profiles.

#### `POST /api/v1/candidates/`

Create a candidate profile.

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "raw_resume": "Experienced Python engineer...",
  "structured_profile": {}
}
```

#### `GET /api/v1/candidates/{id}/`

Retrieve one candidate profile.

### Hiring Runs

#### `GET /api/v1/runs/`

List historical hiring runs.

#### `GET /api/v1/runs/{id}/`

Retrieve a hiring run and its stored explanation payload.

#### `POST /api/v1/runs/run_pipeline/`

Primary integration endpoint. Parses the candidate resume and job description, runs the hiring pipeline, stores profiles, stores the hiring run, and saves an AI artifact.

Request:

```json
{
  "candidate_name": "Jane Doe",
  "resume_text": "Experienced Software Engineer with Python, Django, SQL...",
  "job_title": "Backend Engineer",
  "job_description": "Need 3+ years with Python, Django, SQL and communication."
}
```

Response:

```json
{
  "id": 101,
  "candidate": 50,
  "job": 20,
  "ats_score": 85.5,
  "screening_score": 90.0,
  "interview_score": 80.0,
  "behavior_score": 88.0,
  "final_score": 86.5,
  "decision": "OFFER",
  "explanation": {
    "ats": {},
    "screening": {},
    "interview": {},
    "behavior": {},
    "decision": {}
  },
  "created_at": "2026-05-05T10:00:00Z"
}
```

Validation errors return `400 Bad Request`.

### AI Artifacts

#### `GET /api/v1/artifacts/`

List stored AI artifacts. Artifacts are read-only and should be used for debugging, audit review, and model/version traceability.

#### `GET /api/v1/artifacts/{id}/`

Retrieve one artifact payload.

### Screening Interactions

#### `GET /api/v1/interactions/`

List screening interactions, transcript text, normalized text, confidence level, and scoring payloads.

#### `GET /api/v1/interactions/{id}/`

Retrieve one interaction.

## Dashboard Routes

- `GET /`: demo dashboard home
- `POST /run-demo/`: upload resume and run demo pipeline
- `GET /jobs/`: dashboard job search
- `GET /jobs/{id}/`: dashboard job detail

## Data Formats

### Candidate Profile

```json
{
  "candidate_id": "string",
  "full_name": "string",
  "contact": {"email": "string", "phone": "string", "location": "string"},
  "skills": [{"name": "Python", "category": "technical", "confidence": 0.9}],
  "experience": [{"company": "Acme", "title": "Engineer", "duration_months": 36}],
  "education": [{"degree": "B.Tech", "field": "Computer Science"}],
  "projects": []
}
```

### Job Profile

```json
{
  "job_id": "string",
  "title": "Backend Engineer",
  "department": "Engineering",
  "experience_required_years": 3,
  "required_skills": ["Python", "Django", "SQL"],
  "preferred_skills": ["REST", "AWS"],
  "location": "Bengaluru"
}
```

### Unified Candidate Score

```json
{
  "candidate_id": "string",
  "role_type": "Technical",
  "hiring_fit_percentage": 82.4,
  "decision_band": "Hire",
  "recommendation": "Advance with recruiter validation.",
  "input_scores": {
    "ats_score": 84.0,
    "screening_score": 78.0,
    "hr_interview_score": 86.0
  },
  "applied_weights": {
    "ats_weight": 0.40,
    "screening_weight": 0.20,
    "hr_interview_weight": 0.40
  },
  "risk_flags": []
}
```

## Error Handling

- `400`: invalid payload or missing required fields
- `401/403`: authentication or authorization failure once production auth is enabled
- `404`: resource not found
- `500`: unexpected server error; inspect Django logs and AI artifact payloads

## Integration Notes

- Use `POST /api/v1/runs/run_pipeline/` for first integration.
- Persist external IDs in profile metadata if connecting to an ATS.
- Do not send protected demographic attributes for scoring.
- Call ethics/compliance review before showing final recommendations in production workflows.
