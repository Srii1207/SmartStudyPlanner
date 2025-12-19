from flask import Flask, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

# Initialize database
db.init_db()


@app.route("/api/add-exam", methods=["POST"])
def add_exam():
    data = request.get_json()

    subject = data.get("subject")
    exam_date = data.get("exam_date")
    total_chapters = data.get("total_chapters")
    hours_per_day = data.get("hours_per_day")

    if not all([subject, exam_date, total_chapters, hours_per_day]):
        return jsonify({"error": "Missing fields"}), 400

    exam_id = db.add_exam(
        subject,
        exam_date,
        total_chapters,
        hours_per_day
    )

    return jsonify({
        "message": "Exam added successfully",
        "exam_id": exam_id
    })


@app.route("/api/generate-timetable", methods=["POST"])
def generate_timetable():
    data = request.get_json()
    exam_id = data.get("exam_id")

    if not exam_id:
        return jsonify({"error": "exam_id is required"}), 400

    tasks = db.generate_timetable(exam_id)

    if not tasks:
        return jsonify({
            "error": "Exam not found or no tasks generated"
        }), 404

    return jsonify({
        "message": "Timetable generated successfully",
        "tasks": tasks
    })


if __name__ == "__main__":
    app.run(debug=True)
