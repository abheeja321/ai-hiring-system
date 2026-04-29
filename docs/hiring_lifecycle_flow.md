# Hiring Lifecycle Flow Chart

```mermaid
flowchart TD
    A["Job Posting"] --> B["JD Parser AI"]
    B --> C["Structured Job Profile"]
    D["Resume Submission"] --> E["Resume Parser AI"]
    E --> F["Structured Candidate Profile"]
    C --> G["ATS Scoring AI"]
    F --> G
    G --> H["Shortlist / Review / Reject"]
    H --> I["AI Voice Screening"]
    I --> J["HR Interview AI"]
    J --> K["Technical Interview AI"]
    K --> L["Machine Test AI"]
    L --> M["Behavior & Fairness AI"]
    M --> N["Final Decision AI"]
    N --> O["Offer Automation"]
```

## Stage summary

1. Job posting is converted into a normalized requirement object.
2. Resume submission is converted into a structured candidate object.
3. ATS scoring AI ranks candidates with explainable outputs.
4. Screening AI validates communication, intent, and baseline fit.
5. Interview AI manages HR, technical, and machine-test evaluation.
6. Behavior AI adds fairness-aware behavioral interpretation.
7. Decision AI aggregates signals and triggers offer automation.

