import sqlite3

DB_NAME = "study_planner.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
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
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_chapter INTEGER NOT NULL,
            end_chapter INTEGER NOT NULL,
            hours INTEGER NOT NULL,
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        );
    """)

    conn.commit()
    conn.close()


def insert_exam(subject, exam_date, total_chapters, hours_per_day):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO exams (subject, exam_date, total_chapters, hours_per_day)
        VALUES (?, ?, ?, ?)
    """, (subject, exam_date, total_chapters, hours_per_day))

    conn.commit()
    exam_id = cur.lastrowid
    conn.close()
    return exam_id


def get_all_exams():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, subject, exam_date, total_chapters, hours_per_day FROM exams")
    rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "subject": row[1],
            "exam_date": row[2],
            "total_chapters": row[3],
            "hours_per_day": row[4]
        }
        for row in rows
    ]


def save_timetable_rows(exam_id, rows):
    conn = get_connection()
    cur = conn.cursor()

    # Clear existing timetable for exam
    cur.execute("DELETE FROM timetable WHERE exam_id = ?", (exam_id,))

    for row in rows:
        cur.execute("""
            INSERT INTO timetable (exam_id, date, start_chapter, end_chapter, hours)
            VALUES (?, ?, ?, ?, ?)
        """, (row["exam_id"], row["date"], row["start_chapter"], row["end_chapter"], row["hours"]))

    conn.commit()
    conn.close()


def get_timetable_for_date(date_str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.id, t.exam_id, e.subject, t.date, t.start_chapter, t.end_chapter, t.hours
        FROM timetable t
        JOIN exams e ON t.exam_id = e.id
        WHERE t.date = ?
        ORDER BY e.subject
    """, (date_str,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "exam_id": row[1],
            "subject": row[2],
            "date": row[3],
            "start_chapter": row[4],
            "end_chapter": row[5],
            "hours": row[6]
        }
        for row in rows
    ]
