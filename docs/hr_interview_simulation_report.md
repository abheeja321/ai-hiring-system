# HR Interview Simulation Report

## Objective

Test the full HR interview system end-to-end using controlled candidate simulations and compare AI outputs against manual evaluator benchmarks.

## Candidate types tested

- **Confident**: direct, structured, evidence-backed answers.
- **Hesitant**: uncertainty phrases, shorter answers, weaker confidence signals.
- **Inexperienced**: coachable but limited workplace context.
- **Overqualified**: strong reasoning and communication with possible role-fit or retention risk.

## End-to-end simulation flow

1. Generate reasoning and situational judgment questions.
2. Feed scripted candidate answers into the aptitude evaluator.
3. Convert aptitude, relevance, communication, confidence, and consistency signals into an HR score.
4. Generate recruiter-ready summaries for each simulated session.
5. Compare AI score against manual evaluator benchmark.
6. Flag score gaps and candidate-type-specific scoring inconsistencies.

## Accuracy evaluation

The simulation report emits:

- AI score
- manual benchmark score
- score delta
- mean absolute error across all sessions
- within-10-points accuracy rate
- largest AI/manual gap

## Scoring inconsistency checks

The simulation flags:

- AI/manual score gap above review threshold
- overqualified candidates receiving high scores while role-fit risk is underweighted
- hesitant candidates being over-penalized for nervousness instead of reasoning quality

## Improvement recommendations

- Calibrate scoring weights against manual evaluator benchmarks after each simulation batch.
- Track candidate type separately instead of treating all risk as a generic weakness.
- Separate nervousness penalties from reasoning quality.
- Add a dedicated role-fit and retention-risk modifier for overqualified candidates.
- Review high score deltas before deploying scoring changes to recruiters.

Implementation lives in `zecpath_hiring.ai.hr_interview.simulation`.
