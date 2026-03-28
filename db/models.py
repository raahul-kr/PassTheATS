import os
from pymongo import MongoClient

db = None

def init_db(app):
    global db
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/passtheats")
    client = MongoClient(
        mongo_uri, 
        serverSelectionTimeoutMS=5000, 
        connectTimeoutMS=5000, 
        socketTimeoutMS=5000
    )
    # The database name will be 'passtheats'
    db = client["passtheats"]
    
    try:
        db.users.create_index("email", unique=True, background=True)
    except:
        pass

def get_db():
    return db

class User:
    def __init__(self, doc):
        self.id = str(doc.get("_id"))
        self.name = doc.get("name")
        self.email = doc.get("email")
        self.password_hash = doc.get("password_hash")
        self.created_at = doc.get("created_at")

class Report:
    def __init__(self, doc):
        self.id = str(doc.get("_id"))
        self.user_id = doc.get("user_id")
        self.role = doc.get("role")
        self.ats_score = doc.get("ats_score")
        self.proof_score = doc.get("proof_score")
        self.risk_level = doc.get("risk_level")
        self.role_fit_score = doc.get("role_fit_score")
        self.matched_keywords = doc.get("matched_keywords")
        self.missing_keywords = doc.get("missing_keywords")
        self.report_json = doc.get("report_json")
        self.created_at = doc.get("created_at")
