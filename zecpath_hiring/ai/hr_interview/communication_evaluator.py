import re
import sys
from types import SimpleNamespace
from typing import Dict, Any

try:
    import speech_recognition as sr
except ImportError:
    class _SpeechRecognitionError(Exception):
        pass

    class _MissingSpeechRecognition:
        def __init__(self, *args, **kwargs):
            raise ImportError("speech_recognition is not installed")

    sr = SimpleNamespace(
        Recognizer=_MissingSpeechRecognition,
        AudioFile=_MissingSpeechRecognition,
        UnknownValueError=_SpeechRecognitionError,
        RequestError=_SpeechRecognitionError,
    )
    sys.modules["speech_recognition"] = sr

class CommunicationEvaluator:
    """
    Evaluates candidate communication skills across multiple dimensions:
    fluency, vocabulary, grammar, clarity, and structure.
    """
    
    # Common filler words to detect
    FILLER_WORDS = {"um", "uh", "like", "you know", "basically", "actually", "literally", "sort of", "kind of", "i mean"}

    def detect_filler_words(self, text: str) -> Dict[str, Any]:
        """
        Detects the occurrence of filler words in the candidate's text.
        """
        clean_text = text.lower()
        filler_counts = {}
        total_fillers = 0
        
        for filler in self.FILLER_WORDS:
            # Match whole words/phrases using word boundaries
            count = len(re.findall(rf'\b{filler}\b', clean_text))
            if count > 0:
                filler_counts[filler] = count
                total_fillers += count
                
        word_count = len(re.findall(r'\b\w+\b', clean_text))
        
        return {
            "total_fillers": total_fillers,
            "filler_counts": filler_counts,
            "word_count": word_count
        }

    def evaluate_fluency(self, text: str, wpm: float = None) -> float:
        """
        Evaluates fluency by measuring sentence continuity and penalizing the use of filler words.
        Optionally evaluates Speech Rate (Words Per Minute).
        Max score: 20.0
        """
        stats = self.detect_filler_words(text)
        word_count = stats["word_count"]
        total_fillers = stats["total_fillers"]
        
        if word_count == 0:
            return 0.0
            
        # Acceptable threshold: 1 filler per 30 words (approx 3.3%)
        # Penalize beyond this threshold
        filler_ratio = total_fillers / word_count
        
        # If filler ratio is very high (e.g., > 10%), penalty increases significantly
        penalty = min(20.0, (filler_ratio * 100) * 1.5) 
        fluency_score = max(0.0, 20.0 - penalty)
        
        if wpm is not None and wpm > 0:
            # Ideal WPM is ~130-150. If they speak too slowly (<100) or too fast (>180), penalize.
            wpm_penalty = 0.0
            if wpm < 100:
                wpm_penalty = min(5.0, (100 - wpm) / 5.0)
            elif wpm > 180:
                wpm_penalty = min(5.0, (wpm - 180) / 10.0)
            fluency_score = max(0.0, fluency_score - wpm_penalty)
        
        return round(fluency_score, 1)

    def evaluate_vocabulary(self, text: str) -> float:
        """
        Evaluates vocabulary range using heuristics (lexical density and average word length).
        Max score: 20.0
        """
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        
        if word_count == 0:
            return 0.0
            
        unique_words = set(words)
        lexical_density = len(unique_words) / word_count
        
        avg_word_length = sum(len(w) for w in words) / word_count
        
        # High lexical density (>0.6) and good avg word length (>5.0) approaches a full score
        density_score = min(10.0, (lexical_density / 0.65) * 10.0)
        length_score = min(10.0, (avg_word_length / 5.5) * 10.0)
        
        return round(density_score + length_score, 1)

    def get_llm_evaluation_prompt(self, candidate_response: str, question: str) -> dict:
        """
        Generates a prompt to evaluate Grammar, Clarity, and Structure using an LLM.
        Each aspect is scored out of 20.
        """
        prompt = f"""
You are an expert HR communication evaluator. Please evaluate the following candidate response to an interview question.

Question: "{question}"
Candidate Response: "{candidate_response}"

Evaluate the response on the following criteria and provide a score out of 20 for each:
1. Grammar Quality (0-20): Evaluate sentence correctness, subject-verb agreement, and tense usage.
2. Clarity of Explanation (0-20): Evaluate how easily the answer can be understood, and avoidance of convoluted sentences.
3. Answer Structure (0-20): Evaluate logical progression, cohesiveness, and use of structured methods like STAR (Situation, Task, Action, Result).

Format your response strictly as JSON:
{{
    "grammar_score": <number>,
    "grammar_feedback": "<brief feedback>",
    "clarity_score": <number>,
    "clarity_feedback": "<brief feedback>",
    "structure_score": <number>,
    "structure_feedback": "<brief feedback>"
}}
"""
        return {
            "system_instruction": "You are a communication evaluation assistant that strictly outputs JSON.",
            "prompt_content": prompt
        }

    def normalize_score(self, raw_score: float) -> float:
        """
        Normalizes the final 0-100 score to reduce bias.
        We apply a square root curve (10 * sqrt(raw_score)) which compresses extreme 
        low scores (lifting them up) while keeping high scores proportional.
        This provides a fairer, balanced score for candidates who might have 
        minor nervous filler words.
        """
        if raw_score <= 0:
            return 0.0
            
        normalized = 10 * (raw_score ** 0.5)
        return min(100.0, round(normalized, 1))

    def evaluate_full_response(self, text: str, llm_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Combines heuristic scores and LLM scores to generate the final normalized score.
        
        Args:
            text: The candidate's response text.
            llm_scores: A dictionary containing 'grammar_score', 'clarity_score', and 'structure_score' (each out of 20).
            
        Returns:
            A dictionary containing the final score breakdown.
        """
        fluency = self.evaluate_fluency(text)
        vocabulary = self.evaluate_vocabulary(text)
        
        grammar = llm_scores.get("grammar_score", 0.0)
        clarity = llm_scores.get("clarity_score", 0.0)
        structure = llm_scores.get("structure_score", 0.0)
        
        raw_score = fluency + vocabulary + grammar + clarity + structure
        normalized_score = self.normalize_score(raw_score)
        
        filler_stats = self.detect_filler_words(text)
        
        return {
            "normalized_score": normalized_score,
            "raw_score": round(raw_score, 1),
            "components": {
                "fluency": fluency,
                "vocabulary": vocabulary,
                "grammar": grammar,
                "clarity": clarity,
                "structure": structure
            },
            "filler_stats": filler_stats
        }

    def evaluate_audio_response(self, audio_file_path: str, llm_scores: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Evaluates communication directly from an audio file.
        Transcribes the audio, calculates Speech Rate (WPM), and returns the full evaluation.
        """
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            duration_seconds = source.DURATION
            
        try:
            # Recognize speech using Google Web Speech API (free, no key required)
            transcript = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            transcript = ""
        except sr.RequestError:
            transcript = ""
            
        wpm = 0.0
        if duration_seconds > 0 and transcript:
            word_count = len(re.findall(r'\b\w+\b', transcript.lower()))
            duration_minutes = duration_seconds / 60.0
            wpm = word_count / duration_minutes
            
        # Now evaluate text with the calculated WPM
        fluency = self.evaluate_fluency(transcript, wpm=wpm)
        vocabulary = self.evaluate_vocabulary(transcript)
        
        llm_scores = llm_scores or {}
        grammar = llm_scores.get("grammar_score", 0.0)
        clarity = llm_scores.get("clarity_score", 0.0)
        structure = llm_scores.get("structure_score", 0.0)
        
        raw_score = fluency + vocabulary + grammar + clarity + structure
        normalized_score = self.normalize_score(raw_score)
        
        filler_stats = self.detect_filler_words(transcript)
        
        return {
            "transcript": transcript,
            "wpm": round(wpm, 1),
            "normalized_score": normalized_score,
            "raw_score": round(raw_score, 1),
            "components": {
                "fluency": fluency,
                "vocabulary": vocabulary,
                "grammar": grammar,
                "clarity": clarity,
                "structure": structure
            },
            "filler_stats": filler_stats
        }
