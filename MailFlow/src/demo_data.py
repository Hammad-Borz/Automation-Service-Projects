"""Realistic local messages for the MailFlow demonstration."""

from datetime import datetime, timezone

from .models import EmailMessage


def demo_emails() -> list[EmailMessage]:
    timestamp = datetime(2026, 9, 6, 9, 0, tzinfo=timezone.utc)
    return [
        EmailMessage(message_id="demo-001", sender="ops@acme.example", recipient="team@example.com", subject="URGENT: production checkout outage", body="Customers cannot complete payment. Please investigate immediately.", received_at=timestamp),
        EmailMessage(message_id="demo-002", sender="customer@example.net", recipient="support@example.com", subject="Unable to export my report", body="The export button is not working and shows an error.", received_at=timestamp),
        EmailMessage(message_id="demo-003", sender="prospect@northwind.example", recipient="sales@example.com", subject="Request for pricing and a product demo", body="Could you send a quote for 25 seats?", received_at=timestamp),
        EmailMessage(message_id="demo-004", sender="billing@vendor.example", recipient="finance@example.com", subject="Invoice INV-2048 due Friday", body="Attached is your monthly invoice and payment statement.", received_at=timestamp),
        EmailMessage(message_id="demo-005", sender="news@noreply.example", recipient="team@example.com", subject="Weekly newsletter", body="Read our weekly digest. Unsubscribe at any time.", received_at=timestamp),
    ]
