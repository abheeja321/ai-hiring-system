from zecpath_hiring.ai.data.dentist_models import (
    build_dentist_job_profiles,
    dentist_model_to_job_profile,
    get_dentist_model,
    list_dentist_roles,
)


def test_dentist_pdf_models_are_available_as_structured_roles():
    roles = list_dentist_roles()

    assert len(roles) == 81
    assert roles[0]["title"] == "General Dentist"
    assert roles[-1]["title"] == "Teledentistry Consultant"
    assert roles[0]["responsibilities"]
    assert roles[0]["key_skills"]


def test_get_dentist_model_by_id_or_title():
    by_id = get_dentist_model("dentist_001")
    by_title = get_dentist_model("General Dentist")

    assert by_id == by_title


def test_dentist_model_converts_to_standard_job_profile():
    role = get_dentist_model("Cosmetic Dentist")

    profile = dentist_model_to_job_profile(role)

    assert profile["job_id"] == "dentist_003"
    assert profile["department"] == "Dentistry"
    assert "Aesthetic dental design" in profile["required_skills"]
    assert profile["education_preferences"]
    assert profile["responsibilities"]


def test_all_dentist_models_can_be_built_as_job_profiles():
    profiles = build_dentist_job_profiles()

    assert len(profiles) == 81
    assert all(profile["department"] == "Dentistry" for profile in profiles)
