import streamlit as st
import re
import io
import smtplib

from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
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
# CONSTANT
# =========================================================

# Employees who are still working
# will have this end date.

DEFAULT_END_DATE = date(
    9999,
    12,
    31
)


# =========================================================
# DATE FORMATTER
# =========================================================

def format_date(value):

    if value is None:

        return ""

    try:

        return date.fromisoformat(
            str(value)
        ).strftime(
            "%d/%m/%Y"
        )

    except ValueError:

        return str(value)


# =========================================================
# GENERATE EMPLOYEE PDF
# =========================================================

def generate_employee_pdf(employees):

    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(A4),
        rightMargin=1.0 * cm,
        leftMargin=1.0 * cm,
        topMargin=1.0 * cm,
        bottomMargin=1.0 * cm
    )

    styles = getSampleStyleSheet()

    elements = []


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Employee Management System",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(
            1,
            0.3 * cm
        )
    )

    elements.append(
        Paragraph(
            "Employee Records Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(
            1,
            0.5 * cm
        )
    )


    # -----------------------------------------------------
    # TABLE HEADER
    # -----------------------------------------------------

    data = [[

        "ID",

        "Name",

        "Age",

        "Salary",

        "Gender",

        "Nationality",

        "Employment Start",

        "Employment End",

        "Status"

    ]]


    # -----------------------------------------------------
    # EMPLOYEE DATA
    # -----------------------------------------------------

    for employee in employees:

        still_employed = employee[8]

        if still_employed:

            status = "Still Employed"

        else:

            status = "Employment Ended"


        data.append([

            str(employee[0]),

            str(employee[1]),

            str(employee[2]),

            f"${float(employee[3]):,.2f}",

            str(employee[4]),

            str(employee[5]),

            format_date(employee[6]),

            format_date(employee[7]),

            status

        ])


    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    table = Table(
        data,
        repeatRows=1,
        colWidths=[

            0.8 * cm,

            3.2 * cm,

            1.0 * cm,

            2.3 * cm,

            2.0 * cm,

            2.8 * cm,

            2.8 * cm,

            2.8 * cm,

            3.0 * cm

        ]
    )


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
                (-1, -1),
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
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
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
                5
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            )

        ])
    )


    elements.append(table)


    elements.append(
        Spacer(
            1,
            0.5 * cm
        )
    )


    elements.append(
        Paragraph(
            f"Total Employees: {len(employees)}",
            styles["Normal"]
        )
    )


    document.build(elements)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# =========================================================
# SEND PDF BY EMAIL
# =========================================================

