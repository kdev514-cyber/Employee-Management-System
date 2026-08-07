import sqlite3


DATABASE_NAME = "employee.db"


# -----------------------------------
# Database Connection
# -----------------------------------

def create_connection():
    return sqlite3.connect(DATABASE_NAME)


# -----------------------------------
# Create Employee Table
# -----------------------------------

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


# -----------------------------------
# Create Employer Table
# -----------------------------------

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


# -----------------------------------
# Add Employee
# -----------------------------------

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


# -----------------------------------
# Get All Employees
# -----------------------------------

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


# -----------------------------------
# Get One Employee
# -----------------------------------

def get_employee_by_id(employee_id):

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
        WHERE id = ?
    """, (employee_id,))

    employee = cursor.fetchone()

    conn.close()

    return employee


# -----------------------------------
# Update Employee
# -----------------------------------

def update_employee(
    employee_id,
    name,
    age,
    salary,
    gender,
    nationality
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name = ?,
            age = ?,
            salary = ?,
            gender = ?,
            nationality = ?
        WHERE id = ?
    """, (
        name,
        age,
        salary,
        gender,
        nationality,
        employee_id
    ))

    conn.commit()

    rows_updated = cursor.rowcount

    conn.close()

    return rows_updated > 0


# -----------------------------------
# Delete Employee
# -----------------------------------

def delete_employee(employee_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    conn.commit()

    rows_deleted = cursor.rowcount

    conn.close()

    return rows_deleted > 0


# -----------------------------------
# Register Employer
# -----------------------------------

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


# -----------------------------------
# Check Employer Login
# -----------------------------------

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
