from .keyword_extractor import clean_text

def keyword_match_score(resume_text: str, jd_keywords: list):
    resume_clean = clean_text(resume_text)

    matched = []
    missing = []

    for kw in jd_keywords:
        kw_clean = clean_text(kw)
        if kw_clean in resume_clean:
            matched.append(kw)
        else:
            missing.append(kw)

    total = len(jd_keywords)
    score = round((len(matched) / total) * 100, 2) if total > 0 else 0

    return score, matched, missing



from .keyword_extractor import clean_text

def role_rubric_score(resume_text: str, rubric: dict):
    """
    Returns:
    - score out of 100
    - breakdown list for UI
    """
    resume_clean = clean_text(resume_text)

    total_weight = sum(rubric.values()) if rubric else 0
    if total_weight == 0:
        return 0, []

    gained = 0
    breakdown = []

    for skill, weight in rubric.items():
        skill_clean = clean_text(skill)
        present = skill_clean in resume_clean

        if present:
            gained += weight

        breakdown.append({
            "skill": skill,
            "weight": weight,
            "present": present
        })

    score = round((gained / total_weight) * 100, 2)
    return score, breakdown
