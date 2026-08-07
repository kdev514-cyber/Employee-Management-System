import streamlit as st
import re

from database import (
    create_table,
    create_employer_table,
    save_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
    register_employer,
    check_employer
)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="centered"
)


# -----------------------------------
# CREATE DATABASE TABLES
# -----------------------------------

create_table()
create_employer_table()


# -----------------------------------
# PASSWORD VALIDATION
# -----------------------------------

def validate_password(password):

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one capital letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one small letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, ""


# -----------------------------------
# SESSION STATES
# -----------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.title("👨‍💼 Employee Management System")

    choice = st.radio(
        "Login as:",
        ["Employee", "Employer"]
    )

    if choice == "Employee":

        if st.button("Continue as Employee"):

            st.session_state.page = "employee"
            st.rerun()

    else:

        if st.button("Continue as Employer"):

            st.session_state.page = "employer_login"
            st.rerun()


# ============================================================
# EMPLOYEE PAGE
# ============================================================

elif st.session_state.page == "employee":

    st.title("👤 Employee Details")

    st.write("Fill in your details below.")

    st.divider()

    name = st.text_input("Name")

    age = st.text_input("Age")

    salary = st.text_input("Salary")

    gender = st.selectbox(
        "Gender",
        [
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ]
    )

    nationality = st.text_input("Nationality")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        save = st.button("💾 Save")

    with col2:

        back = st.button("⬅️ Back")

    if save:

        if (
            name == ""
            or age == ""
            or salary == ""
            or nationality == ""
            or gender == "Select Gender"
        ):

            st.error("Please fill all the required fields.")

        else:

            try:

                age_number = int(age)
                salary_number = float(salary)

                save_employee(
                    name,
                    age_number,
                    salary_number,
                    gender,
                    nationality
                )

                st.success(
                    "Employee saved successfully!"
                )

            except ValueError:

                st.error(
                    "Age and Salary must be numbers."
                )

    if back:

        st.session_state.page = "home"
        st.rerun()


# ============================================================
# EMPLOYER LOGIN
# ============================================================

