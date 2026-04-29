FLOW_STATES = {
    "START",
    "ASK_QUESTION",
    "WAIT_FOR_ANSWER",
    "CLARIFY",
    "RETRY",
    "FOLLOW_UP",
    "COMPLETE",
    "FAIL_SAFE",
}


def next_conversation_action(question: dict, transcript: dict, understanding: dict, signal_analysis: dict) -> dict:
    normalization = transcript.get("normalization", {})
    if normalization.get("silence_detected"):
        return {
            "state": "RETRY",
            "prompt": "I could not hear your answer clearly. Could you please repeat that?",
            "reason": "silence_detected",
        }
    if understanding.get("off_topic"):
        return {
            "state": "CLARIFY",
            "prompt": f"Let me rephrase the question about {question.get('category')}. {question.get('question')}",
            "reason": "off_topic_response",
        }
    if understanding.get("missing_information"):
        return {
            "state": "FOLLOW_UP",
            "prompt": _follow_up_prompt(question, understanding),
            "reason": "missing_information",
        }
    if signal_analysis.get("behavioral_indicators", {}).get("hesitation_risk") == "high":
        return {
            "state": "CLARIFY",
            "prompt": "Take your time. Could you answer once more in a simple way?",
            "reason": "hesitation_pattern",
        }
    if signal_analysis.get("contradictions"):
        return {
            "state": "FOLLOW_UP",
            "prompt": "I noticed two different signals in your answer. Could you confirm the correct one?",
            "reason": "possible_contradiction",
        }
    return {
        "state": "ASK_QUESTION",
        "prompt": "Proceed to the next question.",
        "reason": "answer_accepted",
    }


def build_conversation_state_machine() -> dict:
    return {
        "states": sorted(FLOW_STATES),
        "transitions": [
            {"from": "START", "to": "ASK_QUESTION", "when": "call begins"},
            {"from": "ASK_QUESTION", "to": "WAIT_FOR_ANSWER", "when": "question spoken"},
            {"from": "WAIT_FOR_ANSWER", "to": "RETRY", "when": "silence or poor audio detected"},
            {"from": "WAIT_FOR_ANSWER", "to": "CLARIFY", "when": "off-topic or confusion detected"},
            {"from": "WAIT_FOR_ANSWER", "to": "FOLLOW_UP", "when": "missing details or contradiction detected"},
            {"from": "WAIT_FOR_ANSWER", "to": "ASK_QUESTION", "when": "answer accepted"},
            {"from": "RETRY", "to": "FAIL_SAFE", "when": "retry limit exceeded"},
            {"from": "FOLLOW_UP", "to": "ASK_QUESTION", "when": "follow-up resolved"},
            {"from": "ASK_QUESTION", "to": "COMPLETE", "when": "all questions complete"},
        ],
        "fallback_questions": [
            "Could you answer that in one or two clear sentences?",
            "Could you share one concrete example?",
            "Could you confirm the exact number or timeframe?",
        ],
        "failure_logic": {
            "retry_limit": 2,
            "polite_failure_message": "We are having trouble capturing your answer. A recruiter may follow up manually.",
        },
    }


def _follow_up_prompt(question: dict, understanding: dict) -> str:
    missing = understanding.get("missing_information", [])
    if "salary_expectation_missing" in missing:
        return "Could you share your expected salary range for this role?"
    if "availability_missing" in missing:
        return "Could you confirm your notice period or earliest joining date?"
    if "skills_not_identified" in missing:
        return "Could you name the main skills you used most recently?"
    if "experience_duration_missing" in missing:
        return "Could you confirm how many years of relevant experience you have?"
    return f"Could you add a bit more detail for the {question.get('category')} question?"

