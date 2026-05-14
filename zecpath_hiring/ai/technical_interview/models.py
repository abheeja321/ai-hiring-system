from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    BASICS = "0-2 years"
    INTERMEDIATE = "3-5 years"
    ADVANCED = "5+ years"


class SkillDomain(str, Enum):
    MERN = "MERN Stack"
    JAVA = "Java Backend"
    PYTHON = "Python / Django"
    DEVOPS = "DevOps"
    FRONTEND = "Frontend (React/Angular)"
    DATA_SCIENCE = "Data Science"


class QuestionType(str, Enum):
    INTRODUCTION = "Introduction"
    EXPERIENCE_BASED = "Experience-Based"
    CONCEPTUAL = "Conceptual"
    SCENARIO_BASED = "Scenario-Based"


class Question(BaseModel):
    """
    Question Hierarchy Model representing a technical interview question.
    """
    id: str
    domain: SkillDomain
    experience_level: ExperienceLevel
    question_type: QuestionType
    text: str = Field(..., description="The actual question text")
    expected_key_points: List[str] = Field(default_factory=list, description="Keywords or concepts expected in the answer")
    difficulty_score: float = Field(default=5.0, ge=1.0, le=10.0, description="Difficulty of the question from 1 to 10")
    follow_up_prompts: List[str] = Field(default_factory=list, description="Optional prompts for deep dive")

    def __str__(self) -> str:
        return f"[{self.question_type.value}] {self.text} (Difficulty: {self.difficulty_score}/10)"


class CandidateTechnicalProfile(BaseModel):
    """
    Represents the parsed technical profile of a candidate to drive the interview.
    """
    candidate_id: str
    name: str
    primary_domain: SkillDomain
    years_of_experience: float
    skills: List[str] = Field(default_factory=list)
    
    @property
    def computed_experience_level(self) -> ExperienceLevel:
        if self.years_of_experience <= 2.5:
            return ExperienceLevel.BASICS
        elif self.years_of_experience <= 5.5:
            return ExperienceLevel.INTERMEDIATE
        return ExperienceLevel.ADVANCED
