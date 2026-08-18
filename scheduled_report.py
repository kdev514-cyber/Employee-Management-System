import io
import smtplib
import sqlite3
import os

from email.message import EmailMessage

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
# DATABASE
# =========================================================

DATABASE_NAME = "employee.db"


def get_all_employees():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, salary, gender, nationality
        FROM employees
    """)

    employees = cursor.fetchall()

    connection.close()

    return employees


# =========================================================
# GENERATE PDF
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

    elements = []

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

    data = [[
        "ID",
        "Name",
        "Age",
        "Salary",
        "Gender",
        "Nationality"
    ]]

    for employee in employees:

        data.append([
            str(employee[0]),
            str(employee[1]),
            str(employee[2]),
            f"${employee[3]:,.2f}",
            str(employee[4]),
            str(employee[5])
        ])

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
            styles["Normal"]
        )
    )

    document.build(elements)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# =========================================================
# SEND EMAIL
# =========================================================

def send_pdf_email(pdf_data, filename):

    sender_email = os.environ["EMAIL_ADDRESS"]
    sender_password = os.environ["EMAIL_PASSWORD"]

    recipient_1 = os.environ["REPORT_EMAIL_1"]
    recipient_2 = os.environ["REPORT_EMAIL_2"]
    cc_email = os.environ["REPORT_EMAIL_CC"]

    message = EmailMessage()

    message["Subject"] = "Daily Employee Records Report"

    message["From"] = sender_email

    message["To"] = f"{recipient_1}, {recipient_2}"

    message["Cc"] = cc_email

    message.set_content(
        """
Hello,

Please find attached the latest daily Employee Records Report.

This report was automatically generated at 8:00 AM.

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
# MAIN
# =========================================================

def main():

    print("Starting daily employee report...")

    employees = get_all_employees()

    if not employees:

        print("No employee records found.")

        return

    print(
        f"Found {len(employees)} employee records."
    )

    pdf_data = generate_employee_pdf(
        employees
    )

    filename = "daily_employee_records_report.pdf"

    send_pdf_email(
        pdf_data,
        filename
    )

    print(
        "PDF generated and email sent successfully."
    )


if __name__ == "__main__":

    main()
