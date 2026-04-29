from typing import List, Optional

from .categories import ExperienceLevel, HRCategory, InterviewPhase, RoleType
from .question_bank import QuestionBank
from .state_manager import InterviewState
from .follow_up_engine import FollowUpEngine, FollowUpType


class FlowController:
    """
    Manages the transitions between interview phases and delegates question generation to the QuestionBank.
    """

    def __init__(self, state: InterviewState, experience_level: ExperienceLevel, role_type: RoleType):
        self.state = state
        self.question_bank = QuestionBank(experience_level, role_type)
        self.follow_up_engine = FollowUpEngine()

    def determine_next_action(self) -> dict:
        """
        Determines the next action based on the current state phase.
        Returns a dictionary containing the instruction for the LLM.
        """
        if self.state.current_phase == InterviewPhase.INTRODUCTION:
            return self._handle_introduction()
        elif self.state.current_phase == InterviewPhase.CORE_HR:
            return self._handle_core_hr()
        elif self.state.current_phase == InterviewPhase.ROLE_BASED:
            return self._handle_role_based()
        elif self.state.current_phase == InterviewPhase.CLOSING:
            return self._handle_closing()
        
        return {"action": "end", "message": "The interview is complete."}

    def process_candidate_response(self, response_text: str, current_category_context: str) -> Optional[dict]:
        """
        Processes a candidate's response. Uses the FollowUpEngine to check if a follow-up
        is warranted. If so, and the state allows it, returns a prompt for the LLM to generate
        the follow-up. Otherwise, returns None (meaning the flow should proceed to the next base question).
        """
        # Save response to history
        self.state.add_turn("Candidate", response_text, None)
        
        # Don't ask follow-ups during Intro or Closing phases
        if self.state.current_phase in [InterviewPhase.INTRODUCTION, InterviewPhase.CLOSING]:
            return None
            
        follow_up_type = self.follow_up_engine.analyze_response(response_text)
        
        if follow_up_type != FollowUpType.SUFFICIENT:
            if self.state.increment_follow_up():
                instruction = self.follow_up_engine.get_follow_up_instruction(follow_up_type, current_category_context)
                return {
                    "action": "follow_up",
                    "follow_up_type": follow_up_type.value,
                    "system_instruction": "You are a professional HR recruiter. Ask a natural follow-up question based on the candidate's last answer.",
                    "prompt_content": instruction
                }
                
        return None

    def _handle_introduction(self) -> dict:
        if HRCategory.SELF_INTRO not in self.state.asked_categories:
            self.state.mark_category_asked(HRCategory.SELF_INTRO)
            return self.question_bank.generate_llm_prompt(HRCategory.SELF_INTRO)
        
        # Move to next phase
        self.state.current_phase = InterviewPhase.CORE_HR
        return self.determine_next_action()

    def _handle_core_hr(self) -> dict:
        core_categories = [
            HRCategory.CAREER_JOURNEY,
            HRCategory.STRENGTHS_WEAKNESSES,
            HRCategory.TEAMWORK_CULTURE
        ]
        
        for category in core_categories:
            if category not in self.state.asked_categories:
                self.state.mark_category_asked(category)
                return self.question_bank.generate_llm_prompt(category)
                
        # Move to next phase
        self.state.current_phase = InterviewPhase.ROLE_BASED
        return self.determine_next_action()

    def _handle_role_based(self) -> dict:
        # We can reuse some categories or have specific role-based queries.
        # For this design, let's say we ask one deep role-specific teamwork question
        # If we had a specific "Technical Scenarios" category, we'd use it here.
        # Assuming we ask an additional follow-up context question for Role Based:
        if "RoleBased" not in self.state.asked_categories:
            # Using a custom string since it's an abstract concept in this simple design
            self.state.asked_categories.append("RoleBased")
            
            prompt = self.question_bank.generate_llm_prompt(HRCategory.TEAMWORK_CULTURE)
            prompt["system_instruction"] += " Focus deeply on the technical/domain aspects of their role."
            return prompt
            
        self.state.current_phase = InterviewPhase.CLOSING
        return self.determine_next_action()

    def _handle_closing(self) -> dict:
        closing_categories = [
            HRCategory.CAREER_GOALS,
            HRCategory.AVAILABILITY_COMMITMENT
        ]
        
        for category in closing_categories:
            if category not in self.state.asked_categories:
                self.state.mark_category_asked(category)
                return self.question_bank.generate_llm_prompt(category)
                
        self.state.current_phase = InterviewPhase.COMPLETED
        return {"action": "end", "message": "Thank you for your time. The interview is complete."}
