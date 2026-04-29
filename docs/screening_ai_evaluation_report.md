# Screening AI Evaluation Report

## Scope

This report evaluates the current screening subsystem implementation included in the Django project as of April 28, 2026.

## What was evaluated

- transcript normalization behavior
- answer understanding and entity extraction
- per-question screening scoring
- confidence and sentiment analysis
- conversation retries and follow-up logic
- recruiter-facing screening report generation
- edge-case fallback behavior

## Current results

- Automated test status: `15 screening-focused and shared tests passing`
- Django system check: `passing`
- Demo screening output: generated successfully from the current pipeline

## Strengths

- clean modular separation across transcript, understanding, scoring, signals, reporting, and conversation flow
- explainable outputs instead of opaque single-score screening
- recruiter-friendly report structure
- deterministic local behavior for handoff and demo use
- explicit edge-case and retry handling reduces false rejection risk

## Known limitations

- current STT is a simulation scaffold rather than a live speech provider
- intent logic is heuristic and should later be replaced or supplemented with model inference
- sentiment and contradiction detection are rule-based
- multilingual and noisy audio behavior is designed for extension but not benchmarked on a real dataset yet

## Production recommendation

Status: `Ready for controlled integration phase`

Recommended next production steps:

1. plug in a real STT provider and preserve raw audio references
2. run labeled screening-call evaluations against recruiter judgments
3. add async processing, retries, and webhook notifications
4. implement API authentication, rate limiting, and audit logging
5. tune thresholds using real candidate distributions to reduce false rejections

