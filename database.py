import sqlite3

#Employee Database
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

#Employer Database
def create_employer_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()
    


def register_employer(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO employers(username,password)
            VALUES (?,?)
        """,(username,password))

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()

def check_employer(username,password):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM employers
        WHERE username=? AND password=?
    """,(username,password))

    result = cursor.fetchone()

    conn.close()

    return result
