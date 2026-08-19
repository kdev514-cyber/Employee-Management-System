import io
import smtplib
import os

from datetime import datetime

from email.message import EmailMessage

from supabase import create_client

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


# =========================================================
# SUPABASE CONNECTION
# =========================================================

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# GET EMPLOYEES FROM SUPABASE
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
# FORMAT DATE FOR PDF
# =========================================================

def format_date_for_pdf(date_value):

    if not date_value:
        return ""

    try:

        date_object = datetime.strptime(
            str(date_value),
            "%Y-%m-%d"
        )

        return date_object.strftime(
            "%d/%m/%Y"
        )

    except ValueError:

        return str(date_value)


# =========================================================
# GENERATE PDF
# =========================================================

def generate_employee_pdf(employees):

    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=1.0 * cm,
        leftMargin=1.0 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
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
        Spacer(1, 0.3 * cm)
    )

    elements.append(
        Paragraph(
            "Daily Employee Records Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 0.5 * cm)
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
        "Employment End"
    ]]

    # -----------------------------------------------------
    # EMPLOYEE DATA
    # -----------------------------------------------------

    for employee in employees:

        data.append([

            str(employee[0]),

            str(employee[1]),

            str(employee[2]),

            f"${float(employee[3]):,.2f}",

            str(employee[4]),

            str(employee[5]),

            format_date_for_pdf(
                employee[6]
            ),

            format_date_for_pdf(
                employee[7]
            )

        ])

    # -----------------------------------------------------
    # CREATE TABLE
    # -----------------------------------------------------

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            0.7 * cm,
            2.8 * cm,
            0.8 * cm,
            2.0 * cm,
            1.8 * cm,
            2.3 * cm,
            2.5 * cm,
            2.5 * cm
        ]
    )

    # -----------------------------------------------------
    # TABLE STYLE
    # -----------------------------------------------------

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
        Spacer(1, 0.5 * cm)
    )

    # -----------------------------------------------------
    # TOTAL EMPLOYEES
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            f"Total Employees: {len(employees)}",
            styles["Normal"]
        )
    )

    # -----------------------------------------------------
    # BUILD PDF
    # -----------------------------------------------------

    document.build(elements)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# =========================================================
# SEND PDF EMAIL
# =========================================================

def send_pdf_email(pdf_data, filename):

    sender_email = os.environ[
        "EMAIL_ADDRESS"
    ]

    sender_password = os.environ[
        "EMAIL_PASSWORD"
    ]

    recipient_1 = os.environ[
        "REPORT_EMAIL_1"
    ]

    recipient_2 = os.environ[
        "REPORT_EMAIL_2"
    ]

    cc_email = os.environ[
        "REPORT_EMAIL_CC"
    ]

    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

    message = EmailMessage()

    message["Subject"] = (
        "Daily Employee Records Report"
    )

    message["From"] = sender_email

    message["To"] = (
        f"{recipient_1}, {recipient_2}"
    )

    message["Cc"] = cc_email

    # -----------------------------------------------------
    # EMAIL BODY
    # -----------------------------------------------------

    message.set_content(
        """
Hello,

Please find attached the latest daily
Employee Records Report.

This report was automatically generated
at 8:00 AM.

Regards,
Employee Management System
"""
    )

    # -----------------------------------------------------
    # ATTACH PDF
    # -----------------------------------------------------

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=filename
    )

    # -----------------------------------------------------
    # SEND USING GMAIL
    # -----------------------------------------------------

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(
            message
        )


# =========================================================
# MAIN
# =========================================================

def main():

    print(
        "Starting daily employee report..."
    )

    # -----------------------------------------------------
    # GET EMPLOYEES
    # -----------------------------------------------------

    employees = get_all_employees()

    if not employees:

        print(
            "No employee records found in Supabase."
        )

        return

    print(
        f"Found {len(employees)} employee records in Supabase."
    )

    # -----------------------------------------------------
    # GENERATE PDF
    # -----------------------------------------------------

    pdf_data = generate_employee_pdf(
        employees
    )

    filename = (
        "daily_employee_records_report.pdf"
    )

    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    send_pdf_email(
        pdf_data,
        filename
    )

    print(
        "PDF generated and email sent successfully."
    )


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    main()
