# ============================================
# Career Path Explorer - Flask Backend
# ============================================
# Run this file to start the server:
#   pip install flask
#   python app.py
# Then open http://localhost:5000 in your browser
# ============================================

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
import os
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

# --- Database Setup ---
def init_db():
    """Create the students table if it doesn't exist."""
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            email   TEXT    NOT NULL,
            career  TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Career data — easy to extend
CAREERS = {
    "engineering": {
        "title": "Engineering",
        "emoji": "⚙️",
        "desc": "Design and build systems, machines, and software that power the world.",
        "skills": ["Mathematics", "Problem Solving", "Logical Thinking", "Teamwork"],
        "subjects": ["Physics", "Mathematics", "Computer Science"],
        "roles": ["Software Engineer", "Civil Engineer", "Mechanical Engineer", "Google, Infosys, L&T"],
    },
    "medicine": {
        "title": "Medicine",
        "emoji": "🩺",
        "desc": "Diagnose, treat, and prevent illness to improve human health and lives.",
        "skills": ["Empathy", "Attention to Detail", "Communication", "Stamina"],
        "subjects": ["Biology", "Chemistry", "Physics"],
        "roles": ["Doctor", "Surgeon", "Nurse", "AIIMS, Apollo, Fortis"],
    },
    "cybersecurity": {
        "title": "Cybersecurity",
        "emoji": "🔐",
        "desc": "Protect systems and networks from digital attacks and data breaches.",
        "skills": ["Ethical Hacking", "Networking", "Cryptography", "Vigilance"],
        "subjects": ["Computer Science", "Mathematics", "Electronics"],
        "roles": ["Security Analyst", "Penetration Tester", "ISRO, TCS, Palo Alto"],
    },
    "business": {
        "title": "Business",
        "emoji": "📊",
        "desc": "Lead organisations, manage resources, and drive growth and strategy.",
        "skills": ["Leadership", "Communication", "Finance", "Decision Making"],
        "subjects": ["Economics", "Mathematics", "Commerce"],
        "roles": ["Manager", "Entrepreneur", "Analyst", "Deloitte, McKinsey, startups"],
    },
    "design": {
        "title": "Design",
        "emoji": "🎨",
        "desc": "Create visual experiences — from logos and apps to architecture and fashion.",
        "skills": ["Creativity", "Adobe Suite", "Typography", "User Empathy"],
        "subjects": ["Art", "Computer Science", "Psychology"],
        "roles": ["UX Designer", "Graphic Designer", "Architect", "Adobe, Zomato, Canva"],
    },
    "government": {
        "title": "Government Jobs",
        "emoji": "🏛️",
        "desc": "Serve the nation through civil services, defence, banking, and public policy.",
        "skills": ["Dedication", "General Knowledge", "Integrity", "Leadership"],
        "subjects": ["History", "Political Science", "Economics"],
        "roles": ["IAS / IPS Officer", "Bank PO", "Defence Officer", "UPSC, SSC, IBPS"],
    },
}

# Quiz logic — maps answer combos to careers
QUIZ_MAP = {
    ("math",    "solving"):   "engineering",
    ("math",    "managing"):  "business",
    ("math",    "designing"): "cybersecurity",
    ("math",    "helping"):   "engineering",
    ("biology", "helping"):   "medicine",
    ("biology", "solving"):   "medicine",
    ("biology", "managing"):  "government",
    ("biology", "designing"): "design",
    ("business","managing"):  "business",
    ("business","helping"):   "government",
    ("business","solving"):   "business",
    ("business","designing"): "design",
    ("computers","solving"):  "cybersecurity",
    ("computers","designing"):"design",
    ("computers","managing"): "business",
    ("computers","helping"):  "medicine",
}

# ---- Routes ----

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/careers")
def careers():
    return render_template("careers.html", careers=CAREERS)

@app.route("/career/<slug>")
def career_detail(slug):
    career = CAREERS.get(slug)
    if not career:
        return "Career not found", 404
    return render_template("career_detail.html", career=career, slug=slug)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    result = None
    if request.method == "POST":
        subject = request.form.get("subject", "").lower()
        work    = request.form.get("work", "").lower()
        slug    = QUIZ_MAP.get((subject, work), "engineering")
        result  = CAREERS[slug]
        result["slug"] = slug
    return render_template("quiz.html", result=result)

@app.route("/form", methods=["GET", "POST"])
def form():
    success = False
    if request.method == "POST":
        name   = request.form.get("name", "").strip()
        email  = request.form.get("email", "").strip()
        career = request.form.get("career", "").strip()
        if name and email and career:
            conn = sqlite3.connect(DB)
            conn.execute("INSERT INTO students (name, email, career) VALUES (?, ?, ?)",
                         (name, email, career))
            conn.commit()
            conn.close()
            success = True
    return render_template("form.html", careers=CAREERS, success=success)

@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT id, name, email, career FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", students=rows)

# ---- Start ----
if __name__ == "__main__":
    init_db()          # create DB on first run
    app.run(debug=True)
