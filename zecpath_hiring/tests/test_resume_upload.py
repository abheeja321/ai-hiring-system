import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from zecpath_hiring.ai.parsers.resume_reader import extract_uploaded_resume_text


class ResumeUploadTests(unittest.TestCase):
    def test_extract_uploaded_txt_resume(self):
        uploaded_file = SimpleUploadedFile(
            "resume.txt",
            b"Skills\nPython\nDjango\nExperience\nAcme - Engineer 2020 2024",
            content_type="text/plain",
        )
        result = extract_uploaded_resume_text(uploaded_file)
        self.assertIn("Python", result)
        self.assertIn("Django", result)
