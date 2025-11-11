import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


class SmtpEmailService:
    def __init__(self):
        self.smtp_server = os.getenv("EMAIL_SMTP_HOST")
        self.port = os.getenv("EMAIL_SMTP_PORT")
        self.sender_email = os.getenv("EMAIL_HOST_USER")
        self.password = os.getenv("EMAIL_HOST_PASSWORD")

    def send_email(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body, subtype="html")

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port, timeout=20) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            server.send_message(message)
