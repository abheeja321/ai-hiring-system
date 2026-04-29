import unittest

from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text
from zecpath_hiring.ai.screening_ai.conversation_flow import build_conversation_state_machine, next_conversation_action
from zecpath_hiring.ai.screening_ai.edge_cases import analyze_edge_case_risk, fallback_strategy
from zecpath_hiring.ai.screening_ai.reporting import build_screening_report
from zecpath_hiring.ai.screening_ai.service import run_screening
from zecpath_hiring.ai.screening_ai.signals import analyze_confidence_and_sentiment
from zecpath_hiring.ai.screening_ai.transcript_processing import build_clean_transcript
from zecpath_hiring.ai.screening_ai.understanding import understand_answer


class ScreeningAdvancedTests(unittest.TestCase):
    def test_confidence_and_sentiment_analysis_returns_behavioral_indicators(self):
        transcript = build_clean_transcript("intro_001", "I confidently built strong backend systems and delivered results.")
        understanding = understand_answer({"id": "intro_001", "category": "Introduction", "mandatory": True}, transcript["normalized_text"])
        result = analyze_confidence_and_sentiment(transcript, understanding)
        self.assertIn("behavioral_indicators", result)
        self.assertIn(result["communication_strength"], {"strong", "moderate", "weak"})

    def test_conversation_flow_requests_retry_on_silence(self):
        question = {"id": "intro_001", "category": "Introduction", "question": "Introduce yourself."}
        transcript = build_clean_transcript("intro_001", "")
        understanding = understand_answer({"id": "intro_001", "category": "Introduction", "mandatory": True}, "")
        signals = analyze_confidence_and_sentiment(transcript, understanding)
        action = next_conversation_action(question, transcript, understanding, signals)
        self.assertEqual(action["state"], "RETRY")

    def test_edge_case_strategy_handles_language_mixing(self):
        transcript = build_clean_transcript("loc_001", "Haan I am in Bengaluru and open to relocate.")
        understanding = understand_answer({"id": "loc_001", "category": "Location", "mandatory": True}, transcript["normalized_text"])
        risk = analyze_edge_case_risk(transcript, understanding)
        strategy = fallback_strategy(risk)
        self.assertEqual(strategy["action"], "clarify_language")

    def test_report_builder_returns_recruiter_ready_report(self):
        candidate = parse_resume_text(
            "Anita Rao",
            "Summary\nEngineer\nSkills\nPython\nDjango\nSQL\nCommunication\nExperience\nAcme - Engineer 2020 2024",
        )
        candidate["contact"] = {"location": "Bengaluru"}
        job = parse_job_description(
            "Backend Engineer",
            "Need 3+ years experience with Python, Django, SQL and communication.",
        )
        screening = run_screening(candidate, job, {"eligible_for_ai_screening_call": True, "status": "ELIGIBLE"})
        report = build_screening_report(candidate, job, screening)
        self.assertIn("strengths", report)
        self.assertIn("recommendation", report)

    def test_screening_service_includes_report_and_conversation_flow(self):
        candidate = parse_resume_text(
            "Vikram Shah",
            "Summary\nEngineer\nSkills\nPython\nDjango\nSQL\nCommunication\nExperience\nAcme - Engineer 2020 2024",
        )
        candidate["contact"] = {"location": "Bengaluru"}
        job = parse_job_description(
            "Backend Engineer",
            "Need 3+ years experience with Python, Django, SQL and communication.",
        )
        result = run_screening(candidate, job, {"eligible_for_ai_screening_call": True, "status": "ELIGIBLE"})
        self.assertIn("screening_report", result)
        self.assertIn("conversation_flow", result)
        self.assertEqual(result["conversation_flow"], build_conversation_state_machine())
