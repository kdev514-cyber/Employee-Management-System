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
# CREATE EMPLOYEE TABLE
# =========================================================

def create_table():
    # Table is already created in Supabase
    pass


# =========================================================
# CREATE EMPLOYER TABLE
# =========================================================

def create_employer_table():
    # Table is already created in Supabase
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

    if field == "ID":

        query = query.eq(
            "id",
            int(value)
        )

    elif field == "Name":

        query = query.ilike(
            "name",
            f"%{value}%"
        )

    elif field == "Age":

        query = query.eq(
            "age",
            int(value)
        )

    elif field == "Salary":

        query = query.eq(
            "salary",
            float(value)
        )

    elif field == "Gender":

        query = query.eq(
            "gender",
            value
        )

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
