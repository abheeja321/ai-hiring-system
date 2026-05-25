# Developer Knowledge Transfer (KT) Walkthrough

This document is intended for incoming developers and stakeholders taking ownership of the Zecpath AI Hiring System. It maps the repository structure and explains the core algorithmic flows.

## 1. Directory Structure
```text
zecpath_hiring/
├── ai/                     # CORE: All AI logic lives here
│   ├── ats_engine/         # Calculates skill match and eligibility
│   ├── behavior_ai/        # Analyzes sentiment and soft skills
│   ├── decision_ai/        # Aggregates scores for final HIRE/REJECT
│   ├── integrity/          # Flags PII, fake certs, overlapping dates
│   ├── interview_ai/       # Simulates technical Q&A
│   ├── parsers/            # Converts PDFs/Text to structured JSON
│   └── report_generator/   # Builds the Markdown explainable reports
├── apps/                   # Django Applications
│   ├── core/               # Database models (CandidateProfile, HiringRun)
│   └── dashboard/          # UI logic and routing
├── config/                 # Django settings and root URLs
├── scripts/                # Standalone utilities
│   ├── generate_dentist_demo.py # Run this to seed the local DB
│   └── final_system_validation.py # The stress-testing validation suite
└── templates/              # HTML/CSS Frontend files
```

## 2. Core Code Walkthrough

### The Brain: `pipeline.py`
Located at `zecpath_hiring/ai/ats_engine/pipeline.py`, this is the master orchestrator. 
- It accepts the parsed `candidate` JSON and the `job` JSON.
- It invokes every other module (`run_screening`, `run_interview_intelligence`, etc.) wrapped in robust `try/except` blocks to catch external API timeouts.
- If a sub-module errors, it assigns `"ERROR"` instead of `0.0` to protect the candidate's score.

### The Judge: `service.py` (Decision AI)
Located at `zecpath_hiring/ai/decision_ai/service.py`.
- This file reads the outputs from the pipeline.
- It uses a weighted average (ATS 30%, Interview 35%, etc.).
- **Key Logic**: It calculates standard deviation across scores. If a candidate is amazing at ATS but terrible at Interview, it assigns a "Confidence Penalty". 
- If any module reported an `"ERROR"`, it bypasses hard rejections and forces the decision to `HOLD_REVIEW` with an explanation tag.

### Data Validation: `models.py` (Pydantic)
- We use Pydantic (e.g., `ai/report_generator/models.py`) to enforce strict typing on the LLM outputs. 
- During Day 68, we updated the `ModuleSummary` schema to accept `Union[float, str]` to allow graceful handling of the `"ERROR"` string states without crashing the web app.

## 3. Maintenance & Scaling Notes
- **Scaling**: The pipeline is currently synchronous. To scale to thousands of resumes, wrap `run_hiring_pipeline` in a Celery task.
- **LLM Prompts**: The prompts used for the Technical Interview simulation are located in `ai/interview_ai/prompt_builder.py`. If you need to tune the difficulty of the AI, adjust the system instructions there.
