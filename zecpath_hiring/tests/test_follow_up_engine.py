import pytest

from zecpath_hiring.ai.hr_interview.categories import ExperienceLevel, HRCategory, InterviewPhase, RoleType
from zecpath_hiring.ai.hr_interview.flow_controller import FlowController
from zecpath_hiring.ai.hr_interview.follow_up_engine import FollowUpEngine, FollowUpType
from zecpath_hiring.ai.hr_interview.state_manager import InterviewState


def test_follow_up_heuristics():
    engine = FollowUpEngine()
    
    # 1. Too short -> CLARIFICATION
    short_resp = "I did some stuff."
    assert engine.analyze_response(short_resp) == FollowUpType.CLARIFICATION
    
    # 2. Detailed and confident -> SCENARIO_BASED
    confident_resp = "I successfully led the backend team to migrate our architecture to microservices. We improved performance by 40% and achieved our quarterly goals ahead of schedule. The team managed to stay ahead of all sprint deadlines during the process."
    assert engine.analyze_response(confident_resp) == FollowUpType.SCENARIO_BASED
    
    # 3. Medium length, no strong action verbs -> DEEPENING
    medium_resp = "I was part of a team that built the new website. We used Django and React. It took us about 3 months to finish the whole thing and launch it to the public."
    assert engine.analyze_response(medium_resp) == FollowUpType.DEEPENING


def test_flow_controller_follow_up_integration():
    state = InterviewState(candidate_id=1, job_id=1)
    controller = FlowController(state, ExperienceLevel.EXPERIENCED, RoleType.TECHNICAL)
    
    # Move past Intro
    action1 = controller.determine_next_action()
    assert action1["category"] == HRCategory.SELF_INTRO.value
    controller.process_candidate_response("Hi, my name is John and I have 5 years of experience in backend development using Python and Django. I worked at XYZ Corp recently.", "Intro Context")
    
    # Now in CORE_HR phase
    action2 = controller.determine_next_action()
    assert action2["category"] == HRCategory.CAREER_JOURNEY.value
    assert state.current_phase == InterviewPhase.CORE_HR
    
    # Provide a short/vague response to trigger a follow-up
    vague_resp = "I worked on some stuff there."
    follow_up_action = controller.process_candidate_response(vague_resp, "Career journey")
    
    assert follow_up_action is not None
    assert follow_up_action["action"] == "follow_up"
    assert follow_up_action["follow_up_type"] == FollowUpType.CLARIFICATION.value
    
    # Provide another vague response. It should trigger the 2nd (and final allowed) follow up
    follow_up_action_2 = controller.process_candidate_response("Just regular backend stuff.", "Career journey")
    assert follow_up_action_2 is not None
    assert state.current_follow_up_count == 2
    
    # Provide a 3rd vague response. The state manager should block it and return None
    follow_up_action_3 = controller.process_candidate_response("More stuff.", "Career journey")
    assert follow_up_action_3 is None  # Blocked by max_follow_ups_per_category
    
    # Since follow up was None, determine_next_action moves to the next category
    action3 = controller.determine_next_action()
    assert action3["category"] == HRCategory.STRENGTHS_WEAKNESSES.value
    # Assert follow up count was reset
    assert state.current_follow_up_count == 0
