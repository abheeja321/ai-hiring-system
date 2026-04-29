import unittest

from zecpath_hiring.ai.ats_engine.eligibility import evaluate_candidate_eligibility
from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text
from zecpath_hiring.ai.screening_ai.question_bank import build_screening_questions


class EligibilityTests(unittest.TestCase):
    def test_eligibility_marks_candidate_eligible_when_rules_match(self):
        candidate = parse_resume_text(
            "Asha Sharma",
            "Skills\nPython\nDjango\nSQL\nCommunication\nExperience\nAcme - Engineer 2020 2024",
        )
        candidate["contact"] = {"location": "Bengaluru"}
        candidate["availability"] = True
        job = parse_job_description(
            "Backend Engineer",
            "Need 3+ years experience with Python, Django, SQL and communication.",
        )
        ats = {"final_score": 82.0}
        result = evaluate_candidate_eligibility(
            candidate,
            job,
            ats,
            {
                "minimum_ats_score": 70,
                "allowed_locations": ["bengaluru"],
                "availability_required": True,
            },
        )
        self.assertEqual(result["status"], "ELIGIBLE")
        self.assertTrue(result["eligible_for_ai_screening_call"])

    def test_question_bank_returns_conversation_ready_objects(self):
        job = parse_job_description(
            "Backend Engineer",
            "Need 3+ years experience with Python, Django, SQL and communication.",
        )
        pack = build_screening_questions(job, {"status": "ELIGIBLE"})
        self.assertGreaterEqual(pack["question_count"], 5)
        self.assertIn("intro_001", pack["category_mapping"])

    def test_pipeline_contains_eligibility_stage(self):
        candidate = parse_resume_text(
            "Rohit Mehta",
            "Summary\nBackend engineer.\nSkills\nPython\nDjango\nSQL\nCommunication\nProjects\nBuilt an ATS platform.",
        )
        job = parse_job_description(
            "AI Hiring Engineer",
            "Looking for 4+ years with Python, Django, SQL and communication skills.",
        )
        result = run_hiring_pipeline(candidate, job)
        self.assertIn(result["eligibility"]["status"], {"ELIGIBLE", "REVIEW", "REJECTED"})
        self.assertIn("question_pack", result["screening"])
