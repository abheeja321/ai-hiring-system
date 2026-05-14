# AI Compliance Design & Governance Framework

This document outlines the security, audit, and compliance infrastructure for the Zecpath AI Hiring System to ensure ethical, transparent, and legally sound AI operations (aligning with GDPR, CCPA, and general AI safety standards).

## 1. Audit Trail System
To maintain a high level of transparency, an immutable audit trail (`AIAuditLog`) captures all key interactions and automated decisions made by the AI.

- **Score Logs**: All generated scores (ATS, Screening, Technical Interview) are stored alongside the models that generated them, including the `model_version`.
- **Decision Logs**: When the AI outputs a recommendation (e.g., "Hire", "Reject", "Hold"), it triggers an audit log storing the `run_id`, the decision `action`, the associated `actor` (system vs human override), and a timestamp.

## 2. Data Retention & Consent Policies
Candidate privacy is paramount.
- **Consent Tracking**: The `CandidateProfile` captures `consent_given` and the exact `consent_timestamp`. If consent is revoked or expires, automated cleanup tasks must handle redaction.
- **Data Retention Policies**: A `data_retention_date` is enforced on all candidate records. Personal Identifiable Information (PII) and AI artifacts must be purged or heavily anonymized once this retention period lapses.

## 3. Secure Storage
- **Transcripts & Reports**: Interview transcripts (`ScreeningInteraction`) and detailed generated reports (`AIArtifact`) often contain sensitive candidate information. 
- **Encryption**: These models feature `is_encrypted` flags and store an `encryption_key_id`. This allows the application layer to encrypt the data at rest using a KMS (Key Management Service) provider before persisting to the database.

## 4. Access Control Logic
- **API Security**: The Django backend is secured using `IsAuthenticated` and `DjangoModelPermissions`.
- **RBAC (Role-Based Access Control)**: Only authorized personnel (HR Admins, Interviewers) can invoke AI processing pipelines or access candidate transcripts. Unauthenticated requests strictly receive `403 Forbidden` or `401 Unauthorized`.
