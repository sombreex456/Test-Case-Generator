import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_test_cases_email(
    recipient_email: str,
    excel_file: bytes
):

    sender_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        raise ValueError(
            "Email credentials are not configured in the .env file."
        )

    message = EmailMessage()

    message["Subject"] = "AI Generated Test Cases"
    message["From"] = sender_email
    message["To"] = recipient_email

    message.set_content(
        "Hello,\n\n"
        "Please find attached the Excel file containing "
        "the AI-generated test cases.\n\n"
        "Generated using the AI Test Case Generator."
    )

    message.add_attachment(
        excel_file,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="AI_Test_Cases.xlsx"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender_email, app_password)

        server.send_message(message)