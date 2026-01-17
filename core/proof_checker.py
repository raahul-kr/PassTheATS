from .keyword_extractor import clean_text
from .resume_sections import split_into_sections

def build_skill_evidence(resume_text: str, keywords: list):
    """
    Returns evidence dictionary for each keyword:
    in_skills, in_projects, in_experience, strength
    """
    sections = split_into_sections(resume_text)

    skills_text = clean_text(sections.get("skills", ""))
    projects_text = clean_text(sections.get("projects", ""))
    exp_text = clean_text(sections.get("experience", ""))
    full_text = clean_text(resume_text)

    evidence = {}

    for kw in keywords:
        kw_clean = clean_text(kw)

        in_skills = kw_clean in skills_text
        in_projects = kw_clean in projects_text
        in_experience = kw_clean in exp_text

        # Strength logic
        if in_projects or in_experience:
            strength = "Strong"
        elif in_skills:
            strength = "Weak"
        elif kw_clean in full_text:
            strength = "Medium"
        else:
            strength = "Missing"

        evidence[kw] = {
            "in_skills": in_skills,
            "in_projects": in_projects,
            "in_experience": in_experience,
            "strength": strength
        }

    return evidence

def proof_score_from_evidence(evidence: dict):
    """
    Proof score = percentage of matched skills that have Strong evidence
    """
    if not evidence:
        return 0

    total_present = 0
    strong_count = 0

    for kw, data in evidence.items():
        if data["strength"] != "Missing":
            total_present += 1
            if data["strength"] == "Strong":
                strong_count += 1

    if total_present == 0:
        return 0

    return round((strong_count / total_present) * 100, 2)
