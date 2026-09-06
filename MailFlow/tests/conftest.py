"""Shared test fixtures."""

from datetime import datetime, timezone
import pytest

from src.models import EmailMessage


@pytest.fixture
def sample_email() -> EmailMessage:
    return EmailMessage(message_id="test-1", sender="customer@example.com", recipient="team@example.com", subject="Need help with my account", body="The support issue is blocking my work.", received_at=datetime.now(timezone.utc))
