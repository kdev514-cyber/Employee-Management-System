import sqlite3
DATABASE_NAME = "employee.db"

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            salary REAL NOT NULL,
            gender TEXT NOT NULL,
            nationality TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def create_employer_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def save_employee(name, age, salary, gender, nationality):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        (name, age, salary, gender, nationality)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        age,
        salary,
        gender,
        nationality
    ))

    conn.commit()
    conn.close()

def get_all_employees():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            age,
            salary,
            gender,
            nationality
        FROM employees
    """)

    employees = cursor.fetchall()

    conn.close()

    return employees

def register_employer(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO employers
            (username, password)
            VALUES (?, ?)
        """, (
            username,
            password
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()

def check_employer(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employers
        WHERE username = ?
        AND password = ?
    """, (
        username,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user
