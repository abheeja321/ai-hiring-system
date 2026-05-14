from zecpath_hiring.ai.hr_interview.simulation import HRInterviewSimulationRunner


def test_simulation_runs_all_candidate_types():
    runner = HRInterviewSimulationRunner()

    report = runner.run_simulations()

    assert report["report_id"] == "hr-simulation-day-45-final"
    assert report["candidate_types_tested"] == ["Confident", "Hesitant", "Inexperienced", "Overqualified"]
    assert len(report["sessions"]) == 4
    assert "accuracy_evaluation" in report
    assert "improvement_recommendations" in report


def test_simulation_compares_ai_output_against_manual_evaluation():
    runner = HRInterviewSimulationRunner()

    report = runner.run_simulations()
    confident_session = next(
        session for session in report["sessions"] if session["candidate_type"] == "Confident"
    )

    assert confident_session["ai_score"] > 0
    assert confident_session["manager_score"] == 86.0
    assert "score_delta" in confident_session
    assert confident_session["recruiter_report"]["natural_language_report"]


def test_simulation_identifies_scoring_inconsistencies():
    runner = HRInterviewSimulationRunner()

    report = runner.run_simulations()

    assert isinstance(report["scoring_inconsistencies"], list)
    assert report["accuracy_evaluation"]["mean_absolute_error"] >= 0
    assert any("Calibrate AI scoring" in item for item in report["improvement_recommendations"])
