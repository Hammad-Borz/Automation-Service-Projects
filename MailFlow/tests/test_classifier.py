from src.classifier import EmailClassifier
from src.models import EmailCategory


def test_classifier_identifies_support(sample_email) -> None:
    assert EmailClassifier().classify(sample_email) == EmailCategory.SUPPORT


def test_classifier_falls_back_to_general() -> None:
    from src.models import EmailMessage
    email = EmailMessage(message_id="1", sender="a@example.com", recipient="b@example.com", subject="Hello", body="Nice weather today")
    assert EmailClassifier().classify(email) == EmailCategory.GENERAL