elif st.session_state.page == "employer_login":

    st.title("🔐 Employer Login")

    username = st.text_input("User ID")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        login = st.button("🔑 Login")

    with col2:

        back = st.button("⬅️ Back")

    if login:

        user = check_employer(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.page = "dashboard"

            st.rerun()

        else:

            st.error(
                "Invalid User ID or Password."
            )

    st.divider()

    if st.button("New Employer? Register Here"):

        st.session_state.page = "register"
        st.rerun()

    if back:

        st.session_state.page = "home"
        st.rerun()


# ============================================================
# REGISTER PAGE
# ============================================================

elif st.session_state.page == "register":

    st.title("📝 Register New Employer")

    new_user = st.text_input(
        "Create User ID"
    )

    new_password = st.text_input(
        "Create Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Retype Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        register = st.button("Register")

    with col2:

        login_existing = st.button(
            "Login Existing User"
        )

    if register:

        if (
            new_user == ""
            or new_password == ""
            or confirm_password == ""
        ):

            st.error(
                "Please fill all fields."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            valid, message = validate_password(
                new_password
            )

            if not valid:

                st.error(message)

            else:

                result = register_employer(
                    new_user,
                    new_password
                )

                if result:

                    st.success(
                        "Employer registered successfully!"
                    )

                    st.session_state.page = "employer_login"
                    st.rerun()

                else:

                    st.error(
                        "User ID already exists."
                    )

    if login_existing:

        st.session_state.page = "employer_login"
        st.rerun()


# ============================================================
# EMPLOYER DASHBOARD
# ============================================================

elif st.session_state.page == "dashboard":

    st.title("🏢 Employer Dashboard")

    st.write(
        "Manage employee records from the options below."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📋 Get Employee Records",
            use_container_width=True
        ):

            st.session_state.page = "records"
            st.rerun()

    with col2:

        if st.button(
            "➕ Add Employee",
            use_container_width=True
        ):

            st.session_state.page = "employer_add"
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        if st.button(
            "✏️ Edit Employee",
            use_container_width=True
        ):

            st.session_state.page = "employer_edit"
            st.rerun()

    with col4:

        if st.button(
            "🗑️ Delete Employee",
            use_container_width=True
        ):

            st.session_state.page = "employer_delete"
            st.rerun()

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.page = "home"

        st.rerun()


# ============================================================
# GET EMPLOYEE RECORDS
# ============================================================

elif st.session_state.page == "records":

    st.title("📋 Employee Records")

    employees = get_all_employees()

    if employees:

        st.dataframe(
            employees,
            column_config={
                0: "ID",
                1: "Name",
                2: "Age",
                3: "Salary",
                4: "Gender",
                5: "Nationality"
            },
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No employee records found."
        )

    st.divider()

    if st.button("⬅️ Back to Dashboard"):

        st.session_state.page = "dashboard"
        st.rerun()


# ============================================================
# ADD EMPLOYEE
# ============================================================

elif st.session_state.page == "employer_add":

    st.title("➕ Add Employee")

    st.write(
        "Employer can manually add an employee."
    )

    name = st.text_input("Name")

    age = st.text_input("Age")

    salary = st.text_input("Salary")

    gender = st.selectbox(
        "Gender",
        [
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ]
    )

    nationality = st.text_input("Nationality")

    col1, col2 = st.columns(2)

    with col1:

        add = st.button("💾 Add Employee")

    with col2:

        back = st.button("⬅️ Back")

    if add:

        if (
            name == ""
            or age == ""
            or salary == ""
            or nationality == ""
            or gender == "Select Gender"
        ):

            st.error(
                "Please fill all the required fields."
            )

        else:

            try:

                age_number = int(age)
                salary_number = float(salary)

                save_employee(
                    name,
                    age_number,
                    salary_number,
                    gender,
                    nationality
                )

                st.success(
                    "Employee added successfully!"
                )

            except ValueError:

                st.error(
                    "Age and Salary must be numbers."
                )

    if back:

        st.session_state.page = "dashboard"
        st.rerun()


# ============================================================
# EDIT EMPLOYEE
# ============================================================

elif st.session_state.page == "employer_edit":

    st.title("✏️ Edit Employee")

    employee_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1
    )

    load = st.button("🔍 Load Employee")

    if load:

        employee = get_employee_by_id(
            employee_id
        )

        if employee:

            st.session_state.edit_employee = employee

        else:

            st.session_state.edit_employee = None

            st.error(
                "Employee not found."
            )

    if "edit_employee" in st.session_state:

        employee = st.session_state.edit_employee

        if employee:

            st.divider()

            st.subheader(
                f"Editing Employee ID: {employee[0]}"
            )

            edit_name = st.text_input(
                "Name",
                value=employee[1]
            )

            edit_age = st.text_input(
                "Age",
                value=str(employee[2])
            )

            edit_salary = st.text_input(
                "Salary",
                value=str(employee[3])
            )

            gender_options = [
                "Male",
                "Female",
                "Other"
            ]

            gender_index = (
                gender_options.index(employee[4])
                if employee[4] in gender_options
                else 0
            )

            edit_gender = st.selectbox(
                "Gender",
                gender_options,
                index=gender_index
            )

            edit_nationality = st.text_input(
                "Nationality",
                value=employee[5]
            )

            update = st.button(
                "💾 Update Employee"
            )

            if update:

                if (
                    edit_name == ""
                    or edit_age == ""
                    or edit_salary == ""
                    or edit_nationality == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                else:

                    try:

                        age_number = int(edit_age)
                        salary_number = float(edit_salary)

                        result = update_employee(
                            employee[0],
                            edit_name,
                            age_number,
                            salary_number,
                            edit_gender,
                            edit_nationality
                        )

                        if result:

                            st.success(
                                "Employee updated successfully!"
                            )

                            st.session_state.pop(
                                "edit_employee",
                                None
                            )

                        else:

                            st.error(
                                "Employee could not be updated."
                            )

                    except ValueError:

                        st.error(
                            "Age and Salary must be numbers."
                        )

    st.divider()

    if st.button("⬅️ Back to Dashboard"):

        st.session_state.pop(
            "edit_employee",
            None
        )

        st.session_state.page = "dashboard"
        st.rerun()


# ============================================================
# DELETE EMPLOYEE
# ============================================================

elif st.session_state.page == "employer_delete":

    st.title("🗑️ Delete Employee")

    st.warning(
        "Deleting an employee is permanent."
    )

    employee_id = st.number_input(
        "Enter Employee ID to Delete",
        min_value=1,
        step=1
    )

    confirm = st.checkbox(
        "I confirm that I want to delete this employee."
    )

    col1, col2 = st.columns(2)

    with col1:

        delete = st.button("🗑️ Delete Employee")

    with col2:

        back = st.button("⬅️ Back")

    if delete:

        if not confirm:

            st.error(
                "Please confirm the deletion."
            )

        else:

            result = delete_employee(
                employee_id
            )

            if result:

                st.success(
                    "Employee deleted successfully!"
                )

            else:

                st.error(
                    "Employee ID not found."
                )

    if back:

        st.session_state.page = "dashboard"
        st.rerun()
