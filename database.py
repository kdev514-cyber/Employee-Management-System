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

    # The employees table is created in Supabase.
    # Nothing needs to be created from Python.
    pass


# =========================================================
# CREATE EMPLOYER TABLE
# =========================================================

def create_employer_table():

    # The employers table is created in Supabase.
    # Nothing needs to be created from Python.
    pass


# =========================================================
# ADD EMPLOYEE
# =========================================================

def save_employee(
    name,
    age,
    salary,
    gender,
    nationality,
    employment_start_date,
    employment_end_date,
    still_employed
):

    data = {
        "name": name,
        "age": age,
        "salary": salary,
        "gender": gender,
        "nationality": nationality,
        "employment_start_date": str(
            employment_start_date
        ),
        "employment_end_date": str(
            employment_end_date
        ),
        "still_employed": still_employed
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
            """
            id,
            name,
            age,
            salary,
            gender,
            nationality,
            employment_start_date,
            employment_end_date,
            still_employed
            """
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

            employee["nationality"],

            employee["employment_start_date"],

            employee["employment_end_date"],

            employee["still_employed"]

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
            """
            id,
            name,
            age,
            salary,
            gender,
            nationality,
            employment_start_date,
            employment_end_date,
            still_employed
            """
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

            employee["nationality"],

            employee["employment_start_date"],

            employee["employment_end_date"],

            employee["still_employed"]

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
    nationality,
    employment_start_date,
    employment_end_date,
    still_employed
):

    data = {

        "name": name,

        "age": age,

        "salary": salary,

        "gender": gender,

        "nationality": nationality,

        "employment_start_date": str(
            employment_start_date
        ),

        "employment_end_date": str(
            employment_end_date
        ),

        "still_employed": still_employed

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

    except Exception as e:

        st.error(
            f"Supabase employer registration error: {e}"
        )

        return False


# =========================================================
# CHECK EMPLOYER LOGIN
# =========================================================

def check_employer(
    username,
    password
):

    try:

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

    except Exception as e:

        st.error(
            f"Supabase login error: {e}"
        )

        return None
