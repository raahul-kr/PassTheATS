def generate_suggestions(missing_keywords: list):
    suggestions = []
    for kw in missing_keywords[:5]:
        suggestions.append(
            f"Try adding '{kw}' in your Skills or Projects section (only if you truly know it)."
        )
    return suggestions
