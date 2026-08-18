import streamlit as st
from supabase import create_client


# =========================================================
# SUPABASE CONNECTION
# =========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# CREATE TABLE
# =========================================================

def create_table():
    """
    Supabase tables are created from the Supabase dashboard.
    Nothing needs to be created here.
    """
    pass


# =========================================================
# CREATE EMPLOYER TABLE
# =========================================================

def create_employer_table():
    """
    Supabase tables are created from the Supabase dashboard.
    Nothing needs to be created here.
    """
    pass


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

    data = {
        "name": name,
        "age": age,
        "salary": salary,
        "gender": gender,
        "nationality": nationality
    }

    response = (
        supabase
        .table("employees")
        .insert(data)
        .execute()
    )

    return response.data


# =========================================================
# GET ALL EMPLOYEES
# =========================================================

def get_all_employees():

    response = (
        supabase
        .table("employees")
        .select(
            "id, name, age, salary, gender, nationality"
        )
        .order(
            "id"
        )
        .execute()
    )

    employees = []

    for employee in response.data:

        employees.append([
            employee["id"],
            employee["name"],
            employee["age"],
            employee["salary"],
            employee["gender"],
            employee["nationality"]
        ])

    return employees


# =========================================================
# SEARCH EMPLOYEES
# =========================================================

def search_employees(field, value):

    query = (
        supabase
        .table("employees")
        .select(
            "id, name, age, salary, gender, nationality"
        )
    )

    # -----------------------------------------------------
    # SEARCH BY ID
    # -----------------------------------------------------

    if field == "ID":

        query = query.eq(
            "id",
            int(value)
        )


    # -----------------------------------------------------
    # SEARCH BY NAME
    # -----------------------------------------------------

    elif field == "Name":

        query = query.ilike(
            "name",
            f"%{value}%"
        )


    # -----------------------------------------------------
    # SEARCH BY AGE
    # -----------------------------------------------------

    elif field == "Age":

        query = query.eq(
            "age",
            int(value)
        )


    # -----------------------------------------------------
    # SEARCH BY SALARY
    # -----------------------------------------------------

    elif field == "Salary":

        query = query.eq(
            "salary",
            float(value)
        )


    # -----------------------------------------------------
    # SEARCH BY GENDER
    # -----------------------------------------------------

    elif field == "Gender":

        query = query.eq(
            "gender",
            value
        )


    # -----------------------------------------------------
    # SEARCH BY NATIONALITY
    # -----------------------------------------------------

    elif field == "Nationality":

        query = query.ilike(
            "nationality",
            f"%{value}%"
        )


    else:

        return []


    response = (
        query
        .order("id")
        .execute()
    )

    employees = []

    for employee in response.data:

        employees.append([
            employee["id"],
            employee["name"],
            employee["age"],
            employee["salary"],
            employee["gender"],
            employee["nationality"]
        ])

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

    data = {
        "name": name,
        "age": age,
        "salary": salary,
        "gender": gender,
        "nationality": nationality
    }

    response = (
        supabase
        .table("employees")
        .update(data)
        .eq(
            "id",
            employee_id
        )
        .execute()
    )

    return len(response.data) > 0


# =========================================================
# DELETE EMPLOYEE
# =========================================================

def delete_employee(employee_id):

    response = (
        supabase
        .table("employees")
        .delete()
        .eq(
            "id",
            employee_id
        )
        .execute()
    )

    return len(response.data) > 0


# =========================================================
# REGISTER EMPLOYER
# =========================================================

def register_employer(
    username,
    password
):

    try:

        data = {
            "username": username,
            "password": password
        }

        response = (
            supabase
            .table("employers")
            .insert(data)
            .execute()
        )

        return len(response.data) > 0


    except Exception:

        return False


# =========================================================
# CHECK EMPLOYER LOGIN
# =========================================================

def check_employer(
    username,
    password
):

    response = (
        supabase
        .table("employers")
        .select(
            "id, username"
        )
        .eq(
            "username",
            username
        )
        .eq(
            "password",
            password
        )
        .execute()
    )

    if response.data:

        employer = response.data[0]

        return (
            employer["id"],
            employer["username"]
        )

    return None

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
