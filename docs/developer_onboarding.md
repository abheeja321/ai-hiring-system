# Developer Onboarding Guide

Welcome to the Zecpath AI engineering team! This guide will walk you through setting up your local environment, understanding the repository structure, and running your first AI pipeline.

## 1. Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.10+**
- **Git**
- **SQLite3** (Included with Python) or PostgreSQL if working on production replica
- **PowerShell** or standard terminal

## 2. Environment Setup

### Clone the Repository
```bash
git clone <repository-url>
cd "New folder"
```

### Create and Activate Virtual Environment
```bash
# Using standard venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Database & Migrations

Zecpath uses Django's ORM. Setup your local SQLite database:
```bash
python manage.py makemigrations
python manage.py migrate
```

> [!TIP]
> If you encounter migration issues during onboarding, you can safely delete the local `db.sqlite3` and re-run migrations, assuming you are in a purely local dev environment.

## 4. Environment Variables
Create a `.env` file in the root directory (alongside `manage.py`) with the following keys. Ask your team lead for the development API keys:
```env
DEBUG=True
SECRET_KEY=local-dev-secret-key
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///db.sqlite3
```

## 5. Running the Application

Start the local development server:
```bash
python manage.py runserver
```

You can now access:
- **Web Dashboard**: `http://localhost:8000/`
- **Django Admin**: `http://localhost:8000/admin/`

## 6. Project Structure Overview

```text
zecpath_hiring/
├── ai/                 # Core AI evaluation engines (parsers, ats, screening, etc.)
├── apps/
│   ├── core/           # Main data models (CandidateProfile, HiringRun, AIArtifact)
│   └── dashboard/      # Web UI views and templates
├── config/             # Django settings, URLs, WSGI/ASGI
├── static/             # CSS, JS, Images
└── templates/          # HTML Templates for the Dashboard
```

## 7. Running Tests
We enforce rigorous testing for our AI scoring models to prevent regression.
Run the test suite using `pytest`:
```bash
pytest zecpath_hiring/ai/tests/
```

> [!IMPORTANT]
> Never push code without ensuring all parsing and scoring unit tests pass. Changes to prompt engineering or AI models must be validated against our benchmark datasets.

## 8. Next Steps
- Read the **System Architecture Document** to understand the macro workflow.
- Read the **Zecpath AI Technical Handbook** for details on individual AI engines.
- Explore `zecpath_hiring/ai/ats_engine/pipeline.py` as it acts as the primary orchestrator for the hiring run.
