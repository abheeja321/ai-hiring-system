# Zecpath AI Hiring System

This repository is a single Django project that combines:

- hiring lifecycle management
- ATS parsing and scoring
- screening and interview AI service design
- decision and offer workflow scaffolding
- architecture and data design documents
- HTML pages for demo upload and results
- eligibility decision engine and HR screening dataset
- transcript architecture, STT cleaning, answer understanding, and screening scoring
- confidence signals, screening reports, conversation flow, and edge-case handling
- screening system finalization, API explanation, and evaluation handoff

## Project layout

```text
zecpath_hiring/
  config/              Django settings and routes
  apps/
    core/              DB models for jobs, candidates, runs, artifacts
    dashboard/         Demo UI views and forms
  ai/
    data/              JSON schemas and entity design
    parsers/           Resume and JD parsing engines
    ats_engine/        ATS scoring, ranking, shortlist logic
    screening_ai/      Voice/screening orchestration, HR question bank, contracts
    interview_ai/      HR and technical interview intelligence
    behavior_ai/       Soft-skill and bias/fairness analysis
    decision_ai/       Final decision and offer recommendation
    scoring/           Shared explainable scoring logic
    utils/             Logging and common helpers
  tests/               Unit tests for parsers and scoring
docs/                  Architecture, AI responsibilities, data flow
samples/               Example resume/JD inputs and structured outputs
templates/             Django HTML templates
static/                CSS assets
```

## Setup

1. Create a virtual environment:

```powershell
& "C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
```

2. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run migrations:

```powershell
python manage.py migrate
```

5. Start the server:

```powershell
python manage.py runserver
```

6. Open `http://127.0.0.1:8000/`

## Included deliverables

- Hiring lifecycle flow chart: [docs/hiring_lifecycle_flow.md](docs/hiring_lifecycle_flow.md)
- AI architecture diagram: [docs/ai_architecture.md](docs/ai_architecture.md)
- AI responsibilities overview: [docs/zecpath_ai_responsibilities_overview.md](docs/zecpath_ai_responsibilities_overview.md)
- Data entities and schemas: [docs/ai_data_entities.md](docs/ai_data_entities.md)
- Storage and metadata standards: [docs/storage_and_metadata.md](docs/storage_and_metadata.md)
- Eligibility design: [docs/eligibility_decision_engine.md](docs/eligibility_decision_engine.md)
- HR screening dataset: [docs/hr_screening_dataset.md](docs/hr_screening_dataset.md)
- Transcript architecture: [docs/transcript_data_architecture.md](docs/transcript_data_architecture.md)
- STT cleaning: [docs/speech_to_text_and_cleaning.md](docs/speech_to_text_and_cleaning.md)
- Answer understanding and screening scoring: [docs/answer_understanding_and_screening_scoring.md](docs/answer_understanding_and_screening_scoring.md)
- Confidence and sentiment analysis: [docs/confidence_and_sentiment_analysis.md](docs/confidence_and_sentiment_analysis.md)
- Screening report generator: [docs/ai_screening_report_generator.md](docs/ai_screening_report_generator.md)
- Conversation flow design: [docs/ai_conversation_flow_design.md](docs/ai_conversation_flow_design.md)
- Testing and edge cases: [docs/screening_testing_and_edge_cases.md](docs/screening_testing_and_edge_cases.md)
- Screening finalization: [docs/screening_system_finalization.md](docs/screening_system_finalization.md)
- Screening API explanation: [docs/screening_api_design_explanation.md](docs/screening_api_design_explanation.md)
- Screening AI evaluation report: [docs/screening_ai_evaluation_report.md](docs/screening_ai_evaluation_report.md)

## Notes

- The code uses deterministic placeholder AI engines so the end-to-end flow is demonstrable without calling external models.
- The service boundaries and payload contracts are designed so real LLM, speech, embedding, and ranking models can be plugged in later.
