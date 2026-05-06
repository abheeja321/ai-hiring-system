from zecpath_hiring.ai.ethics.compliance import EthicsComplianceReviewer


def test_consent_validation_requires_all_notices():
    reviewer = EthicsComplianceReviewer()

    result = reviewer.validate_consent(
        {
            "ai_screening_consent": True,
            "transcript_processing_consent": True,
        }
    )

    assert result["consent_valid"] is False
    assert "automated_scoring_notice" in result["missing_consent"]
    assert "data_retention_notice" in result["missing_consent"]


def test_protected_demographic_signals_are_removed_recursively():
    reviewer = EthicsComplianceReviewer()

    result = reviewer.remove_demographic_bias_signals(
        {
            "candidate_id": 1,
            "full_name": "Candidate",
            "gender": "female",
            "contact": {"email": "c@example.com", "age": 29},
            "experience": [{"company": "Acme", "nationality": "example"}],
        }
    )

    assert "gender" not in result["sanitized_payload"]
    assert "age" not in result["sanitized_payload"]["contact"]
    assert "nationality" not in result["sanitized_payload"]["experience"][0]
    assert result["removed_protected_signals"] == ["age", "gender", "nationality"]


def test_compliance_report_flags_missing_consent_and_fairness_review():
    reviewer = EthicsComplianceReviewer()

    report = reviewer.build_compliance_readiness_report(
        {"candidate_id": "eth-1", "gender": "male"},
        {
            "input_scores": {"ats_score": 95.0, "screening_score": 55.0, "hr_interview_score": 58.0},
            "risk_flags": ["Cross-round scores are inconsistent and need recruiter review."],
            "applied_weights": {"ats_weight": 0.35, "screening_weight": 0.25, "hr_interview_weight": 0.40},
        },
        {"ai_screening_consent": True},
    )

    assert report["compliance_status"] == "action_required"
    assert "Missing required consent." in report["blocking_items"]
    assert report["fairness_review"]["fairness_review_status"] == "review_required"
    assert report["explainability"]["explainability_available"] is True


def test_retention_policy_contains_delete_dates():
    reviewer = EthicsComplianceReviewer()

    policy = reviewer.build_retention_policy()

    assert policy["transcript"]["retention_days"] == 90
    assert "delete_after" in policy["scorecard"]
