import streamlit as st
from database import *
create_table()
create_employer_table()

st.set_page_config(
    page_title="Employee Management System",
    layout="centered"
)
st.title("Employee Management System")

if "role" not in st.session_state:
    st.session_state.role = None
if st.session_state.role is None:
    choice = st.radio(
        "Login as:",
        ["Employee", "Employer"]
    )

    if choice == "Employee":
        if st.button("Continue as Employee"):
            st.session_state.role="employee"
            st.rerun()
    if choice == "Employer":
        if st.button("Continue as Employer"):
            st.session_state.role="employer"
            st.rerun()



if st.session_state.role=="employee":
st.title("Employee Management System")
st.subheader("Fill in the employee details below.")
st.divider()
name = st.text_input("Name")
age = st.text_input("Age")
salary = st.text_input("Salary")
try:
    age = int(age)
    salary = int(salary)
except ValueError:
    st.error("Age and Salary must be numbers.")
gender = st.selectbox(
    "Gender",
    ["Select Gender", "Male", "Female", "Other"]
)
nationality = st.text_input("Nationality")

st.divider()

col1, col2 = st.columns(2)
with col1:
    save = st.button("Save")
with col2:
    Edit_records = st.button("Edit Current Table")
if save:
    if name == "" or age == "" or salary == "" or gender == "Select Gender" or nationality == "":
        st.error("Please fill all the required fields.")
    else:
        save_employee(name, age, salary, gender, nationality)
        st.success("Employee saved successfully!")

if st.session_state.role=="employer":
    st.title("Employer Login")
    username = st.text_input("User ID")
   password = st.text_input(
        "Password",
        type="password"
    )
    if st.button("Login"):
        user = check_employer(username,password)
        if user:
            st.success("Login successful")
            st.session_state.logged_in=True
            st.rerun()
        else:
            st.error("Invalid username/password")

if st.button("Register New Employer"):
    new_user = st.text_input("Create User ID")
    new_password = st.text_input(
        "Create Password",
        type="password"
    )
    if st.button("Create Account"):

        result = register_employer(
            new_user,
            new_password
        )
        if result:
            st.success("Employer account created")
        else:
            st.error("Username already exists")


if st.session_state.get("logged_in"):
    st.title("Employer Dashboard")
if get_records:
    st.subheader("Employee Records")
    employees = get_all_employees()
    if employees:
        st.table(employees)
    else:
        st.info("No employee records found.")
