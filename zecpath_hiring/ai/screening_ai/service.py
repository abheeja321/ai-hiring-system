from zecpath_hiring.ai.screening_ai.conversation_flow import build_conversation_state_machine, next_conversation_action
from zecpath_hiring.ai.screening_ai.edge_cases import analyze_edge_case_risk, fallback_strategy
from zecpath_hiring.ai.screening_ai.reporting import build_screening_report
from zecpath_hiring.ai.screening_ai.question_bank import build_screening_questions
from zecpath_hiring.ai.screening_ai.scoring import aggregate_screening_scores, score_screening_answer
from zecpath_hiring.ai.screening_ai.signals import analyze_confidence_and_sentiment
from zecpath_hiring.ai.screening_ai.transcript_processing import build_clean_transcript
from zecpath_hiring.ai.screening_ai.understanding import understand_answer


def run_screening(candidate: dict, job: dict, eligibility: dict | None = None) -> dict:
    candidate_skills = {skill["name"] for skill in candidate.get("skills", [])}
    required_skills = set(job.get("required_skills", []))
    intent_alignment = 75 if candidate.get("summary") else 50
    communication_proxy = 85 if "communication" in candidate_skills else 65
    skill_readiness = round((len(candidate_skills & required_skills) / max(len(required_skills), 1)) * 100, 2)
    question_pack = build_screening_questions(job, eligibility)
    synthetic_answers = []
    for question in question_pack["questions"]:
        response_text = _mock_candidate_answer(question, candidate, job)
        transcript = build_clean_transcript(question["id"], response_text)
        understanding = understand_answer(question, transcript["normalized_text"])
        signal_analysis = analyze_confidence_and_sentiment(transcript, understanding)
        edge_case_risk = analyze_edge_case_risk(transcript, understanding)
        next_action = next_conversation_action(question, transcript, understanding, signal_analysis)
        score = score_screening_answer(question, transcript["normalized_text"], understanding)
        synthetic_answers.append(
            {
                "question": question,
                "transcript": transcript,
                "understanding": understanding,
                "signal_analysis": signal_analysis,
                "edge_case_risk": edge_case_risk,
                "next_action": next_action,
                "score": score,
            }
        )
    scored_screening = aggregate_screening_scores([item["score"] for item in synthetic_answers])
    avg_confidence = round(
        sum(item["signal_analysis"]["confidence_score"] for item in synthetic_answers) / max(len(synthetic_answers), 1),
        2,
    )
    screening_score = round(
        (scored_screening["screening_score"] + intent_alignment + communication_proxy + skill_readiness + avg_confidence) / 5,
        2,
    )
    result = {
        "screening_score": screening_score,
        "voice_screening_required": (eligibility or {}).get("eligible_for_ai_screening_call", True),
        "signals": {
            "intent_alignment": intent_alignment,
            "communication_proxy": communication_proxy,
            "skill_readiness": skill_readiness,
            "average_confidence_score": avg_confidence,
        },
        "question_pack": question_pack,
        "transcripts": [item["transcript"] for item in synthetic_answers],
        "understanding": [item["understanding"] for item in synthetic_answers],
        "signal_analysis": [item["signal_analysis"] for item in synthetic_answers],
        "conversation_actions": [item["next_action"] for item in synthetic_answers],
        "edge_case_analysis": [item["edge_case_risk"] for item in synthetic_answers],
        "fallback_actions": [fallback_strategy(item["edge_case_risk"]) for item in synthetic_answers],
        "score_breakdown": scored_screening,
        "conversation_flow": build_conversation_state_machine(),
    }
    result["screening_report"] = build_screening_report(candidate, job, result)
    return result


def _mock_candidate_answer(question: dict, candidate: dict, job: dict) -> str:
    category = question.get("category")
    skills = ", ".join(skill["name"] for skill in candidate.get("skills", [])[:4]) or "general skills"
    experience_years = round(sum(item.get("duration_months", 0) for item in candidate.get("experience", [])) / 12, 1)
    location = candidate.get("contact", {}).get("location", "remote")
    if category == "Introduction":
        return f"I am {candidate.get('full_name', 'the candidate')} and I have {experience_years} years of experience in {skills}."
    if category == "Education":
        return "I completed a bachelor's degree and it supports my problem solving and technical fundamentals."
    if category == "Experience":
        return f"I have {experience_years} years of experience and worked on projects related to {skills}."
    if category == "Skills":
        return f"My strongest skills are {skills} and I used them in recent delivery projects."
    if category == "Location":
        return f"I am based in {location} and open to the role requirements."
    if category == "Salary":
        return "My expected salary is 18 lpa based on the scope of this role."
    if category == "Notice period":
        return "My notice period is 30 days and I can join soon after."
    return candidate.get("summary", "I am interested in the role.")
