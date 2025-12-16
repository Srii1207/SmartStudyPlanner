import sqlite3
from datetime import date

DB_PATH = "study_planner.db"


def get_connection():
    """Create and return a DB connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create required tables for the project."""
    conn = get_connection()
    cur = conn.cursor()

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            total_chapters INTEGER NOT NULL,
            hours_per_day INTEGER NOT NULL
        );
    """)

    
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
    """Insert a new exam and return its ID."""
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


def get_all_exams():
    """Return all exams."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM exams;")
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_exam_by_id(exam_id):
    """Return a single exam by ID."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM exams WHERE id = ?;", (exam_id,))
    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None




def clear_tasks_for_exam(exam_id):
    """Delete existing timetable rows for an exam."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE exam_id = ?;", (exam_id,))
    conn.commit()
    conn.close()


def add_task(exam_id, subject, task_date, start_chapter, end_chapter, hours):
    """Insert one timetable (study) row."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (
            exam_id, subject, task_date,
            start_chapter, end_chapter, hours
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        exam_id,
        subject,
        task_date,
        start_chapter,
        end_chapter,
        hours
    ))

    conn.commit()
    conn.close()


def get_timetable():
    """Return full generated timetable."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM tasks
        ORDER BY task_date;
    """)
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_today_plan(target_date=None):
    """Return today's study plan."""
    if target_date is None:
        target_date = date.today().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM tasks
        WHERE task_date = ?
        ORDER BY subject;
    """, (target_date,))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if _name_ == "_main_":
    init_db()
    print("Database initialized successfully.")
