# AI System Architecture Diagram

```mermaid
flowchart LR
    FE["Frontend (Django Templates / Admin)"] --> BE["Backend (Django Views / ORM / APIs)"]
    BE --> ATS["ATS AI Service"]
    BE --> SCR["Screening AI Service"]
    BE --> INT["Interview Intelligence Service"]
    BE --> BEH["Behavior Analysis Service"]
    BE --> DEC["Decision & Scoring Service"]
    ATS --> STORE["AI Storage / Artifacts / Model Registry"]
    SCR --> STORE
    INT --> STORE
    BEH --> STORE
    DEC --> STORE
    ATS --> MQ["Queues / Async Workers"]
    SCR --> MQ
    INT --> MQ
    MQ --> WH["Webhooks / Event Callbacks"]
    WH --> BE
```

## Service model

- `ATS AI Service`: resume parsing, section detection, skill extraction, semantic matching, ATS score generation.
- `Screening AI Service`: voice screening, transcript analysis, fit validation, communication scoring.
- `Interview Intelligence Service`: HR interview AI, technical interview AI, machine test AI, transcript summaries.
- `Behavior Analysis Service`: behavioral pattern signals, fairness checks, bias reduction controls.
- `Decision & Scoring Service`: weighted aggregation, explainability, final decision, offer-readiness.

## Sync vs async

- Synchronous:
  - JD normalization
  - resume upload acknowledgement
  - quick ATS parsing previews
- Asynchronous:
  - large-document parsing
  - voice analysis
  - interview transcript processing
  - ranking recalculation for bulk applicants
  - retraining dataset creation

## Communication

- REST APIs for immediate request/response actions
- Queues for heavy or long-running AI tasks
- Webhooks for completion callbacks to backend workflows
- Versioned model registry references in every AI payload

