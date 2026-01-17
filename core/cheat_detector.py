def keyword_stuffing_risk(evidence: dict):
    """
    evidence format:
    {
      "AWS": {"in_skills": True, "in_projects": False, "in_experience": False, "strength": "Weak"},
      ...
    }

    Returns:
    - risk_level: LOW / MEDIUM / HIGH
    - reasons: list of strings
    - stats: dict
    """
    if not evidence:
        return "LOW", ["No evidence data available."], {"total": 0, "strong": 0, "weak": 0}

    total = len(evidence)
    strong = 0
    weak = 0
    missing = 0

    for _, data in evidence.items():
        if data["strength"] == "Strong":
            strong += 1
        elif data["strength"] == "Weak":
            weak += 1
        elif data["strength"] == "Missing":
            missing += 1

    # Ratios
    strong_ratio = strong / total if total else 0
    weak_ratio = weak / total if total else 0

    reasons = []

    # Risk logic (MVP but strong)
    if weak_ratio >= 0.60 and strong_ratio <= 0.20:
        risk = "HIGH"
        reasons.append("Many skills are only listed in Skills section but not proven in Projects/Experience.")
        reasons.append("High chance of keyword stuffing or weak project evidence.")
    elif weak_ratio >= 0.40:
        risk = "MEDIUM"
        reasons.append("Some skills are mentioned without project/work proof.")
        reasons.append("Try adding real evidence in Projects/Experience section.")
    else:
        risk = "LOW"
        reasons.append("Most skills are supported with evidence. Looks genuine.")

    stats = {
        "total": total,
        "strong": strong,
        "weak": weak,
        "missing": missing
    }

    return risk, reasons, stats
