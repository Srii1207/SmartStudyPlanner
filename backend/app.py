from flask import Flask, jsonify, request
from flask_cors import CORS
import db  # our db.py file

app = Flask(__name__)
CORS(app)  # allow frontend (HTML/JS) to call APIs

# ---------- BASIC TEST ROUTE ----------
@app.route("/")
def index():
    return "SmartStudyPlanner backend is running"


# ---------- API: GET FULL TIMETABLE ----------
@app.route("/api/timetable", methods=["GET"])
def get_timetable():
    """
    Returns the full timetable.
    Frontend: timetable.js will call this.
    """
    timetable = db.get_timetable()
    return jsonify({"timetable": timetable})


# ---------- API: GET TODAY'S TASKS ----------
@app.route("/api/today", methods=["GET"])
def get_today_tasks():
    """
    Returns tasks/timetable for TODAY.
    Frontend: today.js will call this.
    """
    tasks = db.get_today_tasks()
    return jsonify({"tasks": tasks})


# ---------- API: ADD A TASK ----------
@app.route("/api/tasks", methods=["POST"])
def add_task():
    """
    Example POST endpoint.
    Frontend can send JSON like:
    {
        "subject": "...",
        "date": "...",
        "start_time": "...",
        "end_time": "...",
        "description": "..."
    }
    """
    data = request.get_json()
    db.add_task(data)
    return jsonify({"message": "Task added successfully"}), 201


if __name__ == "__main__":
    # only for local development
    app.run(debug=True)
