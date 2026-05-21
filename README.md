# Zecpath AI Hiring System

Welcome to the **Zecpath AI Hiring System**, an autonomous, end-to-end recruitment platform designed to eliminate hiring bias, reduce manual screening by 80%, and automate technical and behavioral candidate evaluations.

This project was developed as a comprehensive solution for modern HR teams, transforming unstructured candidate data into actionable, explainable intelligence.

---

## 🚀 Features

- **Semantic ATS Engine**: Moves beyond legacy keyword matching by using contextual NLP to evaluate a candidate's skills and experience against a job description.
- **Automated Eligibility Screening**: Instantly gates candidates based on hard constraints (e.g., minimum experience, mandatory degrees, location).
- **Simulated Technical & Behavioral Interviews**: Dynamically generates and evaluates candidate responses based on their specific background, yielding a measurable competency score.
- **Fairness & Integrity AI**: Strips Personally Identifiable Information (PII) to prevent bias and scans for anomalies (e.g., fake certifications, overlapping timelines).
- **Human-in-the-Loop AI**: Generates beautiful, explainable Markdown Intelligence Reports. Rather than failing silently, if an AI module encounters an error, the candidate is gracefully assigned a `HOLD_REVIEW` status.

---

## 🏗️ System Architecture

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **AI/NLP**: Pydantic for strict schema validation, simulated LLM integration endpoints.
- **Frontend**: Django Templates with custom HTML/CSS (Glassmorphism & modern UI).

---

## 💻 Setup Instructions

Follow these steps to run the Zecpath AI system locally.

### 1. Clone the Repository
```bash
git clone https://github.com/abheeja321/ai-hiring-system.git
cd ai-hiring-system
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
Initialize the local SQLite database and apply all Django models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Generate Demo Dataset
We have included a script that populates the database with a realistic "Dentist" hiring scenario, including Job Profiles, Candidate Resumes, and AI Pipeline Outputs:
```bash
python zecpath_hiring/scripts/generate_dentist_demo.py
```
*Note: A static representation of this dataset is also available in the `dental_hiring_demo/` folder.*

### 6. Run the Server
```bash
python manage.py runserver
```
Navigate to `http://localhost:8000` to view the Recruiter Dashboard.

---

## 🧪 Validating the Pipeline

To run a stress test ensuring all AI modules handle edge cases (missing data, malformed JSON, etc.) without crashing:
```bash
python zecpath_hiring/scripts/final_system_validation.py
```

---

## 🤝 Contributing & Review
All core pipeline logic can be found under `zecpath_hiring/ai/`. 
For a deep dive into the scoring logic, refer to the `docs/` directory which contains the Technical Handbook and Architecture Designs.
