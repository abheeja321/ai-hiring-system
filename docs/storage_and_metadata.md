# Storage Structure Documentation and Metadata Standards

## Data flow

```mermaid
flowchart LR
    U["Upload"] --> R["Raw Storage"]
    R --> P["Parsed Profiles"]
    P --> S["ATS Scores"]
    S --> C["Screening Reports"]
    C --> I["Interview Results"]
    I --> D["Decision Outputs"]
    D --> T["Training / Versioned Datasets"]
```

## Storage formats

- `resumes/raw/`: source PDF, DOCX, TXT
- `profiles/candidates/`: parsed candidate JSON
- `profiles/jobs/`: parsed job JSON
- `scores/ats/`: ATS scorecards and shortlist explanations
- `screening/`: transcript summaries and screening scores
- `interviews/`: HR, technical, machine-test outputs
- `decisions/`: final recommendations and offer triggers
- `datasets/`: curated training and retraining snapshots

## Metadata standards

- `candidate_id`
- `job_id`
- `application_id`
- `artifact_type`
- `model_name`
- `model_version`
- `pipeline_stage`
- `created_at`
- `updated_at`
- `requested_by`
- `correlation_id`

## Versioning rules

- Every artifact stores the model version that produced it.
- Parsed profiles are immutable snapshots once used for a scoring decision.
- Retraining data is exported into versioned dataset batches.
- Async jobs publish a correlation ID for webhook reconciliation.

