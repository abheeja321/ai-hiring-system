# AI Ethics & Compliance Review

## Objective

Ensure the HR AI system aligns with ethical AI standards, candidate consent expectations, fair scoring practice, explainability, and data retention readiness.

## Consent requirements

Before AI screening or interview scoring begins, the system must capture:

- AI screening consent
- transcript processing consent
- automated scoring notice acknowledgement
- data retention notice acknowledgement

If any consent flag is missing, the compliance status is `action_required`.

## Protected demographic signal policy

Protected or sensitive demographic attributes must not be used for scoring, ranking, or automated recommendations.

Removed signals include:

- age or date of birth
- gender or sex
- race or ethnicity
- religion or caste
- marital status or pregnancy
- disability
- nationality or citizenship
- candidate photos

The compliance helper recursively removes these fields from candidate payloads before fairness review.

## Fairness review notes

The scoring system should use only job-related criteria:

- resume/job skill alignment
- relevant experience
- screening answer quality
- HR interview communication and clarity
- consistency and role alignment
- aptitude reasoning and situational judgment

Fairness review is required when:

- cross-round score spread is large
- unified scoring already has risk flags
- protected signals were present and removed
- consent is incomplete

## Explainability notes

Recruiter explanations should include:

- input scores
- applied weights
- weighted contributions
- decision band
- recommendation
- risk flags

Candidate-facing explanations should be concise and tied to job-related criteria. The AI score is a decision-support signal, not a final employment decision.

## Data retention readiness

Default retention policy:

- raw resume: 180 days
- transcript: 90 days
- scorecard: 365 days
- audit log: 730 days
- training snapshot: 365 days

Every generated report includes delete-after dates for each artifact category.

## Compliance readiness report

The report includes:

- consent validation
- protected signal removal summary
- fairness review notes
- explainability notes
- retention policy
- blocking compliance items
- readiness status

Implementation lives in `zecpath_hiring.ai.ethics.compliance`.
