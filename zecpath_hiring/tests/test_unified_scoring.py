from zecpath_hiring.ai.hr_interview.categories import RoleType
from zecpath_hiring.ai.scoring.unified import CrossRoundWeights, UnifiedCandidateScore, UnifiedScoringEngine


def test_unified_score_combines_ats_screening_and_hr_interview():
    engine = UnifiedScoringEngine()

    result = engine.calculate_unified_score(
        {"candidate_id": 12},
        {"final_score": 80.0},
        {"screening_score": 70.0},
        {"final_score": 90.0},
        role_type=RoleType.TECHNICAL,
    )

    assert isinstance(result, UnifiedCandidateScore)
    assert result.candidate_id == 12
    assert result.hiring_fit_percentage > 0
    assert result.input_scores == {
        "ats_score": 80.0,
        "screening_score": 70.0,
        "hr_interview_score": 90.0,
    }
    assert round(sum(result.applied_weights.values()), 2) == 1.0


def test_role_based_weight_adjustment_changes_hiring_fit():
    engine = UnifiedScoringEngine()
    base_weights = CrossRoundWeights(ats_weight=0.35, screening_weight=0.25, hr_interview_weight=0.40)

    technical_fit = engine.calculate_hiring_fit_percentage(
        ats_score=95.0,
        screening_score=65.0,
        hr_interview_score=75.0,
        role_type=RoleType.TECHNICAL,
        weights=base_weights,
    )
    non_technical_fit = engine.calculate_hiring_fit_percentage(
        ats_score=95.0,
        screening_score=65.0,
        hr_interview_score=75.0,
        role_type=RoleType.NON_TECHNICAL,
        weights=base_weights,
    )

    assert technical_fit > non_technical_fit


def test_unified_score_flags_cross_round_inconsistency():
    engine = UnifiedScoringEngine()

    result = engine.calculate_unified_score(
        {"candidate_id": "risk"},
        {"final_score": 95.0},
        {"screening_score": 52.0},
        {"overall_hr_score": 58.0},
        role_type="Leadership",
    )

    assert "Cross-round scores are inconsistent and need recruiter review." in result.risk_flags
    assert result.recommendation in {
        "Manual review required before advancing.",
        "Do not advance without substantial new evidence.",
    }


def test_weight_system_documents_rounds_and_adjustments():
    engine = UnifiedScoringEngine()

    weight_system = engine.build_weight_system()

    assert "default_weights" in weight_system
    assert "role_based_adjustments" in weight_system
    assert "ats" in weight_system["rounds"]
