from email.message import EmailMessage as RawEmail

from src.email_parser import parse_email


def test_parse_email_extracts_metadata_and_body() -> None:
    raw = RawEmail()
    raw["Message-ID"] = "<abc>"
    raw["From"] = "sender@example.com"
    raw["To"] = "inbox@example.com"
    raw["Subject"] = "Hello"
    raw["Date"] = "Sun, 06 Sep 2026 09:00:00 +0000"
    raw.set_content("Message body")
    parsed = parse_email(raw)
    assert parsed.message_id == "<abc>"
    assert parsed.subject == "Hello"
    assert parsed.body.strip() == "Message body"
