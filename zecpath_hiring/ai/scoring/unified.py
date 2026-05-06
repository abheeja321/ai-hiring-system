from datetime import UTC, datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from zecpath_hiring.ai.hr_interview.categories import RoleType


class CrossRoundWeights(BaseModel):
    ats_weight: float = 0.35
    screening_weight: float = 0.25
    hr_interview_weight: float = 0.40

    def normalized(self) -> "CrossRoundWeights":
        total = self.ats_weight + self.screening_weight + self.hr_interview_weight
        if total <= 0:
            return CrossRoundWeights()
        return CrossRoundWeights(
            ats_weight=round(self.ats_weight / total, 4),
            screening_weight=round(self.screening_weight / total, 4),
            hr_interview_weight=round(self.hr_interview_weight / total, 4),
        )


class UnifiedCandidateScore(BaseModel):
    candidate_id: str | int | None = None
    role_type: str
    hiring_fit_percentage: float
    decision_band: str
    recommendation: str
    input_scores: Dict[str, float]
    applied_weights: Dict[str, float]
    weighted_contributions: Dict[str, float]
    role_adjustments: Dict[str, float]
    risk_flags: List[str] = Field(default_factory=list)
    generated_at: str


class UnifiedScoringEngine:
    """
    Combines ATS, screening, and HR interview rounds into one hiring-fit score.
    """

    DEFAULT_WEIGHTS = CrossRoundWeights()

    ROLE_ADJUSTMENTS = {
        RoleType.TECHNICAL.value: {
            "ats_weight": 0.05,
            "screening_weight": -0.05,
            "hr_interview_weight": 0.0,
        },
        RoleType.NON_TECHNICAL.value: {
            "ats_weight": -0.05,
            "screening_weight": 0.03,
            "hr_interview_weight": 0.02,
        },
        "Leadership": {
            "ats_weight": -0.05,
            "screening_weight": 0.0,
            "hr_interview_weight": 0.05,
        },
        "Fresher": {
            "ats_weight": -0.05,
            "screening_weight": 0.05,
            "hr_interview_weight": 0.0,
        },
    }

    def calculate_unified_score(
        self,
        candidate: Dict[str, Any],
        ats: Dict[str, Any],
        screening: Dict[str, Any],
        hr_interview: Dict[str, Any],
        role_type: RoleType | str = RoleType.TECHNICAL,
        weights: CrossRoundWeights | None = None,
    ) -> UnifiedCandidateScore:
        base_weights = weights or self.DEFAULT_WEIGHTS
        role_name = role_type.value if isinstance(role_type, RoleType) else str(role_type)
        adjusted_weights = self.apply_role_adjustments(base_weights, role_name)
        input_scores = {
            "ats_score": self._extract_score(ats, ["final_score", "ats_score"]),
            "screening_score": self._extract_score(screening, ["screening_score", "final_score"]),
            "hr_interview_score": self._extract_score(
                hr_interview,
                ["final_score", "interview_score", "overall_hr_score"],
            ),
        }
        weighted_contributions = {
            "ats": round(input_scores["ats_score"] * adjusted_weights.ats_weight, 2),
            "screening": round(input_scores["screening_score"] * adjusted_weights.screening_weight, 2),
            "hr_interview": round(input_scores["hr_interview_score"] * adjusted_weights.hr_interview_weight, 2),
        }
        hiring_fit = round(sum(weighted_contributions.values()), 2)
        risk_flags = self._risk_flags(input_scores, hiring_fit)

        return UnifiedCandidateScore(
            candidate_id=candidate.get("candidate_id") or candidate.get("id"),
            role_type=role_name,
            hiring_fit_percentage=hiring_fit,
            decision_band=self._decision_band(hiring_fit),
            recommendation=self._recommendation(hiring_fit, risk_flags),
            input_scores=input_scores,
            applied_weights=adjusted_weights.model_dump(),
            weighted_contributions=weighted_contributions,
            role_adjustments=self.ROLE_ADJUSTMENTS.get(role_name, {}),
            risk_flags=risk_flags,
            generated_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        )

    def calculate_hiring_fit_percentage(
        self,
        ats_score: float,
        screening_score: float,
        hr_interview_score: float,
        role_type: RoleType | str = RoleType.TECHNICAL,
        weights: CrossRoundWeights | None = None,
    ) -> float:
        score = self.calculate_unified_score(
            {},
            {"final_score": ats_score},
            {"screening_score": screening_score},
            {"final_score": hr_interview_score},
            role_type=role_type,
            weights=weights,
        )
        return score.hiring_fit_percentage

    def apply_role_adjustments(self, weights: CrossRoundWeights, role_name: str) -> CrossRoundWeights:
        adjustments = self.ROLE_ADJUSTMENTS.get(role_name, {})
        adjusted = CrossRoundWeights(
            ats_weight=max(0.0, weights.ats_weight + adjustments.get("ats_weight", 0.0)),
            screening_weight=max(0.0, weights.screening_weight + adjustments.get("screening_weight", 0.0)),
            hr_interview_weight=max(0.0, weights.hr_interview_weight + adjustments.get("hr_interview_weight", 0.0)),
        )
        return adjusted.normalized()

    def build_weight_system(self) -> Dict[str, Any]:
        return {
            "default_weights": self.DEFAULT_WEIGHTS.model_dump(),
            "role_based_adjustments": self.ROLE_ADJUSTMENTS,
            "rounds": {
                "ats": "Resume/job alignment, skill match, experience relevance, and education alignment.",
                "screening": "Pre-interview answer clarity, relevance, completeness, consistency, and intent fit.",
                "hr_interview": "Recruiter interview performance, communication, confidence, consistency, and aptitude logic.",
            },
        }

    def _extract_score(self, score_payload: Dict[str, Any], keys: List[str]) -> float:
        for key in keys:
            if key in score_payload:
                return self._clamp(float(score_payload.get(key) or 0.0))
        return 0.0

    def _clamp(self, value: float) -> float:
        return round(max(0.0, min(100.0, value)), 2)

    def _decision_band(self, hiring_fit: float) -> str:
        if hiring_fit >= 85:
            return "Strong hire"
        if hiring_fit >= 75:
            return "Hire"
        if hiring_fit >= 65:
            return "Final review"
        if hiring_fit >= 55:
            return "Hold"
        return "Reject"

    def _recommendation(self, hiring_fit: float, risk_flags: List[str]) -> str:
        if hiring_fit >= 80 and not risk_flags:
            return "Advance confidently."
        if hiring_fit >= 70:
            return "Advance with recruiter validation."
        if hiring_fit >= 60:
            return "Manual review required before advancing."
        return "Do not advance without substantial new evidence."

    def _risk_flags(self, input_scores: Dict[str, float], hiring_fit: float) -> List[str]:
        flags = []
        if input_scores["ats_score"] < 60:
            flags.append("ATS score is below baseline fit threshold.")
        if input_scores["screening_score"] < 60:
            flags.append("Screening score indicates weak pre-interview signal.")
        if input_scores["hr_interview_score"] < 60:
            flags.append("HR interview score indicates weak live interview performance.")
        score_spread = max(input_scores.values()) - min(input_scores.values())
        if score_spread >= 30:
            flags.append("Cross-round scores are inconsistent and need recruiter review.")
        if hiring_fit < 65:
            flags.append("Hiring fit is below final-review threshold.")
        return flags
