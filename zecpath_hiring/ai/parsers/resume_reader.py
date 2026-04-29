import os
import tempfile
from pathlib import Path

from .common import normalize_text


def extract_resume_text(path: str) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        return normalize_text(file_path.read_text(encoding="utf-8"))
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        return normalize_text("\n".join(page.extract_text() or "" for page in reader.pages))
    if suffix == ".docx":
        from docx import Document

        doc = Document(str(file_path))
        return normalize_text("\n".join(paragraph.text for paragraph in doc.paragraphs))
    raise ValueError(f"Unsupported resume format: {suffix}")


def extract_uploaded_resume_text(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in {".txt", ".pdf", ".docx"}:
        raise ValueError("Unsupported resume format. Please upload a PDF, DOCX, or TXT file.")

    if suffix == ".txt":
        return normalize_text(uploaded_file.read().decode("utf-8", errors="ignore"))

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        return extract_resume_text(temp_file_path)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
