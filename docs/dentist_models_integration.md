# Dentist Models Integration

## Source

The dentist role dataset was extracted from `Dentist Models.pdf`.

## Output Dataset

Structured JSON:

`samples/dentist_models.json`

The dataset contains 81 dentist role models. Each role includes:

- `id`
- `source_order`
- `title`
- `overview`
- `responsibilities`
- `required_qualifications`
- `key_skills`
- `work_settings`

## Loader Module

Implementation:

`zecpath_hiring.ai.data.dentist_models`

Available helpers:

- `load_dentist_models()`
- `list_dentist_roles()`
- `get_dentist_model(role_id_or_title)`
- `dentist_model_to_job_profile(role)`
- `build_dentist_job_profiles()`

## Standard Job Profile Conversion

Each dentist model can be converted into the project job profile format:

```json
{
  "job_id": "dentist_001",
  "title": "General Dentist",
  "department": "Dentistry",
  "experience_required_years": 2,
  "required_skills": ["Clinical diagnosis", "Manual dexterity"],
  "education_preferences": ["Bachelor of Dental Surgery (BDS)"],
  "responsibilities": [],
  "work_settings": [],
  "overview": "...",
  "source": "Dentist Models.pdf"
}
```

## Usage Example

```python
from zecpath_hiring.ai.data.dentist_models import get_dentist_model, dentist_model_to_job_profile

role = get_dentist_model("General Dentist")
job_profile = dentist_model_to_job_profile(role)
```

The resulting `job_profile` can be passed into ATS, screening, HR interview, and unified scoring flows.
