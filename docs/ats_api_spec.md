# ATS API Specification

## Endpoints

### `POST /api/ats/upload-resume/`

- Purpose: upload resume and candidate metadata
- Response: accepted application ID and parsing job ID

### `POST /api/ats/parse-jd/`

- Purpose: convert raw job description into structured job profile
- Response: normalized job profile JSON

### `POST /api/ats/score/`

- Purpose: score one candidate against one job
- Response: ATS score, score breakdown, shortlist band

### `POST /api/ats/shortlist/`

- Purpose: rank a candidate batch for a job
- Response: ordered candidates with reject/review/shortlist zones

## Error standard

```json
{
  "error": {
    "code": "INVALID_PAYLOAD",
    "message": "required_skills field is missing",
    "correlation_id": "corr-12345"
  }
}
```

## Logging standard

- log request ID
- log candidate ID and job ID
- log model version
- log stage start and completion
- log confidence and fallback path when heuristics are used

