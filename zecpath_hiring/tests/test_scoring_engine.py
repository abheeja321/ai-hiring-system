import pytest
from zecpath_hiring.ai.hr_interview.scoring_engine import HRScoringEngine, TurnEvaluation, WeightConfig

def test_hr_scoring_engine_math():
    config = WeightConfig(
        relevance_weight=0.5,
        communication_weight=0.3,
        confidence_weight=0.1,
        consistency_weight=0.1
    )
    engine = HRScoringEngine(config=config)
    
    # 3 turns, testing normalization
    evaluations = [
        TurnEvaluation(turn_id=1, relevance_score=100.0, communication_score=90.0, confidence_score=80.0, contradiction_penalty=0.0),
        TurnEvaluation(turn_id=2, relevance_score=50.0, communication_score=80.0, confidence_score=80.0, contradiction_penalty=20.0),
        TurnEvaluation(turn_id=3, relevance_score=90.0, communication_score=100.0, confidence_score=80.0, contradiction_penalty=10.0),
    ]
    
    # Averages:
    # Relevance: (100 + 50 + 90) / 3 = 80.0
    # Communication: (90 + 80 + 100) / 3 = 90.0
    # Confidence: (80 + 80 + 80) / 3 = 80.0
    # Contradiction: (0 + 20 + 10) / 3 = 10.0 -> Consistency: 90.0
    
    # Weighted Final:
    # 80 * 0.5 = 40.0
    # 90 * 0.3 = 27.0
    # 80 * 0.1 = 8.0
    # 90 * 0.1 = 9.0
    # Total = 84.0
    
    result = engine.calculate_final_score(evaluations)
    
    assert result["averages"]["relevance"] == 80.0
    assert result["averages"]["communication"] == 90.0
    assert result["averages"]["confidence"] == 80.0
    assert result["averages"]["consistency"] == 90.0
    assert result["final_score"] == 84.0

def test_generate_score_report():
    engine = HRScoringEngine()
    
    score_data = {
        "final_score": 92.5,
        "averages": {
            "relevance": 95.0,
            "communication": 90.0,
            "confidence": 88.0,
            "consistency": 100.0
        },
        "num_turns_evaluated": 5
    }
    
    report = engine.generate_score_report("Jane Doe", score_data)
    
    assert "Jane Doe" in report
    assert "92.5/100" in report
    assert "Answer Relevance" in report
    assert "The candidate's story remained highly consistent" in report # Consistency 100 feedback
