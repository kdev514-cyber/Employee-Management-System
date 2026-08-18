import streamlit as st
import re
import io
import smtplib

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from email.message import EmailMessage

from database import (
    create_table,
    create_employer_table,
    save_employee,
    get_all_employees,
    search_employees,
    update_employee,
    delete_employee,
    register_employer,
    check_employer
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Employee Management System",
    layout="centered"
)


# =========================================================
# DATABASE CREATION
# =========================================================

create_table()
create_employer_table()


# =========================================================
# GENERATE EMPLOYEE PDF
# =========================================================

def generate_employee_pdf(employees):

    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    normal = styles["Normal"]

    elements = []

    # Title
    elements.append(
        Paragraph(
            "Employee Management System",
            title
        )
    )

    elements.append(
        Spacer(1, 0.3 * cm)
    )

    elements.append(
        Paragraph(
            "Employee Records Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    # Table header
    data = [[
        "ID",
        "Name",
        "Age",
        "Salary",
        "Gender",
        "Nationality"
    ]]

    # Employee records
    for employee in employees:

        data.append([
            str(employee[0]),
            str(employee[1]),
            str(employee[2]),
            f"${employee[3]:,.2f}",
            str(employee[4]),
            str(employee[5])
        ])

    # Create table
    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            1.0 * cm,
            4.0 * cm,
            1.2 * cm,
            2.8 * cm,
            2.5 * cm,
            3.5 * cm
        ]
    )

    # Table formatting
    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0, 0),
                (0, -1),
                "CENTER"
            ),

            (
                "ALIGN",
                (2, 1),
                (3, -1),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.lightgrey
                ]
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    elements.append(
        Paragraph(
            f"Total Employees: {len(employees)}",
            normal
        )
    )

    # Generate PDF
    document.build(elements)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# =========================================================
# SEND PDF BY EMAIL
# =========================================================

def send_pdf_email(pdf_data, filename):

    sender_email = st.secrets["EMAIL_ADDRESS"]
    sender_password = st.secrets["EMAIL_PASSWORD"]
    email1 = st.secrets["REPORT_EMAIL_1"]
    email2 = st.secrets["REPORT_EMAIL_2"]
    cc_email = st.secrets["REPORT_EMAIL_CC"]
    
    message = EmailMessage()
    message["Subject"] = "Employee Records Report"
    message["From"] = sender_email
    message["To"] = f"{email1}, {email2}"

    # Two recipients
    message["Cc"] = cc_email

    message.set_content(
        """
Hello,

Please find attached the latest Employee Records Report.

This report was generated from the Employee Management System.

Regards,
Employee Management System
"""
    )

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=filename
    )

    # Gmail SMTP
    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(message)


# =========================================================
# PASSWORD VALIDATION
# =========================================================

def validate_password(password):

    if len(password) < 8:

        return False, (
            "Password must contain at least 8 characters."
        )

    if not re.search(r"[A-Z]", password):

        return False, (
            "Password must contain at least one capital letter."
        )

    if not re.search(r"[a-z]", password):

        return False, (
            "Password must contain at least one small letter."
        )

    if not re.search(r"[0-9]", password):

        return False, (
            "Password must contain at least one number."
        )

    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]",
        password
    ):

        return False, (
            "Password must contain at least one special character."
        )

    return True, ""


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.title(
        "Employee Management System"
    )

    st.write(
        "Welcome! Please select how you want to continue."
    )

    choice = st.radio(
        "Login as:",
        [
            "Employee",
            "Employer"
        ]
    )

    # Employee
    if choice == "Employee":

        if st.button(
            "Continue as Employee",
            use_container_width=True
        ):

            st.session_state.page = "employee"

            st.rerun()

    # Employer
    if choice == "Employer":

        if st.button(
            "Continue as Employer",
            use_container_width=True
        ):

            st.session_state.page = "employer_login"

            st.rerun()


# =========================================================
# EMPLOYEE PAGE
# =========================================================

