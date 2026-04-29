from typing import List
import random

from .categories import ExperienceLevel, HRCategory, RoleType


class QuestionBank:
    """
    A dynamic rule-based engine that constructs context-aware instructions for the LLM
    to generate personalized interview questions based on candidate profile.
    """

    def __init__(self, experience_level: ExperienceLevel, role_type: RoleType):
        self.experience_level = experience_level
        self.role_type = role_type

    def _get_base_prompt(self, category: HRCategory) -> str:
        prompts = {
            HRCategory.SELF_INTRO: "Ask the candidate to briefly introduce themselves and walk through their background.",
            HRCategory.CAREER_JOURNEY: "Ask about a significant transition or key learning from their past experiences.",
            HRCategory.STRENGTHS_WEAKNESSES: "Ask the candidate to discuss a core strength and an area they are actively working to improve.",
            HRCategory.TEAMWORK_CULTURE: "Ask a behavioral question about how they handle conflicts or collaborate in a team.",
            HRCategory.CAREER_GOALS: "Ask where they see their career heading in the next 3-5 years and how this role fits.",
            HRCategory.AVAILABILITY_COMMITMENT: "Ask about their availability to start and long-term commitment to the role.",
        }
        return prompts.get(category, "Ask a general HR question.")

    def _get_experience_modifier(self) -> str:
        if self.experience_level == ExperienceLevel.FRESHER:
            return "Focus on their academic projects, internships, adaptability, and willingness to learn."
        return "Focus on their track record, leadership experiences, complex problem-solving, and career trajectory."

    def _get_role_modifier(self) -> str:
        if self.role_type == RoleType.TECHNICAL:
            return "Contextualize the question around technical workflows, such as code reviews, technical debt, or architectural disagreements."
        return "Contextualize the question around client management, cross-functional collaboration, and communication strategies."

    def generate_llm_prompt(self, category: HRCategory) -> dict:
        """
        Returns a structured prompt payload that instructs the LLM on how to phrase the question.
        """
        base_instruction = self._get_base_prompt(category)
        
        # Only apply role/experience modifiers to certain categories where it makes sense
        if category in [HRCategory.CAREER_JOURNEY, HRCategory.TEAMWORK_CULTURE, HRCategory.STRENGTHS_WEAKNESSES]:
            instruction = f"{base_instruction} {self._get_experience_modifier()} {self._get_role_modifier()}"
        else:
            instruction = base_instruction

        return {
            "category": category.value,
            "experience_level": self.experience_level.value,
            "role_type": self.role_type.value,
            "system_instruction": "You are a professional HR recruiter. Ask a natural, conversational question based on the provided instructions. Do not sound robotic.",
            "prompt_content": instruction
        }
