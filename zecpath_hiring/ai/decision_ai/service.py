def make_final_decision(ats: dict, screening: dict, interview: dict, behavior: dict) -> dict:
    final_score = round(
        (ats["final_score"] * 0.4)
        + (screening["screening_score"] * 0.2)
        + (interview["interview_score"] * 0.25)
        + (behavior["behavior_score"] * 0.15),
        2,
    )
    if final_score >= 80:
        decision = "OFFER"
    elif final_score >= 65:
        decision = "FINAL_REVIEW"
    else:
        decision = "REJECT"
    return {
        "final_score": final_score,
        "decision": decision,
        "offer_automation_ready": decision == "OFFER",
    }

