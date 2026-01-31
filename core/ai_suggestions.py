# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()

# def generate_ai_suggestions(ats_score, proof_score, missing_skills, role):
#     api_key = os.getenv("")
#     if not api_key:
#         return []

#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-flash")

#     prompt = f"""
# You are a senior recruiter and resume coach.

# Context:
# - ATS Score: {ats_score}%
# - Proof Score: {proof_score}%
# - Target Role: {role}
# - Missing Skills: {missing_skills}

# Task:
# Give 5 short, actionable resume improvement suggestions.
# Focus on:
# - Adding proof to projects
# - ATS optimization
# - Role relevance

# Rules:
# - Use bullet points
# - Keep each point 1 line
# - No emojis
# """

#     try:
#         response = model.generate_content(prompt)
#         return [line.strip("-• ") for line in response.text.split("\n") if line.strip()]
#     except:
#         return []

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def generate_ai_suggestions(ats_score, proof_score, missing_skills, role):
    api_key = os.getenv("GEMINI_API_KEY")
    print(">>> GEMINI KEY FOUND:", bool(api_key))

    if not api_key:
        return []

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-flash-latest")

    prompt = f"""
You are a resume ATS expert.

Context:
ATS Score: {ats_score}%
Proof Score: {proof_score}%
Target Role: {role}
Missing Skills: {missing_skills}

Task:
Generate EXACTLY 5 resume improvement suggestions.

STRICT RULES:
- Each suggestion must be ONE short sentence
- NO headings, NO numbering, NO markdown
- NO explanations, NO paragraphs
- Start each suggestion with an action verb
- Plain text only

Output format:
- Suggestion 1
- Suggestion 2
- Suggestion 3
- Suggestion 4
- Suggestion 5
"""


    try:
        response = model.generate_content(prompt)
        return [
            line.strip("-• ").strip()
            for line in response.text.split("\n")
            if line.strip()
        ]
    except Exception as e:
        print(">>> GEMINI ERROR:", e)
        return []
