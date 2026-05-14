from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str = Field(default="Unknown Candidate")
    role: str = Field(default="Unknown Role")

class ModuleSummary(BaseModel):
    ats_score: float = Field(default=0.0)
    screening_score: float = Field(default=0.0)
    interview_score: float = Field(default=0.0)
    behavior_score: float = Field(default=0.0)
    integrity_score: float = Field(default=100.0)

class KeyInsights(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    risk_indicators: List[str] = Field(default_factory=list)

class Recommendation(BaseModel):
    decision: str = Field(default="REJECTED")
    confidence_score: float = Field(default=0.0)
    explanation: str = Field(default="")
    automation_ready: bool = Field(default=False)

class FullCandidateReport(BaseModel):
    candidate: CandidateProfile
    scores: ModuleSummary
    insights: KeyInsights
    recommendation: Recommendation
    raw_data: Optional[Dict[str, Any]] = None
