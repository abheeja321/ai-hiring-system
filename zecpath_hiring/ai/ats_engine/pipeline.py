from zecpath_hiring.ai.ats_engine.scoring import calculate_ats_score, shortlist_band
from zecpath_hiring.ai.ats_engine.eligibility import evaluate_candidate_eligibility
from zecpath_hiring.ai.behavior_ai.service import run_behavior_analysis
from zecpath_hiring.ai.decision_ai.service import make_final_decision
from zecpath_hiring.ai.interview_ai.service import run_interview_intelligence
from zecpath_hiring.ai.screening_ai.service import run_screening
from zecpath_hiring.ai.integrity.malpractice_evaluator import MalpracticeEvaluator
from zecpath_hiring.ai.report_generator.generator import HiringIntelligenceReportGenerator
from zecpath_hiring.ai.utils.logging import get_logger


logger = get_logger("pipeline")


def run_hiring_pipeline(candidate: dict, job: dict) -> dict:
    logger.info("Starting hiring pipeline for %s against %s", candidate.get("full_name"), job.get("title"))
    ats = calculate_ats_score(candidate, job)
    eligibility = evaluate_candidate_eligibility(candidate, job, ats)
    try:
        screening = run_screening(candidate, job, eligibility)
    except Exception as e:
        logger.error(f"Screening failed: {e}")
        screening = {"screening_score": 0.0, "error": str(e)}
        
    try:
        interview = run_interview_intelligence(candidate, job)
    except Exception as e:
        logger.error(f"Interview intelligence failed: {e}")
        interview = {"interview_score": 0.0, "error": str(e)}
        
    try:
        behavior = run_behavior_analysis(candidate)
    except Exception as e:
        logger.error(f"Behavior analysis failed: {e}")
        behavior = {"behavior_score": 50.0, "error": str(e)}
    
    # Run Integrity Check
    try:
        # Pass the entire structured profile text so NLP can detect descriptive behavioral anomalies
        behavior_text = str(candidate)
        integrity_evaluator = MalpracticeEvaluator()
        integrity_report = integrity_evaluator.evaluate_session(signals=[], behavior_text=behavior_text)
        integrity_dict = integrity_report.model_dump() if hasattr(integrity_report, "model_dump") else (integrity_report.dict() if hasattr(integrity_report, "dict") else vars(integrity_report))
    except Exception as e:
        logger.error(f"Integrity check failed: {e}")
        integrity_dict = {"risk_level": "UNKNOWN", "integrity_score": 100.0, "flags": [f"Error: {e}"]}
    decision = make_final_decision(ats, screening, interview, behavior, integrity_dict)
    result = {
        "ats": {**ats, "shortlist_band": shortlist_band(ats["final_score"])},
        "eligibility": eligibility,
        "screening": screening,
        "interview": interview,
        "behavior": behavior,
        "integrity": integrity_dict,
        "decision": decision,
    }
    
    # Generate full intelligence report
    report_generator = HiringIntelligenceReportGenerator()
    full_report = report_generator.generate_report(candidate.get("full_name", "Unknown"), job.get("title", "Unknown"), result)
    result["intelligence_report"] = report_generator.export_to_dict(full_report)
    result["intelligence_report_markdown"] = report_generator.export_to_markdown(full_report)
    
    logger.info("Pipeline completed with decision %s and score %s", decision["decision"], decision["final_score"])
    return result
