import unittest

from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text


class ParserTests(unittest.TestCase):
    def test_resume_parser_extracts_known_skills(self):
        result = parse_resume_text(
            "Asha Sharma",
            "Skills\nPython\nDjango\nCommunication\n\nExperience\nAcme Corp - Developer 2020 2024",
        )
        self.assertTrue({"python", "django", "communication"} <= {skill["name"] for skill in result["skills"]})

    def test_job_parser_extracts_required_skills(self):
        result = parse_job_description(
            "Backend Engineer",
            "We need 3+ years experience with Python, Django, SQL, and AWS.",
        )
        self.assertTrue({"python", "django", "sql", "aws"} <= set(result["required_skills"]))
