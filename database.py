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
    still_in_employment
):

    data = {

        "name": name,

        "age": age,

        "salary": salary,

        "gender": gender,

        "nationality": nationality,

        "employment_start_date":
            employment_start_date,

        "employment_end_date":
            employment_end_date,

        "still_in_employment":
            still_in_employment
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
            still_in_employment
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

            employee["still_in_employment"]

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
            still_in_employment
            """
        )
    )


    # -----------------------------------------------------
    # ID
    # -----------------------------------------------------

    if field == "ID":

        query = query.eq(
            "id",
            int(value)
        )


    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    elif field == "Name":

        query = query.ilike(
            "name",
            f"%{value}%"
        )


    # -----------------------------------------------------
    # AGE
    # -----------------------------------------------------

    elif field == "Age":

        query = query.eq(
            "age",
            int(value)
        )


    # -----------------------------------------------------
    # SALARY
    # -----------------------------------------------------

    elif field == "Salary":

        query = query.eq(
            "salary",
            float(value)
        )


    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    elif field == "Gender":

        query = query.eq(
            "gender",
            value
        )


    # -----------------------------------------------------
    # NATIONALITY
    # -----------------------------------------------------

    elif field == "Nationality":

        query = query.ilike(
            "nationality",
            f"%{value}%"
        )


    # -----------------------------------------------------
    # EMPLOYMENT START DATE
    # -----------------------------------------------------

    elif field == "Employment Start Date":

        query = query.eq(
            "employment_start_date",
            value
        )


    # -----------------------------------------------------
    # EMPLOYMENT END DATE
    # -----------------------------------------------------

    elif field == "Employment End Date":

        query = query.eq(
            "employment_end_date",
            value
        )


    # -----------------------------------------------------
    # STILL IN EMPLOYMENT
    # -----------------------------------------------------

    elif field == "Still in Employment":

        if value == "Yes":

            query = query.eq(
                "still_in_employment",
                True
            )

        else:

            query = query.eq(
                "still_in_employment",
                False
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

            employee["still_in_employment"]

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
    still_in_employment
):

    data = {

        "name": name,

        "age": age,

        "salary": salary,

        "gender": gender,

        "nationality": nationality,

        "employment_start_date":
            employment_start_date,

        "employment_end_date":
            employment_end_date,

        "still_in_employment":
            still_in_employment

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
