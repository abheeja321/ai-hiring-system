# Optimization & Stability Report

## Objective

Improve HR interview reliability, scoring consistency, follow-up stability, transcript cleanup, and processing speed.

## Stability updates

- Follow-up decisions now consider answer structure, concrete details, and outcome markers before probing.
- Complete structured answers can be marked sufficient instead of receiving unnecessary follow-ups.
- Vague short answers still trigger clarification, preserving recruiter-quality probing.

## False positive and false negative reduction

- Reduced false positive follow-ups for complete STAR-style answers.
- Reduced false negative clarification by checking both vagueness and lack of concrete detail.
- Added stronger transcript cleanup for filler words, repeated words, broken punctuation, and interrupted speech markers.

## Scoring anomaly fixes

- HR interview scoring now clamps all component scores to `0-100`.
- Contradiction penalties are clamped before consistency calculation.
- Weight totals are normalized before final score calculation, preventing scores above 100 when optional aptitude weights are enabled.
- Applied weights are returned with score output for auditability.

## Processing speed improvements

- Follow-up logic remains deterministic and regex-light.
- Transcript cleanup uses compiled-style simple regex passes and avoids external dependencies.
- Scoring normalization is in-memory and does not add model calls.

## Recommended next refinements

- Add production logs that track follow-up type distribution by interview category.
- Compare follow-up decisions against recruiter labels to tune thresholds.
- Track transcript cleanup confidence separately from candidate quality to avoid penalizing noisy audio as weak performance.
- Add batch-level score drift monitoring for HR score, unified score, and manual reviewer deltas.

Implementation touches:

- `zecpath_hiring.ai.hr_interview.follow_up_engine`
- `zecpath_hiring.ai.hr_interview.scoring_engine`
- `zecpath_hiring.ai.screening_ai.transcript_processing`
