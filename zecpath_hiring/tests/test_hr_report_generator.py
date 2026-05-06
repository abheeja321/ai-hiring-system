from zecpath_hiring.ai.hr_interview.report_generator import HRInterviewReportGenerator


def test_report_generator_builds_recruiter_ready_summary():
    generator = HRInterviewReportGenerator()

    report = generator.generate_structured_summary(
        {"candidate_id": 7, "full_name": "Asha Rao"},
        {
            "final_score": 82.0,
            "averages": {
                "communication": 85.0,
                "confidence": 78.0,
                "consistency": 88.0,
            },
        },
        [
            {
                "strengths": ["Uses structured examples."],
                "weaknesses": ["Could provide more metrics."],
                "culture_fit_indicators": ["Collaborative team orientation."],
                "risk_flags": [],
            }
        ],
    )

    assert report["candidate"]["name"] == "Asha Rao"
    assert report["candidate_strengths"]
    assert report["weaknesses"] == ["Could provide more metrics."]
    assert "Collaborative team orientation." in report["cultural_fit_indicators"]
    assert "natural_language_report" in report
    assert report["recommendation"] == "Proceed to next round."


def test_report_generator_highlights_inconsistencies():
    generator = HRInterviewReportGenerator()

    report = generator.generate_structured_summary(
        {"candidate_id": 8, "full_name": "Review Candidate"},
        {
            "final_score": 66.0,
            "averages": {
                "communication": 62.0,
                "confidence": 60.0,
                "consistency": 68.0,
            },
        },
        [
            {
                "detected_issues": {"contradiction_penalty": 45.0},
                "risk_flags": ["Problem-solving structure is incomplete."],
            }
        ],
    )

    assert report["inconsistencies"]
    assert "Interview contains inconsistencies requiring clarification." in report["risk_flags"]
    assert report["overall_performance"] == "Needs recruiter review"
