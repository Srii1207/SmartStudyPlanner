import sqlite3
from datetime import date

DB_PATH = "study_planner.db"


def get_connection():
    """Create and return a DB connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # so we can return dict-like rows
    return conn


def init_db():
    """
    Create tables if they don't exist.
    Run this once at the start (or from a separate script).
    """
    conn = get_connection()
    cur = conn.cursor()

    # Example basic table – your DB person can modify this.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task_date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            description TEXT,
            completed INTEGER DEFAULT 0
        );
        """
    )

    conn.commit()
    conn.close()


def get_timetable():
    """
    Return ALL tasks (for timetable view).
    TODO: DB person can adjust query (group by day, sort by time, etc.)
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks ORDER BY task_date, start_time;")
    rows = cur.fetchall()
    conn.close()

    # convert to list of dicts
    return [dict(row) for row in rows]


def get_today_tasks():
    """
    Return tasks only for today's date.
    """
    today_str = date.today().isoformat()  # 'YYYY-MM-DD'
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
    """
    Insert a new task.
    task_data is expected to be a dict with keys:
    subject, date, start_time, end_time, description
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks (subject, task_date, start_time, end_time, description)
        VALUES (?, ?, ?, ?, ?);
        """,
        (
            task_data.get("subject"),
            task_data.get("date"),
            task_data.get("start_time"),
            task_data.get("end_time"),
            task_data.get("description"),
        ),
    )

    conn.commit()
    conn.close()


# If you run `python db.py` directly, it will just initialize the DB
if __name__ == "__main__":
    init_db()
    print("Database initialized.")
