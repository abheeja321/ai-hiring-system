ATS_SERVICE_IO = {
    "receives": ["candidate_profile", "job_profile", "resume_text", "model_version"],
    "processes": ["parsing", "skill extraction", "semantic match", "scoring", "ranking"],
    "returns": ["ats_score", "section_tags", "shortlist_band", "explanation"],
}

SCREENING_SERVICE_IO = {
    "receives": ["candidate_profile", "job_profile", "ats_score", "voice_transcript"],
    "processes": ["voice screening", "communication analysis", "fit checks"],
    "returns": ["screening_score", "red_flags", "screening_summary"],
}

INTERVIEW_SERVICE_IO = {
    "receives": ["candidate_profile", "job_profile", "screening_report", "interview_transcript"],
    "processes": ["hr interview AI", "technical interview AI", "machine test AI"],
    "returns": ["interview_score", "question performance", "technical depth summary"],
}

BEHAVIOR_SERVICE_IO = {
    "receives": ["candidate_profile", "transcripts", "interaction_metadata"],
    "processes": ["behavior signals", "fairness checks", "bias reduction"],
    "returns": ["behavior_score", "fairness_report"],
}

DECISION_SERVICE_IO = {
    "receives": ["ats_score", "screening_score", "interview_score", "behavior_score"],
    "processes": ["final ranking", "thresholding", "explainability generation"],
    "returns": ["final_score", "decision", "offer_automation_ready"],
}

