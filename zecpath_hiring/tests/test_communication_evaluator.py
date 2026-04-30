import pytest
from zecpath_hiring.ai.hr_interview.communication_evaluator import CommunicationEvaluator

def test_detect_filler_words():
    evaluator = CommunicationEvaluator()
    text = "Um, I think that, like, you know, it is basically a good idea."
    result = evaluator.detect_filler_words(text)
    
    assert result["total_fillers"] == 4
    assert "um" in result["filler_counts"]
    assert "like" in result["filler_counts"]
    assert "you know" in result["filler_counts"]
    assert "basically" in result["filler_counts"]
    assert result["word_count"] > 10

def test_evaluate_fluency():
    evaluator = CommunicationEvaluator()
    
    # Perfect fluency
    good_text = "I believe my skills are a strong match for this role."
    good_score = evaluator.evaluate_fluency(good_text)
    assert good_score == 20.0
    
    # Poor fluency
    bad_text = "Um, well, like, you know, I basically think it is, uh, good."
    bad_score = evaluator.evaluate_fluency(bad_text)
    assert bad_score < 20.0
    
    # WPM penalty
    slow_score = evaluator.evaluate_fluency(good_text, wpm=80.0)
    assert slow_score < good_score
    
    fast_score = evaluator.evaluate_fluency(good_text, wpm=200.0)
    assert fast_score < good_score
    
    perfect_wpm_score = evaluator.evaluate_fluency(good_text, wpm=140.0)
    assert perfect_wpm_score == 20.0

def test_evaluate_vocabulary():
    evaluator = CommunicationEvaluator()
    
    # Simple vocabulary
    simple_text = "I did a good job on the job."
    simple_score = evaluator.evaluate_vocabulary(simple_text)
    
    # Complex vocabulary
    complex_text = "I successfully orchestrated the deployment of multiple heterogeneous microservices."
    complex_score = evaluator.evaluate_vocabulary(complex_text)
    
    assert complex_score > simple_score

def test_llm_prompt_generation():
    evaluator = CommunicationEvaluator()
    prompt = evaluator.get_llm_evaluation_prompt("I did good.", "How did you do?")
    assert "Grammar Quality" in prompt["prompt_content"]
    assert "Clarity of Explanation" in prompt["prompt_content"]
    assert "Answer Structure" in prompt["prompt_content"]
    assert "system_instruction" in prompt

def test_evaluate_full_response():
    evaluator = CommunicationEvaluator()
    text = "I believe I can contribute effectively."
    llm_scores = {
        "grammar_score": 18.0,
        "clarity_score": 19.0,
        "structure_score": 17.0
    }
    
    result = evaluator.evaluate_full_response(text, llm_scores)
    
    assert "normalized_score" in result
    assert "raw_score" in result
    assert result["components"]["grammar"] == 18.0
    assert result["components"]["fluency"] <= 20.0
    assert result["components"]["vocabulary"] <= 20.0
    
def test_normalize_score():
    evaluator = CommunicationEvaluator()
    
    assert evaluator.normalize_score(100.0) == 100.0
    assert evaluator.normalize_score(64.0) == 80.0
    assert evaluator.normalize_score(36.0) == 60.0
    assert evaluator.normalize_score(0.0) == 0.0

from unittest.mock import patch, MagicMock

@patch('speech_recognition.Recognizer')
@patch('speech_recognition.AudioFile')
def test_evaluate_audio_response(mock_audio_file, mock_recognizer):
    evaluator = CommunicationEvaluator()
    
    # Setup mocks
    mock_rec_instance = mock_recognizer.return_value
    mock_rec_instance.recognize_google.return_value = "I am a very good candidate."
    
    mock_source = MagicMock()
    mock_source.DURATION = 30.0 # 30 seconds
    mock_audio_file.return_value.__enter__.return_value = mock_source
    
    llm_scores = {"grammar_score": 20.0, "clarity_score": 20.0, "structure_score": 20.0}
    
    result = evaluator.evaluate_audio_response("dummy.wav", llm_scores)
    
    assert result["transcript"] == "I am a very good candidate."
    assert "wpm" in result
    assert result["components"]["grammar"] == 20.0
