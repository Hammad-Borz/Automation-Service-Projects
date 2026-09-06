from src.config import Settings


def test_settings_default_to_safe_demo_mode() -> None:
    settings = Settings()
    assert settings.demo_mode is True
    assert settings.smtp_password.get_secret_value() == ""


def test_settings_load_environment(monkeypatch) -> None:
    monkeypatch.setenv("MAILFLOW_DEMO_MODE", "false")
    monkeypatch.setenv("MAILFLOW_SMTP_PORT", "2525")
    settings = Settings.from_environment()
    assert settings.demo_mode is False
    assert settings.smtp_port == 2525
