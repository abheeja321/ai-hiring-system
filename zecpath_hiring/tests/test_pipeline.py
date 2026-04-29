import unittest

from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text


class PipelineTests(unittest.TestCase):
    def test_hiring_pipeline_returns_decision(self):
        candidate = parse_resume_text(
            "Rohit Mehta",
            "Summary\nBackend engineer.\nSkills\nPython\nDjango\nSQL\nCommunication\nProjects\nBuilt an ATS platform.",
        )
        job = parse_job_description(
            "AI Hiring Engineer",
            "Looking for 4+ years with Python, Django, SQL and communication skills.",
        )
        result = run_hiring_pipeline(candidate, job)
        self.assertIn(result["decision"]["decision"], {"OFFER", "FINAL_REVIEW", "REJECT"})
