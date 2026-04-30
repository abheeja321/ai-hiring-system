import pytest
from unittest.mock import patch, MagicMock
from zecpath_hiring.ai.hr_interview.behavioral_evaluator import BehavioralEvaluator

@patch('zecpath_hiring.ai.hr_interview.behavioral_evaluator.pipeline')
@patch('zecpath_hiring.ai.hr_interview.behavioral_evaluator.librosa')
def test_evaluate_behavior_high_confidence(mock_librosa, mock_pipeline):
    # Mock audio features (low stress, high energy)
    mock_librosa.load.return_value = ([0.1, 0.2, 0.1], 22050)
    mock_librosa.feature.rms.return_value = [[0.5, 0.5, 0.5]]
    mock_librosa.pyin.return_value = ([100.0, 105.0], [True, True], [0.9, 0.9])
    
    # Mock sentiment (Positive)
    mock_sentiment = MagicMock()
    mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.95}]
    
    # Mock NLI (No contradiction)
    mock_nli = MagicMock()
    mock_nli.return_value = {'labels': ['entailment', 'neutral', 'contradiction'], 'scores': [0.8, 0.15, 0.05]}
    
    def side_effect(task, **kwargs):
        if task == "sentiment-analysis":
            return mock_sentiment
        elif task == "zero-shot-classification":
            return mock_nli
    
    mock_pipeline.side_effect = side_effect
    
    evaluator = BehavioralEvaluator()
    transcript = "I am very confident about this role. I know I can do it."
    
    result = evaluator.evaluate_behavior("dummy.wav", transcript)
    
    assert result["stress_level"] == "Low"
    assert result["confidence_score"] > 80.0
    assert result["sentiment_score"] == 0.95

@patch('zecpath_hiring.ai.hr_interview.behavioral_evaluator.pipeline')
@patch('zecpath_hiring.ai.hr_interview.behavioral_evaluator.librosa')
def test_evaluate_behavior_high_stress(mock_librosa, mock_pipeline):
    # Mock audio features (High stress: high pitch var, lots of silence/low energy)
    mock_librosa.load.return_value = ([0.0, 0.0, 0.0], 22050)
    mock_librosa.feature.rms.return_value = [[0.01, 0.0, 0.01]] # Very low energy
    mock_librosa.pyin.return_value = ([100.0, 300.0, 150.0], [True, True, True], [0.9, 0.9, 0.9]) # High pitch variance
    
    # Mock sentiment (Negative)
    mock_sentiment = MagicMock()
    mock_sentiment.return_value = [{'label': 'NEGATIVE', 'score': 0.85}] # 0.15 positive equivalent
    
    # Mock NLI (Contradiction)
    mock_nli = MagicMock()
    mock_nli.return_value = {'labels': ['contradiction', 'neutral', 'entailment'], 'scores': [0.9, 0.05, 0.05]}
    
    def side_effect(task, **kwargs):
        if task == "sentiment-analysis":
            return mock_sentiment
        elif task == "zero-shot-classification":
            return mock_nli
            
    mock_pipeline.side_effect = side_effect
    
    evaluator = BehavioralEvaluator()
    # High hesitation text
    transcript = "I... I... I think maybe I can do this. But maybe not."
    
    result = evaluator.evaluate_behavior("dummy.wav", transcript)
    
    # Should flag high stress due to high pitch variance, negative sentiment, and hesitation
    assert result["stress_level"] in ["Medium", "High"]
    # High contradiction penalty and hesitation penalty should lower confidence
    assert result["confidence_score"] < 80.0
    assert result["detected_issues"]["hesitation_penalty"] > 0
    assert result["detected_issues"]["negative_tone"] is True

def test_detect_hesitation_standalone():
    evaluator = BehavioralEvaluator()
    # No pipeline or librosa needed for this
    
    good_text = "I am certain we can achieve the goals."
    assert evaluator.detect_hesitation(good_text) == 0.0
    
    bad_text = "I think maybe I... I will try to see if maybe it works."
    penalty = evaluator.detect_hesitation(bad_text)
    assert penalty > 20.0 # Two 'maybe', one 'i think', one repeated 'i'
