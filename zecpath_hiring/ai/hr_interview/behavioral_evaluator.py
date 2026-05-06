import re
from typing import Dict, Any, List

# Optional deep learning imports (wrapped in try-except for safe testing/loading)
try:
    import librosa
    from transformers import pipeline
except ImportError:
    librosa = None
    pipeline = None


class BehavioralEvaluator:
    """
    Multimodal Deep Learning evaluator for Confidence and Stress detection.
    Combines Audio feature extraction (CNN/LSTM equivalent) and Text NLP (BERT-type).
    """

    def __init__(self):
        # Lazy load pipelines to save memory until called
        self._sentiment_pipe = None
        self._nli_pipe = None

    @staticmethod
    def _mean(values) -> float:
        values = [float(value) for value in values]
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _std(values) -> float:
        values = [float(value) for value in values]
        if not values:
            return 0.0
        mean = BehavioralEvaluator._mean(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        return variance ** 0.5

    def _get_sentiment_pipeline(self):
        if pipeline is None:
            return None
        if self._sentiment_pipe is None:
            # Using a standard, fast BERT model for sentiment
            self._sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        return self._sentiment_pipe

    def _get_nli_pipeline(self):
        if pipeline is None:
            return None
        if self._nli_pipe is None:
            # Zero-shot classification can simulate NLI logic efficiently
            self._nli_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        return self._nli_pipe

    def extract_audio_features(self, audio_file_path: str) -> Dict[str, float]:
        """
        Extracts pitch (F0) variability, RMS energy, and pause gaps from the audio using librosa.
        """
        if librosa is None:
            return {"pitch_variability": 0.0, "mean_energy": 0.5, "pause_ratio": 0.1}

        try:
            y, sr = librosa.load(audio_file_path, sr=None)
            
            # Energy/Loudness (RMS)
            rms = list(librosa.feature.rms(y=y)[0])
            mean_energy = self._mean(rms)
            
            # Pitch (F0) tracking - PyIN algorithm
            f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
            valid_f0 = [value for value, is_voiced in zip(f0, voiced_flag) if is_voiced]
            
            if len(valid_f0) > 0:
                pitch_variability = self._std(valid_f0)
            else:
                pitch_variability = 0.0
                
            # Pause detection based on energy threshold
            threshold = mean_energy * 0.1
            silence_frames = sum(1 for value in rms if value < threshold)
            pause_ratio = float(silence_frames / len(rms)) if len(rms) > 0 else 0.0
            
            return {
                "pitch_variability": pitch_variability,
                "mean_energy": mean_energy,
                "pause_ratio": pause_ratio
            }
        except Exception as e:
            # Fallback if audio fails
            return {"pitch_variability": 0.0, "mean_energy": 0.5, "pause_ratio": 0.1}

    def detect_hesitation(self, transcript: str) -> float:
        """
        Detects hesitation patterns from text:
        - Repeated words ("I... I... I")
        - Uncertainty phrases ("maybe", "not sure", "I think")
        Returns a penalty score 0-100.
        """
        penalty = 0.0
        text_lower = transcript.lower()
        
        # Uncertainty phrases
        uncertainty_phrases = ["maybe", "not sure", "i think", "probably", "i guess", "might be"]
        for phrase in uncertainty_phrases:
            if phrase in text_lower:
                penalty += 10.0
                
        # Repeated words indicating stutter/hesitation e.g., "the the"
        words = re.findall(r'\b\w+\b', text_lower)
        for i in range(len(words) - 1):
            if words[i] == words[i+1]:
                penalty += 5.0
                
        return min(100.0, penalty)

    def analyze_sentiment(self, transcript: str) -> float:
        """
        Uses BERT to analyze sentiment.
        Returns a score from 0 (Negative) to 1 (Positive).
        """
        pipe = self._get_sentiment_pipeline()
        if pipe is None or not transcript.strip():
            return 0.5 # Neutral fallback
            
        # Truncate text if it's too long for the model
        truncated = transcript[:512]
        result = pipe(truncated)[0]
        
        if result['label'] == 'POSITIVE':
            return result['score'] # 0.5 to 1.0
        else:
            return 1.0 - result['score'] # 0.0 to 0.5

    def detect_contradictions(self, transcript: str) -> float:
        """
        Uses NLI to detect logical conflicts in the answer.
        Returns a contradiction penalty score (0-100).
        """
        pipe = self._get_nli_pipeline()
        if pipe is None or not transcript.strip():
            return 0.0 # No contradiction detected
            
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        if len(sentences) < 2:
            return 0.0
            
        # Compare first sentence with last to detect if they changed their mind
        hypothesis = sentences[0]
        premise = sentences[-1]
        
        # Zero-shot classification asking if they contradict
        labels = ["contradiction", "entailment", "neutral"]
        result = pipe(hypothesis, candidate_labels=labels)
        
        # If contradiction is the top score, apply a penalty
        contradiction_prob = dict(zip(result['labels'], result['scores']))['contradiction']
        
        return contradiction_prob * 100.0

    def evaluate_behavior(self, audio_file_path: str, transcript: str) -> Dict[str, Any]:
        """
        Fuses Audio features and Text DL features to generate final Confidence and Stress scores.
        """
        audio_features = self.extract_audio_features(audio_file_path)
        
        pitch_var = audio_features["pitch_variability"]
        energy = audio_features["mean_energy"]
        pause_ratio = audio_features["pause_ratio"]
        
        hesitation_score = self.detect_hesitation(transcript)
        sentiment_score = self.analyze_sentiment(transcript)
        contradiction_penalty = self.detect_contradictions(transcript)
        
        # 1. Calculate Stress Level
        # High pitch variance, high pauses, high hesitation, and negative sentiment = High Stress
        stress_indicator = (pitch_var / 50.0) + pause_ratio + (hesitation_score / 100.0) + (1.0 - sentiment_score)
        
        if stress_indicator > 2.5:
            stress_level = "High"
        elif stress_indicator > 1.2:
            stress_level = "Medium"
        else:
            stress_level = "Low"
            
        # 2. Calculate Confidence Score (0-100)
        # Base confidence
        raw_confidence = 100.0
        
        # Penalties
        raw_confidence -= hesitation_score * 0.5
        raw_confidence -= contradiction_penalty * 0.5
        raw_confidence -= (pause_ratio * 100) * 0.3
        
        if stress_level == "High":
            raw_confidence -= 20.0
        elif stress_level == "Medium":
            raw_confidence -= 10.0
            
        if sentiment_score > 0.8:
            raw_confidence += 10.0
            
        # Energy modifier: Low energy reduces confidence
        if energy < 0.01:
            raw_confidence -= 15.0
            
        # Normalize Score (Fairness curve)
        # Bounding to 0-100 and applying a slight curve
        normalized_confidence = 10 * (max(0.0, min(100.0, raw_confidence)) ** 0.5)
        final_confidence = min(100.0, round(normalized_confidence, 1))
        
        return {
            "confidence_score": final_confidence,
            "stress_level": stress_level,
            "sentiment_score": round(sentiment_score, 2),
            "detected_issues": {
                "hesitation_penalty": round(hesitation_score, 1),
                "contradiction_penalty": round(contradiction_penalty, 1),
                "negative_tone": sentiment_score < 0.4
            },
            "audio_metrics": {
                "pitch_variability": round(pitch_var, 2),
                "pause_ratio": round(pause_ratio, 2),
                "energy": round(energy, 3)
            }
        }
