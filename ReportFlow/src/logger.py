"""Structured application logging."""

import logging
from pathlib import Path


def configure_logging(log_dir: Path) -> logging.Logger:
    """Configure a file and console logger without duplicating handlers."""
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("reportflow")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(log_dir / "reportflow.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
