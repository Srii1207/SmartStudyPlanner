from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date

from db import (
    create_tables,
    insert_exam,
    get_all_exams,
    save_timetable_rows,
    get_timetable_for_date,
)

app = Flask(__name__)
CORS(app)

# Create tables when backend starts
create_tables()


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Backend running"})


# ------------------ ADD EXAM ------------------
@app.route("/api/exams", methods=["POST"])
def api_add_exam():
    data = request.get_json() or {}

    subject = data.get("subject")
    exam_date = data.get("examDate")
    total_chapters = data.get("totalChapters")
    hours_per_day = data.get("hoursPerDay")

    if not subject or not exam_date or total_chapters is None or hours_per_day is None:
        return jsonify({"error": "Missing fields"}), 400

    exam_id = insert_exam(subject, exam_date, total_chapters, hours_per_day)
    return jsonify({"message": "Exam saved", "examId": exam_id})


# ------------------ LIST EXAMS ------------------
@app.route("/api/exams", methods=["GET"])
def api_list_exams():
    exams = get_all_exams()
    return jsonify({"exams": exams})


# ------------------ GENERATE TIMETABLE ------------------
@app.route("/api/generate-timetable", methods=["POST"])
def api_generate_timetable():
    data = request.get_json() or {}
    exam_id = data.get("examId")

    if exam_id is None:
        return jsonify({"error": "examId required"}), 400

    # get exam info
    exams = get_all_exams()
    exam = next((e for e in exams if e["id"] == exam_id), None)

    if exam is None:
        return jsonify({"error": "Exam not found"}), 404

    today = date.today()
    exam_date = datetime.strptime(exam["exam_date"], "%Y-%m-%d").date()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return jsonify({"error": "Exam must be in the future"}), 400

    total_chapters = exam["total_chapters"]
    hours_per_day = exam["hours_per_day"]
    chapters_per_day = max(1, total_chapters // days_left)

    # Generate timetable rows
    timetable_rows = []
    current_chapter = 1
    current_date = today

    while current_chapter <= total_chapters and current_date <= exam_date:
        end_chapter = min(current_chapter + chapters_per_day - 1, total_chapters)

        timetable_rows.append({
            "exam_id": exam_id,
            "date": current_date.strftime("%Y-%m-%d"),
            "start_chapter": current_chapter,
            "end_chapter": end_chapter,
            "hours": hours_per_day
        })

        current_chapter = end_chapter + 1
        current_date = current_date.fromordinal(current_date.toordinal() + 1)

    save_timetable_rows(exam_id, timetable_rows)

    return jsonify({"message": "Timetable generated", "timetable": timetable_rows})


# ------------------ TODAY'S PLAN ------------------
@app.route("/api/today-plan", methods=["GET"])
def api_today_plan():
    date_input = request.args.get("date")
    if date_input:
        try:
            today = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date"}), 400
    else:
        today = date.today()

    rows = get_timetable_for_date(today.strftime("%Y-%m-%d"))

    return jsonify({"date": today.strftime("%Y-%m-%d"), "plan": rows})


if __name__ == "__main__":
    app.run(debug=True)
