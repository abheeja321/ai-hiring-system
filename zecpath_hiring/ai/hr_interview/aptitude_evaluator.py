import re
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .categories import ExperienceLevel, RoleType


class IdealAnswerStructure(BaseModel):
    """Recruiter-facing rubric for reasoning and situational answers."""

    expected_steps: List[str] = Field(default_factory=list)
    positive_signals: List[str] = Field(default_factory=list)
    risk_signals: List[str] = Field(default_factory=list)


class AptitudeQuestion(BaseModel):
    question_id: str
    question_type: str
    prompt: str
    ideal_answer: IdealAnswerStructure


class AptitudeEvaluation(BaseModel):
    logical_thinking_score: float
    problem_solving_clarity_score: float
    situational_judgment_score: float
    overall_aptitude_score: float
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    matched_structure: List[str] = Field(default_factory=list)
    missing_structure: List[str] = Field(default_factory=list)


class AptitudeEvaluator:
    """
    Designs and evaluates cognitive/situational HR interview questions.
    The evaluator is deterministic so it can be used in tests and as an LLM guardrail.
    """

    REASONING_MARKERS = {
        "because",
        "therefore",
        "if",
        "then",
        "assumption",
        "trade-off",
        "tradeoff",
        "evidence",
        "priority",
        "impact",
        "risk",
        "option",
    }
    CLARITY_MARKERS = {"first", "second", "finally", "step", "plan", "measure", "decide", "communicate"}
    STAKEHOLDER_MARKERS = {"manager", "team", "customer", "candidate", "client", "stakeholder", "hr", "recruiter"}

    def design_reasoning_questions(self, role_type: RoleType, experience_level: ExperienceLevel) -> List[AptitudeQuestion]:
        role_context = "engineering delivery" if role_type == RoleType.TECHNICAL else "business operations"
        experience_context = "project or internship" if experience_level == ExperienceLevel.FRESHER else "recent workplace"

        return [
            AptitudeQuestion(
                question_id="logic-prioritization-001",
                question_type="logical_reasoning",
                prompt=(
                    f"You have three urgent {role_context} tasks, but only time to complete one today. "
                    f"How would you decide which one to handle first? Explain your assumptions and trade-offs."
                ),
                ideal_answer=IdealAnswerStructure(
                    expected_steps=["identify constraints", "compare impact", "state assumptions", "choose action"],
                    positive_signals=["uses evidence", "prioritizes business impact", "explains trade-offs"],
                    risk_signals=["jumps to an answer", "ignores constraints", "does not explain reasoning"],
                ),
            ),
            AptitudeQuestion(
                question_id="logic-root-cause-002",
                question_type="logical_reasoning",
                prompt=(
                    f"Think of a {experience_context} problem where the obvious cause was not the real cause. "
                    "How would you investigate it before recommending a solution?"
                ),
                ideal_answer=IdealAnswerStructure(
                    expected_steps=["define the problem", "gather data", "test possible causes", "recommend next step"],
                    positive_signals=["separates facts from assumptions", "tests alternatives", "keeps stakeholders informed"],
                    risk_signals=["blames people quickly", "skips validation", "uses vague examples"],
                ),
            ),
        ]

    def build_situational_scenarios(self, role_type: RoleType, experience_level: ExperienceLevel) -> List[AptitudeQuestion]:
        role_conflict = (
            "a senior engineer asks you to ship a shortcut that may create technical debt"
            if role_type == RoleType.TECHNICAL
            else "a client asks for a commitment your team may not be able to meet"
        )
        seniority = "mentor or manager" if experience_level == ExperienceLevel.FRESHER else "manager and cross-functional partners"

        return [
            AptitudeQuestion(
                question_id="sjt-ethics-001",
                question_type="situational_judgment",
                prompt=(
                    f"You notice {role_conflict}. What would you do, who would you involve, "
                    "and how would you communicate the decision?"
                ),
                ideal_answer=IdealAnswerStructure(
                    expected_steps=["clarify facts", "assess risk", f"involve {seniority}", "communicate transparently"],
                    positive_signals=["balances urgency and ethics", "protects team trust", "documents decision"],
                    risk_signals=["hides the issue", "escalates without facts", "accepts risk without mitigation"],
                ),
            )
        ]

    def evaluate_response(self, response: str, ideal_answer: IdealAnswerStructure) -> AptitudeEvaluation:
        text = response.strip()
        tokens = re.findall(r"\b[\w-]+\b", text.lower())
        token_set = set(tokens)

        matched_steps = self._matched_structure(text, ideal_answer.expected_steps)
        missing_steps = [step for step in ideal_answer.expected_steps if step not in matched_steps]

        reasoning_score = self._score_marker_coverage(token_set, self.REASONING_MARKERS, 55.0)
        reasoning_score += min(25.0, len(matched_steps) * 7.0)
        reasoning_score += 20.0 if len(tokens) >= 45 else max(0.0, len(tokens) / 45.0 * 20.0)

        clarity_score = self._score_marker_coverage(token_set, self.CLARITY_MARKERS, 45.0)
        clarity_score += min(35.0, len(matched_steps) * 9.0)
        clarity_score += 20.0 if self._has_clear_conclusion(text) else 5.0

        situational_score = self._score_marker_coverage(token_set, self.STAKEHOLDER_MARKERS, 35.0)
        situational_score += min(35.0, len(matched_steps) * 8.0)
        situational_score += 30.0 if any(word in token_set for word in {"risk", "impact", "communicate", "document"}) else 10.0

        strengths = self._collect_strengths(token_set, matched_steps)
        weaknesses = self._collect_weaknesses(tokens, missing_steps)
        risk_flags = self._collect_risks(text, tokens, missing_steps, ideal_answer.risk_signals)

        logical = round(min(100.0, reasoning_score), 1)
        clarity = round(min(100.0, clarity_score), 1)
        situational = round(min(100.0, situational_score), 1)
        overall = round((logical * 0.45) + (clarity * 0.35) + (situational * 0.20), 1)

        return AptitudeEvaluation(
            logical_thinking_score=logical,
            problem_solving_clarity_score=clarity,
            situational_judgment_score=situational,
            overall_aptitude_score=overall,
            strengths=strengths,
            weaknesses=weaknesses,
            risk_flags=risk_flags,
            matched_structure=matched_steps,
            missing_structure=missing_steps,
        )

    def build_design(self, role_type: RoleType, experience_level: ExperienceLevel) -> Dict[str, Any]:
        reasoning_questions = self.design_reasoning_questions(role_type, experience_level)
        scenarios = self.build_situational_scenarios(role_type, experience_level)
        return {
            "aptitude_ai_design": {
                "reasoning_questions": [question.model_dump() for question in reasoning_questions],
                "situational_scenarios": [scenario.model_dump() for scenario in scenarios],
            },
            "logical_reasoning_scoring_model": {
                "logical_thinking": "45% of overall aptitude score; checks assumptions, evidence, trade-offs, and conclusion quality.",
                "problem_solving_clarity": "35% of overall aptitude score; checks structured steps, concise explanation, and actionability.",
                "situational_judgment": "20% of overall aptitude score; checks stakeholder awareness, risk handling, and communication.",
            },
            "scenario_evaluation_framework": {
                "ideal_answer_structure": ["clarify facts", "assess impact", "compare options", "communicate decision"],
                "positive_signals": ["balanced judgment", "transparent communication", "evidence-based decisions"],
                "risk_flags": ["unsupported conclusions", "missing stakeholders", "no risk mitigation"],
            },
        }

    def _matched_structure(self, text: str, expected_steps: List[str]) -> List[str]:
        lowered = text.lower()
        matched = []
        for step in expected_steps:
            words = [word for word in re.findall(r"\b\w+\b", step.lower()) if len(word) > 3]
            if any(word in lowered for word in words):
                matched.append(step)
        return matched

    def _score_marker_coverage(self, token_set: set[str], markers: set[str], max_score: float) -> float:
        matches = sum(1 for marker in markers if marker in token_set)
        return min(max_score, (matches / 5.0) * max_score)

    def _has_clear_conclusion(self, text: str) -> bool:
        lowered = text.lower()
        return any(phrase in lowered for phrase in ["i would", "my decision", "therefore", "so i would", "i will"])

    def _collect_strengths(self, token_set: set[str], matched_steps: List[str]) -> List[str]:
        strengths = []
        if {"because", "impact"} & token_set:
            strengths.append("Explains reasoning with impact awareness.")
        if {"risk", "communicate"} & token_set:
            strengths.append("Shows risk and stakeholder communication awareness.")
        if len(matched_steps) >= 3:
            strengths.append("Follows a structured problem-solving path.")
        return strengths

    def _collect_weaknesses(self, tokens: List[str], missing_steps: List[str]) -> List[str]:
        weaknesses = []
        if len(tokens) < 35:
            weaknesses.append("Answer is too brief to fully assess reasoning depth.")
        if missing_steps:
            weaknesses.append(f"Missing expected structure: {', '.join(missing_steps)}.")
        return weaknesses

    def _collect_risks(
        self,
        text: str,
        tokens: List[str],
        missing_steps: List[str],
        configured_risks: List[str],
    ) -> List[str]:
        risk_flags = []
        lowered = text.lower()
        if len(missing_steps) >= 2:
            risk_flags.append("Problem-solving structure is incomplete.")
        if not any(token in {"because", "evidence", "data", "assumption"} for token in tokens):
            risk_flags.append("Conclusion may be unsupported by evidence.")
        for risk in configured_risks:
            risk_text = risk.lower().rstrip(".")
            if risk_text in lowered:
                risk_flags.append(risk.capitalize() + ".")
        return list(dict.fromkeys(risk_flags))
