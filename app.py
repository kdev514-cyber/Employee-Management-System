import streamlit as st
import re

from database import (
    create_table,
    create_employer_table,
    save_employee,
    get_all_employees,
    get_employee_by_id,
    search_employees,
    update_employee,
    delete_employee,
    register_employer,
    check_employer
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="centered"
)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

create_table()
create_employer_table()


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):

    if len(password) < 8:

        return (
            False,
            "Password must contain at least 8 characters."
        )

    if not re.search(r"[A-Z]", password):

        return (
            False,
            "Password must contain at least one capital letter."
        )

    if not re.search(r"[a-z]", password):

        return (
            False,
            "Password must contain at least one small letter."
        )

    if not re.search(r"[0-9]", password):

        return (
            False,
            "Password must contain at least one number."
        )

    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]",
        password
    ):

        return (
            False,
            "Password must contain at least one special character."
        )

    return True, ""


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.title("👨‍💼 Employee Management System")

    st.write(
        "Please select how you want to continue."
    )

    st.divider()

    choice = st.radio(
        "Login as:",
        [
            "Employee",
            "Employer"
        ]
    )


    # -----------------------------------------
    # EMPLOYEE
    # -----------------------------------------

    if choice == "Employee":

        if st.button(
            "Continue as Employee",
            use_container_width=True
        ):

            st.session_state.page = "employee"

            st.rerun()


    # -----------------------------------------
    # EMPLOYER
    # -----------------------------------------

    else:

        if st.button(
            "Continue as Employer",
            use_container_width=True
        ):

            st.session_state.page = "employer_login"

            st.rerun()


# ============================================================
# EMPLOYEE PAGE
# ============================================================

elif st.session_state.page == "employee":

    st.title("👤 Employee Details")

    st.write(
        "Fill in your details below."
    )

    st.divider()


    name = st.text_input(
        "Name"
    )


    age = st.text_input(
        "Age"
    )


    salary = st.text_input(
        "Salary"
    )


    gender = st.selectbox(
        "Gender",
        [
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ]
    )


    nationality = st.text_input(
        "Nationality"
    )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        save = st.button(
            "💾 Save",
            use_container_width=True
        )


    with col2:

        back = st.button(
            "⬅️ Back",
            use_container_width=True
        )


    # -----------------------------------------
    # SAVE EMPLOYEE
    # -----------------------------------------

    if save:

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
                    "Employee saved successfully!"
                )


            except ValueError:

                st.error(
                    "Age must be a whole number and Salary must be a number."
                )


    # -----------------------------------------
    # BACK
    # -----------------------------------------

    if back:

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# EMPLOYER LOGIN
# ============================================================

