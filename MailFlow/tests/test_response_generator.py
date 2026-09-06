from src.models import EmailCategory, Priority
from src.response_generator import DemoResponseGenerator


def test_demo_response_is_deterministic(sample_email) -> None:
    generator = DemoResponseGenerator()
    first = generator.generate(sample_email, EmailCategory.SUPPORT, Priority.MEDIUM)
    assert first == generator.generate(sample_email, EmailCategory.SUPPORT, Priority.MEDIUM)
    assert "support team" in first
