import sqlite3


# Database connection
def create_connection():

    conn = sqlite3.connect("employee.db")

    return conn



# Employee table
def create_table():

    conn = create_connection()

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            salary INTEGER,
            gender TEXT,
            nationality TEXT

        )
    """)


    conn.commit()

    conn.close()



# Employer table
def create_employer_table():

    conn = create_connection()

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT

        )
    """)


    conn.commit()

    conn.close()



# Save employee
def save_employee(name, age, salary, gender, nationality):

    conn = create_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO employees
        (name, age, salary, gender, nationality)

        VALUES (?, ?, ?, ?, ?)

    """,
    (
        name,
        age,
        salary,
        gender,
        nationality
    ))


    conn.commit()

    conn.close()



# Get employee records
def get_all_employees():

    conn = create_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM employees"
    )


    data = cursor.fetchall()


    conn.close()


    return data



# Register employer
def register_employer(username, password):

    conn = create_connection()

    cursor = conn.cursor()


    try:

        cursor.execute("""
            INSERT INTO employers
            (username,password)

            VALUES (?,?)

        """,
        (
            username,
            password
        ))


        conn.commit()

        return True


    except sqlite3.IntegrityError:

        return False


    finally:

        conn.close()



# Check employer login
def check_employer(username, password):

    conn = create_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM employers

        WHERE username=? 
        AND password=?

    """,
    (
        username,
        password
    ))


    user = cursor.fetchone()


    conn.close()


    return user
