# AI Engine Input / Output Specification

## ATS AI Service

- Receives: candidate profile, job profile, raw resume text, model version, application metadata
- Processes: parsing, section classification, skill extraction, experience analysis, semantic matching, ATS scoring
- Returns: parsed profile, section tags, ATS score, shortlist band, explainability payload
- Flow type: synchronous for small uploads, asynchronous for bulk or heavy parsing

## Screening AI Service

- Receives: ATS output, candidate profile, job profile, voice transcript or audio reference
- Processes: communication analysis, intent detection, screening-fit evaluation
- Returns: screening score, red flags, transcript summary, pass/fail recommendation
- Flow type: asynchronous

## Interview Intelligence Service

- Receives: candidate profile, job profile, screening report, HR transcript, technical transcript, machine-test results
- Processes: behavioral questioning, technical depth analysis, machine test interpretation
- Returns: interview score, per-stage scorecards, strengths, gaps, follow-up prompts
- Flow type: asynchronous

## Behavior Analysis Service

- Receives: interview transcripts, interaction metadata, candidate profile snapshot
- Processes: collaboration cues, stability indicators, fairness and bias controls
- Returns: behavior score, fairness report, normalization notes
- Flow type: asynchronous

## Decision & Scoring Service

- Receives: ATS score, screening report, interview outputs, behavior report, policy thresholds
- Processes: weighted aggregation, decision logic, explanation generation, offer readiness
- Returns: final score, decision label, audit-ready explanation, offer automation flag
- Flow type: synchronous once all prior artifacts exist

## Communication patterns

- REST API for immediate backend-triggered requests
- Queue-based workers for resume parsing, audio analysis, and interview processing
- Webhooks for job completion callbacks
- Shared storage for artifacts, model outputs, and retraining datasets

