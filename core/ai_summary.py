import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def generate_ai_summary(ats_score, proof_score, missing_skills, role):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-flash-latest")

    prompt = f"""
You are a senior technical recruiter.

Context:
ATS Score: {ats_score}%
Proof Score: {proof_score}%
Target Role: {role}
Missing Skills: {missing_skills}

Task:
Generate a SHORT recruiter verdict.

STRICT FORMAT:
Line 1: Overall Readiness (one sentence)
Line 2: Strength: <one short point>
Line 3: Gap: <one short point>
Line 4: Gap: <one short point>

RULES:
- No markdown
- No headings
- Plain text only
- Concise and professional
"""

    try:
        response = model.generate_content(prompt)
        lines = [l.strip() for l in response.text.split("\n") if l.strip()]

        # Ensure max 4 lines
        return lines[:4]

    except Exception:
        return None
