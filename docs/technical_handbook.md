# Zecpath AI Technical Handbook

This master handbook serves as the definitive reference for the Zecpath AI Hiring System, detailing its architecture, APIs, data models, and specialized AI sub-modules.

---

## 1. System Architecture

The system operates on a Django backend, orchestrating multiple decoupled AI engines.
Please refer to the detailed [System Architecture Document](file:///c:/Users/admin/.gemini/antigravity/brain/78c12080-b9f4-4af4-9824-321a11093484/system_architecture_doc.md) for a comprehensive visual layout and data flow pipeline.

---

## 2. API Reference

### Internal Subsystem APIs
Each AI module exposes a clean, synchronous Python function interface that the Django orchestrator calls.

#### Core Pipeline Execution
```python
from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline

# Executes the full suite of parsing and scoring engines
result = run_hiring_pipeline(structured_resume, structured_job)
```

#### Parsers
```python
# Converts raw string representations into structured JSON
def parse_resume_text(name: str, text: str) -> dict: ...
def parse_job_description(title: str, description: str) -> dict: ...
```

#### Module APIs
Each module accepts the structured `resume` and `job_description` and returns a dictionary with a calculated score and detailed explanation logic.
```python
def run_ats_scoring(resume: dict, jd: dict) -> dict: ...
def run_screening_scoring(resume: dict, jd: dict) -> dict: ...
def run_behavior_scoring(resume: dict) -> dict: ...
def run_technical_interview(resume: dict, jd: dict) -> dict: ...
```

### External REST API
- `POST /api/v1/runs/run_pipeline/`
  - **Payload**: JSON containing raw `candidate_name`, `resume_file`, `job_title`, and `job_description`.
  - **Response**: The complete `HiringRun` payload including the final decision and individual module scores.

---

## 3. Data Models

The system ensures robust data retention, auditing, and observability.

- **`CandidateProfile`**: Contains candidate demographic data, raw resume text, and the parsed `structured_profile` JSON. Includes fields for GDPR/consent compliance.
- **`JobProfile`**: Stores the `raw_description` and the extracted `structured_profile` (required skills, bounds, responsibilities).
- **`HiringRun`**: The transaction record bridging a candidate to a job. It stores discrete scores: `ats_score`, `screening_score`, `interview_score`, `behavior_score`, and the `final_score` (0-100), along with the `decision` string.
- **`AIArtifact`**: A critical model for observability and compliance. Every interaction with an LLM is logged here along with the `model_version`, prompt `payload`, and the candidate/job context.
- **`AIAuditLog`**: Maintains a chronological ledger of system actions to ensure hiring processes are transparent and explainable.

---

## 4. Scoring Logic & AI Modules Explained

### 4.1 Parsers Module (`ai.parsers`)
**Purpose**: Transforms unstructured text into standardized JSON schemas.
**Logic**: Utilizes LLM structural extraction (e.g., matching a Pydantic schema) to map paragraphs into arrays of skills, education objects (with start/end dates), and work experience nodes.

### 4.2 ATS Engine (`ai.ats_engine`)
**Purpose**: Baseline deterministic skills matching.
**Logic**: Compares the `skills` array from the `structured_profile` of the resume against the `required_skills` of the job description. Calculates a percentage overlap score.

### 4.3 Screening AI (`ai.screening_ai`)
**Purpose**: Eligibility filtering.
**Logic**: Analyzes hard constraints like "Requires 5 years of experience" or "Must be located in New York". Employs semantic analysis to infer equivalent experience (e.g., "Software Engineer" = "Backend Developer").

### 4.4 Machine Test AI / Technical (`ai.machine_test`, `ai.technical_interview`)
**Purpose**: In-depth technical aptitude.
**Logic**: Evaluates specific technical depth by comparing the complexity of projects listed in the resume to the requirements of the JD. May also parse code submission snapshots to assess algorithmic correctness, code quality, and computational complexity (Big O).

### 4.5 Behavior AI (`ai.behavior_ai`, `ai.hr_interview`)
**Purpose**: Assesses soft skills and cultural fit.
**Logic**: Uses sentiment and semantic analysis on the resume's summary and project descriptions to identify traits like leadership, communication, and problem-solving initiative. Assigns a behavioral score index.

### 4.6 Decision AI (`ai.decision_ai`)
**Purpose**: The final aggregator.
**Logic**: 
1. Normalizes all sub-module scores.
2. Applies weighted averages based on the role profile (e.g., technical roles heavily weight the Technical AI score).
3. If critical thresholds fail (e.g., ATS < 40%), issues an auto `REJECT`.
4. Outputs the final integer score and a categoric decision: `HIRE`, `REVIEW`, or `REJECT`.

---

## 5. Deployment Guide

### Application Deployment
The Zecpath backend is a standard WSGI/ASGI Python application.
1. **Infrastructure**: Deploy using Docker on AWS ECS or Heroku.
2. **Server**: Run via Gunicorn for WSGI traffic.
   ```bash
   gunicorn zecpath_hiring.config.wsgi:application --bind 0.0.0.0:8000
   ```
3. **Database**: Use PostgreSQL (Neon or RDS). Update the `DATABASES` dict in `settings.py`.
4. **Static Files**: Run `python manage.py collectstatic` and host using AWS S3 or WhiteNoise.

### Observability & Monitoring
- **Logging**: The system uses JSON-structured logs (`python-json-logger`) for all AI module outputs, enabling easy ingestion into Datadog, ELK, or CloudWatch.
- **Auditing**: Routine jobs should back up the `AIAuditLog` table to cold storage for compliance retention policies.

---
*For further details on getting started, refer to the [Developer Onboarding Guide](file:///c:/Users/admin/.gemini/antigravity/brain/78c12080-b9f4-4af4-9824-321a11093484/developer_onboarding.md).*