elif st.session_state.page == "employer_login":

    st.title("🔐 Employer Login")

    username = st.text_input(
        "User ID"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        login = st.button(
            "🔑 Login",
            use_container_width=True
        )


    with col2:

        back = st.button(
            "⬅️ Back",
            use_container_width=True
        )


    # -----------------------------------------
    # LOGIN
    # -----------------------------------------

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


    # -----------------------------------------
    # REGISTER
    # -----------------------------------------

    if st.button(
        "New Employer? Register Here",
        use_container_width=True
    ):

        st.session_state.page = "register"

        st.rerun()


    # -----------------------------------------
    # BACK
    # -----------------------------------------

    if back:

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# REGISTER EMPLOYER
# ============================================================

elif st.session_state.page == "register":

    st.title("📝 Register New Employer")

    st.write(
        "Create a new employer account."
    )

    st.divider()


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


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        register = st.button(
            "Register",
            use_container_width=True
        )


    with col2:

        login_existing = st.button(
            "Login Existing User",
            use_container_width=True
        )


    # -----------------------------------------
    # REGISTER
    # -----------------------------------------

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


    # -----------------------------------------
    # LOGIN EXISTING
    # -----------------------------------------

    if login_existing:

        st.session_state.page = "employer_login"

        st.rerun()


# ============================================================
# EMPLOYER DASHBOARD
# ============================================================

elif st.session_state.page == "dashboard":

    st.title("🏢 Employer Dashboard")

    st.write(
        "Manage employee records using the options below."
    )

    st.divider()


    # -----------------------------------------
    # ROW 1
    # -----------------------------------------

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


    # -----------------------------------------
    # ROW 2
    # -----------------------------------------

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


    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# GET / SEARCH EMPLOYEE RECORDS
# ============================================================

elif st.session_state.page == "records":

    st.title("📋 Get Employee Records")

    st.write(
        "Search employees using any available field."
    )

    st.divider()


    search_field = st.selectbox(
        "Search Employee By",
        [
            "Show All",
            "ID",
            "Name",
            "Age",
            "Salary",
            "Gender",
            "Nationality"
        ]
    )


    # ========================================================
    # SHOW ALL
    # ========================================================

    if search_field == "Show All":

        if st.button(
            "📋 Show All Employees",
            use_container_width=True
        ):

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


    # ========================================================
    # SEARCH BY GENDER
    # ========================================================

    elif search_field == "Gender":

        gender = st.selectbox(
            "Select Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )


        if st.button(
            "🔍 Search",
            use_container_width=True
        ):

            employees = search_employees(
                "Gender",
                gender
            )


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

                st.warning(
                    "No employees found."
                )


    # ========================================================
    # SEARCH BY OTHER FIELDS
    # ========================================================

    else:

        search_value = st.text_input(
            f"Enter {search_field}"
        )


        if st.button(
            "🔍 Search",
            use_container_width=True
        ):

            if search_value == "":

                st.error(
                    f"Please enter {search_field}."
                )

            else:

                try:

                    # ----------------------------------
                    # Convert ID and Age to integer
                    # ----------------------------------

                    if search_field in [
                        "ID",
                        "Age"
                    ]:

                        search_value = int(
                            search_value
                        )


                    # ----------------------------------
                    # Convert Salary to float
                    # ----------------------------------

                    elif search_field == "Salary":

                        search_value = float(
                            search_value
                        )


                    # ----------------------------------
                    # Search database
                    # ----------------------------------

                    employees = search_employees(
                        search_field,
                        search_value
                    )


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

                        st.warning(
                            "No employees found."
                        )


                except ValueError:

                    st.error(
                        f"{search_field} must contain a valid number."
                    )


    st.divider()


    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state.page = "dashboard"

        st.rerun()


# ============================================================
# ADD EMPLOYEE — EMPLOYER
# ============================================================

elif st.session_state.page == "employer_add":

    st.title("➕ Add Employee")

    st.write(
        "Employer can manually add an employee."
    )

    st.divider()


    name = st.text_input(
        "Name"
    )


    age = st.text_input(
        "Age"
    )


    salary = st.text_input(
        "Salary"
    )


    gender = st.selectbox(
        "Gender",
        [
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ]
    )


    nationality = st.text_input(
        "Nationality"
    )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        add = st.button(
            "💾 Add Employee",
            use_container_width=True
        )


    with col2:

        back = st.button(
            "⬅️ Back",
            use_container_width=True
        )


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
                    "Age must be a whole number and Salary must be a number."
                )


    if back:

        st.session_state.page = "dashboard"

        st.rerun()


# ============================================================
# EDIT EMPLOYEE
# ============================================================

elif st.session_state.page == "employer_edit":

    st.title("✏️ Edit Employee")

    st.write(
        "Enter an employee ID to load their existing information."
    )

    st.divider()


    employee_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1
    )


    if st.button(
        "🔍 Load Employee",
        use_container_width=True
    ):

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


    # ========================================================
    # DISPLAY EMPLOYEE INFORMATION
    # ========================================================

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


            if employee[4] in gender_options:

                gender_index = gender_options.index(
                    employee[4]
                )

            else:

                gender_index = 0


            edit_gender = st.selectbox(
                "Gender",
                gender_options,
                index=gender_index
            )


            edit_nationality = st.text_input(
                "Nationality",
                value=employee[5]
            )


            if st.button(
                "💾 Update Employee",
                use_container_width=True
            ):

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

                        age_number = int(
                            edit_age
                        )

                        salary_number = float(
                            edit_salary
                        )


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
                            "Age must be a whole number and Salary must be a number."
                        )


    st.divider()


    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True
    ):

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

    st.divider()


    employee_id = st.number_input(
        "Employee ID to Delete",
        min_value=1,
        step=1
    )


    confirm = st.checkbox(
        "I confirm that I want to delete this employee."
    )


    col1, col2 = st.columns(2)


    with col1:

        delete = st.button(
            "🗑️ Delete Employee",
            use_container_width=True
        )


    with col2:

        back = st.button(
            "⬅️ Back",
            use_container_width=True
        )


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
