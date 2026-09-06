from src.models import EmailCategory, Priority
from src.prioritizer import EmailPrioritizer


def test_urgent_message_is_high_priority(sample_email) -> None:
    sample_email.subject = "URGENT: account blocked"
    assert EmailPrioritizer().prioritize(sample_email, EmailCategory.URGENT) == Priority.HIGH


def test_newsletter_from_noreply_is_low_priority(sample_email) -> None:
    sample_email.sender = "news@noreply.example"
    assert EmailPrioritizer().prioritize(sample_email, EmailCategory.NEWSLETTER) == Priority.LOW