def send_pdf_email(
    pdf_data,
    filename
):

    sender_email = st.secrets[
        "EMAIL_ADDRESS"
    ]

    sender_password = st.secrets[
        "EMAIL_PASSWORD"
    ]

    recipient_1 = st.secrets[
        "REPORT_EMAIL_1"
    ]

    recipient_2 = st.secrets[
        "REPORT_EMAIL_2"
    ]

    cc_email = st.secrets[
        "REPORT_EMAIL_CC"
    ]


    message = EmailMessage()

    message["Subject"] = (
        "Employee Records Report"
    )

    message["From"] = sender_email

    message["To"] = (
        f"{recipient_1}, {recipient_2}"
    )

    message["Cc"] = cc_email


    message.set_content(
        """
Hello,

Please find attached the latest
Employee Records Report.

The report includes employee information,
employment start dates, employment end dates,
and employment status.

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


    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(message)


# =========================================================
# PASSWORD VALIDATION
# =========================================================

def validate_password(password):

    if len(password) < 8:

        return False, (
            "Password must contain at least 8 characters."
        )

    if not re.search(
        r"[A-Z]",
        password
    ):

        return False, (
            "Password must contain at least one capital letter."
        )

    if not re.search(
        r"[a-z]",
        password
    ):

        return False, (
            "Password must contain at least one small letter."
        )

    if not re.search(
        r"[0-9]",
        password
    ):

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


    # -----------------------------------------------------
    # Employee
    # -----------------------------------------------------

    if choice == "Employee":

        if st.button(
            "Continue as Employee",
            use_container_width=True
        ):

            st.session_state.page = (
                "employee"
            )

            st.rerun()


    # -----------------------------------------------------
    # Employer
    # -----------------------------------------------------

    if choice == "Employer":

        if st.button(
            "Continue as Employer",
            use_container_width=True
        ):

            st.session_state.page = (
                "employer_login"
            )

            st.rerun()


# =========================================================
# EMPLOYEE PAGE
# =========================================================

if st.session_state.page == "employee":

    st.title(
        "Employee Details"
    )

    st.write(
        "Enter the employee information below."
    )


    # -----------------------------------------------------
    # Basic information
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Employment Start Date
    # -----------------------------------------------------

    employment_start_date = st.date_input(
        "Employment Start Date",
        value=date.today()
    )


    # -----------------------------------------------------
    # Still in Employment
    # -----------------------------------------------------

    still_in_employment = st.checkbox(
        "Still in Employment?",
        value=True
    )


    # -----------------------------------------------------
    # Employment End Date
    # -----------------------------------------------------

    if still_in_employment:

        employment_end_date = (
            DEFAULT_END_DATE
        )

        st.info(
            "Employment End Date: 31/12/9999 "
            "(currently employed)"
        )

    else:

        employment_end_date = st.date_input(
            "Employment End Date",
            value=date.today()
        )


    # -----------------------------------------------------
    # Validate date
    # -----------------------------------------------------

    if (
        employment_end_date
        < employment_start_date
    ):

        st.warning(
            "Employment End Date cannot be "
            "before Employment Start Date."
        )


    # -----------------------------------------------------
    # Buttons
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

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

        elif (
            employment_end_date
            < employment_start_date
        ):

            st.error(
                "Employment End Date cannot be "
                "before Employment Start Date."
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

                        nationality.strip(),

                        employment_start_date.isoformat(),

                        employment_end_date.isoformat(),

                        still_in_employment

                    )


                    st.success(
                        "Employee saved successfully!"
                    )


            except ValueError:

                st.error(
                    "Age must be a whole number "
                    "and Salary must be a number."
                )


    # -----------------------------------------------------
    # Back
    # -----------------------------------------------------

    if back:

        st.session_state.page = "home"

        st.rerun()


# =========================================================
# EMPLOYER LOGIN
# =========================================================

if st.session_state.page == "employer_login":

    st.title(
        "Employer Login"
    )

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


    # -----------------------------------------------------
    # Login
    # -----------------------------------------------------

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

                st.session_state.page = (
                    "dashboard"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid User ID or Password."
                )


    st.divider()


    # -----------------------------------------------------
    # Register
    # -----------------------------------------------------

    if st.button(
        "New Employer? Register Here",
        use_container_width=True
    ):

        st.session_state.page = (
            "register"
        )

        st.rerun()


    # -----------------------------------------------------
    # Back
    # -----------------------------------------------------

    if back:

        st.session_state.page = "home"

        st.rerun()


# =========================================================
# REGISTRATION
# =========================================================

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


    # -----------------------------------------------------
    # Register
    # -----------------------------------------------------

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

                    st.session_state.page = (
                        "employer_login"
                    )

                    st.rerun()

                else:

                    st.error(
                        "User ID already exists."
                    )


    # -----------------------------------------------------
    # Login existing
    # -----------------------------------------------------

    if login_existing:

        st.session_state.page = (
            "employer_login"
        )

        st.rerun()


# =========================================================
# EMPLOYER DASHBOARD
# =========================================================

if st.session_state.page == "dashboard":

    # -----------------------------------------------------
    # Security
    # -----------------------------------------------------

    if not st.session_state.logged_in:

        st.session_state.page = (
            "employer_login"
        )

        st.rerun()


    st.title(
        "Employer Dashboard"
    )

    st.write(
        "Manage employee records"
    )


    # -----------------------------------------------------
    # Dashboard menu
    # -----------------------------------------------------

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
                "Nationality",
                "Employment Start Date",
                "Employment End Date",
                "Still in Employment"
            ]
        )


        # -------------------------------------------------
        # All
        # -------------------------------------------------

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


        # -------------------------------------------------
        # Still in employment
        # -------------------------------------------------

        elif search_option == "Still in Employment":

            employment_status = st.selectbox(
                "Employment Status",
                [
                    "Yes",
                    "No"
                ]
            )


            if st.button(
                "Search",
                use_container_width=True
            ):

                employees = search_employees(
                    "Still in Employment",
                    employment_status
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


        # -------------------------------------------------
        # Date searches
        # -------------------------------------------------

        elif search_option in [
            "Employment Start Date",
            "Employment End Date"
        ]:

            search_date = st.date_input(
                "Select Date"
            )


            if st.button(
                "Search",
                use_container_width=True
            ):

                employees = search_employees(
                    search_option,
                    search_date.isoformat()
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


        # -------------------------------------------------
        # Other searches
        # -------------------------------------------------

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


        add_start_date = st.date_input(
            "Employment Start Date",
            value=date.today(),
            key="add_start_date"
        )


        add_still_employed = st.checkbox(
            "Still in Employment?",
            value=True,
            key="add_still_employed"
        )


        if add_still_employed:

            add_end_date = DEFAULT_END_DATE

            st.info(
                "Employment End Date: 31/12/9999 "
                "(currently employed)"
            )

        else:

            add_end_date = st.date_input(
                "Employment End Date",
                value=date.today(),
                key="add_end_date"
            )


        if (
            add_end_date
            < add_start_date
        ):

            st.warning(
                "Employment End Date cannot be "
                "before Employment Start Date."
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

            elif (
                add_end_date
                < add_start_date
            ):

                st.error(
                    "Employment End Date cannot be "
                    "before Employment Start Date."
                )

            else:

                try:

                    age_number = int(
                        add_age
                    )

                    salary_number = float(
                        add_salary
                    )


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

                            add_nationality.strip(),

                            add_start_date.isoformat(),

                            add_end_date.isoformat(),

                            add_still_employed

                        )


                        st.success(
                            "Employee added successfully!"
                        )


                except ValueError:

                    st.error(
                        "Age must be a whole number "
                        "and Salary must be a number."
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
                "Nationality",
                "Employment Start Date",
                "Employment End Date",
                "Still in Employment"
            ],
            key="edit_search_option"
        )


        # -------------------------------------------------
        # Search value
        # -------------------------------------------------

        if search_option == "Still in Employment":

            edit_status = st.selectbox(
                "Employment Status",
                [
                    "Yes",
                    "No"
                ],
                key="edit_status"
            )

            search_value = edit_status


        elif search_option in [
            "Employment Start Date",
            "Employment End Date"
        ]:

            edit_search_date = st.date_input(
                "Select Date",
                key="edit_search_date"
            )

            search_value = (
                edit_search_date.isoformat()
            )


        else:

            search_value = st.text_input(
                f"Enter {search_option}:",
                key="edit_search_value"
            )


        if st.button(
            "Find Employee",
            use_container_width=True
        ):

            if (
                isinstance(search_value, str)
                and search_value.strip() == ""
            ):

                st.error(
                    "Please enter a search value."
                )

            else:

                try:

                    employees = search_employees(
                        search_option,
                        search_value
                    )


                    if employees:

                        st.session_state.edit_results = (
                            employees
                        )

                    else:

                        st.session_state.edit_results = []

                        st.warning(
                            "No matching employee found."
                        )


                except ValueError:

                    st.error(
                        f"{search_option} must contain a valid number."
                    )


        # -------------------------------------------------
        # Show results
        # -------------------------------------------------

        if (
            "edit_results" in st.session_state
            and st.session_state.edit_results
        ):

            employees = (
                st.session_state.edit_results
            )


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


                employee_options[
                    label
                ] = employee_id


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


            # -------------------------------------------------
            # Basic information
            # -------------------------------------------------

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
                ].index(
                    selected_record[4]
                ),
                key=f"edit_gender_{selected_id}"
            )


            edit_nationality = st.text_input(
                "Nationality",
                value=selected_record[5],
                key=f"edit_nationality_{selected_id}"
            )


            # -------------------------------------------------
            # Existing start date
            # -------------------------------------------------

            try:

                existing_start_date = date.fromisoformat(
                    str(selected_record[6])
                )

            except ValueError:

                existing_start_date = date.today()


            edit_start_date = st.date_input(
                "Employment Start Date",
                value=existing_start_date,
                key=f"edit_start_date_{selected_id}"
            )


            # -------------------------------------------------
            # Existing employment status
            # -------------------------------------------------

            existing_still_employed = bool(
                selected_record[8]
            )


            edit_still_employed = st.checkbox(
                "Still in Employment?",
                value=existing_still_employed,
                key=f"edit_still_{selected_id}"
            )


            # -------------------------------------------------
            # End date
            # -------------------------------------------------

            if edit_still_employed:

                edit_end_date = (
                    DEFAULT_END_DATE
                )

                st.info(
                    "Employment End Date: 31/12/9999 "
                    "(currently employed)"
                )

            else:

                try:

                    existing_end_date = date.fromisoformat(
                        str(selected_record[7])
                    )

                except ValueError:

                    existing_end_date = date.today()


                edit_end_date = st.date_input(
                    "Employment End Date",
                    value=existing_end_date,
                    key=f"edit_end_date_{selected_id}"
                )


            if (
                edit_end_date
                < edit_start_date
            ):

                st.warning(
                    "Employment End Date cannot be "
                    "before Employment Start Date."
                )


            # -------------------------------------------------
            # Update
            # -------------------------------------------------

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

                elif (
                    edit_end_date
                    < edit_start_date
                ):

                    st.error(
                        "Employment End Date cannot be "
                        "before Employment Start Date."
                    )

                else:

                    try:

                        new_age = int(
                            edit_age
                        )

                        new_salary = float(
                            edit_salary
                        )


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

                                edit_nationality.strip(),

                                edit_start_date.isoformat(),

                                edit_end_date.isoformat(),

                                edit_still_employed

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
                            "Age must be a whole number "
                            "and Salary must be a number."
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
                "Nationality",
                "Employment Start Date",
                "Employment End Date",
                "Still in Employment"
            ],
            key="delete_search_option"
        )


        if search_option == "Still in Employment":

            delete_status = st.selectbox(
                "Employment Status",
                [
                    "Yes",
                    "No"
                ],
                key="delete_status"
            )

            search_value = delete_status


        elif search_option in [
            "Employment Start Date",
            "Employment End Date"
        ]:

            delete_search_date = st.date_input(
                "Select Date",
                key="delete_search_date"
            )

            search_value = (
                delete_search_date.isoformat()
            )


        else:

            search_value = st.text_input(
                f"Enter {search_option}:",
                key="delete_search_value"
            )


        if st.button(
            "Find Employee",
            use_container_width=True
        ):

            if (
                isinstance(search_value, str)
                and search_value.strip() == ""
            ):

                st.error(
                    "Please enter a search value."
                )

            else:

                try:

                    employees = search_employees(
                        search_option,
                        search_value
                    )


                    if employees:

                        st.session_state.delete_results = (
                            employees
                        )

                    else:

                        st.session_state.delete_results = []

                        st.warning(
                            "No matching employee found."
                        )


                except ValueError:

                    st.error(
                        f"{search_option} must contain a valid number."
                    )


        # -------------------------------------------------
        # Delete results
        # -------------------------------------------------

        if (
            "delete_results" in st.session_state
            and st.session_state.delete_results
        ):

            employees = (
                st.session_state.delete_results
            )


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


                employee_options[
                    label
                ] = employee_id


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
                "I understand that this employee record "
                "will be permanently deleted."
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
                    "There are no employee records "
                    "to include in the report."
                )

            else:

                try:

                    pdf_data = generate_employee_pdf(
                        employees
                    )


                    filename = (
                        "employee_records_report.pdf"
                    )


                    send_pdf_email(
                        pdf_data,
                        filename
                    )


                    st.success(
                        "PDF generated and sent successfully!"
                    )


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
