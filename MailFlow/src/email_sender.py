"""Guarded SMTP delivery service."""

from email.message import EmailMessage as SmtpMessage
import smtplib

from .config import Settings
from .exceptions import ConfigurationError, EmailDeliveryError


class EmailSender:
    """Send email only when explicitly configured outside demo mode."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def send(self, recipient: str, subject: str, body: str) -> bool:
        if self.settings.demo_mode:
            return False
        if not self.settings.smtp_username or not self.settings.smtp_password.get_secret_value():
            raise ConfigurationError("SMTP credentials are required when demo mode is disabled")
        message = SmtpMessage()
        message["From"] = self.settings.smtp_from_address
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)
        try:
            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=20) as client:
                if self.settings.smtp_use_tls:
                    client.starttls()
                client.login(self.settings.smtp_username, self.settings.smtp_password.get_secret_value())
                client.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            raise EmailDeliveryError("SMTP delivery failed") from exc
        return True
