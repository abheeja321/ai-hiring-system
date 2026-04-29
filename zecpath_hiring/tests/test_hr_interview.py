import pytest

from zecpath_hiring.ai.hr_interview.categories import ExperienceLevel, HRCategory, InterviewPhase, RoleType
from zecpath_hiring.ai.hr_interview.flow_controller import FlowController
from zecpath_hiring.ai.hr_interview.question_bank import QuestionBank
from zecpath_hiring.ai.hr_interview.state_manager import InterviewState


def test_question_bank_modifiers():
    qb = QuestionBank(ExperienceLevel.FRESHER, RoleType.TECHNICAL)
    prompt = qb.generate_llm_prompt(HRCategory.TEAMWORK_CULTURE)
    
    assert "Focus on their academic projects" in prompt["prompt_content"]
    assert "code reviews" in prompt["prompt_content"]


def test_flow_controller_phases():
    state = InterviewState(candidate_id=1, job_id=1)
    controller = FlowController(state, ExperienceLevel.EXPERIENCED, RoleType.NON_TECHNICAL)

    # Phase: Intro
    assert state.current_phase == InterviewPhase.INTRODUCTION
    action1 = controller.determine_next_action()
    assert action1["category"] == HRCategory.SELF_INTRO.value
    assert state.current_phase == InterviewPhase.INTRODUCTION  # State stays until it moves to next phase in next turn

    # Call again to move to next category (simulating response received)
    action2 = controller.determine_next_action()
    assert state.current_phase == InterviewPhase.CORE_HR
    assert action2["category"] == HRCategory.CAREER_JOURNEY.value

    action3 = controller.determine_next_action()
    assert action3["category"] == HRCategory.STRENGTHS_WEAKNESSES.value

    action4 = controller.determine_next_action()
    assert action4["category"] == HRCategory.TEAMWORK_CULTURE.value

    # Phase: Role Based
    action5 = controller.determine_next_action()
    assert state.current_phase == InterviewPhase.ROLE_BASED
    assert action5["category"] == HRCategory.TEAMWORK_CULTURE.value  # Role based uses Teamwork deep dive
    assert "Focus deeply on the technical/domain aspects" in action5["system_instruction"]

    # Phase: Closing
    action6 = controller.determine_next_action()
    assert state.current_phase == InterviewPhase.CLOSING
    assert action6["category"] == HRCategory.CAREER_GOALS.value

    action7 = controller.determine_next_action()
    assert action7["category"] == HRCategory.AVAILABILITY_COMMITMENT.value

    # Phase: Completed
    action8 = controller.determine_next_action()
    assert state.current_phase == InterviewPhase.COMPLETED
    assert action8["action"] == "end"


def test_interview_state_recording():
    state = InterviewState(candidate_id=1, job_id=1)
    state.add_turn("AI", "Hello, please introduce yourself.", HRCategory.SELF_INTRO)
    state.add_turn("Candidate", "Hi, I am John...", HRCategory.SELF_INTRO)

    assert len(state.history) == 2
    assert state.history[0].speaker == "AI"
    assert state.history[1].speaker == "Candidate"
    assert state.history[0].category == HRCategory.SELF_INTRO
