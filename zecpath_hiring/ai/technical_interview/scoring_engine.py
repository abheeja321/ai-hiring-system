import math
from functools import lru_cache
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from zecpath_hiring.ai.technical_interview.models import Question, QuestionType
from zecpath_hiring.ai.scoring.explainable import weighted_score


class ScoringParameters(BaseModel):
    accuracy: float = Field(..., ge=0.0, le=100.0, description="Accuracy of the answer")
    depth: float = Field(..., ge=0.0, le=100.0, description="Depth of explanation")
    logic: float = Field(..., ge=0.0, le=100.0, description="Logical reasoning and structure")
    real_world_applicability: float = Field(..., ge=0.0, le=100.0, description="Real-world applicability")


class TechnicalAnswerScore(BaseModel):
    question_id: str
    question_type: QuestionType
    raw_parameters: ScoringParameters
    is_deep_answer: bool
    difficulty_score: float
    normalized_score: float
    explanation: List[str]


class TechnicalScoringEngine:
    """
    Engine to score technical interview answers based on rubrics, detect shallow vs deep answers,
    and normalize scores across difficulty levels.
    """
    
    # Rubrics defining weights for different question types
    RUBRICS = {
        QuestionType.INTRODUCTION: {
            "accuracy": 0.50,
            "depth": 0.20,
            "logic": 0.20,
            "real_world_applicability": 0.10
        },
        QuestionType.EXPERIENCE_BASED: {
            "accuracy": 0.30,
            "depth": 0.40,
            "logic": 0.10,
            "real_world_applicability": 0.20
        },
        QuestionType.CONCEPTUAL: {
            "accuracy": 0.40,
            "depth": 0.40,
            "logic": 0.20,
            "real_world_applicability": 0.00
        },
        QuestionType.SCENARIO_BASED: {
            "accuracy": 0.20,
            "depth": 0.20,
            "logic": 0.30,
            "real_world_applicability": 0.30
        }
    }

    def evaluate_answer(self, question: Question, answer_text: str) -> TechnicalAnswerScore:
        """
        Evaluates a candidate's answer against the expected key points and question type rubric.
        """
        # 1. Heuristic Parsing for basic scoring parameters
        accuracy = self._evaluate_accuracy(answer_text, tuple(question.expected_key_points))
        depth = self._evaluate_depth(answer_text)
        logic = self._evaluate_logic(answer_text)
        real_world = self._evaluate_applicability(answer_text)
        
        raw_params = ScoringParameters(
            accuracy=accuracy,
            depth=depth,
            logic=logic,
            real_world_applicability=real_world
        )
        
        # 2. Apply Rubric Weights
        weights = self.RUBRICS.get(question.question_type, self.RUBRICS[QuestionType.CONCEPTUAL])
        
        components = {
            "accuracy": raw_params.accuracy,
            "depth": raw_params.depth,
            "logic": raw_params.logic,
            "real_world_applicability": raw_params.real_world_applicability
        }
        
        # We reuse the explainable utility
        score_data = weighted_score(components, weights)
        base_score = score_data["final_score"]
        
        # 3. Detect Shallow vs Deep
        is_deep = depth >= 70.0 and logic >= 60.0
        
        # 4. Normalize based on difficulty
        # Difficulty is 1 to 10. A standard question is 5.
        # We scale the score. A difficult question gives a slight bump, an easy one might have a stricter curve.
        difficulty_multiplier = 1.0 + ((question.difficulty_score - 5.0) * 0.05) # +/- 5% per point
        normalized_score = min(100.0, max(0.0, round(base_score * difficulty_multiplier, 2)))
        
        # 5. Build explainable output
        explanations = score_data["explanation"]
        explanations.append(f"Answer classified as {'Deep' if is_deep else 'Shallow'}.")
        explanations.append(f"Applied difficulty multiplier {round(difficulty_multiplier, 2)}x based on difficulty {question.difficulty_score}/10.")
        
        return TechnicalAnswerScore(
            question_id=question.id,
            question_type=question.question_type,
            raw_parameters=raw_params,
            is_deep_answer=is_deep,
            difficulty_score=question.difficulty_score,
            normalized_score=normalized_score,
            explanation=explanations
        )

    def calculate_session_score(self, evaluations: List[TechnicalAnswerScore]) -> Dict[str, Any]:
        """
        Aggregates multiple evaluations into a session-wide skill breakdown.
        """
        if not evaluations:
            return {"overall_score": 0.0, "breakdown": {}}
            
        total_score = sum(e.normalized_score for e in evaluations)
        overall = round(total_score / len(evaluations), 2)
        
        breakdown = {
            "average_accuracy": round(sum(e.raw_parameters.accuracy for e in evaluations) / len(evaluations), 2),
            "average_depth": round(sum(e.raw_parameters.depth for e in evaluations) / len(evaluations), 2),
            "average_logic": round(sum(e.raw_parameters.logic for e in evaluations) / len(evaluations), 2),
            "average_applicability": round(sum(e.raw_parameters.real_world_applicability for e in evaluations) / len(evaluations), 2),
            "deep_answer_percentage": round(sum(1 for e in evaluations if e.is_deep_answer) / len(evaluations) * 100, 2),
        }
        
        return {
            "overall_score": overall,
            "breakdown": breakdown
        }

    # --- Heuristics for simulated evaluation ---

    @lru_cache(maxsize=1024)
    def _evaluate_accuracy(self, text: str, key_points: tuple) -> float:
        if not key_points:
            return 75.0 # Baseline if no key points to check
        text_lower = text.lower()
        matched = sum(1 for kp in key_points if kp.lower() in text_lower)
        # Assuming partial coverage is okay, scale to 100
        return min(100.0, (matched / max(1, len(key_points))) * 120.0)

    @lru_cache(maxsize=1024)
    def _evaluate_depth(self, text: str) -> float:
        # Heuristic: Length and complexity of words
        words = text.split()
        if len(words) < 10:
            return 20.0
        elif len(words) < 30:
            return 50.0
        elif len(words) < 60:
            return 75.0
        else:
            return 95.0

    @lru_cache(maxsize=1024)
    def _evaluate_logic(self, text: str) -> float:
        # Look for logical connectors: because, therefore, however, for example, first, second
        connectors = ["because", "therefore", "however", "example", "first", "second", "if", "then", "lead to", "due to", "as a result", "consequently", "moreover", "furthermore", "in conclusion"]
        text_lower = text.lower()
        count = sum(1 for c in connectors if c in text_lower)
        score = 40.0 + (count * 15.0)
        return min(100.0, score)

    @lru_cache(maxsize=1024)
    def _evaluate_applicability(self, text: str) -> float:
        # Look for experience indicators: in my project, we used, i implemented, production, deployment
        indicators = ["project", "used", "implemented", "production", "deployment", "issue", "team", "client", "real world", "architecture", "scale", "optimize"]
        text_lower = text.lower()
        count = sum(1 for ind in indicators if ind in text_lower)
        score = 30.0 + (count * 20.0)
        return min(100.0, score)
