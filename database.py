import sqlite3

def setup_database():
    """Sets up the database with tables for students, classes, enrollments, and attendance."""
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY, 
            full_name TEXT NOT NULL
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            class_name TEXT UNIQUE NOT NULL
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            student_id TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
            UNIQUE(student_id, class_id)
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            student_id TEXT NOT NULL,
            class_id INTEGER NOT NULL, 
            date TEXT NOT NULL, 
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
        )''')
    
    conn.commit()
    conn.close()

def add_student(student_id, full_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (student_id, full_name) VALUES (?, ?)", (student_id, full_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_students():
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, full_name FROM students ORDER BY full_name")
        return cursor.fetchall()
    finally:
        conn.close()

def update_student(original_student_id, new_full_name):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET full_name = ? WHERE student_id = ?", (new_full_name, original_student_id))
        conn.commit()
    finally:
        conn.close()

def delete_student(student_id):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
    finally:
        conn.close()

def add_class(class_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO classes (class_name) VALUES (?)", (class_name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_classes():
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT class_id, class_name FROM classes ORDER BY class_name")
        return cursor.fetchall()
    finally:
        conn.close()

def update_class(class_id, new_class_name):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE classes SET class_name = ? WHERE class_id = ?", (new_class_name, class_id))
        conn.commit()
    finally:
        conn.close()

def delete_class(class_id):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM classes WHERE class_id = ?", (class_id,))
        conn.commit()
    finally:
        conn.close()

def enroll_student(student_id, class_id):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)", (student_id, class_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_students_by_class(class_id):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.student_id, s.full_name 
            FROM students s 
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE e.class_id = ? 
            ORDER BY s.full_name
        ''', (class_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def mark_attendance(student_id, class_id, date, status):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT attendance_id FROM attendance WHERE student_id = ? AND class_id = ? AND date = ?", (student_id, class_id, date))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("UPDATE attendance SET status = ? WHERE attendance_id = ?", (status, exists[0]))
        else:
            cursor.execute("INSERT INTO attendance (student_id, class_id, date, status) VALUES (?, ?, ?, ?)", (student_id, class_id, date, status))
        conn.commit()
    finally:
        conn.close()

def get_attendance_report(class_id, start_date, end_date):
    conn = sqlite3.connect('attendance.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.student_id, s.full_name, a.date, a.status 
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            WHERE a.class_id = ? AND a.date BETWEEN ? AND ?
            ORDER BY a.date, s.full_name
        ''', (class_id, start_date, end_date))
        return cursor.fetchall()
    finally:
        conn.close()