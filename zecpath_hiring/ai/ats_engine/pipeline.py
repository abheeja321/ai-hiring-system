from zecpath_hiring.ai.ats_engine.scoring import calculate_ats_score, shortlist_band
from zecpath_hiring.ai.ats_engine.eligibility import evaluate_candidate_eligibility
from zecpath_hiring.ai.behavior_ai.service import run_behavior_analysis
from zecpath_hiring.ai.decision_ai.service import make_final_decision
from zecpath_hiring.ai.interview_ai.service import run_interview_intelligence
from zecpath_hiring.ai.screening_ai.service import run_screening
from zecpath_hiring.ai.utils.logging import get_logger


logger = get_logger("pipeline")


def run_hiring_pipeline(candidate: dict, job: dict) -> dict:
    logger.info("Starting hiring pipeline for %s against %s", candidate.get("full_name"), job.get("title"))
    ats = calculate_ats_score(candidate, job)
    eligibility = evaluate_candidate_eligibility(candidate, job, ats)
    screening = run_screening(candidate, job, eligibility)
    interview = run_interview_intelligence(candidate, job)
    behavior = run_behavior_analysis(candidate)
    decision = make_final_decision(ats, screening, interview, behavior)
    result = {
        "ats": {**ats, "shortlist_band": shortlist_band(ats["final_score"])},
        "eligibility": eligibility,
        "screening": screening,
        "interview": interview,
        "behavior": behavior,
        "decision": decision,
    }
    logger.info("Pipeline completed with decision %s and score %s", decision["decision"], decision["final_score"])
    return result
