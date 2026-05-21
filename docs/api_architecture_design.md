# AI API Architecture & Integration Mapping

This document outlines the systematic refactoring of the monolithic Zecpath AI Pipeline into distinct, scalable micro-APIs. It defines the schemas, processing patterns (async vs sync), database interactions, and security requirements necessary to scale the platform.

---

## 1. API Catalog & JSON Schemas

The monolithic `run_pipeline` endpoint will be decomposed into five specialized APIs.

### A. Resume Parsing API
*   **Endpoint**: `POST /api/v1/ai/parse-resume/`
*   **Purpose**: Extracts structured data (skills, experience, education) from raw text or PDF uploads.
*   **Request Schema**:
    ```json
    {
      "candidate_name": "string",
      "resume_text": "string" 
    }
    ```
*   **Response Schema**:
    ```json
    {
      "candidate_id": "uuid",
      "structured_profile": {
        "skills": [{"name": "string", "category": "string", "confidence": "float"}],
        "experience": [],
        "education": []
      }
    }
    ```

### B. ATS Scoring API
*   **Endpoint**: `POST /api/v1/ai/ats-score/`
*   **Purpose**: Compares a `structured_profile` against a Job Profile to determine baseline eligibility.
*   **Request Schema**:
    ```json
    {
      "candidate_id": "uuid",
      "job_id": "uuid"
    }
    ```
*   **Response Schema**:
    ```json
    {
      "final_score": "float",
      "shortlist_band": "string",
      "match_details": {"skills_match": "float", "experience_match": "float"}
    }
    ```

### C. Screening AI API
*   **Endpoint**: `POST /api/v1/ai/screen/`
*   **Purpose**: Generates dynamic screening questions based on ATS gaps and evaluates candidate answers.
*   **Request Schema**:
    ```json
    {
      "candidate_id": "uuid",
      "job_id": "uuid",
      "interaction_log": [{"question": "string", "answer": "string"}]
    }
    ```
*   **Response Schema**:
    ```json
    {
      "screening_score": "float",
      "flags": ["string"],
      "recommended_next_step": "string"
    }
    ```

### D. Interview AI API
*   **Endpoint**: `POST /api/v1/ai/interview/`
*   **Purpose**: Real-time evaluation of technical or behavioral questions.
*   **Request Schema**:
    ```json
    {
      "candidate_id": "uuid",
      "current_phase": "string",
      "question_id": "string",
      "candidate_audio_transcript": "string"
    }
    ```
*   **Response Schema**:
    ```json
    {
      "interview_score": "float",
      "follow_up_generated": "string",
      "is_phase_complete": "boolean"
    }
    ```

### E. Decision AI API
*   **Endpoint**: `POST /api/v1/ai/decision/`
*   **Purpose**: Aggregates all scores across pipeline stages to output the final hiring recommendation.
*   **Request Schema**:
    ```json
    {
      "hiring_run_id": "uuid"
    }
    ```
*   **Response Schema**:
    ```json
    {
      "decision": "string (SELECTED, HOLD_REVIEW, REJECTED)",
      "confidence_score": "float",
      "explanation": "string"
    }
    ```

---

## 2. Backend → AI → Database Interaction Flow

The interaction between the Django Viewsets, the Python AI modules, and the PostgreSQL database follows this unified lifecycle:

1.  **Ingestion**: Frontend sends raw data to `Django ViewSet`. ViewSet creates a `CandidateProfile` record.
2.  **Dispatch**: The ViewSet calls the respective AI Engine (e.g., `ResumeParser` or `DecisionEngine`).
3.  **Processing**: AI Engine queries external LLMs (if required) or processes heuristic logic locally.
4.  **Storage**: 
    - The AI returns a JSON payload.
    - Django saves this payload into the `AIArtifact` table (with encryption flags enabled for compliance).
    - If the step concludes the pipeline, the `HiringRun` table is updated with final scores.
5.  **Audit**: Django fires a signal to generate an `AIAuditLog` record, tracking the exact `model_version` and timestamp for regulatory compliance.

---

## 3. Sync vs Async Processing Design

To handle high concurrency and prevent HTTP timeout errors, the APIs are split into synchronous and asynchronous execution paths.

### Asynchronous Workloads (Celery + Redis/RabbitMQ)
Tasks that take `> 1.0 seconds` or involve heavy file parsing and batch LLM calls must be asynchronous.
*   **Target APIs**: *Resume Parsing API*, *ATS Scoring API*, *Decision AI API* (Report Generation).
*   **Flow**:
    1. Client calls `POST /api/v1/ai/parse-resume/`.
    2. API returns `202 Accepted` with a `{"task_id": "uuid"}` immediately.
    3. Client polls `GET /api/v1/tasks/{task_id}/` (or listens via WebSockets) until status is `COMPLETED`.

### Synchronous Workloads (Real-Time HTTP/WebSockets)
Tasks requiring low-latency conversational feedback must be synchronous.
*   **Target APIs**: *Screening AI API*, *Interview AI API*.
*   **Flow**:
    1. Client submits transcript chunks.
    2. API immediately queries the AI (cached heuristic evaluating or fast-inference Groq API).
    3. API returns the `follow_up_generated` string directly in the HTTP `200 OK` response within `< 500ms`.

---

## 4. Error Handling & Retry Mechanisms

### Standardized HTTP Error Codes
*   `400 Bad Request`: Schema validation failed (e.g., missing `candidate_id`).
*   `422 Unprocessable Entity`: AI failed to parse the text due to gibberish or unsupported language.
*   `429 Too Many Requests`: Client exceeded rate limits for the Interview API.
*   `500 Internal Server Error`: Backend crash.
*   `503 Service Unavailable`: External LLM provider (e.g., OpenAI/Gemini) is down.

### Retry Queues & Backoff Strategy
For Asynchronous Celery tasks, interactions with external LLMs must implement exponential backoff to handle rate limits (`HTTP 429`):
*   **Attempt 1**: Immediate execution.
*   **Attempt 2**: Wait 2 seconds.
*   **Attempt 3**: Wait 4 seconds.
*   **Failure Protocol**: If Attempt 3 fails, write an `error` payload to the `AIArtifact`, set the task state to `FAILED`, and log to `AIAuditLog`.

---

## 5. API Authentication & Security

### JSON Web Tokens (JWT)
All requests to the AI APIs require a valid `Bearer <Token>` passed in the `Authorization` header, leveraging `djangorestframework-simplejwt`. 
*   **Access Token**: Short-lived (15 minutes).
*   **Refresh Token**: 7 days, securely stored in HTTP-only cookies.

### Role-Based Access Control (RBAC)
We utilize `DjangoModelPermissions` combined with custom logic to enforce data silos:
*   `Candidate`: Can only access the *Interview AI API* endpoints linked to their specific `interview_session_token`.
*   `Recruiter`: Can trigger the *Decision AI API* and view `AIArtifact` payloads.
*   `System Admin`: Has global access to view raw `AIAuditLog` events.
