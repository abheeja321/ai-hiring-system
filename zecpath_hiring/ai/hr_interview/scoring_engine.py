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

class TurnEvaluation(BaseModel):
    """
    Represents the collected scores from various models for a single answer/turn.
    """
    turn_id: int
    relevance_score: float # 0-100
    communication_score: float # 0-100
    confidence_score: float # 0-100
    contradiction_penalty: float # 0-100 (High penalty = low consistency)

class HRScoringEngine:
    """
    Aggregates evaluations across all interview turns, normalizes them, 
    and applies the weight configuration to generate a final explainable score.
    """
    def __init__(self, config: WeightConfig = None):
        self.config = config or WeightConfig()
        
    def calculate_final_score(self, evaluations: List[TurnEvaluation]) -> Dict[str, Any]:
        """
        Normalizes scores across different interview lengths by averaging the metrics per turn,
        then calculates the weighted final HR score.
        """
        if not evaluations:
            return {"error": "No evaluations provided"}
            
        num_turns = len(evaluations)
        
        # Averages across all turns (Normalize across interview lengths)
        avg_relevance = sum(e.relevance_score for e in evaluations) / num_turns
        avg_communication = sum(e.communication_score for e in evaluations) / num_turns
        avg_confidence = sum(e.confidence_score for e in evaluations) / num_turns
        
        # Consistency is inversely proportional to contradiction penalties
        avg_contradiction = sum(e.contradiction_penalty for e in evaluations) / num_turns
        consistency_score = max(0.0, 100.0 - avg_contradiction)
        
        # Weighted Final Score
        final_score = (
            (avg_relevance * self.config.relevance_weight) +
            (avg_communication * self.config.communication_weight) +
            (avg_confidence * self.config.confidence_weight) +
            (consistency_score * self.config.consistency_weight)
        )
        
        return {
            "final_score": round(final_score, 1),
            "averages": {
                "relevance": round(avg_relevance, 1),
                "communication": round(avg_communication, 1),
                "confidence": round(avg_confidence, 1),
                "consistency": round(consistency_score, 1)
            },
            "num_turns_evaluated": num_turns
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
        
        report += "## 📊 Scoring Breakdown\n"
        
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
