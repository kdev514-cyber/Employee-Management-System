import sqlite3


DATABASE_NAME = "employee.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def create_connection():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# CREATE EMPLOYEE TABLE
# =========================================================

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


# =========================================================
# CREATE EMPLOYER TABLE
# =========================================================

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


# =========================================================
# ADD EMPLOYEE
# =========================================================

def save_employee(
    name,
    age,
    salary,
    gender,
    nationality
):

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


# =========================================================
# GET ALL EMPLOYEES
# =========================================================

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
        ORDER BY id
    """)

    employees = cursor.fetchall()

    conn.close()

    return employees


# =========================================================
# SEARCH EMPLOYEES
# =========================================================

def search_employees(field, value):

    conn = create_connection()
    cursor = conn.cursor()

    if field == "ID":

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
        """, (int(value),))


    elif field == "Name":

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                salary,
                gender,
                nationality
            FROM employees
            WHERE name LIKE ?
            ORDER BY id
        """, (f"%{value}%",))


    elif field == "Age":

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                salary,
                gender,
                nationality
            FROM employees
            WHERE age = ?
            ORDER BY id
        """, (int(value),))


    elif field == "Salary":

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                salary,
                gender,
                nationality
            FROM employees
            WHERE salary = ?
            ORDER BY id
        """, (float(value),))


    elif field == "Gender":

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                salary,
                gender,
                nationality
            FROM employees
            WHERE gender = ?
            ORDER BY id
        """, (value,))


    elif field == "Nationality":

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                salary,
                gender,
                nationality
            FROM employees
            WHERE nationality LIKE ?
            ORDER BY id
        """, (f"%{value}%",))


    else:

        employees = []

        conn.close()

        return employees


    employees = cursor.fetchall()

    conn.close()

    return employees


# =========================================================
# UPDATE EMPLOYEE
# =========================================================

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


# =========================================================
# DELETE EMPLOYEE
# =========================================================

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


# =========================================================
# REGISTER EMPLOYER
# =========================================================

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

        conn.close()

        return True


    except sqlite3.IntegrityError:

        conn.close()

        return False


# =========================================================
# CHECK EMPLOYER LOGIN
# =========================================================

def check_employer(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username
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
