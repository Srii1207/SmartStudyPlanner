import sqlite3
from datetime import date

DB_PATH = "study_planner.db"


def get_connection():
    """Create and return a DB connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task_date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            description TEXT,
            completed INTEGER DEFAULT 0
        );
    """)

    # Materials table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            file_path TEXT,
            uploaded_on TEXT
        );
    """)

    # Exams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            syllabus TEXT
        );
    """)

    conn.commit()
    conn.close()


def get_timetable():
    """Return all tasks ordered by date and time."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks ORDER BY task_date, start_time;")
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_tasks():
    """Return all tasks."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks;")
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_today():
    """Return today's tasks."""
    today_str = date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tasks WHERE task_date = ? ORDER BY start_time;",
        (today_str,),
    )
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def add_task(task_data: dict):
    """Insert a new task."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (subject, task_date, start_time, end_time, description)
        VALUES (?, ?, ?, ?, ?);
    """, (
        task_data.get("subject"),
        task_data.get("date"),
        task_data.get("start_time"),
        task_data.get("end_time"),
        task_data.get("description"),
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
