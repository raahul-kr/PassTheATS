QUESTION_BANK = {
    "aws": [
        "What is IAM and why is it important in AWS?",
        "Explain the difference between EC2 and Lambda.",
        "What is an S3 bucket and how is it used?"
    ],
    "ec2": [
        "How do you connect to an EC2 instance using SSH?",
        "What is the purpose of a Security Group in EC2?"
    ],
    "s3": [
        "What is the difference between S3 and EBS?",
        "How do you make an S3 object public/private?"
    ],
    "iam": [
        "What is the difference between IAM User and IAM Role?",
        "What is the principle of least privilege?"
    ],
    "linux": [
        "What is chmod and why is it used?",
        "Explain the difference between sudo and su.",
        "What is a process in Linux?"
    ],
    "docker": [
        "What is the difference between Docker Image and Container?",
        "What is a Dockerfile?",
        "Why do we use Docker in deployment?"
    ],
    "git": [
        "What is the difference between git pull and git fetch?",
        "Explain merge conflict and how to resolve it."
    ],
    "sql": [
        "What is the difference between WHERE and HAVING?",
        "Explain primary key vs foreign key."
    ],
    "api": [
        "What is a REST API?",
        "What is the difference between GET and POST?"
    ],
    "react": [
        "What are props and state in React?",
        "What is the use of useEffect hook?"
    ]
}

def generate_interview_questions(missing_keywords, evidence, max_q=8):
    """
    Generate questions from:
    - Missing keywords (learn questions)
    - Weak evidence keywords (prove questions)
    """
    questions = []

    # Questions for missing skills
    for kw in missing_keywords:
        kw_lower = kw.lower()
        if kw_lower in QUESTION_BANK:
            questions.extend(QUESTION_BANK[kw_lower])

    # Questions for weak proof skills
    if evidence:
        for kw, data in evidence.items():
            if data.get("strength") == "Weak":
                questions.append(f"You mentioned '{kw}' in your resume. Where exactly did you use it in a project?")

    # Remove duplicates while keeping order
    final = []
    for q in questions:
        if q not in final:
            final.append(q)

    return final[:max_q]
