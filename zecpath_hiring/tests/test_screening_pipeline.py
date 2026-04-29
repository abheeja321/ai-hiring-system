import unittest

from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text
from zecpath_hiring.ai.screening_ai.scoring import aggregate_screening_scores, score_screening_answer
from zecpath_hiring.ai.screening_ai.service import run_screening
from zecpath_hiring.ai.screening_ai.transcript_processing import build_clean_transcript, normalize_transcript_text
from zecpath_hiring.ai.screening_ai.understanding import understand_answer


class ScreeningPipelineTests(unittest.TestCase):
    def test_transcript_normalization_removes_fillers_and_marks_interruptions(self):
        result = normalize_transcript_text("Um I have 4 years in Python... and Django")
        self.assertIn("python", result["normalized_text"].lower())
        self.assertFalse(result["partial_answer"])
        self.assertTrue(result["interrupted_speech"])

    def test_understanding_extracts_salary_expectation(self):
        question = {
            "id": "sal_001",
            "category": "Salary",
            "mandatory": False,
        }
        understanding = understand_answer(question, "My expected salary is 18 lpa.")
        self.assertEqual(understanding["entities"]["salary_expectation"], "18 lpa")

    def test_scoring_engine_returns_per_question_breakdown(self):
        question = {"id": "intro_001", "category": "Introduction", "importance": "high", "mandatory": True}
        understanding = understand_answer(question, "I am a backend engineer with 4 years experience in python.")
        scored = score_screening_answer(question, "I am a backend engineer with 4 years experience in python.", understanding)
        aggregate = aggregate_screening_scores([scored])
        self.assertGreater(aggregate["screening_score"], 0)

    def test_screening_service_returns_transcripts_and_scores(self):
        candidate = parse_resume_text(
            "Meera Nair",
            "Summary\nEngineer\nSkills\nPython\nDjango\nSQL\nCommunication\nExperience\nAcme - Engineer 2020 2024",
        )
        candidate["contact"] = {"location": "Bengaluru"}
        job = parse_job_description(
            "Backend Engineer",
            "Need 3+ years experience with Python, Django, SQL and communication.",
        )
        result = run_screening(candidate, job, {"eligible_for_ai_screening_call": True, "status": "ELIGIBLE"})
        self.assertEqual(len(result["transcripts"]), result["question_pack"]["question_count"])
        self.assertIn("per_question_scores", result["score_breakdown"])
