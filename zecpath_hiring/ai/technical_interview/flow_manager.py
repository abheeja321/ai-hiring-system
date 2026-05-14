from enum import Enum
from typing import List, Optional, Dict, Any
from .models import CandidateTechnicalProfile, QuestionType, Question
from .domain_mapper import DomainMapper
from .scoring_engine import TechnicalScoringEngine, TechnicalAnswerScore

class InterviewState(str, Enum):
    INTRODUCTION = "Introduction"
    EXPERIENCE_BASED = "Experience_Based"
    CONCEPTUAL = "Conceptual"
    SCENARIO_BASED = "Scenario_Based"
    CLOSING = "Closing"

class TechnicalInterviewSession:
    """
    Manages the state machine and flow of a single technical interview session.
    """
    def __init__(self, candidate: CandidateTechnicalProfile):
        self.candidate = candidate
        self.current_state: InterviewState = InterviewState.INTRODUCTION
        self.asked_questions: List[str] = []
        self.evaluation_data: List[TechnicalAnswerScore] = []
        self.scoring_engine = TechnicalScoringEngine()

    def get_next_question(self) -> Optional[Question]:
        """
        Advances the state machine and retrieves the next appropriate question based on the flow.
        """
        target_q_type = self._map_state_to_question_type(self.current_state)
        if not target_q_type:
            # We are in Closing state or Introduction
            return None

        # Fetch question
        questions = DomainMapper.get_questions_for_candidate(
            domain=self.candidate.primary_domain,
            experience=self.candidate.computed_experience_level,
            q_type=target_q_type,
            limit=10
        )
        
        # Filter already asked
        available = [q for q in questions if q.id not in self.asked_questions]
        
        if available:
            selected = available[0]
            self.asked_questions.append(selected.id)
            return selected
            
        # If no questions left in current state, force transition
        self.advance_state()
        return self.get_next_question()

    def advance_state(self):
        """
        Transitions the interview state forward.
        """
        transitions = {
            InterviewState.INTRODUCTION: InterviewState.EXPERIENCE_BASED,
            InterviewState.EXPERIENCE_BASED: InterviewState.CONCEPTUAL,
            InterviewState.CONCEPTUAL: InterviewState.SCENARIO_BASED,
            InterviewState.SCENARIO_BASED: InterviewState.CLOSING,
            InterviewState.CLOSING: InterviewState.CLOSING
        }
        self.current_state = transitions[self.current_state]

    def _map_state_to_question_type(self, state: InterviewState) -> Optional[QuestionType]:
        mapping = {
            InterviewState.EXPERIENCE_BASED: QuestionType.EXPERIENCE_BASED,
            InterviewState.CONCEPTUAL: QuestionType.CONCEPTUAL,
            InterviewState.SCENARIO_BASED: QuestionType.SCENARIO_BASED,
        }
        return mapping.get(state)

    def evaluate_answer(self, question: Question, answer_text: str) -> Dict[str, Any]:
        """
        Evaluates the answer using the technical scoring engine.
        """
        score_obj = self.scoring_engine.evaluate_answer(question, answer_text)
        self.evaluation_data.append(score_obj)
        
        # Return dict representation for easy API serialization
        return score_obj.model_dump()

    def get_session_score(self) -> Dict[str, Any]:
        """
        Returns the overall session score and skill breakdown.
        """
        return self.scoring_engine.calculate_session_score(self.evaluation_data)
