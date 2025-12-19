import sqlite3
from datetime import date, timedelta

DB_PATH = "study_planner.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Exams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            total_chapters INTEGER NOT NULL,
            hours_per_day INTEGER NOT NULL
        );
    """)
    # Tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            task_date TEXT NOT NULL,
            start_chapter INTEGER NOT NULL,
            end_chapter INTEGER NOT NULL,
            hours INTEGER NOT NULL,
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        );
    """)
    conn.commit()
    conn.close()

def add_exam(subject, exam_date, total_chapters, hours_per_day):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO exams (subject, exam_date, total_chapters, hours_per_day)
        VALUES (?, ?, ?, ?);
    """, (subject, exam_date, total_chapters, hours_per_day))
    conn.commit()
    exam_id = cur.lastrowid
    conn.close()
    return exam_id

def get_exam_by_id(exam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def clear_tasks_for_exam(exam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE exam_id = ?", (exam_id,))
    conn.commit()
    conn.close()

def add_task(exam_id, subject, task_date, start_chapter, end_chapter, hours):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (exam_id, subject, task_date, start_chapter, end_chapter, hours)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (exam_id, subject, task_date, start_chapter, end_chapter, hours))
    conn.commit()
    conn.close()

def generate_timetable(exam_id):
    exam = get_exam_by_id(exam_id)
    if not exam:
        return []

    subject = exam["subject"]
    exam_date = date.fromisoformat(exam["exam_date"])
    total_chapters = exam["total_chapters"]
    hours_per_day = exam["hours_per_day"]

    today = date.today()
    days_available = (exam_date - today).days + 1
    chapters_per_day = max(1, total_chapters // days_available)

    clear_tasks_for_exam(exam_id)

    tasks = []
    start_chapter = 1
    for i in range(days_available):
        task_date = today + timedelta(days=i)
        end_chapter = min(total_chapters, start_chapter + chapters_per_day - 1)
        add_task(exam_id, subject, task_date.isoformat(), start_chapter, end_chapter, hours_per_day)
        tasks.append({
            "task_date": task_date.isoformat(),
            "start_chapter": start_chapter,
            "end_chapter": end_chapter,
            "hours": hours_per_day
        })
        start_chapter = end_chapter + 1
        if start_chapter > total_chapters:
            break

    return tasks