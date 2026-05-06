from zecpath_hiring.ai.hr_interview.aptitude_evaluator import AptitudeEvaluator
from zecpath_hiring.ai.hr_interview.categories import ExperienceLevel, RoleType


def test_aptitude_design_contains_reasoning_and_scenarios():
    evaluator = AptitudeEvaluator()

    design = evaluator.build_design(RoleType.TECHNICAL, ExperienceLevel.EXPERIENCED)

    assert design["aptitude_ai_design"]["reasoning_questions"]
    assert design["aptitude_ai_design"]["situational_scenarios"]
    assert "logical_thinking" in design["logical_reasoning_scoring_model"]
    assert "risk_flags" in design["scenario_evaluation_framework"]


def test_evaluate_response_scores_structured_reasoning_high():
    evaluator = AptitudeEvaluator()
    question = evaluator.design_reasoning_questions(RoleType.TECHNICAL, ExperienceLevel.EXPERIENCED)[0]
    response = (
        "First I would identify constraints and assumptions because time is limited. "
        "Second, I would compare each option by customer impact, delivery risk, and evidence from the team. "
        "Then I would communicate the trade-off to stakeholders and choose the task with the highest impact. "
        "Finally, I would document the decision and measure whether the plan solved the problem."
    )

    result = evaluator.evaluate_response(response, question.ideal_answer)

    assert result.logical_thinking_score >= 80
    assert result.problem_solving_clarity_score >= 80
    assert result.overall_aptitude_score >= 80
    assert result.risk_flags == []


def test_evaluate_response_flags_unclear_answer():
    evaluator = AptitudeEvaluator()
    question = evaluator.design_reasoning_questions(RoleType.NON_TECHNICAL, ExperienceLevel.FRESHER)[0]

    result = evaluator.evaluate_response("I will just do what feels urgent.", question.ideal_answer)

    assert result.overall_aptitude_score < 60
    assert result.missing_structure
    assert "Conclusion may be unsupported by evidence." in result.risk_flags
