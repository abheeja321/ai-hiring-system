from pydantic import BaseModel, Field
from typing import List, Dict, Any

class WeightConfig(BaseModel):
    """
    Defines the exact weightage distribution for the final HR Interview Score.
    Must sum up to 1.0 (100%).
    """
    relevance_weight: float = Field(default=0.40, description="Weight for answering the question properly")
    communication_weight: float = Field(default=0.30, description="Weight for fluency and clarity")
    confidence_weight: float = Field(default=0.20, description="Weight for behavioral stress/confidence")
    consistency_weight: float = Field(default=0.10, description="Weight for lack of contradictions")
    logical_thinking_weight: float = Field(default=0.0, description="Optional weight for aptitude logic scoring")
    problem_solving_clarity_weight: float = Field(default=0.0, description="Optional weight for problem-solving clarity")

class TurnEvaluation(BaseModel):
    """
    Represents the collected scores from various models for a single answer/turn.
    """
    turn_id: int
    relevance_score: float # 0-100
    communication_score: float # 0-100
    confidence_score: float # 0-100
    contradiction_penalty: float # 0-100 (High penalty = low consistency)
    logical_thinking_score: float = 0.0 # 0-100
    problem_solving_clarity_score: float = 0.0 # 0-100

class HRScoringEngine:
    """
    Aggregates evaluations across all interview turns, normalizes them, 
    and applies the weight configuration to generate a final explainable score.
    """
    def __init__(self, config: WeightConfig = None):
        self.config = config or WeightConfig()

    def _clamp_score(self, value: float) -> float:
        return max(0.0, min(100.0, float(value)))

    def _normalized_weights(self) -> Dict[str, float]:
        weights = {
            "relevance": max(0.0, self.config.relevance_weight),
            "communication": max(0.0, self.config.communication_weight),
            "confidence": max(0.0, self.config.confidence_weight),
            "consistency": max(0.0, self.config.consistency_weight),
            "logical_thinking": max(0.0, self.config.logical_thinking_weight),
            "problem_solving_clarity": max(0.0, self.config.problem_solving_clarity_weight),
        }
        total = sum(weights.values())
        if total <= 0:
            return {
                "relevance": 0.40,
                "communication": 0.30,
                "confidence": 0.20,
                "consistency": 0.10,
                "logical_thinking": 0.0,
                "problem_solving_clarity": 0.0,
            }
        return {key: value / total for key, value in weights.items()}
        
    def calculate_final_score(self, evaluations: List[TurnEvaluation]) -> Dict[str, Any]:
        """
        Normalizes scores across different interview lengths by averaging the metrics per turn,
        then calculates the weighted final HR score.
        """
        if not evaluations:
            return {"error": "No evaluations provided"}
            
        num_turns = len(evaluations)
        
        # Averages across all turns (Normalize across interview lengths)
        avg_relevance = sum(self._clamp_score(e.relevance_score) for e in evaluations) / num_turns
        avg_communication = sum(self._clamp_score(e.communication_score) for e in evaluations) / num_turns
        avg_confidence = sum(self._clamp_score(e.confidence_score) for e in evaluations) / num_turns
        avg_logical_thinking = sum(self._clamp_score(e.logical_thinking_score) for e in evaluations) / num_turns
        avg_problem_solving_clarity = sum(self._clamp_score(e.problem_solving_clarity_score) for e in evaluations) / num_turns
        
        # Consistency is inversely proportional to contradiction penalties
        avg_contradiction = sum(self._clamp_score(e.contradiction_penalty) for e in evaluations) / num_turns
        consistency_score = max(0.0, 100.0 - avg_contradiction)
        weights = self._normalized_weights()
        
        # Weighted Final Score
        final_score = (
            (avg_relevance * weights["relevance"]) +
            (avg_communication * weights["communication"]) +
            (avg_confidence * weights["confidence"]) +
            (consistency_score * weights["consistency"]) +
            (avg_logical_thinking * weights["logical_thinking"]) +
            (avg_problem_solving_clarity * weights["problem_solving_clarity"])
        )
        
        return {
            "final_score": round(final_score, 1),
            "averages": {
                "relevance": round(avg_relevance, 1),
                "communication": round(avg_communication, 1),
                "confidence": round(avg_confidence, 1),
                "consistency": round(consistency_score, 1),
                "logical_thinking": round(avg_logical_thinking, 1),
                "problem_solving_clarity": round(avg_problem_solving_clarity, 1)
            },
            "applied_weights": {key: round(value, 4) for key, value in weights.items()},
            "num_turns_evaluated": num_turns
        }

    def calculate_logical_reasoning_score(
        self,
        logical_thinking_score: float,
        problem_solving_clarity_score: float,
        situational_judgment_score: float,
    ) -> Dict[str, Any]:
        """
        Scores aptitude-only performance using the Day 38 logical reasoning model.
        """
        logical = self._clamp_score(logical_thinking_score)
        clarity = self._clamp_score(problem_solving_clarity_score)
        judgment = self._clamp_score(situational_judgment_score)
        final_score = (
            (logical * 0.45) +
            (clarity * 0.35) +
            (judgment * 0.20)
        )
        return {
            "logical_reasoning_score": round(final_score, 1),
            "components": {
                "logical_thinking": round(logical, 1),
                "problem_solving_clarity": round(clarity, 1),
                "situational_judgment": round(judgment, 1),
            },
            "weights": {
                "logical_thinking": 0.45,
                "problem_solving_clarity": 0.35,
                "situational_judgment": 0.20,
            },
        }

    def generate_score_report(self, candidate_name: str, score_data: Dict[str, Any]) -> str:
        """
        Builds an explainable Markdown report based on the scored data and AI models.
        """
        if "error" in score_data:
            return "No data to report."
            
        final = score_data["final_score"]
        avgs = score_data["averages"]
        
        report = f"# HR Interview Evaluation Report: {candidate_name}\n\n"
        report += f"**Final HR Score:** {final}/100\n"
        report += f"**Turns Evaluated:** {score_data['num_turns_evaluated']}\n\n"
        
        report += "## Scoring Breakdown\n"
        
        # Relevance
        report += f"- **Answer Relevance (Weight: {int(self.config.relevance_weight*100)}%):** {avgs['relevance']}/100\n"
        if avgs['relevance'] >= 85:
            report += "  - *Feedback:* The candidate answered the core HR questions directly and effectively, demonstrating strong professional alignment.\n"
        elif avgs['relevance'] <= 60:
            report += "  - *Feedback:* The candidate frequently dodged or misunderstood the core questions.\n"
        else:
            report += "  - *Feedback:* The answers were generally acceptable but lacked deep relevance in some areas.\n"
            
        # Communication
        report += f"- **Communication (Weight: {int(self.config.communication_weight*100)}%):** {avgs['communication']}/100\n"
        if avgs['communication'] >= 85:
            report += "  - *Feedback:* Excellent articulation, minimal filler words, and strong grammatical cohesiveness.\n"
        elif avgs['communication'] <= 60:
            report += "  - *Feedback:* Heavy use of filler words or disjointed sentence structure impacted overall clarity.\n"
        else:
            report += "  - *Feedback:* Average communication skills with occasional filler words or minor grammatical errors.\n"
            
        # Confidence
        report += f"- **Behavioral Confidence (Weight: {int(self.config.confidence_weight*100)}%):** {avgs['confidence']}/100\n"
        if avgs['confidence'] >= 85:
            report += "  - *Feedback:* Deep Learning audio and sentiment analysis detected a highly confident tone, strong energy, and virtually no hesitation.\n"
        elif avgs['confidence'] <= 60:
            report += "  - *Feedback:* Models detected vocal stress, hesitation phrases, or low conversational energy.\n"
        else:
            report += "  - *Feedback:* The candidate showed normal confidence levels with occasional signs of slight hesitation.\n"
            
        # Consistency
        report += f"- **Consistency (Weight: {int(self.config.consistency_weight*100)}%):** {avgs['consistency']}/100\n"
        if avgs['consistency'] >= 90:
            report += "  - *Feedback:* The candidate's story remained highly consistent throughout the interview with no detected logical contradictions.\n"
        else:
            report += "  - *Feedback:* Natural Language Inference (NLI) models detected slight logical contradictions or changing statements across answers.\n"
            
        return report
