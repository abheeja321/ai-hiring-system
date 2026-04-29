from enum import Enum


class HRCategory(str, Enum):
    SELF_INTRO = "Self-introduction"
    CAREER_JOURNEY = "Career journey"
    STRENGTHS_WEAKNESSES = "Strengths & weaknesses"
    TEAMWORK_CULTURE = "Teamwork & culture fit"
    CAREER_GOALS = "Career goals"
    AVAILABILITY_COMMITMENT = "Availability & commitment"


class ExperienceLevel(str, Enum):
    FRESHER = "Fresher"
    EXPERIENCED = "Experienced"


class RoleType(str, Enum):
    TECHNICAL = "Technical"
    NON_TECHNICAL = "Non-technical"


class InterviewPhase(str, Enum):
    INTRODUCTION = "Introduction"
    CORE_HR = "Core HR"
    ROLE_BASED = "Role-based evaluation"
    CLOSING = "Closing"
    COMPLETED = "Completed"
