"""Structured logging setup for MailFlow."""

import json
import logging
from pathlib import Path
from typing import Any

from .config import Settings


class JsonFormatter(logging.Formatter):
    """Format log records as compact JSON for machine-friendly logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, default=str)


def configure_logging(settings: Settings) -> logging.Logger:
    """Configure console and file handlers once and return the app logger."""
    logger = logging.getLogger("mailflow")
    logger.setLevel(settings.log_level.upper())
    if logger.handlers:
        return logger
    formatter = JsonFormatter()
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
