import re


SECTION_HINTS = {
    "skills": ["skills", "technical skills", "core competencies"],
    "experience": ["experience", "work experience", "employment"],
    "education": ["education", "academic background", "qualifications"],
    "certifications": ["certifications", "licenses"],
    "projects": ["projects", "key projects"],
}


def normalize_text(text: str) -> str:
    cleaned = text.replace("\u2022", "-").replace("\t", " ")
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def split_sections(text: str) -> dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections: dict[str, list[str]] = {"summary": []}
    current = "summary"
    for line in lines:
        lowered = line.lower().rstrip(":")
        matched = False
        for name, hints in SECTION_HINTS.items():
            if lowered in hints:
                current = name
                sections.setdefault(current, [])
                matched = True
                break
        if not matched:
            sections.setdefault(current, []).append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}

