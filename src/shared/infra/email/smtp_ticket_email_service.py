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

        if not self.sender_email or not self.password:
            raise ValueError(
                "The environment variables EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are not defined."
            )

    def send_email(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body, subtype="html")

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.send_message(message)
                # TODO: remove print after ticket redeeming implementation
                print(f"Email sent successfully to {to}")
        except Exception as e:
            # TODO: remove print after ticket redeeming implementation
            print(f"Error sending email: {e}")
            raise
