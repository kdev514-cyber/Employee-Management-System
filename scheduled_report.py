import io
import smtplib
import os

from datetime import datetime

from email.message import EmailMessage

from supabase import create_client

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
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

SUPABASE_URL = os.environ[
    "SUPABASE_URL"
]

SUPABASE_KEY = os.environ[
    "SUPABASE_KEY"
]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# FORMAT DATE
# =========================================================

def format_date(value):

    if value is None:

        return ""

    try:

        parsed_date = datetime.strptime(
            str(value),
            "%Y-%m-%d"
        )

        return parsed_date.strftime(
            "%d/%m/%Y"
        )

    except ValueError:

        return str(value)


# =========================================================
# GET EMPLOYEES
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
# GENERATE PDF
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


    # =====================================================
    # TITLE
    # =====================================================

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

            "Daily Employee Records Report",

            styles["Heading2"]

        )

    )


    elements.append(

        Spacer(
            1,
            0.5 * cm
        )

    )


    # =====================================================
    # HEADER
    # =====================================================

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


    # =====================================================
    # EMPLOYEE DATA
    # =====================================================

    for employee in employees:

        if employee[8]:

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


    # =====================================================
    # TABLE
    # =====================================================

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


    # =====================================================
    # TABLE STYLE
    # =====================================================

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
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
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


    # =====================================================
    # TOTAL
    # =====================================================

    elements.append(

        Paragraph(

            f"Total Employees: {len(employees)}",

            styles["Normal"]

        )

    )


    # =====================================================
    # BUILD
    # =====================================================

    document.build(
        elements
    )


    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# =========================================================
# SEND EMAIL
# =========================================================

def send_pdf_email(
    pdf_data,
    filename
):

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


    message = EmailMessage()


    message["Subject"] = (
        "Daily Employee Records Report"
    )


    message["From"] = (
        sender_email
    )


    message["To"] = (
        f"{recipient_1}, {recipient_2}"
    )


    message["Cc"] = (
        cc_email
    )


    message.set_content(
        """
Hello,

Please find attached the latest daily
Employee Records Report.

The report contains:

- Employee information
- Employment start date
- Employment end date
- Current employment status

For employees who are still employed,
the employment end date is recorded as
31/12/9999.

This report was automatically generated
by the Employee Management System.

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


    # =====================================================
    # GMAIL
    # =====================================================

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


    employees = get_all_employees()


    if not employees:

        print(
            "No employee records found in Supabase."
        )

        return


    print(
        f"Found {len(employees)} "
        "employee records in Supabase."
    )


    # =====================================================
    # PDF
    # =====================================================

    pdf_data = generate_employee_pdf(
        employees
    )


    filename = (
        "daily_employee_records_report.pdf"
    )


    # =====================================================
    # EMAIL
    # =====================================================

    send_pdf_email(

        pdf_data,

        filename

    )


    print(
        "PDF generated and email sent successfully."
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()
