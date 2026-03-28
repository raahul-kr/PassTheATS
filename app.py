import os
import json

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from bson.objectid import ObjectId

# Local imports
from core.rubrics import ROLE_RUBRICS
from db.models import init_db, get_db, User, Report
from core.interview_questions import generate_interview_questions
from core.scoring_engine import role_rubric_score, keyword_match_score
from core.cheat_detector import keyword_stuffing_risk
from core.resume_parser import extract_text_from_pdf
from core.keyword_extractor import extract_keywords_from_jd
from core.proof_checker import build_skill_evidence, proof_score_from_evidence
from core.jd_parser import generate_suggestions
from core.jd_templates import ROLE_TEMPLATES
from core.ai_suggestions import generate_ai_suggestions
from core.ai_interview_questions import generate_ai_interview_questions
from core.ai_summary import generate_ai_summary



app = Flask(__name__)
app.secret_key = "hirelens-secret-key"  # later move to env variable
app.config["SECRET_KEY"] = "hirelens-secret-key"

init_db(app)

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_resume(resume_text: str, jd_text: str, role: str = ""):
    jd_keywords = extract_keywords_from_jd(jd_text)

    ats_score, matched, missing = keyword_match_score(resume_text, jd_keywords)

    # Build evidence for matched keywords only
    evidence = build_skill_evidence(resume_text, matched)
    proof = proof_score_from_evidence(evidence)

    risk_level, risk_reasons, risk_stats = keyword_stuffing_risk(evidence)

    # Role Rubric Score (Phase 5)
    role_fit_score = None
    rubric_breakdown = []

    if role in ROLE_RUBRICS:
        role_fit_score, rubric_breakdown = role_rubric_score(resume_text, ROLE_RUBRICS[role])

    print(">>> ATS:", ats_score)
    print(">>> Proof:", proof)
    print(">>> Missing:", missing)
    
    ai_suggestions = generate_ai_suggestions(
    ats_score=ats_score,
    proof_score=proof,
    missing_skills=missing,
    role=role
    

)
    print(">>> AI Suggestions:", ai_suggestions)

    suggestions = ai_suggestions if ai_suggestions else generate_suggestions(missing)
    
    ai_questions = generate_ai_interview_questions(
    ats_score=ats_score,
    proof_score=proof,
    missing_skills=missing,
    evidence=evidence,
    role=role
)

    interview_questions = (
    ai_questions if ai_questions
    else generate_interview_questions(missing, evidence)
)
    ai_summary = generate_ai_summary(
    ats_score=ats_score,
    proof_score=proof,
    missing_skills=missing,
    role=role
)

    return {
        "ai_summary": ai_summary,
        "interview_questions": interview_questions,
        "ats_score": ats_score,
        "proof_score": proof,
        "total_keywords": len(jd_keywords),
        "matched": matched,
        "missing": missing,
        "suggestions": suggestions,
        "evidence": evidence,
        "risk_level": risk_level,
        "risk_reasons": risk_reasons,
        "risk_stats": risk_stats,
        "role_fit_score": role_fit_score,
        "rubric_breakdown": rubric_breakdown,
        "selected_role": role
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        jd_text = request.form.get("job_description", "")
        selected_role = request.form.get("role", "")

        # If user selected a role but JD is empty, auto use template
        if jd_text.strip() == "" and selected_role in ROLE_TEMPLATES:
            jd_text = ROLE_TEMPLATES[selected_role]

        if not resume_file or resume_file.filename == "":
            return render_template("index.html", error="Please upload a resume PDF.", roles=ROLE_TEMPLATES)

        if jd_text.strip() == "":
            return render_template("index.html", error="Please paste job description or select a role template.", roles=ROLE_TEMPLATES)

        file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(file_path)

        resume_text = extract_text_from_pdf(file_path)
        result = analyze_resume(resume_text, jd_text, selected_role)

        if "user_id" in session:
            target_db = get_db()
            report_doc = {
                "user_id": session["user_id"],
                "role": selected_role,
                "ats_score": result["ats_score"],
                "proof_score": result["proof_score"],
                "risk_level": result["risk_level"],
                "role_fit_score": result["role_fit_score"],
                "matched_keywords": ",".join(result["matched"]),
                "missing_keywords": ",".join(result["missing"]),
                "report_json": json.dumps(result),
                "created_at": datetime.utcnow()
            }
            try:
                target_db.reports.insert_one(report_doc)
            except Exception:
                pass

        return render_template("report.html", **result)

    return render_template("index.html", roles=ROLE_TEMPLATES)


@app.route("/demo", methods=["GET", "POST"])
def demo():
    if request.method == "POST":
        resume_text = request.form.get("resume_text", "")
        jd_text = request.form.get("job_description", "")
        selected_role = request.form.get("role", "")

        if jd_text.strip() == "" and selected_role in ROLE_TEMPLATES:
            jd_text = ROLE_TEMPLATES[selected_role]

        if resume_text.strip() == "":
            return render_template("demo.html", error="Please paste resume text.", roles=ROLE_TEMPLATES)

        if jd_text.strip() == "":
            return render_template("demo.html", error="Please paste job description or select a role template.", roles=ROLE_TEMPLATES)

        result = analyze_resume(resume_text, jd_text, selected_role)

        if "user_id" in session:
            target_db = get_db()
            report_doc = {
                "user_id": session["user_id"],
                "role": selected_role,
                "ats_score": result["ats_score"],
                "proof_score": result["proof_score"],
                "risk_level": result["risk_level"],
                "role_fit_score": result["role_fit_score"],
                "matched_keywords": ",".join(result["matched"]),
                "missing_keywords": ",".join(result["missing"]),
                "created_at": datetime.utcnow()
            }
            try:
                target_db.reports.insert_one(report_doc)
            except Exception:
                pass

        return render_template("report.html", **result)

    return render_template("demo.html", roles=ROLE_TEMPLATES)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "").lower()
        password = request.form.get("password", "")

        target_db = get_db()
        try:
            if target_db.users.find_one({"email": email}):
                return render_template("register.html", error="Email already registered.")

            password_hash = generate_password_hash(password)

            user_doc = {
                "name": name,
                "email": email,
                "password_hash": password_hash,
                "created_at": datetime.utcnow()
            }
            res = target_db.users.insert_one(user_doc)

            session["user_id"] = str(res.inserted_id)
            session["user_name"] = name
            return redirect(url_for("history"))
        except Exception as e:
            return render_template("register.html", error=f"Database connection error: {str(e)[:50]}... Is your Render IP allowed in MongoDB Atlas Network Access?")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").lower()
        password = request.form.get("password", "")

        target_db = get_db()
        try:
            user_doc = target_db.users.find_one({"email": email})
            if not user_doc or not check_password_hash(user_doc.get("password_hash", ""), password):
                return render_template("login.html", error="Invalid email or password.")

            session["user_id"] = str(user_doc["_id"])
            session["user_name"] = user_doc["name"]
            return redirect(url_for("history"))
        except Exception as e:
            return render_template("login.html", error=f"Database connection error: {str(e)[:50]}... Is your Render IP allowed in MongoDB Atlas Network Access?")

    return render_template("login.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        return render_template("forgot.html", error="Password reset is currently disabled. Please contact support.")
    return render_template("forgot.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    target_db = get_db()
    try:
        reports_docs = target_db.reports.find({"user_id": session["user_id"]}).sort("created_at", -1)
        reports = [Report(doc) for doc in reports_docs]
    except Exception:
        reports = []
        
    return render_template("history.html", reports=reports)


@app.route("/report/<string:report_id>")
def view_report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    target_db = get_db()
    try:
        obj_id = ObjectId(report_id)
    except:
        return "Invalid report ID", 400

    doc = target_db.reports.find_one({"_id": obj_id, "user_id": session["user_id"]})
    if not doc:
        return "Report not found", 404
        
    report = Report(doc)

    # If full report json exists, use it
    if report.report_json:
        result = json.loads(report.report_json)
        return render_template("report.html", **result)

    # fallback if old report has no json
    matched = report.matched_keywords.split(",") if report.matched_keywords else []
    missing = report.missing_keywords.split(",") if report.missing_keywords else []

    return render_template(
        "report.html",
        ats_score=report.ats_score,
        proof_score=report.proof_score,
        total_keywords=len(matched) + len(missing),
        matched=matched,
        missing=missing,
        suggestions=generate_suggestions(missing),
        evidence={},
        risk_level=report.risk_level,
        risk_reasons=["Old report - full details not stored."],
        risk_stats={"total": len(matched), "strong": 0, "weak": 0},
        role_fit_score=report.role_fit_score,
        rubric_breakdown=[],
        selected_role=report.role,
        interview_questions=[]
    )


@app.route("/delete_report/<string:report_id>")
def delete_report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    target_db = get_db()
    try:
        obj_id = ObjectId(report_id)
        target_db.reports.delete_one({"_id": obj_id, "user_id": session["user_id"]})
    except:
        pass

    return redirect(url_for("history"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
