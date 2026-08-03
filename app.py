import streamlit as st
from database import save_employee, get_all_employees

st.set_page_config(
    page_title="Employee Management System",
    layout="centered"
)

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
    get_records = st.button("Get Employee Records")

if save:
    if name == "" or age == "" or salary == "" or gender == "Select Gender" or nationality == "":
        st.error("Please fill all the required fields.")
    else:
        save_employee(name, age, salary, gender, nationality)
        st.success("Employee saved successfully!")

if get_records:
    st.subheader("Employee Records")
    employees = get_all_employees()
    if employees:
        st.table(employees)
    else:
        st.info("No employee records found.")