if st.session_state.page == "employee":

    st.title("Employee Details")

    st.write(
        "Enter the employee information below."
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

        save = st.button(
            "Save Employee",
            use_container_width=True
        )

    with col2:

        back = st.button(
            "Back",
            use_container_width=True
        )

    # Save employee
    if save:

        if (
            name.strip() == ""
            or age.strip() == ""
            or salary.strip() == ""
            or nationality.strip() == ""
            or gender == "Select Gender"
        ):

            st.error(
                "Please fill all the required fields."
            )

        else:

            try:

                age_number = int(age)

                salary_number = float(salary)

                if age_number <= 18:

                    st.error(
                        "Age must be greater than 18."
                    )

                elif salary_number < 0:

                    st.error(
                        "Salary cannot be negative."
                    )

                else:

                    save_employee(
                        name.strip(),
                        age_number,
                        salary_number,
                        gender,
                        nationality.strip()
                    )

                    st.success(
                        "Employee saved successfully!"
                    )

            except ValueError:

                st.error(
                    "Age must be a whole number and Salary must be a number."
                )

    # Back
    if back:

        st.session_state.page = "home"

        st.rerun()


# =========================================================
# EMPLOYER LOGIN
# =========================================================

if st.session_state.page == "employer_login":

    st.title("Employer Login")

    username = st.text_input(
        "User ID"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        login = st.button(
            "Login",
            use_container_width=True
        )

    with col2:

        back = st.button(
            "Back",
            use_container_width=True
        )

    # Login
    if login:

        if (
            username.strip() == ""
            or password == ""
        ):

            st.error(
                "Please enter User ID and Password."
            )

        else:

            user = check_employer(
                username.strip(),
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

    # Register
    if st.button(
        "New Employer? Register Here",
        use_container_width=True
    ):

        st.session_state.page = "register"

        st.rerun()

    # Back
    if back:

        st.session_state.page = "home"

        st.rerun()


# =========================================================
# REGISTRATION
# =========================================================

if st.session_state.page == "register":

    st.title("Register New Employer")

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

        register = st.button(
            "Register",
            use_container_width=True
        )

    with col2:

        login_existing = st.button(
            "Login Existing User",
            use_container_width=True
        )

    # Register
    if register:

        if (
            new_user.strip() == ""
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
                    new_user.strip(),
                    new_password
                )

                if result:

                    st.success(
                        "Employer registered successfully!"
                    )

                    st.info(
                        "Redirecting to login..."
                    )

                    st.session_state.page = (
                        "employer_login"
                    )

                    st.rerun()

                else:

                    st.error(
                        "User ID already exists."
                    )

    # Login existing
    if login_existing:

        st.session_state.page = "employer_login"

        st.rerun()


# =========================================================
# EMPLOYER DASHBOARD
# =========================================================

if st.session_state.page == "dashboard":

    # Security check
    if not st.session_state.logged_in:

        st.session_state.page = "employer_login"

        st.rerun()

    st.title("Employer Dashboard")

    st.write(
        "Manage employee records"
    )

    # Dashboard menu
    action = st.radio(
        "Choose an action:",
        [
            "Get Employee Records",
            "Add Employee",
            "Edit Employee",
            "Delete Employee",
            "Generate PDF Report"
        ]
    )

    st.divider()

    # =====================================================
    # GET EMPLOYEE RECORDS
    # =====================================================

    if action == "Get Employee Records":

        st.subheader(
            "Get Employee Records"
        )

        search_option = st.selectbox(
            "Search by:",
            [
                "All",
                "ID",
                "Name",
                "Age",
                "Salary",
                "Gender",
                "Nationality"
            ]
        )

        if search_option == "All":

            if st.button(
                "Get All Employee Records",
                use_container_width=True
            ):

                employees = get_all_employees()

                if employees:

                    st.dataframe(
                        employees,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No employee records found."
                    )

        else:

            search_value = st.text_input(
                f"Enter {search_option}:"
            )

            if st.button(
                "Search",
                use_container_width=True
            ):

                if search_value.strip() == "":

                    st.error(
                        "Please enter a search value."
                    )

                else:

                    try:

                        employees = search_employees(
                            search_option,
                            search_value.strip()
                        )

                        if employees:

                            st.dataframe(
                                employees,
                                use_container_width=True
                            )

                        else:

                            st.warning(
                                "No matching employee found."
                            )

                    except ValueError:

                        st.error(
                            f"{search_option} must contain a valid number."
                        )


    # =====================================================
    # ADD EMPLOYEE
    # =====================================================

    elif action == "Add Employee":

        st.subheader(
            "Add Employee"
        )

        add_name = st.text_input(
            "Name",
            key="add_name"
        )

        add_age = st.text_input(
            "Age",
            key="add_age"
        )

        add_salary = st.text_input(
            "Salary",
            key="add_salary"
        )

        add_gender = st.selectbox(
            "Gender",
            [
                "Select Gender",
                "Male",
                "Female",
                "Other"
            ],
            key="add_gender"
        )

        add_nationality = st.text_input(
            "Nationality",
            key="add_nationality"
        )

        if st.button(
            "Add Employee",
            use_container_width=True
        ):

            if (
                add_name.strip() == ""
                or add_age.strip() == ""
                or add_salary.strip() == ""
                or add_nationality.strip() == ""
                or add_gender == "Select Gender"
            ):

                st.error(
                    "Please fill all fields."
                )

            else:

                try:

                    age_number = int(add_age)

                    salary_number = float(add_salary)

                    if age_number <= 0:

                        st.error(
                            "Age must be greater than 0."
                        )

                    elif salary_number < 0:

                        st.error(
                            "Salary cannot be negative."
                        )

                    else:

                        save_employee(
                            add_name.strip(),
                            age_number,
                            salary_number,
                            add_gender,
                            add_nationality.strip()
                        )

                        st.success(
                            "Employee added successfully!"
                        )

                except ValueError:

                    st.error(
                        "Age must be a whole number and Salary must be a number."
                    )


    # =====================================================
    # EDIT EMPLOYEE
    # =====================================================

    elif action == "Edit Employee":

        st.subheader(
            "Edit Employee"
        )

        search_option = st.selectbox(
            "Find employee by:",
            [
                "ID",
                "Name",
                "Age",
                "Salary",
                "Gender",
                "Nationality"
            ],
            key="edit_search_option"
        )

        search_value = st.text_input(
            f"Enter {search_option}:",
            key="edit_search_value"
        )

        if st.button(
            "Find Employee",
            use_container_width=True
        ):

            if search_value.strip() == "":

                st.error(
                    "Please enter a search value."
                )

            else:

                try:

                    employees = search_employees(
                        search_option,
                        search_value.strip()
                    )

                    if employees:

                        st.session_state.edit_results = employees

                    else:

                        st.session_state.edit_results = []

                        st.warning(
                            "No matching employee found."
                        )

                except ValueError:

                    st.error(
                        f"{search_option} must contain a valid number."
                    )

        if (
            "edit_results" in st.session_state
            and st.session_state.edit_results
        ):

            employees = st.session_state.edit_results

            employee_options = {}

            for employee in employees:

                employee_id = employee[0]

                label = (
                    f"ID {employee[0]} | "
                    f"{employee[1]} | "
                    f"Age {employee[2]} | "
                    f"Salary {employee[3]} | "
                    f"{employee[4]} | "
                    f"{employee[5]}"
                )

                employee_options[label] = employee_id

            selected_employee = st.selectbox(
                "Select employee to edit:",
                list(employee_options.keys())
            )

            selected_id = employee_options[
                selected_employee
            ]

            selected_record = next(
                employee
                for employee in employees
                if employee[0] == selected_id
            )

            st.write(
                "Edit the employee information below:"
            )

            edit_name = st.text_input(
                "Name",
                value=selected_record[1],
                key=f"edit_name_{selected_id}"
            )

            edit_age = st.text_input(
                "Age",
                value=str(selected_record[2]),
                key=f"edit_age_{selected_id}"
            )

            edit_salary = st.text_input(
                "Salary",
                value=str(selected_record[3]),
                key=f"edit_salary_{selected_id}"
            )

            edit_gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ],
                index=[
                    "Male",
                    "Female",
                    "Other"
                ].index(selected_record[4]),
                key=f"edit_gender_{selected_id}"
            )

            edit_nationality = st.text_input(
                "Nationality",
                value=selected_record[5],
                key=f"edit_nationality_{selected_id}"
            )

            if st.button(
                "Update Employee",
                use_container_width=True
            ):

                if (
                    edit_name.strip() == ""
                    or edit_age.strip() == ""
                    or edit_salary.strip() == ""
                    or edit_nationality.strip() == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                else:

                    try:

                        new_age = int(edit_age)

                        new_salary = float(edit_salary)

                        if new_age <= 0:

                            st.error(
                                "Age must be greater than 0."
                            )

                        elif new_salary < 0:

                            st.error(
                                "Salary cannot be negative."
                            )

                        else:

                            success = update_employee(
                                selected_id,
                                edit_name.strip(),
                                new_age,
                                new_salary,
                                edit_gender,
                                edit_nationality.strip()
                            )

                            if success:

                                st.success(
                                    "Employee updated successfully!"
                                )

                                st.session_state.edit_results = []

                                st.rerun()

                            else:

                                st.error(
                                    "Employee could not be updated."
                                )

                    except ValueError:

                        st.error(
                            "Age must be a whole number and Salary must be a number."
                        )


    # =====================================================
    # DELETE EMPLOYEE
    # =====================================================

    elif action == "Delete Employee":

        st.subheader(
            "Delete Employee"
        )

        search_option = st.selectbox(
            "Find employee by:",
            [
                "ID",
                "Name",
                "Age",
                "Salary",
                "Gender",
                "Nationality"
            ],
            key="delete_search_option"
        )

        search_value = st.text_input(
            f"Enter {search_option}:",
            key="delete_search_value"
        )

        if st.button(
            "Find Employee",
            use_container_width=True
        ):

            if search_value.strip() == "":

                st.error(
                    "Please enter a search value."
                )

            else:

                try:

                    employees = search_employees(
                        search_option,
                        search_value.strip()
                    )

                    if employees:

                        st.session_state.delete_results = employees

                    else:

                        st.session_state.delete_results = []

                        st.warning(
                            "No matching employee found."
                        )

                except ValueError:

                    st.error(
                        f"{search_option} must contain a valid number."
                    )

        if (
            "delete_results" in st.session_state
            and st.session_state.delete_results
        ):

            employees = st.session_state.delete_results

            employee_options = {}

            for employee in employees:

                employee_id = employee[0]

                label = (
                    f"ID {employee[0]} | "
                    f"{employee[1]} | "
                    f"Age {employee[2]} | "
                    f"Salary {employee[3]} | "
                    f"{employee[4]} | "
                    f"{employee[5]}"
                )

                employee_options[label] = employee_id

            selected_employee = st.selectbox(
                "Select employee to delete:",
                list(employee_options.keys()),
                key="delete_selected_employee"
            )

            selected_id = employee_options[
                selected_employee
            ]

            st.warning(
                "Deleting an employee is permanent."
            )

            confirm_delete = st.checkbox(
                "I understand that this employee record will be permanently deleted."
            )

            if st.button(
                "Delete Employee",
                use_container_width=True
            ):

                if not confirm_delete:

                    st.error(
                        "Please confirm the deletion first."
                    )

                else:

                    success = delete_employee(
                        selected_id
                    )

                    if success:

                        st.success(
                            "Employee deleted successfully!"
                        )

                        st.session_state.delete_results = []

                        st.rerun()

                    else:

                        st.error(
                            "Employee could not be deleted."
                        )


    # =====================================================
    # GENERATE PDF REPORT
    # =====================================================

    elif action == "Generate PDF Report":

        st.subheader(
            "Generate Employee PDF Report"
        )

        st.write(
            "Generate a PDF containing all employee records "
            "and automatically send it to the configured email address."
        )

        if st.button(
            "Generate PDF & Send to Email",
            use_container_width=True
        ):

            employees = get_all_employees()

            if not employees:

                st.warning(
                    "There are no employee records to include in the report."
                )

            else:

                try:

                    # Generate PDF
                    pdf_data = generate_employee_pdf(
                        employees
                    )

                    filename = (
                        "employee_records_report.pdf"
                    )

                    # Send email
                    send_pdf_email(
                        pdf_data,
                        filename
                    )

                    st.success(
                        "PDF generated and sent successfully!"
                    )

                    # Download PDF
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Failed to generate or send the PDF: {e}"
                    )


    # =====================================================
    # LOGOUT
    # =====================================================

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.page = "home"

        st.rerun()
