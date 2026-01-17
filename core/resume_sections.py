import re
from .keyword_extractor import clean_text

SECTION_HEADERS = {
    "skills": ["skills", "technical skills", "tech stack"],
    "projects": ["projects", "project", "academic projects"],
    "experience": ["experience", "work experience", "internship", "internships"],
    "education": ["education", "academics"]
}

def split_into_sections(resume_text: str):
    """
    Basic section splitter:
    Finds headings and separates text blocks.
    Works for most student resumes.
    """
    text = resume_text.replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    joined = "\n".join(lines)

    # Default whole resume
    sections = {
        "skills": "",
        "projects": "",
        "experience": "",
        "education": "",
        "other": joined
    }

    lower = joined.lower()

    # Find indices of headings
    heading_positions = []
    for sec, headers in SECTION_HEADERS.items():
        for h in headers:
            pattern = rf"\n{re.escape(h)}\n|\n{re.escape(h)}:|\n{re.escape(h)}\s"
            match = re.search(pattern, lower)
            if match:
                heading_positions.append((match.start(), sec))

    if not heading_positions:
        return sections

    heading_positions.sort(key=lambda x: x[0])

    # Slice sections by heading order
    for i in range(len(heading_positions)):
        start_pos, sec_name = heading_positions[i]
        end_pos = heading_positions[i + 1][0] if i + 1 < len(heading_positions) else len(joined)
        block = joined[start_pos:end_pos]
        sections[sec_name] = block

    return sections
