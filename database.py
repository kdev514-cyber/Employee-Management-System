import sqlite3

def create_database():
    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            salary REAL,
            gender TEXT,
            nationality TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_employee(name, age, salary, gender, nationality):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        (name, age, salary, gender, nationality)

        VALUES (?, ?, ?, ?, ?)
    """, (name, age, salary, gender, nationality))

    conn.commit()
    conn.close()

def get_all_employees():

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees


create_database()