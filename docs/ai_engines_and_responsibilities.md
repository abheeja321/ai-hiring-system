# AI Engines and Responsibilities

## Core AI engines

1. `Resume Reader Engine`
   Reads PDF, DOCX, and TXT resumes and extracts raw text for downstream processing.
2. `Resume Parser Engine`
   Cleans text, normalizes sections, and produces structured candidate profiles.
3. `Resume Section Classifier`
   Detects skills, experience, education, certifications, and projects blocks.
4. `Skill Extraction Engine`
   Identifies technical and non-technical skills, synonym variants, and confidence scores.
5. `Experience Parser`
   Extracts companies, titles, durations, and relevance patterns from work history.
6. `Education & Certification Engine`
   Standardizes degree, institution, year, and certification details.
7. `JD Parser Engine`
   Converts raw job descriptions into structured job requirement objects.
8. `Semantic Matching Engine`
   Measures deeper candidate-to-job relevance beyond exact keyword overlap.
9. `ATS Scoring Engine`
   Calculates explainable shortlist scores using weighted hiring dimensions.
10. `Ranking & Shortlisting Engine`
    Converts ATS scores into shortlist, review, and reject bands.
11. `Eligibility Decision Engine`
    Applies ATS cutoffs, mandatory skills, experience, and recruiter rules to decide if AI screening should begin.
12. `Screening AI Service`
    Runs voice-screening and first-round fit analysis from transcript-level signals.
13. `HR Screening Question Engine`
    Builds conversation-ready HR screening question packs by category, answer type, and importance.
14. `HR Interview AI`
    Evaluates behavioral, motivation, policy-fit, and communication responses.
15. `Technical Interview AI`
    Assesses technical depth, problem-solving quality, and role readiness.
16. `Machine Test AI`
    Interprets practical test output and maps results to job requirements.
17. `Behavior Analysis Engine`
    Produces fairness-aware collaboration, consistency, and soft-skill signals.
18. `Decision AI`
    Aggregates all scores into a final recommendation with explainability.
19. `Offer Automation Engine`
    Triggers final workflow readiness once a candidate meets decision thresholds.

## Why AI is required

- It automates repetitive recruiter review work across large applicant volumes.
- It improves speed from resume intake to final decision.
- It enables standardized, fairness-aware evaluation signals.
- It supports scalability through asynchronous service boundaries.
- It strengthens compliance through structured artifacts, audit trails, and model versioning.
