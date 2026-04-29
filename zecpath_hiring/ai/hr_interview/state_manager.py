from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

from .categories import InterviewPhase, HRCategory


class InterviewTurn(BaseModel):
    turn_id: int
    speaker: str  # "AI" or "Candidate"
    category: Optional[HRCategory] = None
    content: str


class InterviewState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_id: int
    job_id: int
    current_phase: InterviewPhase = InterviewPhase.INTRODUCTION
    history: List[InterviewTurn] = Field(default_factory=list)
    asked_categories: List[HRCategory] = Field(default_factory=list)
    
    # State tracking
    can_follow_up: bool = True
    current_follow_up_count: int = 0
    max_follow_ups_per_category: int = 1

    def add_turn(self, speaker: str, content: str, category: Optional[HRCategory] = None):
        turn_id = len(self.history) + 1
        turn = InterviewTurn(
            turn_id=turn_id,
            speaker=speaker,
            category=category,
            content=content
        )
        self.history.append(turn)

    def mark_category_asked(self, category: HRCategory):
        if category not in self.asked_categories:
            self.asked_categories.append(category)
            self.current_follow_up_count = 0  # Reset follow-ups for new category
