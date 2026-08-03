import streamlit as st
import re
from database import *

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



st.set_page_config(
    page_title="Employee Management System",
    layout="centered"
)
# -----------------------------
# SESSION STATES
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "home":
    st.title("Employee Management System")
    choice = st.radio(
        "Login as:",
        ["Employee", "Employer"]
    )
    if choice == "Employee":
        if st.button("Continue as Employee"):
            st.session_state.page = "employee"
            st.rerun()
    if choice == "Employer":
        if st.button("Continue as Employer"):
            st.session_state.page = "employer_login"
            st.rerun()

# -----------------------------
# EMPLOYEE PAGE
# -----------------------------
if st.session_state.page == "employee":
    st.title("Employee Details")
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
        save = st.button("Save")
    with col2:
        back = st.button("Back")
    if save:
        if (
            name == ""
            or age == ""
            or salary == ""
            or nationality == ""
            or gender == "Select Gender"
        ):
            st.error("Please fill all fields.")
        else:
            try:
                age = int(age)
                salary = int(salary)
                save_employee(
                    name,
                    age,
                    salary,
                    gender,
                    nationality
                )
                st.success(
                    "Employee saved successfully!"
                )
            except:
                st.error(
                    "Age and Salary must be numbers."
                )
    if back:
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# EMPLOYER LOGIN PAGE
# -----------------------------
if st.session_state.page == "employer_login":
    st.title("Employer Login")
    username = st.text_input(
        "User ID"
    )
    password = st.text_input(
        "Password",
        type="password"
    )
    col1,col2 = st.columns(2)
    with col1:
        login = st.button("Login")
    with col2:
        back = st.button("Back")
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
                "Invalid User ID or Password"
            )
    st.divider()
    if st.button(
        "New Employer? Register Here"
    ):
        st.session_state.page = "register"
        st.rerun()
    if back:
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# REGISTER PAGE
# -----------------------------
if st.session_state.page == "register":
    st.title(
        "Register New Employer"
    )
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
    col1,col2 = st.columns(2)
    with col1:
        register = st.button(
            "Register"
        )
    with col2:
        back_login = st.button(
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
             valid, message = validate_password(new_password)
    if not valid:
        st.error(message)
    else:
        result = register_employer(
            new_user,
            new_password
        )
        if result:
            st.success(
                "Registration successful!"
            )
            st.session_state.page = "employer_login"
            st.rerun()
        else:
            st.error(
                "User ID already exists."
            )
    if back_login:
        st.session_state.page = "employer_login"
        st.rerun()


# -----------------------------
# EMPLOYER DASHBOARD
# -----------------------------
if st.session_state.page == "dashboard":
    st.title(
        "Employer Dashboard"
    )
    st.subheader(
        "Employee Records"
    )
    employees = get_all_employees()
    if employees:
        st.table(employees)
    else:
        st.info(
            "No employee records found."
        )
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.rerun()
