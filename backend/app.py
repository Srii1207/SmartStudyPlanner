from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date, timedelta

import db

app = Flask(__name__)
CORS(app)


db.init_db()


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Smart Study Planner backend running"})


@app.route("/api/exams", methods=["POST"])
def add_exam():
    """
    Add a new exam.
    Input JSON:
    {
        "subject": "DBMS",
        "exam_date": "2025-12-20",
        "total_chapters": 10,
        "hours_per_day": 4
    }
    """
    data = request.get_json()

    subject = data.get("subject")
    exam_date = data.get("exam_date")
    total_chapters = data.get("total_chapters")
    hours_per_day = data.get("hours_per_day")

    if not all([subject, exam_date, total_chapters, hours_per_day]):
        return jsonify({"error": "Missing required fields"}), 400

    exam_id = db.add_exam(
        subject,
        exam_date,
        total_chapters,
        hours_per_day
    )

    return jsonify({"message": "Exam added", "exam_id": exam_id})


@app.route("/api/exams", methods=["GET"])
def list_exams():
    """Return all exams."""
    exams = db.get_all_exams()
    return jsonify({"exams": exams})




@app.route("/api/generate-timetable", methods=["POST"])
def generate_timetable():
    """
    Generate timetable for a given exam.
    Input JSON:
    {
        "exam_id": 1
    }
    """
    data = request.get_json()
    exam_id = data.get("exam_id")

    exam = db.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    subject = exam["subject"]
    exam_date = datetime.strptime(exam["exam_date"], "%Y-%m-%d").date()
    total_chapters = exam["total_chapters"]
    hours_per_day = exam["hours_per_day"]

    today = date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return jsonify({"error": "Exam date must be in the future"}), 400

    # Clear any old timetable for this exam
    db.clear_tasks_for_exam(exam_id)

    # Simple, explainable logic
    chapters_per_day = max(1, total_chapters // days_left)

    current_chapter = 1
    current_date = today

    while current_chapter <= total_chapters and current_date <= exam_date:
        end_chapter = min(
            current_chapter + chapters_per_day - 1,
            total_chapters
        )

        db.add_task(
            exam_id=exam_id,
            subject=subject,
            task_date=current_date.isoformat(),
            start_chapter=current_chapter,
            end_chapter=end_chapter,
            hours=hours_per_day
        )

        current_chapter = end_chapter + 1
        current_date += timedelta(days=1)

    return jsonify({"message": "Timetable generated successfully"})


# ---------------- FETCH TIMETABLE ----------------

@app.route("/api/timetable", methods=["GET"])
def get_timetable():
    """Return full timetable."""
    timetable = db.get_timetable()
    return jsonify({"timetable": timetable})


@app.route("/api/today-plan", methods=["GET"])
def today_plan():
    """Return today's study plan."""
    date_param = request.args.get("date")

    if date_param:
        plan = db.get_today_plan(date_param)
    else:
        plan = db.get_today_plan()

    return jsonify({"today_plan": plan})


# ---------------- MAIN ----------------

if __name__ == "__main__":
        app.run(debug=True)
