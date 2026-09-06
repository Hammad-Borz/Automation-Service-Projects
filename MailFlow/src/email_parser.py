"""Parsing helpers for raw provider messages."""

from datetime import datetime, timezone
from email.message import Message
from email.utils import parsedate_to_datetime

from .models import EmailMessage


def _body_from_message(message: Message) -> str:
    if message.is_multipart():
        parts = [part for part in message.walk() if part.get_content_type() == "text/plain"]
        return parts[0].get_payload(decode=True).decode(errors="replace") if parts else ""
    payload = message.get_payload(decode=True)
    return payload.decode(errors="replace") if isinstance(payload, bytes) else str(payload or "")


def parse_email(message: Message, message_id: str | None = None) -> EmailMessage:
    """Convert a standard library email message into a validated model."""
    date_header = message.get("Date")
    received_at = parsedate_to_datetime(date_header) if date_header else datetime.now(timezone.utc)
    if received_at.tzinfo is None:
        received_at = received_at.replace(tzinfo=timezone.utc)
    return EmailMessage(
        message_id=message_id or message.get("Message-ID", "unknown"),
        sender=message.get("From", "unknown@example.com"),
        recipient=message.get("To", "unknown@example.com"),
        subject=message.get("Subject", "(no subject)"),
        body=_body_from_message(message),
        received_at=received_at,
    )
