import json
from pathlib import Path
from typing import Any, Dict, List


DATASET_PATH = Path(__file__).resolve().parents[3] / "samples" / "dentist_models.json"


def load_dentist_models(dataset_path: Path | None = None) -> Dict[str, Any]:
    """
    Load dentist role models extracted from the source PDF.
    """
    path = dataset_path or DATASET_PATH
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_dentist_roles(dataset_path: Path | None = None) -> List[Dict[str, Any]]:
    return load_dentist_models(dataset_path)["roles"]


def get_dentist_model(role_id_or_title: str, dataset_path: Path | None = None) -> Dict[str, Any]:
    lookup = role_id_or_title.strip().lower()
    for role in list_dentist_roles(dataset_path):
        if role["id"].lower() == lookup or role["title"].lower() == lookup:
            return role
    raise ValueError(f"Dentist model not found: {role_id_or_title}")


def dentist_model_to_job_profile(role: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a dentist role model into the standard job profile format used by the hiring pipeline.
    """
    title = role["title"]
    skills = role.get("key_skills", [])
    qualifications = role.get("required_qualifications", [])
    responsibilities = role.get("responsibilities", [])
    settings = role.get("work_settings", [])
    return {
        "job_id": role["id"],
        "title": title,
        "department": "Dentistry",
        "experience_required_years": _infer_experience_years(qualifications),
        "required_skills": skills,
        "preferred_skills": [],
        "education_preferences": qualifications,
        "keywords": _dedupe(skills + responsibilities + settings),
        "responsibilities": responsibilities,
        "location": "Flexible",
        "work_settings": settings,
        "overview": role.get("overview", ""),
        "source": "Dentist Models.pdf",
    }


def build_dentist_job_profiles(dataset_path: Path | None = None) -> List[Dict[str, Any]]:
    return [dentist_model_to_job_profile(role) for role in list_dentist_roles(dataset_path)]


def _infer_experience_years(qualifications: List[str]) -> int:
    text = " ".join(qualifications).lower()
    if "experienced" in text or "experience" in text:
        return 2
    return 0


def _dedupe(items: List[str]) -> List[str]:
    return list(dict.fromkeys(item for item in items if item))
