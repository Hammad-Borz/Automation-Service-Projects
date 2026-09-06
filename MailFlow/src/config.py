"""Environment-backed application configuration."""

from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr

load_dotenv()


class Settings(BaseModel):
    """Validated runtime settings, with safe demo defaults."""

    demo_mode: bool = True
    log_level: str = "INFO"
    log_file: Path = Path("logs/mailflow.log")
    imap_host: str = "imap.example.com"
    imap_port: int = 993
    imap_username: str = ""
    imap_password: SecretStr = Field(default=SecretStr(""))
    imap_folder: str = "INBOX"
    imap_use_ssl: bool = True
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: SecretStr = Field(default=SecretStr(""))
    smtp_from_address: str = "automation@example.com"
    smtp_use_tls: bool = True
    response_provider: str = "demo"
    ai_api_key: SecretStr = Field(default=SecretStr(""))

    @classmethod
    def from_environment(cls) -> "Settings":
        """Load MAILFLOW_* variables without exposing secret values."""
        values: dict[str, object] = {}
        mapping = {
            "demo_mode": "MAILFLOW_DEMO_MODE", "log_level": "MAILFLOW_LOG_LEVEL",
            "log_file": "MAILFLOW_LOG_FILE", "imap_host": "MAILFLOW_IMAP_HOST",
            "imap_port": "MAILFLOW_IMAP_PORT", "imap_username": "MAILFLOW_IMAP_USERNAME",
            "imap_password": "MAILFLOW_IMAP_PASSWORD", "imap_folder": "MAILFLOW_IMAP_FOLDER",
            "imap_use_ssl": "MAILFLOW_IMAP_USE_SSL", "smtp_host": "MAILFLOW_SMTP_HOST",
            "smtp_port": "MAILFLOW_SMTP_PORT", "smtp_username": "MAILFLOW_SMTP_USERNAME",
            "smtp_password": "MAILFLOW_SMTP_PASSWORD", "smtp_from_address": "MAILFLOW_SMTP_FROM_ADDRESS",
            "smtp_use_tls": "MAILFLOW_SMTP_USE_TLS", "response_provider": "MAILFLOW_RESPONSE_PROVIDER",
            "ai_api_key": "MAILFLOW_AI_API_KEY",
        }
        for field_name, env_name in mapping.items():
            value = os.getenv(env_name)
            if value is not None:
                values[field_name] = value
        return cls(**values)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide cached settings instance."""
    return Settings.from_environment()
