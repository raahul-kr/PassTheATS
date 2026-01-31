import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def generate_ai_interview_questions(ats_score, proof_score, missing_skills, evidence, role):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return []

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-flash-latest")

    weak_skills = [
        skill for skill, data in evidence.items()
        if data.get("strength") in ("Weak", "Missing")
    ]

    prompt = f"""
You are a technical interviewer hiring for the role: {role or "Software Engineer"}.

Context:
ATS Score: {ats_score}%
Proof Score: {proof_score}%
Missing Skills: {missing_skills}
Weak/Unproven Skills: {weak_skills}

Task:
Generate EXACTLY 5 interview questions.

STRICT RULES:
- One question per line
- Plain text only (no numbering, no markdown)
- Questions must be technical and role-relevant
- Ask to explain concepts OR real project experience
- Keep questions concise

Output:
5 questions only.
"""

    try:
        response = model.generate_content(prompt)
        lines = [l.strip() for l in response.text.split("\n") if l.strip()]

        questions = []
        for line in lines:
            line = line.lstrip("-•0123456789. ").strip()
            if len(line) > 10:
                questions.append(line)
            if len(questions) == 5:
                break

        return questions

    except Exception:
        return []
