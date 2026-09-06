"""Readable structured logging configuration."""

import logging
from pathlib import Path


def configure_logging(logs_dir: Path) -> logging.Logger:
    """Configure the application logger with file and console handlers."""
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("dataops")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(logs_dir / "dataops.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
