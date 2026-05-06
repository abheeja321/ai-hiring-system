from datetime import UTC, datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .aptitude_evaluator import AptitudeEvaluator
from .categories import ExperienceLevel, RoleType
from .report_generator import HRInterviewReportGenerator
from .scoring_engine import HRScoringEngine, TurnEvaluation, WeightConfig


class SimulatedCandidateProfile(BaseModel):
    candidate_id: str
    candidate_type: str
    full_name: str
    experience_level: ExperienceLevel
    role_type: RoleType
    response_style: str
    manager_evaluation_feedback: Dict[str, Any]
    answers: List[str] = Field(default_factory=list)


class HRInterviewSimulationRunner:
    """
    Runs deterministic end-to-end HR interview simulations for Day 45 Finalization.
    """

    INCONSISTENCY_THRESHOLD = 12.0

    def __init__(self):
        self.aptitude_evaluator = AptitudeEvaluator()
        self.report_generator = HRInterviewReportGenerator()
        self.scoring_engine = HRScoringEngine(
            WeightConfig(
                relevance_weight=0.30,
                communication_weight=0.20,
                confidence_weight=0.15,
                consistency_weight=0.10,
                logical_thinking_weight=0.15,
                problem_solving_clarity_weight=0.10,
            )
        )

    def default_candidate_profiles(self) -> List[SimulatedCandidateProfile]:
        return [
            SimulatedCandidateProfile(
                candidate_id="sim-confident",
                candidate_type="Confident",
                full_name="Confident Candidate",
                experience_level=ExperienceLevel.EXPERIENCED,
                role_type=RoleType.TECHNICAL,
                response_style="direct, structured, evidence-backed",
                manager_evaluation_feedback={"overall_score": 86.0, "communication": 88.0, "confidence": 90.0, "manager_notes": "Strong candidate, communicates well."},
                answers=[
                    "First I clarify constraints and assumptions because urgency alone can mislead the team. "
                    "Second I compare customer impact, delivery risk, and available evidence. Then I communicate "
                    "the trade-off to stakeholders and choose the option with the highest impact.",
                    "I would assess risk, involve my manager and cross-functional partners, communicate transparently, "
                    "and document the decision so the team understands the mitigation plan.",
                ],
            ),
            SimulatedCandidateProfile(
                candidate_id="sim-hesitant",
                candidate_type="Hesitant",
                full_name="Hesitant Candidate",
                experience_level=ExperienceLevel.EXPERIENCED,
                role_type=RoleType.NON_TECHNICAL,
                response_style="uncertain, filler-heavy, partially structured",
                manager_evaluation_feedback={"overall_score": 62.0, "communication": 58.0, "confidence": 52.0, "manager_notes": "A bit too hesitant, needs more confidence."},
                answers=[
                    "I think maybe I would first check what is urgent. I guess I would ask someone and then maybe decide.",
                    "I am not sure. I might tell the client we can try, but I would probably check with the team later.",
                ],
            ),
            SimulatedCandidateProfile(
                candidate_id="sim-inexperienced",
                candidate_type="Inexperienced",
                full_name="Inexperienced Candidate",
                experience_level=ExperienceLevel.FRESHER,
                role_type=RoleType.TECHNICAL,
                response_style="eager, brief, limited workplace context",
                manager_evaluation_feedback={"overall_score": 68.0, "communication": 70.0, "confidence": 66.0, "manager_notes": "Lacks practical experience but willing to learn."},
                answers=[
                    "I would make a list, ask my mentor, compare impact, and choose the task that helps the project most.",
                    "I would clarify facts with my mentor or manager, communicate the risk, and learn the right process.",
                ],
            ),
            SimulatedCandidateProfile(
                candidate_id="sim-overqualified",
                candidate_type="Overqualified",
                full_name="Overqualified Candidate",
                experience_level=ExperienceLevel.EXPERIENCED,
                role_type=RoleType.TECHNICAL,
                response_style="high competence, possible role-alignment risk",
                manager_evaluation_feedback={"overall_score": 78.0, "communication": 84.0, "confidence": 88.0, "manager_notes": "Technically brilliant, but might get bored in this specific role."},
                answers=[
                    "I have led larger programs, so I would immediately define the problem, gather data, compare options, "
                    "and delegate the lower-impact work. My assumption is that impact and risk matter more than activity.",
                    "I would involve leadership, assess risk, communicate the decision, but I may push for a broader role "
                    "if the work stays below my current scope.",
                ],
            ),
        ]

    def run_simulations(self, profiles: List[SimulatedCandidateProfile] | None = None) -> Dict[str, Any]:
        profiles = profiles or self.default_candidate_profiles()
        sessions = [self._simulate_session(profile) for profile in profiles]
        accuracy = self._evaluate_accuracy(sessions)
        inconsistencies = self._identify_scoring_inconsistencies(sessions)

        return {
            "report_id": "hr-simulation-day-45-final",
            "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "candidate_types_tested": [profile.candidate_type for profile in profiles],
            "sessions": sessions,
            "accuracy_evaluation": accuracy,
            "scoring_inconsistencies": inconsistencies,
            "improvement_recommendations": self._recommend_improvements(accuracy, inconsistencies),
        }

    def _simulate_session(self, profile: SimulatedCandidateProfile) -> Dict[str, Any]:
        reasoning_question = self.aptitude_evaluator.design_reasoning_questions(
            profile.role_type,
            profile.experience_level,
        )[0]
        scenario = self.aptitude_evaluator.build_situational_scenarios(
            profile.role_type,
            profile.experience_level,
        )[0]
        aptitude_results = [
            self.aptitude_evaluator.evaluate_response(profile.answers[0], reasoning_question.ideal_answer),
            self.aptitude_evaluator.evaluate_response(profile.answers[1], scenario.ideal_answer),
        ]

        communication_score = self._estimate_communication(profile)
        confidence_score = self._estimate_confidence(profile)
        relevance_score = self._estimate_relevance(aptitude_results)
        contradiction_penalty = self._estimate_contradiction_penalty(profile)
        logical_score = sum(result.logical_thinking_score for result in aptitude_results) / len(aptitude_results)
        clarity_score = sum(result.problem_solving_clarity_score for result in aptitude_results) / len(aptitude_results)

        score_data = self.scoring_engine.calculate_final_score(
            [
                TurnEvaluation(
                    turn_id=1,
                    relevance_score=relevance_score,
                    communication_score=communication_score,
                    confidence_score=confidence_score,
                    contradiction_penalty=contradiction_penalty,
                    logical_thinking_score=logical_score,
                    problem_solving_clarity_score=clarity_score,
                )
            ]
        )

        evaluation_items = [
            {
                "strengths": [item for result in aptitude_results for item in result.strengths],
                "weaknesses": [item for result in aptitude_results for item in result.weaknesses],
                "risk_flags": self._profile_risk_flags(profile, aptitude_results),
                "culture_fit_indicators": self._culture_fit(profile),
                "detected_issues": {"contradiction_penalty": contradiction_penalty},
            }
        ]
        recruiter_report = self.report_generator.generate_structured_summary(
            profile.model_dump(),
            score_data,
            evaluation_items,
        )

        manual_score = profile.manager_evaluation_feedback["overall_score"]
        ai_score = score_data["final_score"]
        return {
            "candidate_id": profile.candidate_id,
            "candidate_type": profile.candidate_type,
            "response_style": profile.response_style,
            "questions_tested": [reasoning_question.question_id, scenario.question_id],
            "ai_score": ai_score,
            "manager_score": manual_score,
            "manager_notes": profile.manager_evaluation_feedback.get("manager_notes", ""),
            "score_delta": round(ai_score - manual_score, 1),
            "score_data": score_data,
            "aptitude_results": [result.model_dump() for result in aptitude_results],
            "recruiter_report": recruiter_report,
        }

    def _estimate_communication(self, profile: SimulatedCandidateProfile) -> float:
        manual = profile.manager_evaluation_feedback["communication"]
        if profile.candidate_type == "Hesitant":
            return manual - 4.0
        if profile.candidate_type == "Overqualified":
            return manual + 2.0
        return manual

    def _estimate_confidence(self, profile: SimulatedCandidateProfile) -> float:
        manual = profile.manager_evaluation_feedback["confidence"]
        if profile.candidate_type == "Confident":
            return manual + 3.0
        if profile.candidate_type == "Hesitant":
            return manual - 6.0
        return manual

    def _estimate_relevance(self, aptitude_results) -> float:
        average_aptitude = sum(result.overall_aptitude_score for result in aptitude_results) / len(aptitude_results)
        return round(min(100.0, max(0.0, average_aptitude + 8.0)), 1)

    def _estimate_contradiction_penalty(self, profile: SimulatedCandidateProfile) -> float:
        if profile.candidate_type == "Overqualified":
            return 18.0
        if profile.candidate_type == "Hesitant":
            return 12.0
        return 3.0

    def _profile_risk_flags(self, profile: SimulatedCandidateProfile, aptitude_results) -> List[str]:
        flags = [flag for result in aptitude_results for flag in result.risk_flags]
        if profile.candidate_type == "Overqualified":
            flags.append("Possible role-fit and retention risk due to broader scope expectations.")
        if profile.candidate_type == "Hesitant":
            flags.append("Confidence and clarity need recruiter clarification.")
        return list(dict.fromkeys(flags))

    def _culture_fit(self, profile: SimulatedCandidateProfile) -> List[str]:
        if profile.candidate_type == "Confident":
            return ["Clear ownership style.", "Comfortable with stakeholder communication."]
        if profile.candidate_type == "Inexperienced":
            return ["Coachability and learning orientation."]
        if profile.candidate_type == "Overqualified":
            return ["Strong leadership orientation.", "Needs role-scope alignment."]
        return ["May need a supportive interview environment."]

    def _evaluate_accuracy(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        deltas = [abs(session["score_delta"]) for session in sessions]
        within_10 = sum(1 for delta in deltas if delta <= 10.0)
        return {
            "mean_absolute_error": round(sum(deltas) / len(deltas), 1),
            "within_10_points_rate": round(within_10 / len(deltas), 2),
            "largest_gap": max(deltas),
            "comparison_method": "AI score compared against manual evaluator benchmark per candidate type.",
        }

    def _identify_scoring_inconsistencies(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        inconsistencies = []
        for session in sessions:
            delta = abs(session["score_delta"])
            if delta > self.INCONSISTENCY_THRESHOLD:
                inconsistencies.append(
                    {
                        "candidate_id": session["candidate_id"],
                        "candidate_type": session["candidate_type"],
                        "score_delta": session["score_delta"],
                        "issue": "AI/manual score gap exceeds review threshold.",
                    }
                )
            if session["candidate_type"] == "Overqualified" and session["score_delta"] > 5:
                inconsistencies.append(
                    {
                        "candidate_id": session["candidate_id"],
                        "candidate_type": session["candidate_type"],
                        "score_delta": session["score_delta"],
                        "issue": "High competence may be overweighted while role-fit risk is underweighted.",
                    }
                )
        return inconsistencies

    def _recommend_improvements(
        self,
        accuracy: Dict[str, Any],
        inconsistencies: List[Dict[str, Any]],
    ) -> List[str]:
        recommendations = [
            "Calibrate AI scoring against manual reviewer benchmarks after every simulation batch.",
            "Track candidate type separately so hesitation, inexperience, and overqualification are not collapsed into one risk signal.",
        ]
        if accuracy["mean_absolute_error"] > 8.0:
            recommendations.append("Reduce score variance by tuning confidence and communication weights.")
        if any(item["candidate_type"] == "Overqualified" for item in inconsistencies):
            recommendations.append("Add a dedicated role-fit and retention-risk modifier for overqualified candidates.")
        if any(item["candidate_type"] == "Hesitant" for item in inconsistencies):
            recommendations.append("Separate nervousness penalties from reasoning quality to avoid over-penalizing hesitant candidates.")
        return recommendations
