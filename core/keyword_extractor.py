import re

DEFAULT_SKILLS = [
    "python", "java", "c++", "javascript", "flask", "django", "react",
    "aws", "ec2", "s3", "iam", "docker", "kubernetes",
    "linux", "git", "github", "sql", "mysql", "postgresql",
    "api", "rest", "microservices", "ci/cd", "devops"
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\.\/-]", " ", text)  # keep +, #, /, -
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords_from_jd(jd_text: str, keywords_list=None):
    if keywords_list is None:
        keywords_list = DEFAULT_SKILLS

    jd_clean = clean_text(jd_text)

    found = []
    for kw in keywords_list:
        kw_clean = clean_text(kw)
        if kw_clean in jd_clean:
            found.append(kw)

    return sorted(list(set(found)))
