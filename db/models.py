from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="reports")

    role = db.Column(db.String(50), nullable=True)
    ats_score = db.Column(db.Float, nullable=False)
    proof_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    role_fit_score = db.Column(db.Float, nullable=True)

    matched_keywords = db.Column(db.Text, nullable=True)
    missing_keywords = db.Column(db.Text, nullable=True)

    report_json = db.Column(db.Text, nullable=True)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
