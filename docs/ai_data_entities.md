# AI Data Entity Design

## Resume structured schema

```json
{
  "candidate_id": "cand-10001",
  "full_name": "Asha Sharma",
  "contact": {
    "email": "asha@example.com",
    "phone": "+91-9000000000",
    "location": "Bengaluru"
  },
  "summary": "Backend engineer with ATS and NLP experience.",
  "skills": [
    {
      "name": "python",
      "category": "technical",
      "confidence": 0.97
    }
  ],
  "experience": [
    {
      "company": "Acme",
      "title": "Software Engineer",
      "start_date": "2021-01",
      "end_date": "2024-02",
      "duration_months": 37,
      "highlights": ["Built recruitment workflows"]
    }
  ],
  "education": [
    {
      "degree": "B.Tech",
      "field": "Computer Science",
      "institution": "ABC University",
      "graduation_year": 2020
    }
  ],
  "certifications": [
    {
      "name": "AWS Practitioner",
      "issuer": "AWS",
      "year": 2023,
      "relevance": "cloud"
    }
  ],
  "projects": [
    {
      "name": "Hiring Copilot",
      "description": "Built a hiring intelligence dashboard",
      "skills": ["python", "django", "nlp"]
    }
  ]
}
```

## Job description schema

```json
{
  "job_id": "job-9001",
  "title": "AI Hiring Platform Engineer",
  "department": "Product Engineering",
  "experience_required_years": 4,
  "required_skills": ["python", "django", "sql", "nlp"],
  "preferred_skills": ["aws", "docker"],
  "education_preferences": ["Bachelor's degree in CS or related field"],
  "keywords": ["ats", "semantic matching", "recruitment automation"],
  "responsibilities": [
    "Build ATS scoring services",
    "Design interview intelligence systems"
  ],
  "location": "Hybrid"
}
```

## Standard entities

- `Candidate profile`: identity, skills, experience, education, certifications, projects, summaries, section tags.
- `Job profile`: title, role family, experience requirements, required/preferred skills, responsibilities, location, education preferences.
- `Skill object`: normalized name, category, confidence, synonyms, evidence source.
- `Experience object`: company, title, dates, duration, domain, relevance score, gap indicators.

