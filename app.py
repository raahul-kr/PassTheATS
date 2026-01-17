import os
import json

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# Local imports
from core.rubrics import ROLE_RUBRICS
from db.models import db, User, Report
from core.interview_questions import generate_interview_questions
from core.scoring_engine import role_rubric_score, keyword_match_score
from core.cheat_detector import keyword_stuffing_risk
from core.resume_parser import extract_text_from_pdf
from core.keyword_extractor import extract_keywords_from_jd
from core.proof_checker import build_skill_evidence, proof_score_from_evidence
from core.jd_parser import generate_suggestions
from core.jd_templates import ROLE_TEMPLATES

app = Flask(__name__)
app.secret_key = "hirelens-secret-key"  # later move to env variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hirelens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

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

    suggestions = generate_suggestions(missing)
    interview_questions = generate_interview_questions(missing, evidence)

    return {
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
            report = Report(
                user_id=session["user_id"],
                role=selected_role,
                ats_score=result["ats_score"],
                proof_score=result["proof_score"],
                risk_level=result["risk_level"],
                role_fit_score=result["role_fit_score"],
                matched_keywords=",".join(result["matched"]),
                missing_keywords=",".join(result["missing"]),
                report_json=json.dumps(result)
            )
            db.session.add(report)
            db.session.commit()

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
            report = Report(
                user_id=session["user_id"],
                role=selected_role,
                ats_score=result["ats_score"],
                proof_score=result["proof_score"],
                risk_level=result["risk_level"],
                role_fit_score=result["role_fit_score"],
                matched_keywords=",".join(result["matched"]),
                missing_keywords=",".join(result["missing"])
            )
            db.session.add(report)
            db.session.commit()

        return render_template("report.html", **result)

    return render_template("demo.html", roles=ROLE_TEMPLATES)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "").lower()
        password = request.form.get("password", "")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already registered.")

        password_hash = generate_password_hash(password)

        user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["user_name"] = user.name
        return redirect(url_for("history"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user.id
        session["user_name"] = user.name
        return redirect(url_for("history"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    reports = Report.query.filter_by(user_id=session["user_id"]).order_by(Report.created_at.desc()).all()
    return render_template("history.html", reports=reports)


@app.route("/report/<int:report_id>")
def view_report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    report = Report.query.filter_by(id=report_id, user_id=session["user_id"]).first()
    if not report:
        return "Report not found", 404

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


@app.route("/delete_report/<int:report_id>")
def delete_report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    report = Report.query.filter_by(id=report_id, user_id=session["user_id"]).first()
    if report:
        db.session.delete(report)
        db.session.commit()

    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)